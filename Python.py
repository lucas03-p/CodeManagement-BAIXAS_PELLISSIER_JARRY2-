import serial
import time
import numpy as np
import matplotlib.pyplot as plt

PORT = 'COM3'


def acquisition(duree):
    """Lance l'Arduino, lit pendant 'duree' secondes, renvoie 3 listes."""
    sp = serial.Serial()
    sp.baudrate = 115200
    sp.parity = serial.PARITY_NONE
    sp.bytesize = serial.EIGHTBITS
    sp.stopbits = serial.STOPBITS_ONE
    sp.port = PORT
    sp.timeout = 1
    sp.open()

    time.sleep(2)
    sp.reset_input_buffer()

    sp.write('r'.encode(encoding='ascii'))  # 'r' = 114
    sp.flush()

    temps, brutes, masses = [], [], []
    t0 = time.time()
    while (time.time() - t0) < duree:
        if sp.in_waiting > 0:
            ligne = sp.readline().decode('ascii', errors='ignore').strip()
            try:
                v = ligne.split(';')
                temps.append(int(v[0]) / 1000.0)      # ms -> s
                brutes.append(int(v[1]))
                masses.append(int(v[2]) / 1000.0)     # mg -> g
            except (ValueError, IndexError):
                pass

    sp.write('s'.encode(encoding='ascii'))  # 's' = 115
    sp.flush()
    sp.close()
    time.sleep(2)  # laisser la carte redémarrer
    return temps, brutes, masses


# ===================== PHASE 1 : CALIBRATION =====================
# (Arduino avec OFFSET = 0.0 et SCALE = 1.0)
CALIBRATION = True

if CALIBRATION:
    masses_connues = [0, 5, 10, 20, 50]   # en grammes : adapte à tes petites masses
    moyennes_brutes = []

    for m in masses_connues:
        input(f"Pose la masse de {m} g, puis appuie sur Entrée...")
        _, brutes, _ = acquisition(3)
        moy = np.mean(brutes)
        moyennes_brutes.append(moy)
        print(f"{m} g -> valeur brute moyenne : {moy:.1f} ({len(brutes)} mesures)")

    # Droite : brute = SCALE * masse + OFFSET
    SCALE, OFFSET = np.polyfit(masses_connues, moyennes_brutes, 1)
    print("\n=== À recopier dans l'Arduino ===")
    print(f"const float OFFSET = {OFFSET:.1f};")
    print(f"const float SCALE = {SCALE:.2f};")

    plt.plot(masses_connues, moyennes_brutes, 'o')
    plt.plot(masses_connues, SCALE * np.array(masses_connues) + OFFSET)
    plt.xlabel("Masse (g)")
    plt.ylabel("Valeur brute")
    plt.title("Calibration")
    plt.show()

# ===================== PHASE 2 : MESURE =====================
# (après avoir mis OFFSET et SCALE dans l'Arduino et téléversé)
else:
    temps, brutes, masses = acquisition(10)
    print("Nombre de mesures :", len(masses))
    print("Premières masses (g) :", masses[:10])

    plt.plot(temps, masses)
    plt.xlabel("Temps (s)")
    plt.ylabel("Masse (g)")
    plt.show()
    




