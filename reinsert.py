"""
    LA reinserter.
    Based on the CRW reinserter base.
"""

import os
from shutil import copyfile

from rominfo import SEGMENTS, ImgSegment, SjisSegment, PointerSegment, CodeSegment
from asm import EDITS
from romtools.dump import DumpExcel, SegmentPointer

DUMP_XLS_PATH = 'LA_Text.xlsx'

Dump = DumpExcel(DUMP_XLS_PATH)

copyfile('original/LA7.iso', 'patched/LA7.iso')

# Stuff to always include
EDITED_IMG_SEGMENTS = [
    ImgSegment(0x5547cd0, 0x55484d0, "FontBlue-40-7f"),
    ImgSegment(0x554a190, 0x554a990, "FontBlack-40-7f"),
]

POINTER_SEGMENTS = [ps for ps in SEGMENTS if isinstance(ps, PointerSegment)]
for ps in POINTER_SEGMENTS:
    copyfile('original/%s' % ps.filename, 'patched/%s' % ps.filename)
    with open('patched/%s' % ps.filename, 'rb') as f:
        ps.string = f.read()

CODE_SEGMENTS = [cs for cs in SEGMENTS if isinstance(cs, CodeSegment)]
for cs in CODE_SEGMENTS:
    # Copy the code sgement
    copyfile('original/%s' % cs.filename, 'patched/%s' % cs.filename)
    with open('patched/%s' % cs.filename, 'rb') as f:
        ps.string = f.read()

    # Apply edits to the copied code segment
    with open('patched/%s' % cs.filename, 'rb+') as f:
        for e in EDITS:
            abs_address, new_code = e[0], e[1]
            if cs.start <= abs_address <= cs.stop:
                print("Doing an edit")
                local_address = abs_address - cs.start
                print(local_address)
                f.seek(local_address, 0)
                f.write(new_code)

edited_segments = [] + EDITED_IMG_SEGMENTS + CODE_SEGMENTS

def segment_with_pointer(location):
    for ps in POINTER_SEGMENTS:
        if ps.start <= location <= ps.stop:
            return ps
    return None

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


for seg in SEGMENTS:
    if isinstance(seg, ImgSegment):
        continue
    elif isinstance(seg, CodeSegment):
        continue
    edited = False
    print(seg.filename)
    for t in Dump.get_translations(seg.filename, sheet_name="LA", include_blank=True):
        #print(t.japanese.decode('shift-jis'))
        #print(t.english)
        if t.english != b'':
            edited = True

    if edited:
        print(seg.filename, "was edited")
        copyfile('original/%s' % seg.filename, 'patched/%s' % seg.filename)
        edited_segments.append(seg)
        with open('patched/%s' % seg.filename, 'rb+') as f:
            seg_filestring = f.read()

            diff = 0
            #last_offset = 0

            for t in Dump.get_translations(seg.filename, sheet_name="LA", include_blank=True):
                if not isinstance(seg, SjisSegment):
                    print(t.japanese.decode('shift-jis'))
                    #print(t.pointer, segment_with_pointer(t.pointer))
                    if t.pointer and diff != 0:
                        # TODO: Need to point to something much lower
                        t.pointer = SegmentPointer(segment=segment_with_pointer(t.pointer),
                                                   pointer_location=t.pointer,
                                                   text_location=t.location)

                    #for entry in TABLE:
                    #    print(entry, TABLE[entry])
                    tabled_jp = b''
                    buf = t.japanese
                    while buf:
                        if len(buf) >= 2:
                            #print(buf[0:2])
                            if buf[0:2] in TABLE:
                                tabled_jp += TABLE[buf[0:2]]
                                print(TABLE[buf[0:2]])
                                buf = buf[2:]
                            else:
                                #print(buf[0].to_bytes(1, 'little'))
                                tabled_jp += TABLE[buf[0].to_bytes(1, 'little')]
                                buf = buf[1:]
                        else:
                            tabled_jp += TABLE[buf[0].to_bytes(1, 'little')]
                            buf = b''

                    # Text replacements if necessary
                    if t.english == b'':
                        continue
                    print(tabled_jp)
                    t.japanese = tabled_jp

                else:
                    # Make the lowercase letters safe
                    safe_string = b''
                    print("Processing a sjis string")

                    marks = [b'\x40', b'\x49', b'\x68', b'\x94', b'\x90', b'\x93', b'\x95', b'\x66',
                             b'\x69', b'\x6a', b'\x96', b'\x7b', b'\x43', b'\x5b', b'\x44', b'\x5e', ]

                    marks2 = [b'\x46', b'\x47', b'\x83', b'\x81', b'\x84', b'\x48', b'\x97']

                    for c in t.english:
                        # Punctuation 1
                        if c < 0x30:
                            safe_string += marks[c-0x20]
                        # Numbers
                        elif c <= 0x39:
                            safe_string += (c + 0x1f).to_bytes(1, 'little')
                        # Punctuation 2
                        elif c <= 0x40:
                            safe_string += marks2[c-0x3a]
                        # Uppercase
                        elif c <= 0x60:
                            safe_string += (c + 0x1f).to_bytes(1, 'little')
                        # Lowercase
                        else:
                            safe_string += (c + 0x20).to_bytes(1, 'little')
                    t.english = safe_string

                    # Reinsert the same string if no translation

                    if t.english == b'':
                        t.english = t.japanese



                try:
                    i = seg_filestring.index(t.japanese)
                    print(i, t.location)
                    this_diff = len(t.english) - len(t.japanese)
                    seg_filestring = seg_filestring.replace(t.japanese, t.english, 1)

                    if t.pointer is not None and diff != 0:
                        #print("About to try to edit pointer")
                        t.pointer.edit(diff)
                        print("Edited pointer")
                    diff += this_diff

                except ValueError:
                    for c in t.japanese:
                        print(hex(c)),
                    print()
                    print(t.japanese, "(%s)" % t.japanese.decode('shift-jis'), "not found")

            while diff < 0:
                seg_filestring += b'\x00'
                diff += 1
            assert diff == 0
            f.seek(0)
            f.write(seg_filestring)

for p in POINTER_SEGMENTS:
    with open('patched/%s' % p.filename, 'rb+') as f:
        f.write(p.string)
    edited_segments.append(p)

# Write the edit.lst file here instead of in rip_segments.py.
# Use only the segments that got edited.
with open('patched/edit.lst', 'w') as lst:
    for s in edited_segments:
        lst.write(s.safe_offset() + ',' + 'patched/' + s.filename + '\n')

os.system("isopatch patched/edit.lst patched/LA7.iso /M1")


"""
    Try to undo the random other damage done by isopatch
"""
with open('original/LA7.iso', 'rb+') as original:
    with open('patched/LA7.iso', 'rb+') as patched:
        while True:
            preamble = original.read(16)
            preamble2 = patched.read(16)
            data = original.read(2048)
            data2 = patched.read(2048)
            mode_1_stuff = original.read(288)
            mode_1_stuff2 = patched.read(288)

            #print(data[:20])
            #print(data2[:20])
            if data[:20] != data2[:20]:
                print(data[:20])
                print(data2[:20])


            if preamble == b'':
                break