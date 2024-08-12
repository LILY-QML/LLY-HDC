import numpy as np

class TokenSystem:
    """Represents a token system that applies operations on the main circuit."""

    def __init__(self, circuit, num_qubits=20):
        self.num_qubits = num_qubits
        self.qubit_range = list(circuit.allocate_qubits(num_qubits))  # Zuordnung der Qubits für das Token-System
        self.circuit = circuit.get_circuit()
        self.tp_matrix = np.random.rand(3, num_qubits) * 2 * np.pi  # 3 Phasen für die Token-Matrix

    def apply_operations(self):
        """Apply token operations to the allocated qubits."""
        for i, qubit in enumerate(self.qubit_range[:19]):  # Für die ersten 19 Qubits
            for j in range(3):
                self.circuit.p(self.tp_matrix[j, i], qubit)  # Drei Phasengatter
                if j < 2:
                    self.circuit.h(qubit)  # Hadamard-Gatter zwischen den Phasengattern

        # Für das 20. Qubit nur drei Phasengatter, ohne Hadamard-Gatter
        qubit = self.qubit_range[19]
        for j in range(3):
            self.circuit.p(self.tp_matrix[j, 19], qubit)
