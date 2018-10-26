"""
    LA reinserter.
    Based on the CRW reinserter base.
"""

import os
from shutil import copyfile

from rominfo import SEGMENTS, ImgSegment, SjisSegment
from romtools.dump import DumpExcel

DUMP_XLS_PATH = 'LA_Text.xlsx'

Dump = DumpExcel(DUMP_XLS_PATH)

copyfile('original/LA7.iso', 'patched/LA7.iso')

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


edited_segments = []
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
        copyfile('original/%s' % seg.filename, 'patched/%s' % seg.filename)
        edited_segments.append(seg)
        with open('patched/%s' % seg.filename, 'rb+') as f:
            seg_filestring = f.read()

            for t in Dump.get_translations(seg.filename, sheet_name="LA", include_blank=True):
                print(t.japanese.decode('shift-jis'))

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
                try:
                    i = seg_filestring.index(tabled_jp)
                    print(i, t.location)
                    seg_filestring = seg_filestring.replace(tabled_jp, t.english, 1)
                except ValueError:
                    print(tabled_jp, "(%s)" % t.japanese.decode('shift-jis'), "not found")
            f.seek(0)
            f.write(seg_filestring)

# Write the edit.lst file here instead of in rip_segments.py.
# Use only the segments that got edited.
with open('patched/edit.lst', 'w') as lst:
    for s in edited_segments:
        lst.write(s.safe_offset() + ',' + 'patched/' + s.filename + '\n')

os.system("isopatch patched/edit.lst patched/LA7.iso /M1")
