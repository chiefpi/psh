import os
import sys
from inspect import getmembers, isfunction
from threading import Thread
import subprocess

from parse import AST
from job import Job, JobList
import lib


class Shell(object):

    prompt = '> '
    functions = {n:f for n, f in getmembers(lib, isfunction)}
    functions['help'] = functions['helpsh']

    def environ(self):
        for k, v in self.env.items():
            print('{}={}'.format(k, v))

    def set(self, var, val):
        self.env[var] = val

    def unset(self, var):
        del self.env[var]

    def jobs(self):
        print(self.joblist)

    def fg(self, jid):
        pass
        
    def __init__(self):
        self.functions['environ'] = self.environ
        self.functions['set'] = self.set
        self.functions['unset'] = self.unset
        self.functions['jobs'] = self.jobs
        
        self.env = {}
        self.joblist = JobList()
        self.end = False
        while not self.end:
            self.joblist.check()
            text = input('[{}]{}'.format(os.getcwd(), self.prompt))
            self.interpret(text)

    def interpret(self, text):
        ast = AST(text)
        self.execute(ast.root)

    def execute(self, root):
        for pipe, bg in root:
            if bg:
                thread = Thread(target=self.execute_pipe, args=(pipe,), daemon=True)
                thread.start()
                self.joblist.add_job(Job(pipe, thread))
            else:
                self.execute_pipe(pipe)

    def execute_pipe(self, root):
        # save for restoring later on
        sin, sout = (0, 0)
        sin = os.dup(0)
        sout = os.dup(1)

        # first command takes commandut from stdin
        fdin = os.dup(sin)

        pipe_len = len(root)
        for i, command in enumerate(root):
            # fdin will be stdin if it's the first iteration
            # and the readable end of the pipe if not.
            os.dup2(fdin, 0)
            os.close(fdin)

            # restore stdout if this is the last command
            if i == pipe_len - 1:
                fdout = os.dup(sout)
            else:
                fdin, fdout = os.pipe()

            # redirect stdout to pipe
            os.dup2(fdout, 1)
            os.close(fdout)

            self.execute_command(command)

        # restore stdout and stdin
        os.dup2(sin, 0)
        os.dup2(sout, 1)
        os.close(sin)
        os.close(sout)

    def execute_command(self, command):
        stdin = sys.stdin
        stdout = sys.stdout

        if command.rin:
            sys.stdin = open(command.rin, 'r')
        if command.rout:
            sys.stdout = open(command.rout, 'w')
        elif command.rapp:
            sys.stdout = open(command.rapp, 'a')

        self.execute_args(command.args)

        sys.stdin = stdin
        sys.stdout = stdout

    def execute_args(self, args):
        head = args[0]
        if head not in self.functions:
            try:
                subprocess.run(args)
            except FileNotFoundError:
                print('psh: no such command: {}'.format(head))
        else:
            try:
                self.end = self.functions[head](*args[1:]) is not None
            except TypeError:
                print('{}: invalid args length'.format(head))


if __name__ == '__main__':
    psh = Shell()
