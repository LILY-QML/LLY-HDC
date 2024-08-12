from qiskit import QuantumCircuit

class Circuit:
    """
    Represents the global main quantum circuit.

    This class manages the allocation of qubits and the construction of
    a quantum circuit using Qiskit. It allows subsystems and token systems
    to request a specific number of qubits from the total available qubits.

    Attributes:
    -----------
    total_qubits : int
        The total number of qubits available in the circuit.
    circuit : QuantumCircuit
        The QuantumCircuit object that represents the quantum circuit.
    qubits_allocated : int
        The number of qubits that have been allocated so far.
    """

    def __init__(self, total_qubits=50):
        """
        Initializes the Circuit with a specified number of qubits.

        Parameters:
        -----------
        total_qubits : int, optional
            The total number of qubits available in the circuit (default is 50).
        """
        self.total_qubits = total_qubits
        self.circuit = QuantumCircuit(total_qubits)
        self.qubits_allocated = 0

    def allocate_qubits(self, num_qubits):
        """
        Allocate qubits for a subsystem or token system.

        This method allocates a specific number of qubits from the total available
        qubits for use by a subsystem or token system. If there are not enough
        qubits available, it raises a ValueError.

        Parameters:
        -----------
        num_qubits : int
            The number of qubits to allocate.

        Returns:
        --------
        range
            A range object representing the indices of the allocated qubits.

        Raises:
        -------
        ValueError
            If there are not enough qubits available to allocate the requested number.
        """
        if self.qubits_allocated + num_qubits > self.total_qubits:
            raise ValueError("Not enough qubits available to allocate.")
        
        allocated_start_index = self.qubits_allocated
        self.qubits_allocated += num_qubits
        return range(allocated_start_index, allocated_start_index + num_qubits)

    def get_circuit(self):
        """
        Get the QuantumCircuit object.

        This method returns the underlying QuantumCircuit object that
        represents the quantum circuit.

        Returns:
        --------
        QuantumCircuit
            The QuantumCircuit object.
        """
        return self.circuit
