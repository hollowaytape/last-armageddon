### Bestiary
* Width limit is 20 fullwidth chars
	* Probably less than this for the first 4 lines (which show sprite)
* Numbers and some punctuation don't seem to get properly encoded
	* < = "c"
		* Encoded as "83"; should get rerouted to 81 83 (but is getting written as 82 83)
	* > = "d"
	* ~ = (hirigana "i")
	* 1 = overline
	* 6 = hirigana "gu"
	* 0 = "^"
	* Looks like the branch that decreases 82 to 81 (if the value is <60) is not working as expected.
		* Check the reads to b57c, etc
		* "83" is above 60. We are encoding punctuation wrong in the reinserter.
* What is going on with the text anyway? Does this use the same ASM hack I applied to the rest of the text?
	* Actually, I haven't hacked the gameplay text at all - just replaced the font
	* Original text is SJIS
	* There's a hack to use a 16x16 font instead of 20x20 (sjis specific)
	* I think each letter fits into a 40x40 box on the screen
		* Any way to decrease this? (hex = 28)
	* Even though the 20x20 and 16x16 uppercase letters look similar, they are indeed smaller in the 16x16 one
* Text width hack attempt
	* Watching b57c-b59f
	* b57c-b58b are "AAAAA" (60), b58e are "BBBB" (61)
		* 20-21 are the index of reading
		* Bytes that increase with every read:
			* 00 +4
			* 1a +2
			* 1c increases by 1 for every line, I think?
			* 1d +2
				* 1d and 1c are probably used for coordinates of the text
			* 1e +40
			* 6f +2
				* This gets read from 2219, which gets inc'd twice
				* Removing one of the inc's: squishes the text a little too much
					( 380d -> ea ea ea)
				* Gets stored in X
				* X -> 2d32
				* LDA $2D31
				* STA $1D
				* 1c gets loaded later, then a bunch of ASL/ROL instructions
				* 1d gets loaded - clc, adc $1A, sta $1a
				* What is 70? Alternates between 0d/0e twice for each 6f read


### Gameplay
* last menu option choice (text speed?) crashes the game
	* Check if this is resolved after dump fixes

### Dump
* Missing text from dump (not AAAA'd)
	* Second menu option prompt (dare ga tsukai masuka?)
		* Fixed
	* Third menu option prompt ("dare ga watashi masuka?")
		* c0 deda B6 DE dc c2 bc d3 bf 86
		* Fixed
		* Third menu confirm prompt ("Orc no nani e watashi mosuka AAA AAAAAA AAAA Jin")
		* Third menu third option
			* Still broken
		* Third menu fourth option
			* Fixed
	* 5th menu confirm prompt (Orc AAAAAA A(na) A(na))
	* Last menu first option prompt ("me o"AAAAAAAA)
		* 92 7e 70 7c
		* Choices are (A(na), A(na), A(na))
* Check out the mingled katakana/hiragana the translator pointed out
	* Likely garbage - adjust the rominfo for these

### Tablets
* What's up with these right now?
* Maybe a different text display system? Doesn't seem to execute the SJIS code above
	* Doesn't display anything when the text is AAAA'd. Displays fine when the other text ASM is inserted, so probably a different system