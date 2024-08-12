class Interconnect:
    """
    Handles the entanglement between different systems on the main circuit.

    This class manages the process of entangling a TokenSystem with multiple
    subsystems on a quantum circuit. The entanglement is done in two stages:
    the first 10 qubits of the TokenSystem are entangled with the qubits of
    each Subsystem, and the next 10 qubits repeat the process.
    
    Attributes:
    -----------
    circuit : QuantumCircuit
        The quantum circuit where the entanglement is performed.
    """

    def __init__(self, circuit):
        """
        Initializes the Interconnect with a given quantum circuit.

        Parameters:
        -----------
        circuit : Circuit
            The Circuit object that contains the quantum circuit where the
            entanglement will take place.
        """
        self.circuit = circuit.get_circuit()

    def entangle(self, qubits_token, qubits_subsystems):
        """
        Entangle the TokenSystem with each Subsystem.

        This method entangles the TokenSystem with multiple Subsystems by
        applying controlled-NOT (CX) gates. The first 10 qubits of the TokenSystem
        are entangled with the qubits in each Subsystem. Then, the next 10 qubits
        of the TokenSystem are again entangled with the same qubits in the Subsystem.

        Parameters:
        -----------
        qubits_token : list of int
            The list of qubits that belong to the TokenSystem.
        
        qubits_subsystems : list of range
            A list of ranges, where each range represents the qubits allocated
            to a Subsystem.

        Returns:
        --------
        None
        """
        for subsystem_range in qubits_subsystems:
            for i in range(10):
                # Entangle the first half of the TokenSystem with the Subsystem
                self.circuit.cx(qubits_token[i], subsystem_range[i])

                # Entangle the second half of the TokenSystem with the same Subsystem
                self.circuit.cx(qubits_token[10 + i], subsystem_range[i])
