"""
    LA reinserter.
    Based on the CRW reinserter base.
"""

import os
from shutil import copyfile

from rominfo import SEGMENTS, ImgSegment, SjisSegment, PointerSegment
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

edited_segments = [] + EDITED_IMG_SEGMENTS

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

        print(token, meaning)
        TABLE[token] = meaning


for seg in SEGMENTS:
    if isinstance(seg, ImgSegment):
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
                    print(t.pointer, segment_with_pointer(t.pointer))
                    if t.pointer:
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

                try:
                    i = seg_filestring.index(t.japanese)
                    print(i, t.location)
                    this_diff = len(t.english) - len(t.japanese)
                    seg_filestring = seg_filestring.replace(t.japanese, t.english, 1)

                    print("About to try to edit pointer")
                    t.pointer.edit(diff)
                    print("Edited pointer")
                    diff += this_diff
                    # TODO: edit_pointers_in_range()
                    #last_offset = t.location
                except ValueError:
                    print(t.japanese, "(%s)" % t.japanese.decode('shift-jis'), "not found")
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
