"""
    Text dumper for Last Armageddon.
    Based on a .tbl file which interprets characters.
"""
import xlsxwriter
from rominfo import ORIGINAL_DATA_TRACK, SEGMENTS, ImgSegment, SjisSegment, PointerSegment, CodeSegment

class Dumpstring:
    def __init__(self, string, segment, loc, length):
        self.string = string
        self.segment = segment
        self.loc = loc
        self.length = length

def index_of_subsequence(seq, subseq):
    if subseq == []:
        return None

    for i in range(len(seq)):
        sl = seq[i:i+len(subseq)]
        if sl == subseq:
            return i
    return None

LOOKBACK = 400

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
            print(s.name)
            seg = file_contents[s.start:s.stop]
            cursor = 0
            buf = b''

            seg_sjis_strings = []

            # Length of the buffer: also includes diacritic marks
            buflen = 0

            # SJIS Segments
            if isinstance(s, SjisSegment):
                while cursor < len(seg):
                    #print(cursor)
                    b = seg[cursor]
                    if b == 0:
                        if len(buf) > 0:
                            loc = cursor - len(buf)
                            seg_sjis_strings.append(Dumpstring(buf, s, loc, len(buf)*2))
                        buf = b''
                        buflen = 0
                    elif 0x80 <= b <= 0x9f or 0xe0 <= b <= 0xef:
                        #print(bytes(contents[cursor]))
                        buf += b.to_bytes(1, byteorder='little')
                        cursor += 1

                        b = seg[cursor]
                        buf += b.to_bytes(1, byteorder='little')
                        buflen += 2
                    else:
                        if len(buf) > 2:
                            loc = cursor - len(buf)
                            seg_sjis_strings.append(Dumpstring(buf, s, loc, len(buf)*2))
                        buf = b''
                        buflen = 0

                    # Tablets are separated with long strings of 8140s, not 00s
                    if len(buf) > 10:
                        if buf[-10:] == b'\x81\x40\x81\x40\x81\x40\x81\x40\x81\x40':
                            loc = cursor - len(buf) + 1
                            seg_sjis_strings.append(Dumpstring(buf, s, loc, len(buf)*2))
                            buf = b''
                            buflen = 0

                    cursor += 1

                if len(buf) > 0:
                    loc = cursor - len(buf)
                    seg_sjis_strings.append(Dumpstring(buf, s, loc, len(buf)*2))
                buf = b''
                buflen = 0

                # TODO: Find pointers for SJIS strings? Maybe not necessary
                sjis_strings += seg_sjis_strings
                
            elif isinstance(s, ImgSegment):
                # Don't dump this one
                continue
            elif isinstance(s, PointerSegment):
                continue
            elif isinstance(s, CodeSegment):
                continue

            else:
                while cursor < len(seg):
                    b = seg[cursor]

                    # <END> control code. End the buffer
                    if b == 0:
                        if len(buf) > 2:
                            #print(hex(cursor), buf)
                            loc = cursor - buflen
                            #g.write(s.name.encode() + b' ' + loc + b' ' + buf + b'\n')
                            seg_sjis_strings.append(Dumpstring(buf, s, loc, buflen))
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
                            #print(hex(cursor), buf)
                            loc = cursor - buflen
                            #g.write(s.name.encode() + b' ' + loc + b' ' + buf + b'\n')
                            seg_sjis_strings.append(Dumpstring(buf, s, loc, buflen))
                        buf = b''
                        buflen = 0
                    cursor += 1

                # Catch whatever's left in buf at the end of the segment
                if len(buf) > 2:
                    #print(hex(cursor), buf)
                    loc = cursor - buflen
                    #g.write(s.name.encode() + b' ' + loc + b' ' + buf + b'\n')
                    seg_sjis_strings.append(Dumpstring(buf, s, loc, buflen))

                """
                    Find the pointer table for this series of strings.
                """
                # Find the sequence of increases in location.
                pointers_found = False

                vals = []
                diffs = []
                for i, _ in enumerate(seg_sjis_strings):
                    vals.append(seg_sjis_strings[i].loc)
                    if i+1 < len(seg_sjis_strings):
                        diffs.append(seg_sjis_strings[i+1].loc - seg_sjis_strings[i].loc)
                #print(diffs)

                # Now look in the last X bytes for a series of little-endian numbers that
                # increase in that precise sequence.
                with open('original/track2_plain.bin', 'rb') as f:
                    track = f.read()

                    # TODO: Really, need to try this with an odd number too
                    cursor = s.start - LOOKBACK
                    track_vals = []
                    track_diffs = []
                    odd_track_vals = []
                    odd_track_diffs = []

                    for b in range(0, LOOKBACK, 2):
                        #print(track[cursor+b:cursor+b+2])
                        val = int.from_bytes(track[cursor+b:cursor+b+2], byteorder='little')
                        track_vals.append(val)
                    for b in range(0, LOOKBACK, 2):
                        #print(track[cursor+b:cursor+b+2])
                        val = int.from_bytes(track[cursor+b+1:cursor+b+3], byteorder='little')
                        odd_track_vals.append(val)

                    #print(track_vals)
                    for i, _ in enumerate(track_vals):
                        if i+1 < len(track_vals):
                            track_diffs.append(track_vals[i+1] - track_vals[i])

                    for i, _ in enumerate(track_vals):
                        if i+1 < len(odd_track_vals):
                            odd_track_diffs.append(odd_track_vals[i+1] - odd_track_vals[i])
                #print(track_diffs)
                #print(odd_track_diffs)

                if diffs == []:
                    # The pointer table can't be found
                    pass
                else:
                    #print("diffs are", diffs)
                    ind = index_of_subsequence(track_diffs, diffs)
                    skip_first = False
                    if ind is None:
                        print("ind was none, trying again")
                        ind = index_of_subsequence(track_diffs, diffs[1:])
                        skip_first = True

                    if ind is None:
                        print("Couldn't find the pointers for this segment, trying odd lookback")
                        # TODO: Try using an odd lookback for these
                        ind = index_of_subsequence(odd_track_diffs, diffs)
                    else:
                        #print(track_diffs)
                        #print([hex(thing) for thing in track_vals[ind:ind+len(diffs)]])
                        table_start = s.start - LOOKBACK + (ind*2)
                        pointer_location = table_start
                        for sss in seg_sjis_strings:
                            if sss == seg_sjis_strings[0] and skip_first:
                                continue
                            sss.pointer = pointer_location
                            pointer_location += 2
                        pointers_found = True

                    if ind is None:
                        print("Couldn't find the pointers for this segment")
                        pointers_found = False
                    else:
                        # TODO: No, this is running whenever all pointers are found, odd lookback or not
                        # Found it with an odd lookback
                        #print(track_diffs)
                        #print([hex(thing) for thing in odd_track_vals[ind:ind+len(diffs)]])
                        print(hex(s.start), hex(LOOKBACK), hex(ind*2))
                        table_start = s.start - LOOKBACK + (ind*2)
                        print(hex(table_start))
                        # (Is this enough for the odd lookback thing?)
                        #table_start += 1
                        pointer_location = table_start
                        for sss in seg_sjis_strings:
                            if sss == seg_sjis_strings[0] and skip_first:
                                continue
                            sss.pointer = pointer_location
                            print(hex(sss.loc), hex(sss.pointer))
                            pointer_location += 2
                        pointers_found = True


                if not pointers_found and len(vals) > 1:
                    # TODO: Some way to hardcode the poitner constant once we've found it?
                    print("No pointers found - try a new approach")
                    #print(vals)
                    #print([hex(v) for v in track_vals])
                    # x = num in vals
                    # y = num in track_vals
                    # Z = pointer_constant
                    # Is there some Z for which every x+Z is present in y?
                    if not s.pointer_constant:
                        print("Trying to calculate pointer constant")
                        best_pc = 0
                        best_pc_string_count = 0
                        use_odd_track = 0

                        # for key items, it should be 0x4800
                        for z in range(0x1000, 0xffff):
                            current_pc_string_count = 0
                            for x in vals:
                                if x + z in track_vals:
                                    current_pc_string_count += 1
                            if current_pc_string_count > best_pc_string_count:
                                best_pc = z
                                best_pc_string_count = current_pc_string_count
                                #print(hex(best_pc), best_pc_string_count)

                        for z in range(0x1000, 0xffff):
                            current_pc_string_count = 0
                            for x in vals:
                                if x + z in odd_track_vals:
                                    current_pc_string_count += 1
                            if current_pc_string_count > best_pc_string_count:
                                best_pc = z
                                best_pc_string_count = current_pc_string_count
                                use_odd_track = True
                                s.pointer_constant_odd_track = True
                                #print(hex(best_pc), best_pc_string_count)

                        print("Best pointer constant is " + hex(best_pc) + " with %s strings (of %s)" % (best_pc_string_count, len(vals)))
                        if best_pc_string_count > (len(vals)) * 0.8:
                            print("Good enough, let's assume that is the right pointer constant")
                            print(s.filename, hex(best_pc))
                            s.pointer_constant = best_pc
                        else:
                            print("(Not good enough)")
                    else:
                        print("We can use the existing pointer constant")

                    # TODO: For Combat3, StatsMenu2, Combat1, PartyNames, Skills, StatUps, Abilities


                    if (s.pointer_constant):
                        for sss in seg_sjis_strings:
                            lookback_start = s.start - LOOKBACK
                            try:
                                if (s.pointer_constant_odd_track):
                                    pointer_location = (odd_track_vals.index(sss.loc + s.pointer_constant))*2 + lookback_start
                                else:
                                    pointer_location = (track_vals.index(sss.loc + s.pointer_constant))*2 + lookback_start
                                
                                sss.pointer = pointer_location
                                #print(hex(sss.loc + s.start), hex(pointer_location))
                            except ValueError:
                                #print("Not found")
                                pass

                print("")



                sjis_strings += seg_sjis_strings

    worksheet = workbook.add_worksheet("LA")

    worksheet.set_column('A:A', 12)
    worksheet.write(0, 0, 'Offset (Total)', header)

    worksheet.write(0, 1, 'Offset', header)

    worksheet.set_column('C:C', 12)
    worksheet.write(0, 2, 'Pointer', header)

    # Block column should be narrow
    worksheet.set_column('D:D', 20)
    worksheet.write(0, 3, 'File', header)

    # JP column should be wide
    worksheet.set_column('E:E', 30)
    worksheet.write(0, 4, 'Japanese', header)

    # JP_LEN column
    worksheet.set_column('F:F', 5)
    worksheet.write(0, 5, 'JP_Len', header)

    # EN column
    worksheet.set_column('G:G', 30)
    worksheet.write(0, 6, 'English', header)

    # EN_LEN column
    worksheet.set_column('H:H', 5)
    worksheet.write(0, 7, 'EN_Len', header)

    # Comments column
    worksheet.write(0, 8, 'Comments', header)
    row = 1

    for s in sjis_strings:

        if s.string.strip(b'\x81\x40') == b'':
            continue
        #print(row)

        total_loc = '0x' + hex(s.loc + s.segment.start).lstrip('0x').zfill(8)
        loc = '0x' + hex(s.loc).lstrip('0x').zfill(3)
        #print(loc)
        try:
            pointer = '0x' + hex(s.pointer).lstrip('0x').zfill(8)
        except AttributeError:
            pointer = ''
        segment = str(s.segment.filename)
        #print(s.string)
        try:
            jp = s.string.decode('shift_jis_2004')
        except UnicodeDecodeError:
            jp = "I dunno"
        #print(jp)
        length = s.length


        worksheet.write(row, 0, total_loc)
        worksheet.write(row, 1, loc)
        worksheet.write(row, 2, pointer)
        worksheet.write(row, 3, segment)
        worksheet.write(row, 4, jp)
        worksheet.write(row, 5, length)

        # Also write JP to the EN column, per kuoushi request
        #worksheet.write(row, 6, jp)

        # Add the JP/EN length formulas.
        #worksheet.write(row, 5, "=LEN(E%s)" % str(row+1))
        worksheet.write(row, 7, "=LEN(G%s)" % str(row+1))
        row += 1

    workbook.close()