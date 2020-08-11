import os
import subprocess
from multiprocessing import Process

class Shell(object):

    builtin_cmds = {'bg', 'cd', 'clr', 'dir', 'echo', 'exec', 'exit', 'environ', 'fg', 'help', 'jobs', 'pwd', 'quit', 'set', 'shift', 'test', 'time', 'umask', 'unset'}
    prompt = '> '

    def __init__(self):
        self.end = False
        while not self.end:
            command = input('[{}]{}'.format(os.getcwd(), self.prompt))
            self.interpret(command)

    def interpret(self, command):
        """Interprets command.
        Args:
            command (string)
        """
        cmds = [cmd for cmd in command.split('|') if cmd]
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

    def execute_one(self, cmd):
        tokens = cmd.split()

        head = tokens[0]
        if head not in self.builtin_cmds:
            raise NotImplementedError
        args = ','.join(["'{}'".format(t) for t in tokens[1:]])

        eval('self.{}({})'.format(head, args))
        #p = Process(target=eval('self.{}'.format(tokens[0])), args=tokens[1:])
        #p.start()
        #p.join()
        #except Exception:
        #    print('psh: cmd not found: {}'.format(cmd))
        
    def cd(self, path):
        try:
            os.chdir(os.path.abspath(path))
        except FileNotFoundError:
            print('cd: no such directory: {}'.format(path))

    def clr(self):
        os.system('clear')

    def dir(self, path='.'):
        try:
            print('  '.join(os.listdir(path)))
        except FileNotFoundError:
            print('dir: no such directory: {}'.format(path))
        except NotADirectoryError:
            print('dir: not a directory: {}'.format(path))

    def echo(self, *comment):
        print(' '.join(comment))

    def exec(self):
        pass

    def exit(self):
        self.end = True

    def environ(self):
        print(os.environ) 

    def fg(self):
        pass

    def help(self):
        pass

    def jobs(self):
        pass

    def pwd(self):
        print(os.getcwd())

    def quit(self):
        self.end = True


if __name__ == '__main__':
    psh = Shell()
