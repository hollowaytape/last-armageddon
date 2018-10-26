"""
    Text dumper for Last Armageddon.
    Based on a .tbl file which interprets characters.
"""
import xlsxwriter
from rominfo import ORIGINAL_DATA_TRACK, SEGMENTS, ImgSegment, SjisSegment

class Dumpstring:
    def __init__(self, string, segment, loc):
        self.string = string
        self.segment = segment
        self.loc = loc

workbook_FILENAME = 'LA_Text.xlsx'

workbook = xlsxwriter.Workbook(workbook_FILENAME)
header = workbook.add_format({'bold': True, 'align': 'center', 'bottom': True, 'bg_color': 'gray'})

if __name__ == '__main__':
    TABLE = {}
    sjis_strings = []
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
        file_contents = f.read()
        for s in SEGMENTS:
            if isinstance(s, SjisSegment):
                # Not yet implemented
                continue
            elif isinstance(s, ImgSegment):
                # Don't dump this one
                continue
            seg = file_contents[s.start:s.stop]
            cursor = 0
            buf = b''

            # Length of the buffer: also includes diacritic marks
            buflen = 0
            while cursor < len(seg):
                b = seg[cursor]

                # <END> control code. End the buffer
                if b == 0:
                    if len(buf) > 2:
                        print(hex(cursor), buf)
                        loc = cursor - buflen + 1
                        #g.write(s.name.encode() + b' ' + loc + b' ' + buf + b'\n')
                        sjis_strings.append(Dumpstring(buf, s, loc))
                    buf = b''
                    buflen = 0
                # ゛ increases the SJIS index of the previous char by 1
                elif b == 0x9e or b == 0xde:
                    if buf:
                        buf = buf[:-1] + (buf[-1] + 1).to_bytes(1, 'little')
                        buflen += 1
                # ﾟ does it by 2
                elif b == 0x9f or b == 0xdf:
                    if buf:
                        buf = buf[:-1] + (buf[-1] + 2).to_bytes(1, 'little')
                        buflen += 1
                # The normal case
                elif b in TABLE:
                    buf += TABLE[b]
                    buflen += 1
                # Something else. End the buffer
                else:
                    if len(buf) > 2:
                        print(hex(cursor), buf)
                        loc = cursor - buflen + 1
                        #g.write(s.name.encode() + b' ' + loc + b' ' + buf + b'\n')
                        sjis_strings.append(Dumpstring(buf, s, loc))
                    buf = b''
                    buflen = 0
                cursor += 1

            # Catch whatever's left in buf at the end of the segment
            if len(buf) > 2:
                print(hex(cursor), buf)
                loc = cursor - buflen + 1
                #g.write(s.name.encode() + b' ' + loc + b' ' + buf + b'\n')
                sjis_strings.append(Dumpstring(buf, s, loc))

    worksheet = workbook.add_worksheet("LA")
    for s in sjis_strings:

        worksheet.set_column('A:A', 15)
        worksheet.write(0, 0, 'Offset (Total)', header)

        worksheet.write(0, 1, 'Offset', header)

        # Block column should be narrow
        worksheet.set_column('C:C', 20)
        worksheet.write(0, 2, 'File', header)

        # JP column should be wide
        worksheet.set_column('D:D', 30)
        worksheet.write(0, 3, 'Japanese', header)

        # JP_LEN column
        worksheet.set_column('E:E', 5)
        worksheet.write(0, 4, 'JP_Len', header)

        # EN column
        worksheet.set_column('F:F', 30)
        worksheet.write(0, 5, 'English', header)

        # EN_LEN column
        worksheet.set_column('G:G', 5)
        worksheet.write(0, 6, 'EN_Len', header)

        # Comments column
        worksheet.write(0, 7, 'Comments', header)
        row = 1
        for s in sjis_strings:

            total_loc = '0x' + hex(s.loc + s.segment.start).lstrip('0x').zfill(8)
            loc = '0x' + hex(s.loc).lstrip('0x').zfill(3)
            segment = str(s.segment.filename)
            jp = s.string.decode('shift_jis_2004')


            worksheet.write(row, 0, total_loc)
            worksheet.write(row, 1, loc)
            worksheet.write(row, 2, segment)
            worksheet.write(row, 3, jp)

            # Also write JP to the EN column, per kuoushi request
            #worksheet.write(row, 6, jp)

            # Add the JP/EN length formulas.
            # TODO: Get a regex for this to ignore bracketed stuff
            # Excel can't do regex like GSheets...
            worksheet.write(row, 4, "=LEN(D%s)" % str(row+1))
            worksheet.write(row, 6, "=LEN(F%s)" % str(row+1))
            row += 1

    workbook.close()