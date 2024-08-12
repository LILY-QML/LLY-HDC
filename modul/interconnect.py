class Interconnect:
    """Handles the entanglement between different systems on the main circuit."""

    def __init__(self, circuit):
        self.circuit = circuit.get_circuit()

    def entangle(self, qubits_token, qubits_subsystems):
        """Entangle the TokenSystem with each Subsystem.
           The first 10 Qubits of the TokenSystem will be entangled with each qubit in the Subsystem.
           The next 10 Qubits will start over again with the Subsystem.
        """
        for subsystem_range in qubits_subsystems:
            for i in range(10):
                # Erste Hälfte des Token-Systems mit Subsystem verschränken
                self.circuit.cx(qubits_token[i], subsystem_range[i])

                # Zweite Hälfte des Token-Systems erneut mit dem Subsystem verschränken
                self.circuit.cx(qubits_token[10 + i], subsystem_range[i])
