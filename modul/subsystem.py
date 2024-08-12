import numpy as np

class Subsystem:
    """Represents a subsystem that applies operations on the main circuit."""

    def __init__(self, circuit, num_qubits=10):
        self.num_qubits = num_qubits
        self.qubit_range = list(circuit.allocate_qubits(num_qubits))  # Zuordnung der Qubits für dieses Subsystem
        self.circuit = circuit.get_circuit()
        self.tp_matrix = np.random.rand(num_qubits, 3) * 2 * np.pi  # 3 Spalten für die Phasen, 10 Zeilen für die Qubits

    def apply_operations(self):
        """Apply subsystem operations to the allocated qubits."""
        for i, qubit in enumerate(self.qubit_range):  # Korrekte Zuordnung der Qubits
            # Apply Phase-Hadamard-Phase-Hadamard-Phase sequence
            self.circuit.p(self.tp_matrix[i, 0], qubit)  # Erste Phase
            self.circuit.h(qubit)                        # Erste Hadamard
            self.circuit.p(self.tp_matrix[i, 1], qubit)  # Zweite Phase
            self.circuit.h(qubit)                        # Zweite Hadamard
            self.circuit.p(self.tp_matrix[i, 2], qubit)  # Dritte Phase
