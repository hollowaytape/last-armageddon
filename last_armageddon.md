# Game Text
track02.iso
Credits at 0
HP MP DEAD POIS, PARA SLEE STON @ 0x4a46580
main menu options (モンスタ) @ 0x11260
	monster encyclopedia text is from 0x8130 - 0x10ff0
	Also continues 21130 - 2c940 (maybe stats are here at the end?)
Debug mode text @ 0x14000
	List of audio scenes at 0x141dc - BASECAMP, GAMEOVER, TREE0-3, etc

Replacing 心して聞け、 with ＡＢＣａｂｃ: Game crashes
Replacing 1.6m with 1.6n: Can't read that encyclopedia entry
	Damn. The only fullwidth Latin characters allowed are k, g, and m.

There's clearly a font towards the end of the data track, with full English, small kana, and icons for items.
	But editing it doesn't seem to do anything? Maybe there's a duplicate somewhere.

Item names are in the full disk at x05ca570, in ASCII.
	Each one is preceded by a byte like 03, 0f, etc. Probably stands for the item symbol.
		21 different symbols. I bet some are for spells and such.
		A = 0x41, Z = 0x5A
		space = 0x60
		0x67 = little kata A
		0x71 = kata A
		0x7f = kata '/
		0x80 = kata be?
		0x9d = kata ')
		0x9e = "
		0xa0 = space? ln?
		0xa6 = hira ka
		0xa7 = hira lil a
		0xb0 = hira -
		0xb1 = hira a
		0xd0 = hira mi
		0xdd = hira n
		0xde = hira "
		0x ef - ff = more Latin characters for status elements?

		So, can I find the spell/item "shiato" (katakana)?
		9a - 71 - 84
			Yep! It's in there six times (3 times, then duplicated).
				0x5ca5ab6

		O - ku
		75 - 70 - 78

		Battle command: te-i-se-i c3 b2 be b2


		Command "hikou" (hiragana)
		cb - ba - b3
		 y    h    a
			Yep. Editing RAM 
			05D954E8

		Watching at 0x7028:
			* 0xea9c: STA ($FA), Y @ $7d28
				* Indirect Indexed, Y. 
					* 
			* $FA = 00 7d (7d00) + 28
			* STA ($FA), Y: A = (big-endian value at FA) + Y.
			* A = CB, the first byte. How'd it get there?
				* Prev instruction: LDA $1808       @1808 = $CB.
				* $1808 always has the next byte in it.
					*

Loop:
LDA $1808
STA ($FA, y)
LDA $F8
BNE $EAA4     ; (the lone DEC instruction below)
DEC $F9
DEC
STA $F8
ORA $F9       ; OR the accumulator with $F9
BEQ $EAB5
INY           ; increase Y
BNE $EA99     ; LDA $1808

Y acts as a counter, it increases as each byte is copied.
$F8-$F9 decreases by one as each byte is copied. (It gets loaded into A to do this)
The byte that gets loaded into 1808 when DEC happens (?) is one byte at a time coming from 0x5d93430 in the disk.
	* hikou at 0x5d954e8, 0x5da8e97

* $1800 changes from 88 ** to C8 ** when crossing the BNE, and C8 to 88 after the LDA $1808. How are these getting modified?
	* The 1800 section has something to do with the CD, and its "ID locations".
	* I have no idea where those particular bytes are coming from.

		Watch at 7d29 - that's where "hikou" gets loaded
			* 0x3add: LDA ($00),Y   @ $7d29 = $BA
				* Y = 01
				* 00 = 28
				* Load the address at the value specified by Y. (really indrect)
				
		"mu" 8x8 character - what would be its hex representation?
		* 20 f0 24 e2 a4 e4 e8
			* Not found anywhere.

* Menu options in RAM can be replaced with capital ASCII and they'll show up fine.

# System Text
* The game probably uses PCE system functions for the normal black/white kanji.
	* Try corrupting the PCE card's kanji table and see what happens?

# Audio
* All the cut scenes are voice acted. That's a shame.
	* Some PCE hack mentioned putting JPEG subtitles in with a scene? Find that RHDN entry again.
	* The split audio tracks don't include the voice-acting audio.
	* Does the debug menu allow access to this audio?
		* Yes
