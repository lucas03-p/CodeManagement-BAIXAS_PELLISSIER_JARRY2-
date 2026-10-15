import serial
import time
# création et configuration port serie
serialPort = serial.Serial()
serialPort.baudrate = 1000000
serialPort.parity = serial.PARITY_NONE
serialPort.bytesize = serial.EIGHTBITS
serialPort.stopbits = serial.STOPBITS_ONE
serialPort.port = 'COM5'
# ouvrir port serie
serialPort.open()
# envoyer le code "r" : 114
cmd = 'r'
serialPort.write(cmd.encode(encoding = 'ascii'))# ici on encode en ascii la lettre r donc mis à 114
serialPort.flush()

times = []

startTime= time.time()
while(( time.time() - startTime) < 10):
    if serialPort.in_waiting > 0:
        value = serialPort.readline().decode().strip()

        if value:
            times.append(float(value))

cmd = 's'
serialPort.write(cmd.encode(encoding = 'ascii'))
serialPort.flush()

# fermer le port serie
serialPort.close()
