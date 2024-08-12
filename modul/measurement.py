class Measurement:
    """
    Handles the measurement of qubits in the main circuit.

    This class is responsible for performing measurements on specific qubits
    within the quantum circuit. It supports measuring qubits associated with
    subsystems or token systems, as well as measuring the entanglement between
    the TokenSystem and various subsystems.

    Attributes:
    -----------
    circuit : QuantumCircuit
        The quantum circuit where the measurements are performed.
    """

    def __init__(self, circuit):
        """
        Initializes the Measurement class with a given quantum circuit.

        Parameters:
        -----------
        circuit : Circuit
            The Circuit object that contains the quantum circuit where the
            measurements will be performed.
        """
        self.circuit = circuit.get_circuit()

    def measure_subsystem(self, qubit_range, label="Subsystem"):
        """
        Measure a specific range of qubits (for a subsystem or token system).

        This method measures the qubits in the given range and maps the results
        to corresponding classical bits. It is typically used to measure the
        state of a subsystem or a token system within the quantum circuit.

        Parameters:
        -----------
        qubit_range : range
            The range of qubits to be measured.

        label : str, optional
            A label to identify the measurement in output (default is "Subsystem").

        Returns:
        --------
        None
        """
        classical_bits = range(len(qubit_range))  # Match classical bits to quantum bits
        self.circuit.measure(qubit_range, classical_bits)
        print(f"Measuring {label}: {qubit_range}")

    def measure_entanglement(self, qubits_token, qubits_subsystem, label="Entanglement"):
        """
        Measure the entanglement between the TokenSystem and a specific Subsystem.

        This method measures the entangled state between the qubits of the
        TokenSystem and a specified Subsystem. The measurement results are mapped
        to corresponding classical bits.

        Parameters:
        -----------
        qubits_token : list of int
            The list of qubits that belong to the TokenSystem.

        qubits_subsystem : list of int
            The list of qubits that belong to the Subsystem.

        label : str, optional
            A label to identify the measurement in output (default is "Entanglement").

        Returns:
        --------
        None
        """
        combined_range = list(qubits_token) + list(qubits_subsystem)
        classical_bits = range(len(combined_range))  # Match classical bits to quantum bits
        self.circuit.measure(combined_range, classical_bits)
        print(f"Measuring {label}: Token Qubits {qubits_token} with Subsystem Qubits {qubits_subsystem}")