* Offsets after ADPCM debug menu scene names:
30 d1 0a 00 10 00 00
80 f1 0a 00 48 00 00
40 c2 0c 00 93 00 00
98 55 0d 00 98 00 00
c0 ed 0d 00 96 00 00
b0 83 0e 00 22 00 00
10 16 4e 00 63 00 00
18 7a 10 00 5f 00 00
f8 d9 10 00 14 01 00
a0 ed 11 00 11 01 00

BASECAMP = 10.51s
GAMEOVER = 4.57s
MAKAI = 19.59s
TREE0 = 38.25s
TREE1 = 40.53s


* Any kind of location I could get from this?
* Scrolling through the list:
	* First byte increments by 6
	* Byte D1 increments up to 09, then increments byte D2 and resets
	* FC and FE change to various different values

* Load the plain track into Audacity. (VOX ADPCM, normal sample rate, little endian)
	* Clear vocals punctuated by horiffic noise (graphics & data). Graphics every time there's a scene change.
	* Decrease the speed to around .36 of the original.


# Dumping
* Any dumper would ideally also convert the [ku]['] to a [gu] character, maybe in another column.

# Error correcting codes
* It appears that all of the data has a way of correcting itself after I edit it, and declares itself unrecoverable if it's edited too much.
	* Are the fuzzy sections the error-correcting parts?
	* Black+white kana segment: sector 41613
	* Latin text after that:    sector 41614
	* So yeah, the fuzzy sections occur before every sector.
		* Sectors are 8 rows of tiles (128 8x8 2-bit tiles = 2048 bytes
* The plain track2.iso doesn't have the error correcting fuzzy sections. 
* CD-ROM Mode 1. 12 (Sync pattern)	3 (Address)	1 (Mode, 0x01)	2,048 (Data)	4 (Error detection)	8 (Reserved, zero)	276 (Error correction)
	* A sector begins at 0x5cd77d0.
		* Sync pattern: 00 FF FF FF FF FF FF FF FF FF FF 00
		* Address: 09 16 66
		* Mode: 01
	* Error detection is a 32-bit CRC.
		* Hm. With and without the header, the CRC-32 doesn't seem to match what I get from a generator online.
	* Error correction is a RSPC (Reed Solomon)
* One possible solution - in a reinserter, reinsert blocks as Mode 2, which doesn't have error detection/correction. More room for data that way too.

* Scratch all that, use isopatch.
	* isopatch hikou.lst LA7.iso /M1
	* Try reinserting the whole data track?
		* That works. Use track2.iso (has headers + CRCs and stuff). Edit it, then run:
			* isopatch hikou.lst LA7.iso /M1
			* (can rename hikou.lst to anything)
			* Hm. This worked once but it's been crashing without patching the iso all the other times. Need to investigate further.

# Mapping
## Track2.bin (track 2 with headers)
(0x9448, 0x1373c),   # encyclopedia
Lots of headers in there, sometimes interrupting the string. Need to test out editing/reinserting the un-headered iso instead.

## track2.iso (no headers)
(0x8000, 0x11000) - a segment of encyclopedia, gets interrupted at 0x11000
(0x1124b, 0x11275) - main menu?
(0x14000, 0x16000) - debug menus
(0x21130, 0x2c950) - rest of encyclopedia


# A weird pattern I noticed
* There's a pattern around 0x1c7490 (in track2.bin) where there's 00*8, then roughly 0x100 later, FF*8. This occurs every 2352 bytes. Is this a header to ADPCM or something?
	* The 2352 is definitely related to some CD thing.
	* Maybe it's audio?

# More problems
* Reinserting by full 0x930 tracks doesn't seem to work. The changes are getting overwritten again.
	* Neither does reinserting 0x800 length tracks.
	* Try without the initial header line next?

# Pointers
* Before menu options, these values:
28 7d
2c 7d (+4) FLY
2f 7d (+3) SE
33 7d (+4) USE
37 7d (+4) TRA
3b 7d (+4) TOS
40 7d (+5) EQUP
47 7d (+7) ORDER_
* Yep, must be pointers.

# Unexplained crashes
* Certain segments being reinserted, with very minor changes that don't change the length, are causing consistent crashes.
	* Is it possible that isopatch's generated ECCs are incorrect? Need to check these.

	* Successful EDC calculation on this site: http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
		* Options: CRC-32, Custom, both reflections are True
		* Polynomial:      0x8001801B
		* Initial Value:   0x00000000
		* Final xor Value: 0x00000000
	* Hm. Well, these CRC values are correct at least.
* So, VBinDiff shows two edited bytes at the beginning that I didn't ask it for. Why's it doing this?
	* Restoring those two bytes and re-calculating the CRC-32 fixes the crash!

# System printing functions
* "Gargoyle" (82 66 82 81 82 92 82 87...) is at b57c.

Read every byte and prepend it with 82:
After this code: ee 19 22 ee 19 22 4c 96 37 a0 01 b1 20 12 20 f0 16
381b: lda $20 (b2 20) -> lda #$82 (a9 82)
381f: inc $20 (e6 20) -> nop nop (ea ea)

Next step: add 1f to the $21 value. (adc )
381b: adc $1f (69 1f)
381d: lda #$82 (a9 82)
381f: nop nop (ea ea)

Next steps after this: Add the condition where you check if it's lowercase, and if so add 1. (Optional)
Figure out how to get proper punctuation. Currently all the spaces just repeat the last character, and all the punctuation is coming out Greek.
	Need to find a proper map of all the characters.
		Well, it's just SJIS. I need to use proper sjis
		And also figure out if there's any ascii in there I guess.
	Need to do something like:
	381b: cmp #$40 (c9 40)
	381d: lda #$81 (81 a9)
	381f: sta $f9 (85 f9)
	3821: bcc +02 (90 02)
	3823: inc $f9 (36 f9)

Bytes that change as it looks at different text:
206f (goes up by 2 when writing text, by 1 while writing the sprite)
	206f comes from 2219
	There are two instructions "inc $2219", let's get rid of one
	Context is: 62651f851fee1922ee1922
		Replace one of the ee1922's with eaeaea
			This will work for a cursor hack. But the 12px font won't work - it only displays the left 8 pixels.

41f4 = Orc position
	Orc = 4f 72 63

I think 00 00 00 00 is a divider between records, maybe there are no pointers?
	TODO: Did I mess with the code that checks for 4 consecutive 00s?
		No, it's probably pointers. Text seems to be ending at the right places, if not beginning at the right ones.
		Second entry begins at byte 14a
		Third is at 256
		Fourth is at 360
		Pointer-detector isn't finding this because it's looking at the diffs of each consecutive string. Or not looking for sjis pointers at all...

$21 seems to be the row number. Messing with one of the binary shift operations done to it makes the rows smaller, but not in a helpful way.

TODO: Need to edit stuff like commas and numbers in the font, to make them fit better
* Palette:
	* Black is color 0 (50)
	* Grey is color e (5e)
	* Background is color 9 (59)

# Audio Mapping
"Actually, most of the VO in the first LoX game is ADPCM embedded in the data track, and not CD Audio ... but that's not really important.

Replacing sample data in the Knight Rider HuCard might not be too horrible. There are only a couple of sane ways to store it in a HuCard.

The "fun" would be in trying to figure out where it's stored, and how long it is.

If you're running Mednafen, then you'd put a breakpoint on the Timer IRQ or the HBLANK IRQ, and trace through the code to find out where the pointer to the sound data is stored."
	Need to do this on the ADPCM debug menu, that should help slice up the audio a bit
	Stuff that has to do with the first sample (BASECAMP): b9 0a 00 26 00 30
	b9 0a 00 26 00 00 30 (BASECAMP)
	41 0a 00 10 00 00 80 (GAMEOVER)
		Length: 4.11
			Change 10 -> 08: Only loads 2.37 of the sample, but continues playing the leftovers of another sample
	61 0a 00 48 00 00 40
	32 0c 00 93 00 00 98
	c5 0c 00 98 00 00 c0
		First byte: Changes start time ("overlay index"? Finer than second byte)
		Second byte: changing it totally changes what audio is played ("sector offset"?)
		Middle byte: Number of sectors? Length?
		Last two bytes seem to be the "write address" for the audio. Not sure why that would affect length
			BASECAMP (00 30) writes to 3000, GAMEOVER (80) to 8000, etc
			The length stuff may just be a coincidence.