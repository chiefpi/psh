import os
import subprocess

class Shell(object):
    def __init__(self):
        self.prompt = 'psh>'
        self.exit = False
        while not self.exit:
            cmd = input(self.prompt)
            self.interpret(cmd)

    def interpret(self, cmd):
        sub_cmds = cmd.split('|')
        sin = os.dup(0)
        sout = os.dup(1)

        tin = os.dup(sin) # TODO

        os.dup2(sin, 0)
        os.dup2(sout, 1)
        os.close(sin)
        os.close(sout)

        if "|" in cmd:
            # save for restoring later on
            s_in = os.dup(0)
            s_out = os.dup(1)

            # first cmd takes cmdut from stdin
            fdin = os.dup(s_in)

            # iterate over all the cmds that are piped
            
            for i, c in enumerate(cmd.split("|"):
                # fdin will be stdin if it's the first iteration
                # and the readable end of the pipe if not.
                os.dup2(fdin, 0)
                os.close(fdin)

                # restore stdout if this is the last cmd
                if c == cmd.split("|")[-1]:
                    fdout = os.dup(s_out)
                else:
                    fdin, fdout = os.pipe()

                # redirect stdout to pipe
                os.dup2(fdout, 1)
                os.close(fdout)

                try:
                    self.
                except Exception:
                    print("psh: cmd not found: {}".format(cmd.strip()))

            # restore stdout and stdin
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            self.execute_one(cmd)

    def execute_one(self, cmd):
        try:
            tokens = cmd.split()
            p = Process(target=eval('self.{}'.format(tokens[0])), args=tokens[1:])
            p.start()
            p.join()
        except Exception:
            print('psh: cmd not found: {}'.format(cmd))
        
    def cd(self, path):
        try:
            os.chdir(os.path.abspath(path))
        except Exception:
            print('cd: no such directory: {}'.format(path))


if __name__ == '__main__':
    psh = Shell()
