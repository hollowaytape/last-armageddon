# ASM code locations and edits for Last Armageddon.

EDITS = [
    #
    #"""
    #    lda ($20)  ; (instead of lda ($20),y, which checks the second byte)
    #    nop
    #    nop
    #    beq $3831  ; jump if zero? 
    #    cmp #$60   ; cmp
    #    lda #$82
    #    sta $f9
    #    bcs $3825  ; skip next instruction if byte > 0x60
    #    dec $f9
    #"""

    (0x4a17815, b'\xb2\x20\xea\xea\xf0\x16\xc9\x60\xa9\x82\x85\xf9\xb0\x02\xc6\xf9'),


    # Skip "inc $20", do some more instructions, and add #$1f right after $20 gets loaded
    #(0x5516fff, b'\xd0\x02\xe6\x21\xb2\x20\x69\x1f'),

    # Use the 12x12 system font instead of 16x16
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

]