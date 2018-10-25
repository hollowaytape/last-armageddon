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

        self.filename = '%s_%s.bin' % (hex(start)[2:].zfill(8), name)

    def safe_offset(self):
        return hex(self.iso_start)[2:].zfill(8)

# Offsets of locations in track2.bin (89,227 KB, headered).
SEGMENTS = [
    Segment(0x60c5, 0x63f0, "Names1"),
    Segment(0x6520, 0x69e5, "Names2"),
    #Segment(0x9310, 0x9b10, "Encyclo-1"),  # One sector of encyclopedia
    #Segment(0x13aab, 0x13ae6, "MainMenu"),  # Uses SJIS
    Segment(0x151de, 0x152d0, "NamesA"),
    Segment(0x15400, 0x15afe, "NamesB"),
    Segment(0x16f90, 0x174d7, "Debug"),
    #Segment(0x25e70, 0x26670, "Encyclo-2"),

    #Segment(0x55473c0, 0x554bbf0, "FontImg"),

    Segment(0x5517af5, 0x5517de4, "Dunno5"),

    Segment(0x5518fe4, 0x5519040, "Spells1"),
    Segment(0x55194a0, 0x55198f0, "Spells2"),

    Segment(0x5526ef0, 0x5526f33, "Combat1"),

    #Segment(0x5528b90, 0x5529390, "Dunno1"),  # No text here?
    Segment(0x5529b8f, 0x5529de0, "Dunno2"),

    Segment(0x554ec88, 0x554eccd, "Combat2"),

    Segment(0x555260d, 0x5552a30, "Dunno3"),

    Segment(0x56090f5, 0x5609116, "Menu"),
    Segment(0x561be27, 0x561be44, "Submenu1"),
    Segment(0x561c5cb, 0x561c670, "Submenu2"),
    Segment(0x561d1e4, 0x561d290, "Submenu3"),
    Segment(0x561d9db, 0x561da2f, "Submenu4"),

    Segment(0x561f3c6, 0x55529a6, "Dunno4"),

    Segment(0x561fb50, 0x561fcbd, "Weapons"),
]

# Font is in iso at 0x5cd37a0-0x5cd7fe0.
# (55473b0-)

# 2352 = 0x930
# 2048 = 0x800

# Spell: 8b 9f 84 9e