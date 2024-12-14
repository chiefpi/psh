class Command(object):
    def __init__(self, args=[], rin=None, rout=None, rapp=None):
        self.args = args
        self.rin = rin
        self.rout = rout
        self.rapp = rapp

    def __repr__(self):
        return ' '.join(self.args)


class AST(object):
    """
    Attributes:
        root: list[tuple[list[Command], bool]] - bg/fg pipes
    """
    def __init__(self, text):
        self.root = AST.parse(text)

    def __repr__(self):
        return str(self.root)

    @staticmethod
    def clear_split(text, d):
        return [s.strip() for s in text.split(d) if s.strip()]

    @staticmethod
    def parse(text):
        root = []
        # FIXME
        pipelines = AST.clear_split(text, '&')
        pipe_num = len(pipelines)
        bg_num = text.count('&')
        for i, pipe in enumerate(pipelines):
            if i == pipe_num - 1 and pipe_num != bg_num:
                root.append((AST.parse_pipe(pipe), False))
            else:
                root.append((AST.parse_pipe(pipe), True))
        return root

    @staticmethod
    def parse_pipe(text):
        root = []
        commands = AST.clear_split(text, '|')
        for command in commands:
            root.append(AST.parse_command(command))
        return root

    @staticmethod
    def parse_command(text):
        tokens = text.split()

        args = []
        rin, rout, rapp = None, None, None
        fin, fout, fapp = False, False, False
        for i, token in enumerate(tokens):
            if token == '<':
                fin = True
            elif fin:
                rin = token
                fin = False
            elif token == '>':
                fout = True
            elif fout:
                rout = token
                fout = False
            elif token == '>>':
                fapp = True
            elif fapp:
                rapp = token
                fapp = False
            else:
                args.append(token)

        return Command(args, rin, rout, rapp)
