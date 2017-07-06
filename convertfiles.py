# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import binascii
import struct

class ConvertWem():
    
    def main(self):
        # makes a list of all the files in the directory
        files = [f for f in listdir('.') if isfile(f)]
        # The bytes we want
        self.rightBytes=b'\x03\x00\x00\x00'
        # The files created may have this bytes wrong
        self.wrongBytes=b'\x02\x31\x00\x00'
        # Offset 40 bytes
        self.channelMaskOffset=40
        i=0
        for file in files:
            # Only select Wem Files
            if file.endswith('.wem'):
                i=i+1
                self.logic(file)
        print(i, "files converted")
        
    def logic(self, file):
        ''' this function open tem file
            Then compare the bytes at channelMaskOffset
            if its wrong, overwrite the bytes'''
        self.openFile(file)
        self.readChannelMask()
        if(self.channelMask==self.rightBytes):
            print("File (Y)", file, "is right")
        elif(self.channelMask==self.wrongBytes):
            print("File (N)", file, "is wrong, converting")
            self.writeBytes(self.rightBytes, self.channelMaskOffset)
        else:
            print("File", file, "not recognized, may be MONO our else")
            print("This program does not check blockAlign")
        self.closeFile()

    def openFile(self, file):
        # Function to open in byte mode
        self.fh = open(file, "r+b")

    def closeFile(self):
        # Function to close file
        self.fh.close()

    def writeBytes(self, rightBytes, seek):
        # Function to write bytes
        self.fh.seek(seek)
        self.fh.write(rightBytes)

    def readChannelMask(self):
        # Function to read the bytes that represent the channel mask
        self.fh.seek(self.channelMaskOffset)
        self.channelMask = self.fh.read(4)

if __name__ == "__main__":
        ConvertWem().main()
