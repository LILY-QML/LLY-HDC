class Measurement:
    """Handles the measurement of qubits in the main circuit."""

    def __init__(self, circuit):
        self.circuit = circuit.get_circuit()

    def measure_subsystem(self, qubit_range, label="Subsystem"):
        """Measure a specific range of qubits (for a subsystem or token system)."""
        classical_bits = range(len(qubit_range))  # Match classical bits to quantum bits
        self.circuit.measure(qubit_range, classical_bits)
        print(f"Measuring {label}: {qubit_range}")

    def measure_entanglement(self, qubits_token, qubits_subsystem, label="Entanglement"):
        """Measure the entanglement between the TokenSystem and a specific Subsystem."""
        combined_range = list(qubits_token) + list(qubits_subsystem)
        classical_bits = range(len(combined_range))  # Match classical bits to quantum bits
        self.circuit.measure(combined_range, classical_bits)
        print(f"Measuring {label}: Token Qubits {qubits_token} with Subsystem Qubits {qubits_subsystem}")
