# ASM code locations and edits for Last Armageddon.
# To add a new edit - add it here, then add the piece of code as a CodeSegment in rominfo.py.
# (TODO: Automatically add CodeSegments based on what is in here!)

EDITS = [
    # SJIS text hack - switch to single-byte text
    #
    #"""
    #    lda ($20)  ; (instead of lda ($20),y, which checks the second byte)
    #    nop
    #    nop
    #    beq $3831  ; jump if zero? 
    #    cmp #$4e   ; cmp - 83 > 4e = -> Z = 0, C = 1
    #    lda #$82
    #    sta $f9
    #    bcs $3825  ; skip next instruction if byte > 0x4e
    #    dec $f9
    #    
    #"""
    # another idea: cmp 4e, if it's lower also add 4e or something
        # This won't work since by that time, $f9 = 82

    #(0x4a17815, b'\xb2\x20\xea\xea\xf0\x16\xc9\x60\xa9\x82\x85\xf9\xb0\x02\xc6\xf9'),
    (0x4a17815,  b'\xb2\x20\xf0\x18\xc9\x4e\xa9\x82\x85\xf9\xb0\x04\xc6\xf9\xea\xea'),
    # Tried adding "69 47" (adc 47) to the nops at the end - won't trigger correctly


    # Skip "inc $20", do some more instructions, and add #$1f right after $20 gets loaded
    #(0x5516fff, b'\xd0\x02\xe6\x21\xb2\x20\x69\x1f'),

    # Use the 12x12 system font instead of 16x16 for SJIS
    #"""
    #    lda #$01   ; replace a "stz ff" with this, to give the 12x12 argument (1) to EX_GETFNT
    #    sta $ff
    #    jsr $e060
    #    stz $f7    ; get more space by using stz instead of lda #$00, sta, etc
    #    stz $0000
    #"""
    (0x4a177b0, b'\xa9\x01\x85\xff\x20\x60\xe0\x64\xf7\x9c\x00\x00'),

    # bra 3815   ; jump back to the LDA ($20) instruction, not something else
    (0x4a17850, b'\xc4'),


    # Very bad text hack - halves cursor movement for fullwidth text (cuts each character off partially, hard to read)
    #(0x4a1780d, b'\xea\xea\xea'), # 0x4a1780d

]