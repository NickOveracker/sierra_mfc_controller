import binascii

def calcLRC(cmnd):
    # cmnd is a byte array containing the command ASCII string; example: cmnd="setr2.00"
    # an unsigned 16 bit integer is returned to the calling program
    # only the lower 16 bits contain the lrc

    lrc = 0 # initialize lrc to zero
    
    for character in cmnd: # this for loop starts with ASCII 's' and loops through to the last ASCII '0'
        hex_char = (int(ord(character)))
        lrc=lrc+hex_char # Add the ASCII value to the lrc
        # end of i loop

    # Get 2's complement of lrc
    lrc = -lrc

    # Convert to two byte ascii
    high_byte = "%X" % ((lrc&0xF0) >> 4)
    low_byte  = "%X" % (lrc&0x0F)

    return(hight_byte + "" + low_byte)
