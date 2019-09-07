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

        self.filename = '%s_%s.bin' % (name, hex(start)[2:].zfill(8),)

    def safe_offset(self):
        return hex(self.iso_start)[2:].zfill(8)


class ImgSegment(Segment):
    pass

class CodeSegment(Segment):
    pass


class SjisSegment(Segment):
    pass


class PointerSegment(Segment):
    pass

# Offsets of locations in track2.bin (89,227 KB, headered).

SEGMENTS = [
    # Names1/2 don't appear to show up. And the encyclopedia part is unused.
    # Maybe everything before MainMenu is unused?
    #Segment(0x60cc, 0x63f0, "Names1"),
    #Segment(0x6520, 0x69e5, "Names2"),
    #SjisSegment(0x9440, 0x9b10, "Encyclo-01"),  # One sector of encyclopedia
    #SjisSegment(0x9c40, 0xa440, "Encyclo-02"),  # One sector of encyclopedia
    #SjisSegment(0xa570, 0xad70, "Encyclo-03"),  # One sector of encyclopedia
    #SjisSegment(0xaea0, 0xb6a0, "Encyclo-04"),  # One sector of encyclopedia
    #SjisSegment(0xb7d0, 0xbfd0, "Encyclo-05"),  # One sector of encyclopedia
    #SjisSegment(0xc100, 0xc900, "Encyclo-06"),  # One sector of encyclopedia
    #SjisSegment(0xca30, 0xd230, "Encyclo-07"),  # One sector of encyclopedia
    #SjisSegment(0xd360, 0xdb60, "Encyclo-08"),  # One sector of encyclopedia
    #SjisSegment(0xdc90, 0xe490, "Encyclo-09"),  # One sector of encyclopedia
    #SjisSegment(0xe5c0, 0xedc0, "Encyclo-10"),  # One sector of encyclopedia
    #SjisSegment(0xeef0, 0xf6f0, "Encyclo-11"),  # One sector of encyclopedia
    #SjisSegment(0xf820, 0x10020, "Encyclo-12"),  # One sector of encyclopedia
    #SjisSegment(0x10150, 0x10950, "Encyclo-13"),  # One sector of encyclopedia
    #SjisSegment(0x10a80, 0x11280, "Encyclo-14"),  # One sector of encyclopedia
    #SjisSegment(0x113b0, 0x11bb0, "Encyclo-15"),  # One sector of encyclopedia
    #SjisSegment(0x11ce0, 0x124e0, "Encyclo-16"),  # One sector of encyclopedia
    #SjisSegment(0x12610, 0x12e10, "Encyclo-17"),  # One sector of encyclopedia
    #SjisSegment(0x12f40, 0x13740, "Encyclo-18"),  # One sector of encyclopedia

    SjisSegment(0x13abb, 0x13ae6, "MainMenu"),  # Uses SJIS, also crashes maybe
    Segment(0x151de, 0x152d0, "EncycloNames1"),
    Segment(0x15400, 0x15afe, "EncycloNames2"),
    #Segment(0x16f90, 0x174d7, "Debug"),
    SjisSegment(0x25fa0, 0x26670, "Encyclo-01"),
    SjisSegment(0x267a0, 0x26fa0, 'Encyclo-02'),
    SjisSegment(0x270d0, 0x278d0, 'Encyclo-03'),
    SjisSegment(0x27a00, 0x28200, 'Encyclo-04'),
    SjisSegment(0x28330, 0x28b30, 'Encyclo-05'),
    SjisSegment(0x28c60, 0x29460, 'Encyclo-06'),
    SjisSegment(0x29590, 0x29d90, 'Encyclo-07'),
    SjisSegment(0x29ec0, 0x2a6c0, 'Encyclo-08'),
    SjisSegment(0x2a7f0, 0x2aff0, 'Encyclo-09'),
    SjisSegment(0x2b120, 0x2b920, 'Encyclo-10'),
    SjisSegment(0x2ba50, 0x2c250, 'Encyclo-11'),
    SjisSegment(0x2c380, 0x2cb80, 'Encyclo-12'),
    SjisSegment(0x2ccb0, 0x2d4b0, 'Encyclo-13'),
    SjisSegment(0x2d5e0, 0x2dde0, 'Encyclo-14'),
    SjisSegment(0x2df10, 0x2e710, 'Encyclo-15'),
    SjisSegment(0x2e840, 0x2f040, 'Encyclo-16'),
    SjisSegment(0x2f170, 0x2f970, 'Encyclo-17'),
    SjisSegment(0x2faa0, 0x302a0, 'Encyclo-18'),
    SjisSegment(0x303d0, 0x30bd0, 'Encyclo-19'),
    SjisSegment(0x30d00, 0x31500, 'Encyclo-20'),
    SjisSegment(0x31630, 0x31e30, 'Encyclo-21'),
    SjisSegment(0x31f60, 0x32760, 'Encyclo-22'),
    SjisSegment(0x32890, 0x33090, 'Encyclo-23'),
    SjisSegment(0x331c0, 0x339c0, 'Encyclo-24'),

    ImgSegment(0x55476c0, 0x5547ba0, "FontBlue-00-3f"),
    ImgSegment(0x5547cd0, 0x55484d0, "FontBlue-40-7f"),
    ImgSegment(0x5548600, 0x5548e00, "FontBlue-80-bf"),
    ImgSegment(0x5548f30, 0x5549730, "FontBlue-c0-ff"),

    ImgSegment(0x5549b80, 0x554a060, "FontBlack-00-3f"),
    ImgSegment(0x554a190, 0x554a990, "FontBlack-40-7f"),
    ImgSegment(0x554aac0, 0x554b2c0, "FontBlack-80-bf"),
    ImgSegment(0x554b3f0, 0x554bbf0, "FontBlack-c0-ff"),

    PointerSegment(0x5517ad2, 0x5517aea, "NamesCPointers"),
    Segment(0x5517af6, 0x5517b46, "NamesC"),

    PointerSegment(0x5517b46, 0x5517bb6, "SkillsPointers"),
    Segment(0x5517bb6, 0x5517de4, "Skills"),

    Segment(0x5518fe4, 0x551903c, "SpellSystem"),
    Segment(0x55192cc, 0x5519370, "Spells1"),  # Splits at sector boundary
    Segment(0x55194a0, 0x55198f0, "Spells2"),

    SjisSegment(0x5520c10, 0x5521410, "Tablets1"),
    SjisSegment(0x5521540, 0x5521d40, "Tablets2"),
    SjisSegment(0x5521e70, 0x5522670, "Tablets3"),
    SjisSegment(0x55227a0, 0x5522fa0, "Tablets4"),
    SjisSegment(0x55230d0, 0x55238d0, "Tablets5"),
    SjisSegment(0x5523a00, 0x55241c0, "Tablets6"),
    SjisSegment(0x5524330, 0x5524b30, "Tablets7"),

    Segment(0x5524e83, 0x5524e8d, "Jin1"),

    #Segment(0x5526ef0, 0x5526f33, "Combat1"),  # maybe Combat2 is the right one?

    Segment(0x55293d8, 0x55294b0, "StatsMenu1"),

    Segment(0x5529b8f, 0x5529c0b, "CreationSystem"),
    Segment(0x554c899, 0x554c8a4, "Jin2"),
    Segment(0x554ec8e, 0x554ec96, "Combat2"),
    PointerSegment(0x554ec96, 0x554eca6, "CombatPointers"),
    Segment(0x554eca6, 0x554ecd9, "Combat3"),   # This one shows up in combat
    Segment(0x5551366, 0x55513a7, "Dunno4"),

    PointerSegment(0x55513a7, 0x55513b7, "StatUpsPointers"),
    Segment(0x55513b7, 0x555141e, "StatUps"),

    CodeSegment(0x5516e60, 0x5516e70, "SjisTextCode-1"),
    CodeSegment(0x5516ff5, 0x5517040, "SjisTextCode-2"),

    Segment(0x5551b1d, 0x5551b96, "Dunno5"),

    Segment(0x555260d, 0x5552a30, "Enemies"),
    SjisSegment(0x5608ef9, 0x5608f09, "BattleStart"),
    Segment(0x5608f09, 0x5608f0f, "TabletNum"),
    PointerSegment(0x56090e3, 0x56090f3, "MenuPointers"),
    Segment(0x56090f3, 0x560911b, "Menu"),

    PointerSegment(0x561be19, 0x561be27, "Submenu1Pointers"),
    Segment(0x561be27, 0x561be46, "Submenu1"),  # this one definitely crashes.
    Segment(0x561c5cb, 0x561c670, "Submenu2"),
    Segment(0x561c9fd, 0x561ca10, "SubmenuQuestions"),
    Segment(0x561d1e4, 0x561d290, "Submenu3"),

    PointerSegment(0x561d239, 0x561d24b, "StatsMenu2Pointers"),
    Segment(0x561d24b, 0x561d290, "StatsMenu2"),
    Segment(0x561d9db, 0x561da2f, "Submenu4"),

    Segment(0x561e054, 0x561e081, "Jin3"),
    Segment(0x561ebd8, 0x561ec0d, "Jin4"),

    PointerSegment(0x5551aff, 0x5551b1d, "Dunno5Pointers"),
    Segment(0x561f3c6, 0x561f3f5, "Dunno5"),

    Segment(0x561f7be, 0x561f850, "KeyItems"),
    Segment(0x561f9f6, 0x561fa20, "Equipment1"),
    Segment(0x561fb50, 0x561fcbd, "Equipment2"),

]

# Font is in iso at 0x5cd37a0-0x5cd7fe0.
# (55473b0-)

# 2352 = 0x930
# 2048 = 0x800

# Spell: 8b 9f 84 9e

#a3e7 points to 55513b0
#so, pointer constant is 5546fc9.
#The pointer to 5551367 will be 