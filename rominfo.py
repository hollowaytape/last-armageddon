"""
    Rom info for Last Armageddon.
"""
ORIGINAL_DATA_TRACK = 'original/track2_plain.bin'
DATA_START_IN_ISO = 0x78c3f0

def to_plain(h):
    """ 
        Convert a headered location to a plain one. 
    """
    # plain data0x22130 to 0x2d000
    #SjisSegment(0x25fa0,   0x339c0, 'Encyclopedia'),

    # Headered structure: 2048 data, 304 header stuff
    #                     0x800     0x130
    # Getting rid of headers: 
    #   Figure out how many sectors (0x930-long sections),
    #   then subtract how many headers (0x130-long sections).

    # Currently it is giving values too large by 0x10. Let me check if that's the case in another segment
    # Yep. Let's just subtract 0x10, then

    return h - ((h // 0x930) * 0x130) - 0x10

def to_headered(p):
    return p + ((p // 0x800) * 0x130) + 0x10

class Segment:
    def __init__(self, start, stop, name, pointer_constant=None, pointer_constant_odd_track=False):
        self.start = start
        self.stop = stop
        self.name = name

        self.iso_start = DATA_START_IN_ISO + to_headered(start)

        # Unused
        #self.iso_stop = DATA_START_IN_ISO + to_headered(stop)

        self.filename = '%s_%s.bin' % (name, hex(start)[2:].zfill(8),)

        self.pointer_constant = pointer_constant
        self.pointer_constant_odd_track = pointer_constant_odd_track

    def safe_offset(self):
        return hex(self.iso_start)[2:].zfill(8)

# Various other types of segments
class ImgSegment(Segment):
    pass

class CodeSegment(Segment):
    pass


class SjisSegment(Segment):
    pass


class PointerSegment(Segment):
    pass

# TODO: For pointers, can I skip the segment-defining part for them?
# WOuld be better just to get the location's value, adjust it, write new value
# to a "segment" file, and add that to the edit list.
# And either clean them up at the end or just leave htem for debugging.
    # Would need to make sure to put them all after the text segments, just in case a pointer needs to override part of a segment.

# Offsets of locations in track2_plain.bin.
# No longer using the headered locations.

SEGMENTS = [
    # Some bestiary text before MainMenu, but it doesn't get used.
    # The later versions get used
    SjisSegment(0x1124b, 0x11276, 'MainMenu'),
    Segment(0x1270e, 0x12f00, 'BestiaryNames'),
    SjisSegment(0x21138, 0x2d000, 'Bestiary'),
    ImgSegment(0x4a41b20, 0x4a42000, 'FontBlue-00-3f'),
    ImgSegment(0x4a42000, 0x4a42800, 'FontBlue-40-7f'),
    ImgSegment(0x4a42800, 0x4a43000, 'FontBlue-80-bf'),
    ImgSegment(0x4a43000, 0x4a43800, 'FontBlue-c0-ff'),
    ImgSegment(0x4a43b20, 0x4a44000, 'FontBlack-00-3f'),
    ImgSegment(0x4a44000, 0x4a44800, 'FontBlack-40-7f'),
    ImgSegment(0x4a44800, 0x4a45000, 'FontBlack-80-bf'),
    ImgSegment(0x4a45000, 0x4a45800, 'FontBlack-c0-ff'),
    Segment(0x4a181e6, 0x4a18236, 'PartyNames'),
    Segment(0x4a182a6, 0x4a184d4, 'Skills', pointer_constant=0x42a6),
    Segment(0x4a19474, 0x4a194cc, 'SpellSystem'),
    Segment(0x4a1975c, 0x4a19c50, 'Spells'),
    SjisSegment(0x4a20000, 0x4a23800, 'Tablets'),
    Segment(0x4a23a23, 0x4a23a2d, 'Jin1'),
    Segment(0x4a25700, 0x4a2570e, "CombatPrompt"),
    Segment(0x4a2571c, 0x4a25743, 'Combat1'),
    Segment(0x4a25c29, 0x4a25c44, 'CombatSomething'),
    Segment(0x4a25d52, 0x4a25d58, 'Arimasen1'),
    Segment(0x4a26f0b, 0x4a26f21, 'MissMessage'),
    Segment(0x4a27728, 0x4a27769, 'StatsMenu1'),
    Segment(0x4a27779, 0x4a277e0, 'StatsMenu2'),
    Segment(0x4a27daf, 0x4a27e2b, 'CreationSystem'),
    Segment(0x4a4624a, 0x4a46254, 'Jin2'),
    Segment(0x4a4817e, 0x4a48186, 'Combat2'),
    Segment(0x4a48196, 0x4a481c9, 'Combat3'),
    Segment(0x4a48765, 0x4a48780, 'CombatDunno'),
    Segment(0x4a4888c, 0x4a48892, 'Arimasen2'),
    Segment(0x4a49b30, 0x4a49b42, 'CombatDunno'),
    Segment(0x4a49b69, 0x4a49b7f, 'CombatDunno'),
    Segment(0x4a4a396, 0x4a4a3d7, 'BattleRewards'),
    Segment(0x4a4a3e7, 0x4a4a44e, 'StatUps'),
    CodeSegment(0x4a177b0, 0x4a177c0, 'SjisTextCode-1'),
    CodeSegment(0x4a1780d, 0x4a17810, 'SjisTextCode-2_5'),
    CodeSegment(0x4a17815, 0x4a17860, 'SjisTextCode-2'),
    Segment(0x4a4aa1d, 0x4a4aa96, 'Abilities'),
    Segment(0x4a4b3dd, 0x4a4b777, 'Enemies', pointer_constant=0xb3dd),
    SjisSegment(0x4aea329, 0x4aea339, 'BattleStart'),
    Segment(0x4aea339, 0x4aea33f, 'TabletNum'),
    Segment(0x4aea523, 0x4aea54b, 'Menu'),
    Segment(0x4afab27, 0x4afab46, 'Submenu1'),
    Segment(0x4afb19b, 0x4afb1ba, "Submenu2"),
    Segment(0x4afb1be, 0x4afb1c5, "SubmenuOnOff"),
    Segment(0x4afb1cb, 0x4afb1d7, "SubmenuSpeed"),
    Segment(0x4afb1dd, 0x4afb240, 'Submenu3'),
    Segment(0x4afb5cd, 0x4afb5e0, 'SubmenuQuestions'),
    Segment(0x4afb5f1, 0x4afb627, "SubmenuDunno"),
    Segment(0x4afb62b, 0x4afb63e, "SumbenuCreate"),
    Segment(0x4afb65c, 0x4afb6d0, "SubmenuAbilities", pointer_constant=0x6e5c),
    Segment(0x4afbc84, 0x4afbcd9, "Submenu4"),
    Segment(0x4afbceb, 0x4afbd30, 'StatsMenu3'),
    Segment(0x4afc351, 0x4afc369, 'UseMenu1'),
    Segment(0x4afc36f, 0x4afc39f, 'UseMenu2'),
    Segment(0x4afc894, 0x4afc8c1, 'Jin3'),
    Segment(0x4afcc3e, 0x4afcc45, 'YesNo'),
    Segment(0x4afd2e8, 0x4afd31d, 'Jin4'),
    Segment(0x4afd34a, 0x4afd383, 'Jin5'),
    Segment(0x4afd55c, 0x4afd573, "EquipMenuQuestion"),
    Segment(0x4afd9ad, 0x4afd9c6, 'EquipMenu1', pointer_constant=0x441d),
    Segment(0x4afd9ca, 0x4afd9d5, 'EquipMenu2'),
    Segment(0x4afdd59, 0x4afdd5f, 'Arimasen3'),
    Segment(0x4afdd9e, 0x4afde30, 'KeyItems', pointer_constant=0x959e),
    Segment(0x4afdfd6, 0x4afe168, 'Equipment', pointer_constant=0x97d6),

]

MERGED_STRINGS = {
    0x4aea537: 0x4afab32,  # Toss
}

# Font is in iso at 0x5cd37a0-0x5cd7fe0.
# (55473b0-)

# 2352 = 0x930
# 2048 = 0x800

# Spell: 8b 9f 84 9e

#a3e7 points to 55513b0
#so, pointer constant is 5546fc9.
#The pointer to 5551367 will be 



if __name__ == "__main__":
    for s in SEGMENTS:
        #print(s.name)
        print("Segment(%s, %s, '%s')," % (hex(to_plain(s.start)), hex(to_plain(s.stop)), s.name))
        #print(hex(s.start), hex(to_plain(s.start)))
        #print(hex(s.stop), hex(to_plain(s.stop)))