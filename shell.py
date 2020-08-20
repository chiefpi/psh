import os
import sys
from inspect import getmembers, isfunction
from multiprocessing import Process
import subprocess

from parse import AST
from job import Job, JobList
import lib


class Shell(object):

    prompt = '> '
    functions = {n:f for n, f in getmembers(lib, isfunction)}
    functions['help'] = functions['helpsh']

    env_job_function_names = ['environ', 'set', 'unset', 'jobs']

    def environ(self):
        for k, v in self.env.items():
            print('{}={}'.format(k, v))

    def set(self, var, val):
        self.env[var] = val

    def unset(self, var):
        del self.env[var]

    def jobs(self):
        print(self.joblist)

    def __init__(self, batch_file=None):
        for n in self.env_job_function_names:
            self.functions[n] = getattr(self, n)
        
        self.env = {}
        self.joblist = JobList()
        if batch_file:
            texts = open(batch_file, 'r').readlines()
            for text in texts:
                self.interpret(text)
        else:
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
                subp = Process(target=self.execute_pipe, args=(pipe,), daemon=True)
                subp.start()
                self.joblist.add_job(Job(pipe, subp))
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
    argc = len(sys.argv) 
    if argc == 2:
        Shell(sys.argv[1])
    elif argc  == 1:
        Shell()
    else:
        print('unknown usage')
