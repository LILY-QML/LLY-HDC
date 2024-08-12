import numpy as np

class TokenSystem:
    """
    Represents a token system that applies operations on the main circuit.

    This class is responsible for managing a specific set of qubits within the
    main quantum circuit and applying a sequence of quantum operations to them.
    The TokenSystem is initialized with a given number of qubits and applies a
    predefined sequence of operations using two randomly generated phase matrices.

    Attributes:
    -----------
    num_qubits : int
        The number of qubits allocated to this token system.
    qubit_range : range
        The range of qubit indices allocated to this token system.
    circuit : QuantumCircuit
        The quantum circuit where the operations are applied.
    tp_matrix : numpy.ndarray
        A matrix of randomly generated phase values (in radians) for the token operations.
        The matrix has 3 rows (one for each phase operation) and `num_qubits` columns.
    ip_matrix : numpy.ndarray
        A matrix of randomly generated phase values (in radians) for the additional operations.
        The matrix has 3 rows (one for each phase operation) and `num_qubits` columns.
    """

    def __init__(self, circuit, num_qubits=20):
        """
        Initializes the TokenSystem with a given circuit and number of qubits.

        Parameters:
        -----------
        circuit : Circuit
            The Circuit object that manages the quantum circuit and qubit allocation.
        num_qubits : int, optional
            The number of qubits to allocate to this token system (default is 20).
        """
        self.num_qubits = num_qubits
        self.qubit_range = circuit.allocate_qubits(num_qubits)
        self.circuit = circuit.get_circuit()
        self.tp_matrix = np.random.rand(3, num_qubits) * 2 * np.pi
        self.ip_matrix = np.random.rand(3, num_qubits) * 2 * np.pi

    def apply_operations(self):
        """
        Apply token operations to the allocated qubits.

        This method applies a sequence of operations to each qubit in the token system.
        The sequence consists of phase (P) gates applied using values from the `tp_matrix`
        and `ip_matrix`. Between the phase gates, Hadamard (H) gates are applied.

        The operations are as follows:
        - Phase gate from `tp_matrix`.
        - Phase gate from `ip_matrix`.
        - Hadamard gate (except after the last phase gate).

        The sequence is repeated three times for each qubit, with the Hadamard gate applied
        after the first two iterations.

        Returns:
        --------
        None
        """
        for qubit in self.qubit_range:
            for i in range(3):
                self.circuit.p(self.tp_matrix[i, qubit], qubit)
                self.circuit.p(self.ip_matrix[i, qubit], qubit)
                if i < 2:
                    self.circuit.h(qubit)
