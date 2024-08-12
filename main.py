from modul.tokenizer import Tokenizer
from modul.circuit import Circuit
from modul.tokensystem import TokenSystem
from modul.subsystem import Subsystem
from modul.interconnect import Interconnect
import numpy as np

def main():
    total_qubits = 50    # 20 Qubits für das Token-System und 30 Qubits für drei Subsysteme (jeweils 10 Qubits)
    main_qubits = 20     # Die Anzahl der Qubits, die dem Token-System zugewiesen werden
    subsystem_qubits = 10  # Die Anzahl der Qubits, die jedem Subsystem zugewiesen werden
    subsystems_count = 3  # Anzahl der Subsysteme
    shots = 1024

    # Wort zur Tokenisierung
    word = "HELLOQUANTUM"

    # Initialisiere den Tokenizer und tokenisiere das Wort
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(word)

    # Gebe das Wort und die resultierende Token-Matrix aus
    print(f"Original word: {word}")
    print(f"Tokenized Matrix:\n{np.array(tokens)}")

    # Initialisiere den Hauptcircuit
    main_circuit = Circuit(total_qubits)

    # Erstelle und initialisiere das Token-System mit der Token-Matrix
    token_system = TokenSystem(main_circuit, num_qubits=main_qubits)
    token_system.tp_matrix = np.array(tokens).T[:3, :main_qubits]  # Setze die Token-Matrix als IP-Matrix
    token_system.apply_operations()  # Wende die Operationen des Token-Systems an

    # Erstelle die Subsysteme
    subsystems = []
    subsystems_ranges = []
    for _ in range(subsystems_count):
        subsystem_matrix = np.random.rand(subsystem_qubits, 3) * 2 * np.pi
        print(f"Subsystem Matrix (Phasen) für Subsystem {_ + 1}:\n{subsystem_matrix}")

        subsystem = Subsystem(main_circuit, num_qubits=subsystem_qubits)
        subsystem.tp_matrix = subsystem_matrix
        subsystem.apply_operations()  # Wende die Operationen des Subsystems an
        subsystems.append(subsystem)
        subsystems_ranges.append(subsystem.qubit_range)

    # Erstelle und initialisiere die Interconnect-Klasse
    interconnect = Interconnect(main_circuit)
    interconnect.entangle(token_system.qubit_range, subsystems_ranges)  # Verschränke Token-System und Subsysteme

    # Ausgabe des resultierenden Circuits
    print(main_circuit.get_circuit())

if __name__ == "__main__":
    main()
