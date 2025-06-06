"""
Apfel QML-System: Quantum Machine Learning für Apfel-Eigenschaftsvorhersage

Dieses Paket implementiert ein vollständiges Quantum Machine Learning System zur
Vorhersage von Apfel-Eigenschaften (Haltbarkeit und Geschmack) basierend auf der
Frische als Input.

Hauptkomponenten:
- QuantumAppleModel: Kern-QML-Modell mit 9 Qubits
- DataGenerator: Synthetische Datengenerierung
- Trainer: Training und Optimierung
- Visualizer: Umfassende Visualisierungstools

Autor: QML-Entwicklungsteam
Version: 1.0.0
Lizenz: MIT
"""

__version__ = "1.0.0"
__author__ = "QML-Entwicklungsteam"

from .quantum_apple_model import QuantumAppleModel
from .data_generator import AppleDataGenerator
from .trainer import QuantumTrainer
from .visualizer import QuantumVisualizer

__all__ = [
    'QuantumAppleModel',
    'AppleDataGenerator', 
    'QuantumTrainer',
    'QuantumVisualizer'
]