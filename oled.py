import gpio as GPIO
import time
import numpy as np
import font as FONT
OLED_SDA = 431
OLED_SCK = 432

GPIO.setup(OLED_SDA, GPIO.OUT)
GPIO.setup(OLED_SCK, GPIO.OUT)

OLED_GRAM = np.zeros((144,8),int)
OLED_CMD  = 0	#写命令
OLED_DATA = 1	#写数据

def I2C_Start():
    GPIO.output(OLED_SDA, GPIO.HIGH)
    GPIO.output(OLED_SCK, GPIO.HIGH)

    GPIO.output(OLED_SDA, GPIO.LOW)

    GPIO.output(OLED_SCK, GPIO.LOW)
  

def I2C_Stop():
    GPIO.output(OLED_SDA, GPIO.LOW)
    GPIO.output(OLED_SCK, GPIO.HIGH)

    GPIO.output(OLED_SDA, GPIO.HIGH)

def I2C_WaitAck():
    GPIO.output(OLED_SDA, GPIO.HIGH)

    GPIO.output(OLED_SCK, GPIO.HIGH)
    
    GPIO.output(OLED_SCK, GPIO.LOW)
    

def Send_Byte(dat):
    for i in range(0,8):
        if dat&0x80:
            GPIO.output(OLED_SDA, GPIO.HIGH)
        else :
            GPIO.output(OLED_SDA, GPIO.LOW)
        
        GPIO.output(OLED_SCK, GPIO.HIGH)
       
        GPIO.output(OLED_SCK, GPIO.LOW)
        dat <<=1

def WR_Byte(dat,mode):
    I2C_Start()
    Send_Byte(0x78)
    I2C_WaitAck()
    if mode :
        Send_Byte(0x40)
    else :
        Send_Byte(0x00)
    I2C_WaitAck()
    Send_Byte(dat)
    I2C_WaitAck()
    I2C_Stop()

def Refresh():
    for i in range(0,8):
        WR_Byte(0xb0+i,OLED_CMD)
        WR_Byte(0x00,OLED_CMD)
        WR_Byte(0x10,OLED_CMD)
        I2C_Start()
        Send_Byte(0x78)
        I2C_WaitAck()
        Send_Byte(0x40)
        I2C_WaitAck()
        for n in range(0,128):
            Send_Byte(OLED_GRAM[n][i])
            I2C_WaitAck()
        I2C_Stop()
        

def Clear():
    for i in range(0,8):
        for n in range(0,128):
            OLED_GRAM[n][i] = 0
    Refresh()

def DrawPoint(x,y,t):
    i = int(y/8)    
    m = int(y%8)    
    n = 1 << m
    if t == 1:
        OLED_GRAM[x][i] =  OLED_GRAM[x][i] |n
    else :
        OLED_GRAM[x][i]=~OLED_GRAM[x][i]
        OLED_GRAM[x][i]|=n
        OLED_GRAM[x][i]=~OLED_GRAM[x][i]

def ShowChar(x,y,chr,size1,mode):
    if size1%8:
        size3 = 1
    else :
        size3 = 0
    x0=x
    y0=y
    size2= int((size1/8+ size3)*(size1/2))
    chr1 = ord(chr) - ord(' ')
    #print("chr = %d" %ord(chr))
    #print(" = %d" %ord(' '))
    for i in range(0,size2):
        temp = FONT.asc2_1608[chr1][i]
        for m in range(0,8):
            if temp&0x01:
                DrawPoint(x,y,int(bool(mode)) )
            else :
                DrawPoint(x,y,int(bool(1-mode)))
            temp = temp >> 1
            y = y+1
        x = x+1
        if (size1!=8) and ((x-x0) == size1/2):
            x=x0
            y0=y0+8
        y=y0
def ShowString(x,y,chr,size1,mode):
    str_len = len(chr)
    for i in range(0,str_len):
        if ord(chr[i]) >= ord(' ') and ord(chr[i]) <= ord('~'):
            ShowChar(x,y,chr[i],size1,mode)
            if size1==8:
                x = x+6
            else :
                x = x + int(size1/2)





def Init():

    time.sleep(0.2)
    WR_Byte(0xAE,OLED_CMD)
    WR_Byte(0x00,OLED_CMD)
    WR_Byte(0x10,OLED_CMD)
    WR_Byte(0x40,OLED_CMD)
    WR_Byte(0x81,OLED_CMD)
    WR_Byte(0xCF,OLED_CMD)
    WR_Byte(0xA1,OLED_CMD)
    WR_Byte(0xC8,OLED_CMD)
    WR_Byte(0xA6,OLED_CMD)
    WR_Byte(0xA8,OLED_CMD)
    WR_Byte(0x3f,OLED_CMD)
    WR_Byte(0xD3,OLED_CMD)
    WR_Byte(0x00,OLED_CMD)
    WR_Byte(0xd5,OLED_CMD)
    WR_Byte(0x80,OLED_CMD)
    WR_Byte(0xD9,OLED_CMD)
    WR_Byte(0xF1,OLED_CMD)
    WR_Byte(0xDA,OLED_CMD)
    WR_Byte(0x12,OLED_CMD)
    WR_Byte(0xDB,OLED_CMD)
    WR_Byte(0x30,OLED_CMD)
    WR_Byte(0x20,OLED_CMD)
    WR_Byte(0x02,OLED_CMD)
    WR_Byte(0x8D,OLED_CMD)
    WR_Byte(0x14,OLED_CMD)
    Clear()
    WR_Byte(0xAF,OLED_CMD)
