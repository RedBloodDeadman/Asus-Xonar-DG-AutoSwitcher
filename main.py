#!/usr/bin/env python3
import re
import os
import time


class ChangeAudioInput():
    ALL_FRONT_DISCONNECTED = '0'
    HEADPHONES_FRONT_CONNECTED = '1'
    HEADPHONES_MULTICHANNEL = '2'
    MIC_FRONT_DISCONNECTED = '3'
    MIC_FRONT_CONNECTED = '4'
    ALL_FRONT_CONNECTED = '5'

    pathToDGXCard = '/proc/asound/DG'
    channelNumber = None
    currentHeadphonesStatus = None

    def start(self):
        self.loop()

    def loop(self):
        # We wait symlink
        while not os.path.islink(self.pathToDGXCard):
            time.sleep(2)

        time.sleep(7)

        self.getChannelNumber()

        while True:
            status = self.getStatus()

            if self.currentHeadphonesStatus is None:
                self.changeHeadphones(status)

            if self.currentHeadphonesStatus != status:
                self.changeHeadphones(status)

            time.sleep(1)

    def getChannelNumber(self):
        self.channelNumber = re.findall("card(\d+)", os.popen(f"ls -ld {self.pathToDGXCard}").read())[0]

    def getStatus(self):
        splitted = self.getStatusCode()

        if splitted in ['68', 'e8']:
            # print('HEADPHONES_FRONT_CONNECTED')
            return self.HEADPHONES_FRONT_CONNECTED

        if splitted in ['78', 'f8']:
            # print('ALL_FRONT_DISCONNECTED')
            return self.ALL_FRONT_DISCONNECTED

        if splitted in ['f0', '70']:
            # print('MIC_FRONT_CONNECTED')
            return self.MIC_FRONT_CONNECTED

        if splitted in ['e0', '60']:
            # print('ALL_FRONT_CONNECTED')
            return self.ALL_FRONT_CONNECTED

        return self.HEADPHONES_MULTICHANNEL

    def changeHeadphones(self, status):
        if status == self.ALL_FRONT_CONNECTED:
            status = self.HEADPHONES_FRONT_CONNECTED
        if status == self.MIC_FRONT_CONNECTED:
            status = self.ALL_FRONT_DISCONNECTED
        os.popen(f"amixer -c {self.channelNumber} cset name='Analog Output Playback Enum' {status}")

        self.currentHeadphonesStatus = status

    def getStatusCode(self):
        cardBytes = os.popen(f'cat /proc/asound/card{self.channelNumber}/oxygen').read()
        search = re.findall("a0: (.*)", cardBytes)
        splitted = search[0].split()[6]

        return splitted

if __name__ == '__main__':
    try:
        ChangeAudioInput().start()
    except KeyboardInterrupt:
        print('Exited by user')
