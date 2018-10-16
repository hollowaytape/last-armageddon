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

# System Text
* The game probably uses PCE system functions for the normal black/white kanji.
	* Try corrupting the PCE card's kanji table and see what happens?

# Audio
* All the cut scenes are voice acted. That's a shame.
	* Some PCE hack mentioned putting JPEG subtitles in with a scene? Find that RHDN entry again.
	* The split audio tracks don't include the voice-acting audio.
	* Does the debug menu allow access to this audio?