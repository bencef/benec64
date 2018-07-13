from asm import asm
from instruction import lda, jmp, ldx

program = [lda(0x41, label='start'),
           jmp(0xFFD2),
           ldx(0xBE)]


def main():
    code = bytes(asm(0xC000, program))
    # print('Program: ' + repr(code))
    with open('out.prg', 'wb') as f:
        f.write(code)

if __name__ == '__main__':
    main()
