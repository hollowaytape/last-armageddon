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

		Command "hikou" (hiragana)
		cb - ba - b3
		 y    h    a
			Yep. Editing RAM 

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

# Dumping
* Any dumper would ideally also convert the [ku]['] to a [gu] character, maybe in another column.