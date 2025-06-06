"""
Quantum Apple Model - Kernkomponente des QML-Systems

Dieses Modul implementiert das Hauptmodell für die Quantum Machine Learning
Vorhersage von Apfel-Eigenschaften. Das Modell verwendet 9 Qubits in drei
Subsystemen zur Kodierung von Frische, Haltbarkeit und Geschmack.

Architektur:
- 3 Qubits für Frische (Input): Q0-Q2
- 3 Qubits für Haltbarkeit (Output 1): Q3-Q5  
- 3 Qubits für Geschmack (Output 2): Q6-Q8

Das Modell nutzt parametrisierte Quantengatter für trainierbare Kopplungen
zwischen den Subsystemen.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
import logging
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantumAppleModel:
    """
    Quantum Machine Learning Modell für Apfel-Eigenschaftsvorhersage.
    
    Das Modell verwendet ein parametrisiertes Quantenschaltkreis (PQC) zur
    Vorhersage von Haltbarkeit und Geschmack basierend auf der Frische eines Apfels.
    
    Attributes:
        n_qubits_per_property (int): Anzahl Qubits pro Eigenschaft (Standard: 3)
        n_total_qubits (int): Gesamtanzahl Qubits (9)
        freshness_qubits (List[int]): Qubit-Indizes für Frische-Subsystem
        durability_qubits (List[int]): Qubit-Indizes für Haltbarkeits-Subsystem  
        taste_qubits (List[int]): Qubit-Indizes für Geschmacks-Subsystem
        param_values (Dict): Aktuelle Werte der trainierbaren Parameter
        simulator (AerSimulator): Quantum-Simulator für Ausführung
    """
    
    def __init__(self, n_qubits_per_property: int = 3, seed: Optional[int] = None):
        """
        Initialisiert das Quantum Apple Model.
        
        Args:
            n_qubits_per_property: Anzahl Qubits pro Eigenschaft (Standard: 3)
            seed: Zufallsseed für reproduzierbare Parameter-Initialisierung
        """
        logger.info(f"Initialisiere QuantumAppleModel mit {n_qubits_per_property} Qubits pro Eigenschaft")
        
        # Grundkonfiguration
        self.n_qubits_per_property = n_qubits_per_property
        self.n_total_qubits = 3 * n_qubits_per_property
        
        # Qubit-Zuordnung zu Subsystemen
        self._setup_qubit_mapping()
        
        # Trainierbare Parameter definieren
        self._setup_parameters()
        
        # Parameter-Werte initialisieren
        self._initialize_parameters(seed)
        
        # Quantum-Simulator konfigurieren
        self.simulator = AerSimulator()
        
        logger.info(f"Modell erfolgreich initialisiert: {self.n_total_qubits} Qubits, "
                   f"{len(self.param_values)} Parameter")
    
    def _setup_qubit_mapping(self) -> None:
        """
        Definiert die Zuordnung der Qubits zu den drei Subsystemen.
        
        Mapping:
        - Frische: Q0-Q2 (Input-Subsystem)
        - Haltbarkeit: Q3-Q5 (Erstes Output-Subsystem)
        - Geschmack: Q6-Q8 (Zweites Output-Subsystem)
        """
        self.freshness_qubits = list(range(0, self.n_qubits_per_property))
        self.durability_qubits = list(range(
            self.n_qubits_per_property, 
            2 * self.n_qubits_per_property
        ))
        self.taste_qubits = list(range(
            2 * self.n_qubits_per_property, 
            3 * self.n_qubits_per_property
        ))
        
        logger.debug(f"Qubit-Mapping - Frische: {self.freshness_qubits}, "
                    f"Haltbarkeit: {self.durability_qubits}, "
                    f"Geschmack: {self.taste_qubits}")
    
    def _setup_parameters(self) -> None:
        """
        Definiert die trainierbaren Parameter für die Quantengatter.
        
        Parameter-Typen:
        - θ_FH: Frische → Haltbarkeit Kopplung (3 Parameter)
        - θ_HG: Haltbarkeit → Geschmack Kopplung (3 Parameter)  
        - θ_FG: Direkte Frische → Geschmack Kopplung (3 Parameter)
        """
        # Frische → Haltbarkeit Parameter
        self.theta_FH = [
            Parameter(f'theta_FH_{i}') 
            for i in range(self.n_qubits_per_property)
        ]
        
        # Haltbarkeit → Geschmack Parameter
        self.theta_HG = [
            Parameter(f'theta_HG_{i}') 
            for i in range(self.n_qubits_per_property)
        ]
        
        # Direkte Frische → Geschmack Parameter
        self.theta_FG = [
            Parameter(f'theta_FG_{i}') 
            for i in range(self.n_qubits_per_property)
        ]
        
        logger.debug(f"Parameter definiert: {len(self.theta_FH + self.theta_HG + self.theta_FG)} total")
    
    def _initialize_parameters(self, seed: Optional[int] = None) -> None:
        """
        Initialisiert die Parameter-Werte zufällig.
        
        Args:
            seed: Zufallsseed für reproduzierbare Initialisierung
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Alle Parameter mit zufälligen Werten zwischen 0 und 2π initialisieren
        self.param_values = {}
        
        for param_list in [self.theta_FH, self.theta_HG, self.theta_FG]:
            for param in param_list:
                self.param_values[param] = np.random.uniform(0, 2 * np.pi)
        
        logger.debug(f"Parameter initialisiert mit Seed={seed}")
    
    def encode_freshness(self, qc: QuantumCircuit, freshness: float) -> None:
        """
        Kodiert den Frische-Wert in das Quanten-Subsystem.
        
        Die Frische wird auf einen Rotationswinkel θ_F = (π/10) * freshness
        abgebildet und mit RY- und RZ-Gattern kodiert.
        
        Args:
            qc: Quantenschaltkreis für die Kodierung
            freshness: Frische-Wert zwischen 1 und 10
        """
        # Normalisierung: Frische (1-10) → Rotationswinkel (π/10 bis π)
        theta_F = (np.pi / 10) * freshness
        
        logger.debug(f"Kodiere Frische {freshness} als Winkel {theta_F:.3f}")
        
        # State Preparation auf allen Frische-Qubits
        for i in self.freshness_qubits:
            # Haupt-Rotation auf Y-Achse
            qc.ry(theta_F, i)
            
            # Zusätzliche Z-Rotation nur auf erstem Qubit für mehr Expressivität
            if i == self.freshness_qubits[0]:
                qc.rz(theta_F / 2, i)
    
    def build_entanglement_layer(self, qc: QuantumCircuit) -> None:
        """
        Konstruiert die parametrisierte Verschränkungsschicht.
        
        Diese Schicht implementiert die trainierbaren Kopplungen zwischen
        den drei Subsystemen mittels CNOT-Gattern und parametrisierten
        Rotationen.
        
        Kopplungen:
        1. Frische → Haltbarkeit (CNOT + RY(θ_FH))
        2. Haltbarkeit → Geschmack (CNOT + RY(θ_HG))  
        3. Direkte Frische → Geschmack (CNOT + RZ(θ_FG))
        
        Args:
            qc: Quantenschaltkreis für die Verschränkung
        """
        # 1. Frische → Haltbarkeit Kopplung
        for i in range(self.n_qubits_per_property):
            # CNOT: Frische als Control, Haltbarkeit als Target
            qc.cx(self.freshness_qubits[i], self.durability_qubits[i])
            # Parametrisierte Rotation auf Target
            qc.ry(self.theta_FH[i], self.durability_qubits[i])
        
        # 2. Haltbarkeit → Geschmack Kopplung  
        for i in range(self.n_qubits_per_property):
            # CNOT: Haltbarkeit als Control, Geschmack als Target
            qc.cx(self.durability_qubits[i], self.taste_qubits[i])
            # Parametrisierte Rotation auf Target
            qc.ry(self.theta_HG[i], self.taste_qubits[i])
        
        # 3. Direkte Frische → Geschmack Kopplung (optional)
        for i in range(self.n_qubits_per_property):
            # Direkte CNOT: Frische → Geschmack
            qc.cx(self.freshness_qubits[i], self.taste_qubits[i])
            # Z-Rotation für Phasen-Information
            qc.rz(self.theta_FG[i], self.taste_qubits[i])
        
        logger.debug("Verschränkungsschicht konstruiert")
    
    def build_circuit(self, freshness: float) -> QuantumCircuit:
        """
        Erstellt den vollständigen parametrisierten Quantenschaltkreis.
        
        Der Schaltkreis besteht aus drei Hauptteilen:
        1. State Preparation: Kodierung der Frische
        2. Parametrisierte Verschränkung: Trainierbare Kopplungen
        3. Messungen: Separate Messungen für Haltbarkeit und Geschmack
        
        Args:
            freshness: Input-Frische zwischen 1 und 10
            
        Returns:
            QuantumCircuit: Vollständiger parametrisierter Schaltkreis
        """
        # Quantum- und Classical-Register definieren
        qr = QuantumRegister(self.n_total_qubits, 'q')
        cr_durability = ClassicalRegister(self.n_qubits_per_property, 'durability')
        cr_taste = ClassicalRegister(self.n_qubits_per_property, 'taste')
        
        # Schaltkreis initialisieren
        qc = QuantumCircuit(qr, cr_durability, cr_taste)
        
        # 1. State Preparation: Frische kodieren
        self.encode_freshness(qc, freshness)
        
        # 2. Parametrisierte Verschränkungsschicht
        self.build_entanglement_layer(qc)
        
        # 3. Messungen der Output-Subsysteme
        qc.measure(self.durability_qubits, cr_durability)
        qc.measure(self.taste_qubits, cr_taste)
        
        logger.debug(f"Schaltkreis erstellt für Frische={freshness}, "
                    f"Tiefe={qc.depth()}, Gates={len(qc)}")
        
        return qc
    
    def run_circuit(self, circuit: QuantumCircuit, shots: int = 1024) -> Dict:
        """
        Führt den Quantenschaltkreis auf dem Simulator aus.
        
        Args:
            circuit: Zu simulierender Quantenschaltkreis
            shots: Anzahl der Messwiederholungen
            
        Returns:
            Dict: Messergebnisse als Häufigkeitsverteilung
        """
        try:
            # Parameter in den Schaltkreis einsetzen
            bound_circuit = circuit.assign_parameters(self.param_values)
            
            # Simulation ausführen
            job = self.simulator.run(bound_circuit, shots=shots)
            result = job.result()
            counts = result.get_counts()
            
            logger.debug(f"Schaltkreis ausgeführt mit {shots} Shots, "
                        f"{len(counts)} verschiedene Ergebnisse")
            
            return counts
            
        except Exception as e:
            logger.error(f"Fehler bei Schaltkreis-Ausführung: {e}")
            raise
    
    def extract_values(self, counts: Dict) -> Tuple[float, float]:
        """
        Extrahiert Haltbarkeits- und Geschmackswerte aus den Messergebnissen.
        
        Die Bitstrings werden in Dezimalwerte umgewandelt und auf die
        1-10 Skala normalisiert. Der Erwartungswert wird über alle
        Messergebnisse berechnet.
        
        Args:
            counts: Messergebnisse als Häufigkeitsverteilung
            
        Returns:
            Tuple[float, float]: (Haltbarkeit, Geschmack) auf 1-10 Skala
        """
        total_shots = sum(counts.values())
        
        # Erwartungswerte initialisieren
        durability_expectation = 0.0
        taste_expectation = 0.0
        
        # Über alle Messergebnisse iterieren
        for bitstring, count in counts.items():
            # Bitstring aufteilen: [taste_bits][durability_bits]
            taste_bits = bitstring[:self.n_qubits_per_property]
            durability_bits = bitstring[self.n_qubits_per_property:]
            
            # In Dezimalwerte umwandeln
            durability_val = int(durability_bits, 2)
            taste_val = int(taste_bits, 2)
            
            # Gewichtete Summe für Erwartungswert
            probability = count / total_shots
            durability_expectation += durability_val * probability
            taste_expectation += taste_val * probability
        
        # Auf 1-10 Skala normalisieren
        max_val = 2**self.n_qubits_per_property - 1  # 7 für 3 Qubits
        durability_scaled = 1 + (durability_expectation / max_val) * 9
        taste_scaled = 1 + (taste_expectation / max_val) * 9
        
        logger.debug(f"Werte extrahiert - Haltbarkeit: {durability_scaled:.3f}, "
                    f"Geschmack: {taste_scaled:.3f}")
        
        return durability_scaled, taste_scaled
    
    def predict(self, freshness: float) -> Tuple[float, float]:
        """
        Führt eine Vorhersage für gegebene Frische durch.
        
        Dies ist die Hauptschnittstelle für Inferenz. Der vollständige
        Workflow von Schaltkreis-Erstellung bis Ergebnis-Extraktion
        wird durchgeführt.
        
        Args:
            freshness: Input-Frische zwischen 1 und 10
            
        Returns:
            Tuple[float, float]: Vorhersage für (Haltbarkeit, Geschmack)
        """
        if not (1 <= freshness <= 10):
            logger.warning(f"Frische {freshness} außerhalb des erwarteten Bereichs [1,10]")
        
        # Vollständiger Inferenz-Workflow
        circuit = self.build_circuit(freshness)
        counts = self.run_circuit(circuit)
        durability, taste = self.extract_values(counts)
        
        logger.info(f"Vorhersage für Frische {freshness}: "
                   f"Haltbarkeit={durability:.2f}, Geschmack={taste:.2f}")
        
        return durability, taste
    
    def compute_loss(self, predictions: List[Tuple[float, float]], 
                     targets: List[Tuple[float, float]]) -> float:
        """
        Berechnet den Mean Squared Error zwischen Vorhersagen und Zielen.
        
        Args:
            predictions: Liste von (Haltbarkeit, Geschmack) Vorhersagen
            targets: Liste von (Haltbarkeit, Geschmack) Zielwerten
            
        Returns:
            float: MSE Loss-Wert
        """
        if len(predictions) != len(targets):
            raise ValueError("Predictions und Targets müssen gleiche Länge haben")
        
        total_loss = 0.0
        for (pred_dur, pred_taste), (target_dur, target_taste) in zip(predictions, targets):
            # Squared Error für beide Outputs
            loss_dur = (pred_dur - target_dur) ** 2
            loss_taste = (pred_taste - target_taste) ** 2
            total_loss += loss_dur + loss_taste
        
        mse_loss = total_loss / len(predictions)
        
        logger.debug(f"Loss berechnet: {mse_loss:.4f} für {len(predictions)} Samples")
        
        return mse_loss
    
    def update_parameters(self, gradients: Dict[Parameter, float], 
                         learning_rate: float = 0.1) -> None:
        """
        Aktualisiert die Parameter basierend auf Gradienten.
        
        Gradient Descent Update: θ_new = θ_old - learning_rate * gradient
        
        Args:
            gradients: Dictionary mit Parameter → Gradient Zuordnung
            learning_rate: Schrittgröße für Update
        """
        updated_count = 0
        for param, grad in gradients.items():
            if param in self.param_values:
                old_value = self.param_values[param]
                self.param_values[param] -= learning_rate * grad
                updated_count += 1
                
                logger.debug(f"Parameter {param} updated: "
                           f"{old_value:.4f} → {self.param_values[param]:.4f}")
        
        logger.info(f"{updated_count} Parameter mit Learning Rate {learning_rate} aktualisiert")
    
    def visualize_circuit(self, freshness: float = 5.0, 
                         filename: Optional[str] = None,
                         output_format: str = 'mpl') -> Optional[plt.Figure]:
        """
        Visualisiert den Quantenschaltkreis.
        
        Args:
            freshness: Frische-Wert für Beispiel-Schaltkreis
            filename: Dateiname für Speicherung (optional)
            output_format: Format ('mpl' für matplotlib, 'text' für Text)
            
        Returns:
            Optional[plt.Figure]: Matplotlib Figure oder None bei Text-Output
        """
        circuit = self.build_circuit(freshness)
        bound_circuit = circuit.assign_parameters(self.param_values)
        
        try:
            if output_format == 'mpl':
                # Versuche matplotlib Visualisierung
                fig = circuit_drawer(bound_circuit, output='mpl', style='iqp')
                
                if filename:
                    plt.savefig(filename, dpi=300, bbox_inches='tight')
                    logger.info(f"Schaltkreis gespeichert als {filename}")
                else:
                    plt.show()
                
                return fig
                
            else:
                # Text-Fallback
                text_circuit = circuit_drawer(bound_circuit, output='text')
                print(f"\nSchaltkreis für Frische={freshness}:")
                print("=" * 50)
                print(text_circuit)
                
                if filename:
                    with open(filename, 'w') as f:
                        f.write(f"Schaltkreis für Frische={freshness}\n")
                        f.write("=" * 50 + "\n")
                        f.write(str(text_circuit))
                    logger.info(f"Schaltkreis-Text gespeichert als {filename}")
                
                return None
                
        except Exception as e:
            logger.warning(f"Visualisierung fehlgeschlagen: {e}")
            # Fallback auf Text-Ausgabe
            print("Hinweis: Für bessere Visualisierung installiere 'pip install pylatexenc'")
            text_circuit = circuit_drawer(bound_circuit, output='text')
            print(f"\nSchaltkreis für Frische={freshness}:")
            print(text_circuit)
            return None
    
    def get_model_info(self) -> Dict:
        """
        Gibt umfassende Informationen über das Modell zurück.
        
        Returns:
            Dict: Modell-Metadaten und Statistiken
        """
        return {
            'total_qubits': self.n_total_qubits,
            'qubits_per_property': self.n_qubits_per_property,
            'total_parameters': len(self.param_values),
            'parameter_types': {
                'theta_FH': len(self.theta_FH),
                'theta_HG': len(self.theta_HG),  
                'theta_FG': len(self.theta_FG)
            },
            'qubit_mapping': {
                'freshness': self.freshness_qubits,
                'durability': self.durability_qubits,
                'taste': self.taste_qubits
            },
            'parameter_ranges': {
                'min': min(self.param_values.values()),
                'max': max(self.param_values.values()),
                'mean': np.mean(list(self.param_values.values())),
                'std': np.std(list(self.param_values.values()))
            }
        }