from modul.tokenizer import Tokenizer
from modul.circuit import Circuit
from modul.tokensystem import TokenSystem
from modul.subsystem import Subsystem
from modul.interconnect import Interconnect
import numpy as np

def main():
    """
    Main function to execute the quantum circuit operations.

    This function initializes a quantum circuit with 50 qubits and performs the following steps:
    1. Tokenizes a given word using the `Tokenizer` class.
    2. Initializes the main quantum circuit and assigns qubits to a token system.
    3. Creates and applies quantum operations on multiple subsystems.
    4. Entangles the token system with the subsystems using the `Interconnect` class.
    5. Outputs the final quantum circuit configuration.

    The circuit is then ready for simulation or execution on a quantum device.
    """
    total_qubits = 50    # 50 Qubits insgesamt im Circuit
    main_qubits = 20     # Anzahl der Qubits, die dem Token-System zugewiesen werden
    subsystem_qubits = 10  # Anzahl der Qubits, die jedem Subsystem zugewiesen werden
    subsystems_count = 3  # Anzahl der Subsysteme
    shots = 1024  # Anzahl der Schüsse (Simulationen) für die Messung (wird hier jedoch nicht verwendet)

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

    # Initialisiere das Token-System mit der Token-Matrix
    token_system = TokenSystem(main_circuit, num_qubits=main_qubits)
    token_system.tp_matrix = np.array(tokens).T[:3, :main_qubits]  # Setze die Token-Matrix als TP-Matrix
    token_system.apply_operations()  # Wende die Operationen des Token-Systems an

    # Erstelle die Subsysteme
    subsystems = []
    subsystems_ranges = []
    for i in range(subsystems_count):
        # Erzeuge eine Zufallsmatrix für die Phasenoperationen des Subsystems
        subsystem_matrix = np.random.rand(subsystem_qubits, 3) * 2 * np.pi
        print(f"Subsystem Matrix (Phasen) für Subsystem {i + 1}:\n{subsystem_matrix}")

        # Initialisiere das Subsystem mit einer neuen Qubit-Zuweisung
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
