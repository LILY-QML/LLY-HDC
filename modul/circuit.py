from qiskit import QuantumCircuit

class Circuit:
    """Represents the global main quantum circuit."""

    def __init__(self, total_qubits):
        self.total_qubits = total_qubits
        self.circuit = QuantumCircuit(total_qubits)
        self.token_start_index = 0
        self.subsystem_start_index = 20
        self.qubits_allocated = 0

    def allocate_qubits(self, num_qubits):
        """Allocate qubits for a subsystem or token system."""
        if self.qubits_allocated + num_qubits > self.total_qubits:
            raise ValueError("Not enough qubits available to allocate.")
        
        allocated_start_index = self.qubits_allocated
        self.qubits_allocated += num_qubits
        return range(allocated_start_index, allocated_start_index + num_qubits)

    def get_circuit(self):
        return self.circuit
