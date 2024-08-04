from io import BufferedReader, BufferedWriter


def write_variable_length_number(file: BufferedWriter, num: int):
    """The var-length writing function from the midi spec. Loads the number
    backwards into a buffer, and then prints that buffer backwards."""

    buffer = num & 0x7f # this will be the last byte we write to the file
    
    while (num >> 7) > 0:
        num = num >> 7
        buffer = buffer << 8
        buffer = buffer | 0x80 # set first bit
        buffer += (num & 0x7f)

    while True: # write the buffer backwards
        file.write((buffer & 0xff).to_bytes())
        if buffer & 0x80:
            buffer = buffer >> 8
        else:
            break

def read_variable_length_number(file: BufferedReader) -> int:
    """Read and return a variable-length number from the given file. Copied
    from the midi spec."""
    num = int.from_bytes(file.read(1))
    if not num & 0x80:
        return num

    num = num & 0x7f
    while True:
        byte_read = int.from_bytes(file.read(1))
        num = (num << 7) + (byte_read & 0x7f)
        if not byte_read & 0x80:
            break
    return num

def write_8(file: BufferedWriter, int8: int):
    """Write the given byte to the given file."""
    file.write(int8.to_bytes())

def write_16(file: BufferedWriter, int16: int):
    """Write the given bytes to the given file."""
    file.write(((int16 & 0xff00) >> 8).to_bytes())
    file.write((int16 & 0xff).to_bytes())
