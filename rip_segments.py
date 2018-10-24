"""
    Rip sgements of Last Armageddon into separate files for easier reinsertion.
"""

from rominfo import ORIGINAL_DATA_TRACK, SEGMENTS

if __name__ == '__main__':
    with open(ORIGINAL_DATA_TRACK, 'rb') as f:
        full_file = f.read()
        for s in SEGMENTS:
            segment_contents = full_file[s.start:s.stop]
            with open('original/' + s.filename, 'wb') as g:
                g.write(segment_contents)

with open('patched/edit.lst', 'w') as f:
    for s in SEGMENTS:
        f.write(s.safe_offset() + '@' + s.filename + '\n')