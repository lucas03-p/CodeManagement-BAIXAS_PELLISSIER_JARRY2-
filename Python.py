
import serial
import time
import csv
import os
import matplotlib.pyplot as plt

# Configuration
PORT = 'COM3'
BAUDRATE = 115200

DUREE = 10
NOMBRE_ESSAIS = 10

# Connexion Arduino
serialPort = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# Dossier d'enregistrement
dossier = os.path.dirname(os.path.abspath(__file__))

try:
    # Attendre la connexion
    time.sleep(2)
    serialPort.reset_input_buffer()

    # Boucle des essais
    for essai in range(1, NOMBRE_ESSAIS + 1):

        print(f"\n===== ESSAI {essai}/{NOMBRE_ESSAIS} =====")

        times = []
        raw_values = []
        erreurs = 0

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

        # Arrêter l'acquisition et réinitialiser Arduino
        serialPort.write(b's')
        serialPort.flush()

        # Attendre le redémarrage de l'Arduino
        time.sleep(2)
        serialPort.reset_input_buffer()

        # Export CSV avec numéro d'essai
        nom_fichier = os.path.join(
            dossier,
            f"donnees_jauge_essai_{essai:02d}.csv"
        )

        with open(nom_fichier, "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")

            writer.writerow(["Temps (s)", "Valeur brute"])

            writer.writerows(zip(times, raw_values))

        # Résultats de l'essai
        print(f"Essai {essai} terminé.")
        print("Nombre de mesures :", len(raw_values))
        print("Lignes non reconnues :", erreurs)
        print("Fichier enregistré :", nom_fichier)

        # Graphique de l'essai
        if len(raw_values) > 0:

            plt.figure()
            plt.plot(times, raw_values, '.-')

            plt.xlabel("Temps (s)")
            plt.ylabel("Valeur brute HX711")

            plt.title(f"Signal de la jauge - Essai {essai}")

            plt.grid(True)

    print("\n===== TOUS LES ESSAIS SONT TERMINÉS =====")

    plt.show()

finally:
    serialPort.close()

