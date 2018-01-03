from instruction import unpack16, jsr

# data Instruction
###
# Word16 -> (Asm, Word16)

# data Asm
###
# { label :: Maybe String
# , address :: Word16
# , data :: List (Either Word8 String) }


def asm(start_address, instructions):
    '''Word16 -> List Instruction -> List Word8'''
    output = []
    program_counter = start_address
    for instruction in instructions:
        (new_data, new_counter) = instruction(program_counter)
        output.append(new_data)
        program_counter += new_counter
    return fix(output)


def fix(asm):
    '''List Asm -> List Word8'''
    def extract(addr):
        inst = next(filter(lambda i: i['label'] == addr, asm))
        return unpack16(inst['address'])
    out = []
    for a in asm:
        for byte in a['data']:
            if isinstance(byte, str):
                out.extend(extract(byte))
            else:
                out.append(byte)
    return out
