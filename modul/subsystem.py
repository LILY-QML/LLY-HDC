import numpy as np

class Subsystem:
    """
    Represents a subsystem that applies operations on the main circuit.

    This class is responsible for managing a specific set of qubits within the
    main quantum circuit and applying a sequence of quantum operations to them.
    Each subsystem has a specific number of qubits allocated to it, and these
    qubits undergo a predefined sequence of operations.

    Attributes:
    -----------
    num_qubits : int
        The number of qubits allocated to this subsystem.
    qubit_range : list of int
        The list of qubit indices allocated to this subsystem.
    circuit : QuantumCircuit
        The quantum circuit where the operations are applied.
    tp_matrix : numpy.ndarray
        A matrix of randomly generated phase values (in radians) for the operations.
        Each row corresponds to a qubit, and each column corresponds to a phase
        in the sequence of operations.
    """

    def __init__(self, circuit, num_qubits=10):
        """
        Initializes the Subsystem with a given circuit and number of qubits.

        Parameters:
        -----------
        circuit : Circuit
            The Circuit object that manages the quantum circuit and qubit allocation.

        num_qubits : int, optional
            The number of qubits to allocate to this subsystem (default is 10).
        """
        self.num_qubits = num_qubits
        self.qubit_range = list(circuit.allocate_qubits(num_qubits))  # Allocate qubits for this subsystem
        self.circuit = circuit.get_circuit()
        self.tp_matrix = np.random.rand(num_qubits, 3) * 2 * np.pi  # 3 columns for phases, num_qubits rows for qubits

    def apply_operations(self):
        """
        Apply subsystem operations to the allocated qubits.

        This method applies a sequence of operations to each qubit in the subsystem.
        The sequence consists of a Phase-Hadamard-Phase-Hadamard-Phase pattern, where
        each phase is determined by the corresponding value in the `tp_matrix`.

        Operations:
        -----------
        - Phase (P) gate with a specific angle from `tp_matrix`.
        - Hadamard (H) gate.

        The sequence is repeated twice for each qubit, followed by a final phase.

        Returns:
        --------
        None
        """
        for i, qubit in enumerate(self.qubit_range):  # Correct mapping of qubits
            # Apply Phase-Hadamard-Phase-Hadamard-Phase sequence
            self.circuit.p(self.tp_matrix[i, 0], qubit)  # First Phase
            self.circuit.h(qubit)                        # First Hadamard
            self.circuit.p(self.tp_matrix[i, 1], qubit)  # Second Phase
            self.circuit.h(qubit)                        # Second Hadamard
            self.circuit.p(self.tp_matrix[i, 2], qubit)  # Third Phase
