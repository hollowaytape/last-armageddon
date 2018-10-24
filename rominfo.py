"""
    Rom info for Last Armageddon.
"""
ORIGINAL_DATA_TRACK = 'original/track2.bin'
DATA_START_IN_ISO = 0x78c3f0

class Segment:
    def __init__(self, start, stop, name):
        self.start = start
        self.stop = stop
        self.name = name

        self.iso_start = DATA_START_IN_ISO + start
        self.iso_stop = DATA_START_IN_ISO + stop

        self.filename = '%s_%s.bin' % (hex(start), name)

    def safe_offset(self):
        return hex(self.iso_start)[2:].zfill(8)

# Offsets of locations in track2.bin (89,227 KB, headered).
SEGMENTS = [
    #Segment(0x09448, 0x1373c, "Encyclo-1"),
    #Segment(0x9300, 0x9c30, "Encyclo-1"),  # One sector of encyclopedia
    #Segment(0x13aab, 0x13ae6, "MainMenu"),
    #Segment(0x16f90, 0x189f0, "Debug"),
    #Segment(0x25e60, 0x26790, "Encyclo-2"),

    #Segment(0x55473c0, 0x554bbf0, "FontImg"),
    Segment(0x5608bc0, 0x56094f0, "Menu"),
]

# Font is in iso at 0x5cd37a0-0x5cd7fe0.
# (55473b0-)

# 2352 = 0x930
# 2048 = 0x800