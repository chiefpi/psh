class Command(object):
    def __init__(self, args=[], rin=None, rout=None, rapp=None):
        self.args = args
        self.rin = rin
        self.rout = rout
        self.rapp = rapp

    def __repr__(self):
        return ' '.join(self.args)


class ParseError(Exception):
    def __init__(self, pos, ch):
        self.pos = pos
        self.ch = ch
        super().__init__(self.__str__())

    def __str__(self):
        return f'Parse error: \'{self.ch}\' at {self.pos}'


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
    def clear_split(text, delimiter, allow_delimiter_end):
        # seg delim seg delim [seg]
        if not text:
            return []

        segs = [] # (seg, ends_with_delimiter)
        seg_start = 0
        text = text.strip()
        for seg_end, ch in enumerate(text):
            if ch == delimiter:
                seg = text[seg_start:seg_end].strip()
                if not seg:
                    raise ParseError(seg_end, ch)
                segs.append((seg, True))
                seg_start = seg_end + 1

        if seg_start > seg_end:
            # The text ends with the delimiter.
            if not allow_delimiter_end:
                raise ParseError(seg_end, delimiter)
        else:
            # The text ends with a segment.
            segs.append((text[seg_start:].strip(), False))

        return segs

    @staticmethod
    def parse(text):
        pipes = AST.clear_split(text, '&', True)
        return [(AST.parse_pipe(pipe), bg) for pipe, bg in pipes]

    @staticmethod
    def parse_pipe(text):
        commands = AST.clear_split(text, '|', False)
        return [AST.parse_command(command) for command, _ in commands]

    @staticmethod
    def parse_command(text):
        tokens = text.split()

        args = []
        rin, rout, rapp = None, None, None
        fin, fout, fapp = False, False, False
        for token in tokens:
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
