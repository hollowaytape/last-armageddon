# Take a SJIS string and looks for its encoded version in track2.bin.

import re

search_string = 'こうげきは'

if __name__ == "__main__":

    # Populate the table
    TABLE = {}
    with open('LA_inverse.tbl', 'rb') as f:
        for line in f.readlines():
            try:
                token, meaning = line.split(b'=')
            except ValueError:
                token, meaning = line[0:1], bytes(line[3])
            meaning = meaning.rstrip(b'\r\n')
            if len(meaning) == 2:
                meaning = int(meaning, base=16).to_bytes(1, 'big')
            elif len(meaning) == 4:
                meaning = int(meaning, base=16).to_bytes(2, 'big')

            #print(token, meaning)
            TABLE[token] = meaning
            #print(token, meaning)

    encoded = b''

    sjis = search_string.encode('shift-jis')
    for i in range(len(sjis))[::2]:
        c = sjis[i:i+2]
        #print(TABLE[c])
        encoded += TABLE[c]

    #print(encoded)

    with open('original/track2_plain.bin', 'rb') as f:
        contents = f.read()
        #print(contents)
        locs = re.finditer(encoded, contents)
        for l in locs:
            print(hex(l.start()))

