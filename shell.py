import os
import subprocess
from multiprocessing import Process

class Shell(object):
    def __init__(self):
        self.prompt = 'psh> '
        self.exit = False
        while not self.exit:
            cmd = input(self.prompt)
            self.interpret(cmd)

    def interpret(self, command):
        """Interprets command.
        Args:
            cmd (string)
        """
        cmds = command.split('|')
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
            self.execute_one(cmds[0])
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
        #try:
        tokens = cmd.split()
        p = Process(target=eval('self.{}'.format(tokens[0])), args=tokens[1:])
        p.start()
        p.join()
        #except Exception:
        #    print('psh: cmd not found: {}'.format(cmd))
        
    def cd(self, path):
        try:
            os.chdir(os.path.abspath(path))
        except Exception:
            print('cd: no such directory: {}'.format(path))

    def ls(self):
        subprocess.run('ls')

    def quit(self):
        print('quit')
        self.exit = True


if __name__ == '__main__':
    psh = Shell()
