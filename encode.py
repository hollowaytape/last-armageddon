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

    for s in b'ジンをてにいれた':
        print(TABLE[s])