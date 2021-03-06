from instruction import unpack16

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
        program_counter = new_counter
    result = unpack16(start_address)
    result.extend(link(output))
    return result


def link(asm):
    '''List Asm -> List Word8'''
    def get_address(addr):
        inst = next(filter(lambda i: i.label == addr, asm))
        return unpack16(inst.address)
    out = []
    for a in asm:
        for byte in a.data:
            if isinstance(byte, str):
                out.extend(get_address(byte))
            else:
                out.append(byte)
    return out
