from asm import asm
from instruction import *

msg = 'CICA'
msg_len = len(msg)

prg = [ldx(0x00),
       lda(index('text', 'x'), 'loop'),
       jsr(0xFFD2),
       inx(),
       cpx(msg_len),
       bne('loop'), # WARN TODO: Is this relative?
       rts(),
       data(string(msg), 'text')]

print(list(map(lambda x: hex(x), asm(0xC000, prg))))
