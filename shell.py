import os
from inspect import getmembers, isfunction
from multiprocessing import Process

from parse import AST
import lib


class Shell(object):

    functions = {n:f for n, f in getmembers(lib, isfunction)}
    functions['help'] = functions['helpsh']
    prompt = '> '

    def __init__(self):
        self.end = False
        while not self.end:
            text = input('[{}]{}'.format(os.getcwd(), self.prompt))
            self.interpret(text)

    def interpret(self, text):
        ast = AST(text)
        self.execute(ast.root)

    def execute(self, root):
        for pipe in root:
            self.execute_pipe(pipe)

    def execute_pipe(self, root):
        for command in root:
            self.execute_command(command)

    def execute_command(self, command):
        try:
            self.execute_args(command.args)
        except NotImplementedError:
            print('psh: no such command: {}'.format(command.args[0]))

    def execute_args(self, args):
        head = args[0]
        if head not in self.functions:
            raise NotImplementedError
        self.end = self.functions[head](*args[1:]) is not None

    def interpret_old(self, command):
        """Interprets command.
        Args:
            command (string)
        """
        cmds = [cmd.strip() for cmd in command.split('|') if cmd]
        if len(cmds) == 0:
            return

        # standard io
        sin = os.dup(0)
        sout = os.dup(1)

        def interpret_pipe(cmds, fdin):
            """Interprets piped commands.
            Args:
                cmds (list of strings)
                fdin: input file descriptor
                fdout: output file descriptor
            """
            if len(cmds) == 1: # the last
                os.dup2(fdin, 0)
                os.close(fdin)
                fdout = os.dup(sout)
            else:
                fdin, fdout = os.pipe()

            os.dup2(fdout, 1)
            os.close(fdout)

            # executes commands recursively
            try:
                self.execute_one(cmds[0])
            except NotImplementedError:
                print('psh: no such command: {}'.format(cmds[0].split()[0]))

            if len(cmds) > 1:
                interpret_pipe(cmds[1:], fdin)

        # input file descriptor
        fdin = os.dup(sin)
        interpret_pipe(cmds, fdin)

        # restores stdin and stdout
        os.dup2(sin, 0)
        os.dup2(sout, 1)
        os.close(sin)
        os.close(sout)


if __name__ == '__main__':
    psh = Shell()
