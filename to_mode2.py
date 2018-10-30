with open('original/track2.bin', 'rb') as f:
    with open('original/track2_plain.bin', 'wb') as g:
        while True:
            preamble = f.read(16)
            data = f.read(2048)
            mode_1_stuff = f.read(288)

            if preamble == b'':
                break

            ## Set mode byte to 2
            #preamble = preamble[:15] + b'\x02'

            #g.write(preamble)
            g.write(data)
            #padding = b'\x00' * (288)
            #g.write(padding)

#with open('original/track2_mode2.bin', 'rb') as g:
#    mode2_data = g.read()
#    with open('patched/LA7.iso', 'rb+') as f:
#        f.seek(0x78c3f0)
#        f.write(mode2_data)
#        #padding = b'\x00' * (0x5722ad0 - len(mode2_data))
#        #f.write(padding)
