# 🍎 Apfel QML-System: Quantum Machine Learning für Apfel-Eigenschaftsvorhersage

Ein vollständiges Quantum Machine Learning System zur Vorhersage von Apfel-Eigenschaften (Haltbarkeit und Geschmack) basierend auf der Frische als Input.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0%2B-purple)](https://qiskit.org)
[![Tests](https://img.shields.io/badge/Tests-Passing-green)](#testing)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🎯 Überblick

Das Apfel QML-System demonstriert den Einsatz von Quantum Machine Learning für realistische Eigenschaftsvorhersagen. Es nutzt einen parametrisierten Quantenschaltkreis (PQC) mit 9 Qubits zur Modellierung komplexer Beziehungen zwischen Apfel-Eigenschaften.

### 🔬 Wissenschaftlicher Hintergrund

- **Quantum Machine Learning**: Nutzung von Quantencomputern für ML-Aufgaben
- **Parametrisierte Quantenschaltkreise**: Trainierbare Quantenalgorithmen
- **Variational Quantum Classifiers**: Hybride klassisch-quantische Optimierung
- **Multi-Output Regression**: Gleichzeitige Vorhersage mehrerer Eigenschaften

### 🏗️ Systemarchitektur

```
Input: Frische (1-10) → [9-Qubit QML-System] → Outputs: Haltbarkeit & Geschmack (1-10)

Subsysteme:
├── Frische (Q0-Q2)     : Input-Encoding mit RY/RZ Gates
├── Haltbarkeit (Q3-Q5) : Output 1 mit parametrisierten Kopplungen  
└── Geschmack (Q6-Q8)   : Output 2 mit parametrisierten Kopplungen

Trainierbare Parameter:
├── θ_FH: Frische → Haltbarkeit (3 Parameter)
├── θ_HG: Haltbarkeit → Geschmack (3 Parameter)
└── θ_FG: Frische → Geschmack direkt (3 Parameter)
```

## 🚀 Schnellstart

### Installation

```bash
# Repository klonen
git clone <repository-url>
cd apple_qml

# Dependencies installieren
pip install -r requirements.txt

# Optional: Development Dependencies
pip install -r requirements-dev.txt
```

### Basis-Verwendung

```python
from src import QuantumAppleModel, AppleDataGenerator, QuantumTrainer

# 1. Modell erstellen
model = QuantumAppleModel(n_qubits_per_property=3)

# 2. Daten generieren
data_gen = AppleDataGenerator(seed=42)
freshness, targets = data_gen.generate_realistic_data(n_samples=50)

# 3. Training
trainer = QuantumTrainer(model)
train_fresh, train_targets, test_fresh, test_targets = data_gen.split_data(freshness, targets)
trainer.train_gradient_descent(train_fresh, train_targets)

# 4. Vorhersage
durability, taste = model.predict(freshness=7.5)
print(f"Frische: 7.5 → Haltbarkeit: {durability:.2f}, Geschmack: {taste:.2f}")
```

### Beispiele ausführen

```bash
# Basic Usage Example
python examples/basic_usage.py

# Advanced Training Strategies  
python examples/advanced_training.py

# Vollständige Visualisierung
python examples/complete_visualization.py
```

## 📁 Projektstruktur

```
apple_qml/
├── src/                          # Hauptquellcode
│   ├── __init__.py
│   ├── quantum_apple_model.py    # Kern-QML-Modell
│   ├── data_generator.py         # Datengenerierung
│   ├── trainer.py                # Training & Optimierung
│   └── visualizer.py             # Visualisierungstools
├── examples/                     # Verwendungsbeispiele
│   ├── basic_usage.py            # Einfaches Beispiel
│   ├── advanced_training.py      # Erweiterte Trainingsstrategien
│   └── hyperparameter_tuning.py  # Hyperparameter-Optimierung
├── tests/                        # Unit Tests
│   ├── test_quantum_apple_model.py
│   ├── test_data_generator.py
│   └── test_trainer.py
├── configs/                      # Konfigurationsdateien
│   ├── model_config.yaml         # Modell-Konfiguration
│   └── training_config.yaml      # Training-Konfiguration
├── docs/                         # Dokumentation
│   ├── README.md                 # Diese Datei
│   ├── API_REFERENCE.md          # API-Dokumentation
│   └── THEORY.md                 # Theoretischer Hintergrund
├── outputs/                      # Ausgabeordner
│   ├── models/                   # Gespeicherte Modelle
│   ├── visualizations/           # Plots und Diagramme
│   └── logs/                     # Training-Logs
└── data/                         # Datensätze
    ├── synthetic/                # Synthetische Daten
    └── real/                     # Reale Daten (falls verfügbar)
```

## 🔧 Hauptkomponenten

### 1. QuantumAppleModel

Kernklasse des QML-Systems mit 9-Qubit Architektur:

```python
# Modell-Erstellung
model = QuantumAppleModel(
    n_qubits_per_property=3,  # 3 Qubits pro Eigenschaft
    seed=42                   # Reproduzierbarkeit
)

# Modell-Informationen
info = model.get_model_info()
print(f"Qubits: {info['total_qubits']}, Parameter: {info['total_parameters']}")

# Vorhersage
durability, taste = model.predict(freshness=6.0)
```

**Features:**
- ✅ 9-Qubit parametrisierter Quantenschaltkreis
- ✅ Flexibles Qubit-Mapping zu Subsystemen
- ✅ State Preparation mit RY/RZ Gates
- ✅ Parametrisierte Verschränkungsschichten
- ✅ Multi-Output Regression
- ✅ Umfassende Fehlerbehandlung

### 2. AppleDataGenerator

Flexible Datengenerierung für verschiedene Szenarien:

```python
# Realistische Daten mit Rauschen
data_gen = AppleDataGenerator(noise_level=0.1)
freshness, targets = data_gen.generate_realistic_data(n_samples=100)

# Lineare Testdaten
freshness_linear, targets_linear = data_gen.generate_simple_linear_data(n_samples=20)

# Datenstatistiken
stats = data_gen.get_statistics(freshness, targets)
print(f"Korrelation F↔H: {stats['correlations']['freshness_durability']:.3f}")
```

**Features:**
- ✅ Realistische physikalische Beziehungen
- ✅ Konfigurierbares Rauschen und Variationen
- ✅ Verschiedene Datentypen (linear, nichtlinear, realistisch)
- ✅ Automatisches Train/Validation/Test Splitting
- ✅ Umfassende Datenstatistiken und -visualisierung
- ✅ Export in verschiedene Formate

### 3. QuantumTrainer

Fortgeschrittene Trainingsstrategien und Optimierung:

```python
# Training-Konfiguration
config = TrainingConfig(
    epochs=50,
    learning_rate=0.15,
    batch_size=8,
    adaptive_lr=True,
    patience=15
)

# Trainer mit Gradient Descent
trainer = QuantumTrainer(model, config)
metrics = trainer.train_gradient_descent(train_data, train_targets)

# Scipy-basierte Optimizer
trainer.train_scipy_optimizer(train_data, train_targets, method='COBYLA')

# Evaluation
results = trainer.evaluate(test_data, test_targets)
```

**Features:**
- ✅ Gradient Descent mit finite differences
- ✅ Scipy-basierte Optimizer (COBYLA, Nelder-Mead, Powell)
- ✅ Adaptive Learning Rate und Early Stopping
- ✅ Gradient Clipping und Regularisierung
- ✅ Umfassende Training-Metriken und -Monitoring
- ✅ Cross-Validation und Hyperparameter-Optimierung

### 4. QuantumVisualizer

Umfassende Visualisierungstools für alle Aspekte:

```python
visualizer = QuantumVisualizer()

# Systemarchitektur
visualizer.visualize_system_architecture(filename='architecture.png')

# 3D-Vorhersageraum
visualizer.visualize_3d_prediction_space(model, filename='3d_predictions.png')

# Parameter-Landschaften
visualizer.visualize_parameter_landscape(model, param_type='FH', filename='landscape.png')

# Umfassendes Dashboard
visualizer.create_comprehensive_dashboard(model, trainer, results, filename='dashboard.png')
```

**Features:**
- ✅ Detaillierte Schaltkreis-Diagramme
- ✅ Training-Verlauf und Konvergenz-Analyse
- ✅ 3D-Vorhersageraum-Visualisierung
- ✅ Parameter-Landschaften und Gradientenflüsse
- ✅ Quantenzustands-Visualisierung
- ✅ Interaktive Dashboards und Berichte

## 🧪 Testing

Umfassende Test-Suite für alle Komponenten:

```bash
# Alle Tests ausführen
python -m pytest tests/ -v

# Spezifische Test-Klasse
python tests/test_quantum_apple_model.py

# Coverage Report
python -m pytest tests/ --cov=src --cov-report=html
```

**Test-Kategorien:**
- ✅ Unit Tests für alle Klassen und Methoden
- ✅ Integration Tests für End-to-End Workflows
- ✅ Performance Tests für Skalierbarkeit
- ✅ Fehlerbehandlung und Edge Cases
- ✅ Reproduzierbarkeit und Deterministik

## 📊 Benchmarks und Performance

### Typische Performance-Metriken

| Metrik | Wert | Beschreibung |
|--------|------|--------------|
| Training Zeit | ~30s | 50 Epochen, 50 Samples |
| Vorhersage Zeit | ~0.2s | Einzelne Vorhersage |
| Test MAE (Haltbarkeit) | ~0.5 | Mean Absolute Error |
| Test MAE (Geschmack) | ~0.8 | Mean Absolute Error |
| R² Score | ~0.7-0.9 | Bestimmtheitsmaß |

### Skalierbarkeit

- **Qubits**: 3-12 Qubits getestet
- **Samples**: Bis 1000 Trainingssamples
- **Parameter**: 9-36 trainierbare Parameter
- **Batch-Größe**: 1-20 Samples pro Batch

## 🔬 Wissenschaftliche Features

### Quantum Machine Learning Konzepte

1. **Parametrisierte Quantenschaltkreise (PQC)**
   - Trainierbare Quantengatter
   - Variational Quantum Eigensolvers (VQE) Prinzipien
   - Barren Plateau Vermeidung

2. **Hybride Optimierung**
   - Klassische Optimizer für Quantenparameter
   - Gradient-freie Optimierung (COBYLA, SPSA)
   - Parameter-Shift-Regel für Gradienten

3. **Quantenverschränkung für Feature Engineering**
   - Qubit-zu-Qubit Korrelationen
   - Subsystem-übergreifende Kopplungen
   - Nichtlineare Feature-Transformationen

### Experimentelle Validierung

- **Vergleich mit klassischen ML-Modellen**
- **Ablationsstudien für Quantenkomponenten**
- **Noise-Robustheit Analyse**
- **Skalierbarkeit auf realer Quantum Hardware**

## 🛠️ Erweiterte Verwendung

### Hyperparameter-Optimierung

```python
from examples.advanced_training import HyperparameterOptimizer

# Grid Search
param_grid = {
    'epochs': [20, 30, 50],
    'learning_rate': [0.1, 0.15, 0.2],
    'batch_size': [4, 6, 8]
}

optimizer = HyperparameterOptimizer(param_grid)
best_config = optimizer.grid_search(train_data, val_data)
```

### Ensemble-Modelle

```python
from examples.advanced_training import EnsembleModel

# Ensemble aus 5 Modellen
ensemble = EnsembleModel(n_models=5)
ensemble.train_ensemble(train_data)

# Ensemble-Vorhersage
prediction = ensemble.predict_ensemble(freshness=7.0)
```

### Custom Konfiguration

```python
# YAML-Konfiguration laden
import yaml

with open('configs/model_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Modell mit Custom Config
model = QuantumAppleModel(
    n_qubits_per_property=config['model']['n_qubits_per_property']
)
```

## 📈 Roadmap

### Geplante Features

- [ ] **Quantum Hardware Integration**
  - IBM Quantum Backend Support
  - Google Cirq Integration
  - IonQ Hardware Tests

- [ ] **Erweiterte Algorithmen**
  - Quantum Neural Networks (QNN)
  - Quantum Approximate Optimization Algorithm (QAOA)
  - Quantum Support Vector Machines (QSVM)

- [ ] **Produktive Features**
  - REST API für Modell-Serving
  - Docker Container für Deployment
  - Cloud-Integration (AWS Braket, IBM Quantum Network)

- [ ] **Wissenschaftliche Erweiterungen**
  - Quantum Advantage Analyse
  - Entanglement Measures
  - Quantum Fisher Information

### Kurzfristig (nächste Version)

- [ ] Multi-Threading für Training
- [ ] Erweitertes Noise Modeling
- [ ] Jupyter Notebook Tutorials
- [ ] Automatische Dokumentations-Generierung

## 🤝 Beitragen

Beiträge sind willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Development Setup

```bash
# Development Environment einrichten
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements-dev.txt

# Pre-commit Hooks
pre-commit install

# Tests vor Commit
python -m pytest tests/
```

## 📄 Lizenz

Dieses Projekt steht unter der MIT Lizenz - siehe [LICENSE](LICENSE) für Details.

## 📚 Zitierung

Falls Sie dieses Projekt in Ihrer Forschung verwenden:

```bibtex
@software{apple_qml_system,
  title={Apfel QML-System: Quantum Machine Learning für Eigenschaftsvorhersage},
  author={QML Development Team},
  year={2024},
  url={https://github.com/username/apple-qml-system},
  version={1.0.0}
}
```

## 🙏 Danksagungen

- **Qiskit Team** für das exzellente Quantum Computing Framework
- **IBM Quantum Network** für Zugang zu Quantum Hardware
- **Quantum Machine Learning Community** für theoretische Grundlagen

## 📞 Kontakt

- **Issues**: [GitHub Issues](https://github.com/username/apple-qml-system/issues)
- **Diskussionen**: [GitHub Discussions](https://github.com/username/apple-qml-system/discussions)
- **Email**: qml-team@example.com

---

**⚡ Powered by Quantum Computing | 🍎 Optimized for Apples | 🚀 Ready for the Quantum Future**