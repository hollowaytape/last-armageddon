## Last Armageddon
* Romhacking tools and notes for Last Armageddon PCE-CD.
* Requires an ISO of the game, isopatch, and the 46 OkuMen romtools package.

### Getting an excel dump
```
	python rip_segments.py
	python dump.py
	excel LA_Text.xlsx
```

### Reinserting the edited script
```
	python reinsert.py
```

### Playing the game
```
	./mednafen/mednafen ./patched\LA7.cue
```

### Looking at stuff within the game
* Open WindHex, look at original/track2_plain.bin
* Use LA.tbl as the table