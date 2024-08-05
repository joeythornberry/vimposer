from io import BufferedReader, BufferedWriter

class WriteCounter:
    num_writes: int
    log: str

    def __init__(self):
        self.num_writes = 0
        self.log = ""

    def count_writes(self, new_writes: int, msg: str):
        self.num_writes += new_writes
        self.log = f"{self.log}\n{msg}"

    def reset(self):
        self.log = f"reset at num_writes = {self.num_writes}"
        self.num_writes = 0

def write_variable_length_number(file: BufferedWriter, num: int, write_counter: WriteCounter):
    """Write the given int to the given file as a variable-length number, and return its size in bytes. 

    The var-length writing function from the midi spec. Loads the number
    backwards into a buffer, and then prints that buffer backwards."""

    buffer = num & 0x7f # this will be the last byte we write to the file

    while (num >> 7) > 0:
        num = num >> 7
        buffer = buffer << 8
        buffer = buffer | 0x80 # set first bit
        buffer += (num & 0x7f)

    length = 0
    while True: # write the buffer backwards
        length += 1
        file.write((buffer & 0xff).to_bytes())
        if buffer & 0x80:
            buffer = buffer >> 8
        else:
            break

    write_counter.count_writes(length, f"added {length} byte varlen number")

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

def write_8(file: BufferedWriter, int8: int, write_counter: WriteCounter):
    """Write the given byte to the given file."""
    file.write(int8.to_bytes())
    write_counter.count_writes(1, "added 1 byte for write_8")

def write_16(file: BufferedWriter, int16: int, write_counter: WriteCounter):
    """Write the given bytes to the given file."""
    file.write(((int16 & 0xff00) >> 8).to_bytes())
    file.write((int16 & 0xff).to_bytes())
    write_counter.count_writes(2, "added 2 bytes for write_16")
