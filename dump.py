"""
    Text dumper for Last Armageddon.
    Based on a .tbl file which interprets characters.
"""

from rominfo import ORIGINAL_DATA_TRACK, SEGMENTS

if __name__ == '__main__':
    TABLE = {}
    with open('LA.tbl', 'rb') as f:
        for line in f.readlines():
            try:
                token, meaning = line.split(b'=')
            except ValueError:
                token, meaning = line[0:1], bytes(line[3])
            token = int(token, base=16)
            meaning = meaning.rstrip(b'\n')
            TABLE[token] = meaning 

    with open(ORIGINAL_DATA_TRACK, 'rb') as f:
        with open('dump.txt', 'wb') as g:
            file_contents = f.read()
            for s in SEGMENTS:
                seg = file_contents[s.start:s.stop]
                cursor = 0
                buf = b''
                while cursor < len(seg):
                    b = seg[cursor]
                    #print(b)
                    #print(TABLE)
                    # TODO: If it's a breath mark, change the most recent character.
                    if b == 0:
                        if len(buf) > 2:
                            print(hex(cursor), buf)
                            loc = hex(cursor + s.start - len(buf)).encode()
                            g.write(s.name.encode() + b' ' + loc + b' ' + buf + b'\n')
                        buf = b''
                    elif b in TABLE:
                        buf += TABLE[b]
                    else:
                        if len(buf) > 2:
                            print(hex(cursor), buf)
                            loc = hex(cursor + s.start - len(buf)).encode()
                            g.write(s.name.encode() + b' ' + loc + b' ' + buf + b'\n')
                        buf = b''
                    cursor += 1

