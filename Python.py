# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 10:20:58 2026

@author: lucas
"""

import serial

# configuration port serie

serialPort = serial.Serial()
serialPort.baudrate = 1000000
serialPort.parity = serial.PARITY_NONE
serialPort.bytesize = serial.EIGHTBITS
serialPort.stopbits = serial.STOPBITS_ONE
serialPort.port = "COM4"

# ouvrir port serie

serialPort.open()

# envoyerle code "r" : 114

serialPort.write(114)

# fermer le port serie

serialPort.close()
