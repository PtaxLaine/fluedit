
def offset_to_line(data, offset: int) -> (int, str):
    line = 1
    for i in range(offset):
        if data[i] == '\n':
            line += 1
    return line, data[offset:].split('\n', 1)[0].strip()
