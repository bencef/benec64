from collections import namedtuple


def unpack16(word):
    # TODO: byte order
    return [word & 0xff, word >> 8]

Asm = namedtuple('Asm', ['label', 'address', 'data'])


class Instruction:

    def __call__(self, addr):
        (length, data) = self.get_data()
        asm = Asm(self.label, addr, data)
        new_addr = addr+length
        return (asm, new_addr)


class jsr(Instruction):

    def __init__(self, jump_to, label=None):
        self.jump_to = jump_to
        self.label = label

    def get_data(self):
        out = [0x20]
        where = [self.jump_to]
        if not isinstance(self.jump_to, str):
            where = unpack16(self.jump_to)
        out.extend(where)
        return (3, out)
