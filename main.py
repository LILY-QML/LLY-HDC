from modul.tokenizer import Tokenizer
from modul.circuit import Circuit, TokenLayer
import numpy as np

def main():
    qubits = 5
    layers = 4
    shots = 1024

    # Wort zur Tokenisierung
    word = "HELLOQUANTUM"

    # Initialisiere den Tokenizer
    tokenizer = Tokenizer()

    # Tokenisiere das Wort
    tokens = tokenizer.tokenize(word)

    # Konvertiere die Tokens in eine numpy-Array-Matrix für die IP-Phasen
    ip_matrix = np.array(tokens).T[:3, :qubits]  # Nehme die ersten 3 Komponenten und nur so viele Qubits wie benötigt

    # Erstelle eine zufällige Trainingsphase-Matrix
    tp_matrix = np.random.rand(3, qubits) * 2 * np.pi

    # Erstelle TokenLayer
    token_layer = TokenLayer(qubits, tp_matrix, ip_matrix)

    # Baue den Schaltkreis auf
    circuit = Circuit(qubits, [token_layer] * layers, shots)

    # Führe den Schaltkreis aus und zeige das Ergebnis
    circuit.run()
    print(circuit)
    print("Counts:", circuit.get_counts())

if __name__ == "__main__":
    main()
