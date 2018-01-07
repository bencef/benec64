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


class lda(Instruction):

    Variant = namedtuple('Variant', ['opcode', 'length'])
    INDX = Variant(0xA1, 2)
    ZPAGE = Variant(0xA5, 2)
    IMM = Variant(0xA9, 2)
    ABS = Variant(0xAD, 3)
    INDY = Variant(0xB1, 2)
    ZPAGEX = Variant(0xB5, 2)
    ABSY = Variant(0xB9, 3)
    ABSX = Variant(0xBD, 3)

    def __init__(self, value_or_address, label=None):
        self.label = label
        if False:
            pass
        else:
            self.variant = self.IMM
            self.value = value_or_address

    def get_data(self):
        return (self.variant.length, [self.variant.opcode, self.value])
