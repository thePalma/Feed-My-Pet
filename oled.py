# Custom driver

import i2c

DISPLAY_ADDR = 0x3C
COMMAND_REGISTER = 0x80
DATA_REGISTER = 0x40
DISPLAY_ON = 0xAF
NORMAL_MODE = 0xA6
PAGE_ADDRESSING_MODE = 0x02

def begin():
    turnON()
    NormalDisplayMode()
    setPageMode()
    writeCommand(0x8d)
    writeCommand(0x14)
    clearFullDisplay()

def writeCommand(command):
    slave = i2c.I2c(DISPLAY_ADDR)
    write_buf = bytearray([COMMAND_REGISTER, command])
    slave.write(write_buf)

def writeData(data):
    slave = i2c.I2c(DISPLAY_ADDR)
    write_buf = bytearray([DATA_REGISTER, data])
    slave.write(write_buf)

def turnON():
    writeCommand(DISPLAY_ON)

def NormalDisplayMode():
    writeCommand(NORMAL_MODE)

def setPageMode():
    writeCommand(0x20)
    writeCommand(PAGE_ADDRESSING_MODE)

def clearFullDisplay():
    for page in range(8):
        setCursor(0, page)
        for column in range(128):
            writeData(0x00)
    setCursor(0, 0)

def writeChar(char):
    import fonts
    curr=fonts.vet[char]
    for i in curr:
        writeData(i)

def setCursor(X, Y):
    writeCommand(0x00 + (X & 0x0F))
    writeCommand(0x10 + ((X >> 4) & 0x0F))
    writeCommand(0xB0 + Y)

# This function has 4 parameters: the string that has to be printer on the display,
# the X and Y position where the printing starts
# and the last one that clears the display if True (set to True by default)
def print(string,begin_X=0,begin_Y=0,clear=True):
    if(clear):
        clearFullDisplay()
    setCursor(begin_X, begin_Y)                  
    curr=1
    max=21
    c=0
    for char in string:
        if(c==20):
            setCursor(begin_X, begin_Y+curr)
            curr += 1
            c=0
        if(char=='\n'):
            setCursor(begin_X, begin_Y+curr)
            curr+=1
        else:
            writeChar(char)
            c+=1