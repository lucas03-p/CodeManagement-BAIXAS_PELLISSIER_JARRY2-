import serial
import time
import csv
import os
import matplotlib.pyplot as plt

# Configuration
PORT = 'COM3'
BAUDRATE = 115200
DUREE = 10

serialPort = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

times = []
raw_values = []
erreurs = 0

try:
    time.sleep(2)
    serialPort.reset_input_buffer()

    # Démarrer l'acquisition
    serialPort.write(b'r')
    serialPort.flush()

    print("Acquisition démarrée...")

    startTime = time.time()

    while (time.time() - startTime) < DUREE:

        line = serialPort.readline().decode(
            'ascii', errors='replace'
        ).strip()

        if line:
            try:
                values = line.split(';')

                temps = float(values[0])
                valeurBrute = int(values[1])

                times.append(temps)
                raw_values.append(valeurBrute)

            except (ValueError, IndexError):
                erreurs += 1

    # Arrêter l'acquisition
    serialPort.write(b's')
    serialPort.flush()

finally:
    serialPort.close()

# Export CSV
dossier = os.path.dirname(os.path.abspath(__file__))
nom_fichier = os.path.join(dossier, "donnees_jauge.csv")

with open(nom_fichier, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Temps (s)", "Valeur brute"])
    writer.writerows(zip(times, raw_values))

# Résultats
print("\nAcquisition terminée.")
print("Nombre de mesures :", len(raw_values))
print("Lignes non reconnues :", erreurs)
print("Fichier enregistré :", nom_fichier)

if len(raw_values) > 0:
    plt.figure()
    plt.plot(times, raw_values, '.-')
    plt.xlabel("Temps (s)")
    plt.ylabel("Valeur brute HX711")
    plt.title("Signal de la jauge de contrainte")
    plt.grid(True)
    plt.show()
else:
    print("ATTENTION : aucune mesure reçue.")


