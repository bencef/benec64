from collections import namedtuple


def unpack16(word):
    return [word & 0xff, word >> 8]

class CharLiteralError(Exception):
    def __init__(self, char):
        super(CharLiteralError, self).__init__('No char literal for ' + repr(char))

class WrongRegisterError(Exception):
    def __init__(self, register):
        super(WrongRegisterError, self).__init__('No such register: ' + repr(register))

lut = {' ': 0x20,
       'A': 0x41,
       'B': 0x42,
       'C': 0x43,
       'D': 0x44,
       'E': 0x45,
       'F': 0x46,
       'G': 0x47,
       'H': 0x48,
       'I': 0x49,
       'J': 0x4a,
       'K': 0x4b,
       'L': 0x4c,
       'M': 0x4d,
       'N': 0x4e,
       'O': 0x4f,
       'P': 0x50,
       'Q': 0x51,
       'R': 0x52,
       'S': 0x53,
       'T': 0x54,
       'U': 0x55,
       'V': 0x56,
       'W': 0x57,
       'X': 0x58,
       'Y': 0x59,
       'Z': 0x5a}

def string(str):
    result = []
    for c in str:
        try:
            result.append(lut[c])
        except KeyError as e:
            raise CharLiteralError(c) from e
    return result

class XIndexed():
    def __init__(self, base):
        self.base = base

class YIndexed():
    def __init__(self, base):
        self.base = base

def index(base, register):
    if register == 'x':
        return XIndexed(base)
    elif register == 'y':
        return YIndexed(base)
    else:
        raise WrongRegisterError(register)

Asm = namedtuple('Asm', ['label', 'address', 'data'])
Variant = namedtuple('Variant', ['opcode', 'length'])


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


class rts(Instruction):

    def __init__(self, label=None):
        self.label = label

    def get_data(self):
        return (1, [0x60])


class jmp(Instruction):

    ABS = Variant(0x4C, 3)
    IND = Variant(0x6C, 3)

    def __init__(self, address, label=None):
        self.label = label
        self.variant = self.ABS
        self.address = address

    def get_data(self):
        result = [self.variant.opcode]
        result.extend(unpack16(self.address))
        return (self.variant.length, result)


class ldx(Instruction):

    IMM = Variant(0xA2, 2)
    ZPAGE = Variant(0xA6, 2)
    ABS = Variant(0xAE, 3)
    ZPAGEY = Variant(0xB6, 2)
    ABSY = Variant(0xBE, 3)

    def __init__(self, value_or_address, label=None):
        self.label = label
        if False:
            pass
        else:
            self.variant = self.IMM
            self.value = value_or_address

    def get_data(self):
        result = [self.variant.opcode, self.value]
        return (self.variant.length, result)


class inx(Instruction):

    IMP = Variant(0xE8, 1)

    def __init__(self, label=None):
        self.label = label
        self.variant = self.IMP

    def get_data(self):
        result = [self.variant.opcode]
        return (self.variant.length, result)


class cpx(Instruction):

    IMM = Variant(0xE0, 2)
    ZPAGE = Variant(0xE4, 3)
    ABS = Variant(0xEC, 4)

    def __init__(self, address, label=None):
        self.label = label
        if False:
            pass
        else:
            self.variant = self.ABS
            self.address = address

    def get_data(self):
        result = [self.variant.opcode]
        result.extend(unpack16(self.address))
        return (self.variant.length, result)


class data(Instruction):

    def __init__(self, data, label=None):
        self.label = label
        self.data = data

    def get_data(self):
        return (len(self.data), self.data)
