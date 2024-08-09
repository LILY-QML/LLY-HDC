from qiskit import QuantumCircuit, transpile
import numpy as np
from qiskit_aer import Aer


class TokenLayer:
    """Class to apply a layer of operations on a range of qubits based on a phase matrix."""

    def __init__(self, qubits, tp_matrix, ip_matrix):
        """
        Initialize the TokenLayer with training and input phase matrices.
        :param qubits: The number of qubits.
        :param tp_matrix: The training phase matrix (numpy array of shape (3, qubits)).
        :param ip_matrix: The input phase matrix (numpy array of shape (3, qubits)).
        """
        self.qubits = qubits
        self.tp_matrix = tp_matrix  # 3xQubits matrix for training phases
        self.ip_matrix = ip_matrix  # 3xQubits matrix for input phases

    def apply(self, circuit):
        """
        Apply the operations based on the phase matrices to the quantum circuit.
        :param circuit: The QuantumCircuit object to which the operations are applied.
        """
        for qubit in range(self.qubits):
            for i in range(3):
                # Apply the training phase (TP)
                circuit.p(self.tp_matrix[i, qubit], qubit)
                # Apply the input phase (IP)
                circuit.p(self.ip_matrix[i, qubit], qubit)

                # Apply Hadamard gate between the first and second TP-IP pair, and after the third pair
                if i < 2:
                    circuit.h(qubit)
    
    def __repr__(self):
        return f"TokenLayer(tp_matrix={self.tp_matrix}, ip_matrix={self.ip_matrix}, qubits={self.qubits})"

class Circuit:
    """Represents a quantum circuit composed of multiple layers."""

    def __init__(self, qubits, layers, shots):
        self.qubits = qubits
        self.layers = layers  # List of Layer objects
        self.shots = shots
        self.circuit = QuantumCircuit(qubits, qubits)
        self.simulation_result = None

        self.build_circuit()
        self.measure()

    def build_circuit(self):
        """Build the quantum circuit by applying each layer in sequence."""
        for layer in self.layers:
            layer.apply(self.circuit)

    def measure(self):
        """Add measurement operations to all qubits."""
        self.circuit.measure(range(self.qubits), range(self.qubits))

    def run(self, simulator=None):
        """Run the quantum circuit simulation and return the result."""
        if simulator is None:
            simulator = Aer.get_backend(
                "aer_simulator"
            )  # Standardmäßig den Aer Simulator verwenden
        compiled_circuit = transpile(
            self.circuit, simulator
        )  # Ensure transpile is used here
        self.simulation_result = simulator.run(
            compiled_circuit, shots=self.shots
        ).result()
        return self.simulation_result

    def get_counts(self):
        """Return the counts from the last simulation run."""
        if self.simulation_result is not None:
            return self.simulation_result.get_counts(self.circuit)
        else:
            raise RuntimeError("The circuit has not been run yet.")

    def __repr__(self):
        return self.circuit.draw(output="text").__str__()
