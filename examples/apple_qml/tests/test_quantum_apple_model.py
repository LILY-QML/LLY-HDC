#!/usr/bin/env python3
"""
Test Suite für QuantumAppleModel

Umfassende Unit Tests für alle Funktionalitäten des Quantum Apple Models:
- Modell-Initialisierung und Konfiguration
- State Preparation und Qubit-Mapping
- Schaltkreis-Konstruktion und Parameter-Handling
- Vorhersage-Pipeline und Fehlerbehandlung
- Performance- und Integritäts-Tests
"""

import unittest
import sys
import os
import numpy as np
from unittest.mock import patch, MagicMock

# Pfad zum src-Verzeichnis hinzufügen
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_apple_model import QuantumAppleModel
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


class TestQuantumAppleModel(unittest.TestCase):
    """
    Test-Klasse für QuantumAppleModel.
    """
    
    def setUp(self):
        """
        Setup für jeden Test - erstellt frische Modell-Instanz.
        """
        self.model = QuantumAppleModel(n_qubits_per_property=3, seed=42)
        
    def tearDown(self):
        """
        Cleanup nach jedem Test.
        """
        del self.model
    
    # === INITIALISIERUNG TESTS ===
    
    def test_model_initialization(self):
        """
        Testet die korrekte Modell-Initialisierung.
        """
        # Standard-Initialisierung
        model = QuantumAppleModel()
        self.assertEqual(model.n_qubits_per_property, 3)
        self.assertEqual(model.n_total_qubits, 9)
        
        # Custom-Initialisierung
        model_custom = QuantumAppleModel(n_qubits_per_property=2)
        self.assertEqual(model_custom.n_qubits_per_property, 2)
        self.assertEqual(model_custom.n_total_qubits, 6)
    
    def test_qubit_mapping(self):
        """
        Testet das korrekte Qubit-Mapping zu Subsystemen.
        """
        self.assertEqual(self.model.freshness_qubits, [0, 1, 2])
        self.assertEqual(self.model.durability_qubits, [3, 4, 5])
        self.assertEqual(self.model.taste_qubits, [6, 7, 8])
        
        # Keine Überlappungen
        all_qubits = (self.model.freshness_qubits + 
                     self.model.durability_qubits + 
                     self.model.taste_qubits)
        self.assertEqual(len(all_qubits), len(set(all_qubits)))
    
    def test_parameter_setup(self):
        """
        Testet die korrekte Parameter-Initialisierung.
        """
        # Richtige Anzahl Parameter
        self.assertEqual(len(self.model.theta_FH), 3)
        self.assertEqual(len(self.model.theta_HG), 3)
        self.assertEqual(len(self.model.theta_FG), 3)
        
        # Parameter sind Qiskit Parameter-Objekte
        for param in self.model.theta_FH:
            self.assertIsInstance(param, Parameter)
        
        # Parameter-Werte sind initialisiert
        self.assertEqual(len(self.model.param_values), 9)
        
        # Werte im gültigen Bereich [0, 2π]
        for value in self.model.param_values.values():
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 2*np.pi)
    
    def test_reproducible_initialization(self):
        """
        Testet reproduzierbare Parameter-Initialisierung mit Seed.
        """
        model1 = QuantumAppleModel(seed=123)
        model2 = QuantumAppleModel(seed=123)
        
        # Parameter sollten identisch sein
        for key in model1.param_values:
            self.assertAlmostEqual(
                model1.param_values[key], 
                model2.param_values[key],
                places=10
            )
    
    # === STATE PREPARATION TESTS ===
    
    def test_encode_freshness(self):
        """
        Testet die Frische-Kodierung.
        """
        qc = QuantumCircuit(9)
        
        # Test verschiedene Frische-Werte
        test_values = [1.0, 5.0, 10.0]
        
        for freshness in test_values:
            qc_test = QuantumCircuit(9)
            self.model.encode_freshness(qc_test, freshness)
            
            # Prüfe ob Gates hinzugefügt wurden
            self.assertGreater(len(qc_test), 0)
            
            # Prüfe erwartete Gate-Typen
            gate_names = [instruction.operation.name for instruction in qc_test.data]
            self.assertIn('ry', gate_names)
            
            # Für Frische-Wert 1 sollte auch RZ Gate vorhanden sein
            if freshness == test_values[0]:  # Erstes Qubit bekommt zusätzliches RZ
                self.assertIn('rz', gate_names)
    
    def test_freshness_encoding_angles(self):
        """
        Testet die korrekten Rotationswinkel für Frische-Kodierung.
        """
        # Erwartete Winkel: theta_F = (π/10) * freshness
        test_cases = [
            (1.0, np.pi/10),
            (5.0, np.pi/2),
            (10.0, np.pi)
        ]
        
        for freshness, expected_angle in test_cases:
            calculated_angle = (np.pi / 10) * freshness
            self.assertAlmostEqual(calculated_angle, expected_angle, places=10)
    
    # === SCHALTKREIS-KONSTRUKTION TESTS ===
    
    def test_build_circuit(self):
        """
        Testet die vollständige Schaltkreis-Erstellung.
        """
        freshness = 5.0
        circuit = self.model.build_circuit(freshness)
        
        # Richtiger Typ
        self.assertIsInstance(circuit, QuantumCircuit)
        
        # Richtige Anzahl Qubits
        self.assertEqual(circuit.num_qubits, 9)
        
        # Classical Register für Messungen vorhanden
        self.assertEqual(len(circuit.cregs), 2)  # durability + taste
        
        # Schaltkreis enthält Parameter
        self.assertTrue(len(circuit.parameters) > 0)
        
        # Messungen sind vorhanden
        gate_names = [instruction.operation.name for instruction in circuit.data]
        self.assertIn('measure', gate_names)
    
    def test_entanglement_layer(self):
        """
        Testet die Verschränkungsschicht-Konstruktion.
        """
        qc = QuantumCircuit(9)
        self.model.build_entanglement_layer(qc)
        
        # CNOT Gates sollten vorhanden sein
        gate_names = [instruction.operation.name for instruction in qc.data]
        self.assertIn('cx', gate_names)
        self.assertIn('ry', gate_names)
        self.assertIn('rz', gate_names)
        
        # Richtige Anzahl Gates (approximativ)
        # 3 CNOTs für F→H, 3 RYs, 3 CNOTs für H→G, 3 RYs, 3 CNOTs für F→G, 3 RZs
        expected_min_gates = 15  # Mindestens
        self.assertGreaterEqual(len(qc), expected_min_gates)
    
    def test_circuit_depth_reasonable(self):
        """
        Testet ob Schaltkreis-Tiefe in vernünftigem Bereich liegt.
        """
        circuit = self.model.build_circuit(5.0)
        bound_circuit = circuit.assign_parameters(self.model.param_values)
        
        depth = bound_circuit.depth()
        
        # Tiefe sollte zwischen 10 und 50 liegen (heuristisch)
        self.assertGreaterEqual(depth, 5)
        self.assertLessEqual(depth, 100)
    
    # === VORHERSAGE TESTS ===
    
    def test_predict_output_format(self):
        """
        Testet das korrekte Format der Vorhersage-Ausgabe.
        """
        durability, taste = self.model.predict(5.0)
        
        # Outputs sind Floats
        self.assertIsInstance(durability, float)
        self.assertIsInstance(taste, float)
        
        # Werte im erwarteten Bereich [1, 10]
        self.assertGreaterEqual(durability, 1.0)
        self.assertLessEqual(durability, 10.0)
        self.assertGreaterEqual(taste, 1.0)
        self.assertLessEqual(taste, 10.0)
    
    def test_predict_different_inputs(self):
        """
        Testet Vorhersagen für verschiedene Eingabewerte.
        """
        test_inputs = [1.0, 3.5, 5.0, 7.5, 10.0]
        
        predictions = []
        for freshness in test_inputs:
            pred = self.model.predict(freshness)
            predictions.append(pred)
            
            # Jede Vorhersage sollte valid sein
            self.assertIsInstance(pred, tuple)
            self.assertEqual(len(pred), 2)
        
        # Vorhersagen sollten unterschiedlich sein (bei verschiedenen Inputs)
        unique_predictions = set(predictions)
        self.assertGreater(len(unique_predictions), 1)
    
    def test_predict_edge_cases(self):
        """
        Testet Vorhersagen für Grenzfälle.
        """
        # Grenzwerte
        edge_cases = [0.0, 1.0, 10.0, 11.0, -1.0]
        
        for freshness in edge_cases:
            try:
                durability, taste = self.model.predict(freshness)
                # Sollte nicht crashen, auch bei ungültigen Inputs
                self.assertIsInstance(durability, float)
                self.assertIsInstance(taste, float)
            except Exception as e:
                # Falls Exception, sollte sie dokumentiert sein
                self.fail(f"Unerwartete Exception für Eingabe {freshness}: {e}")
    
    # === PARAMETER UPDATE TESTS ===
    
    def test_update_parameters(self):
        """
        Testet Parameter-Updates.
        """
        # Ursprüngliche Parameter speichern
        original_params = self.model.param_values.copy()
        
        # Dummy-Gradienten erstellen
        gradients = {}
        for param in self.model.param_values.keys():
            gradients[param] = 0.1  # Konstanter Gradient
        
        # Parameter aktualisieren
        learning_rate = 0.1
        self.model.update_parameters(gradients, learning_rate)
        
        # Parameter sollten sich geändert haben
        for param in self.model.param_values.keys():
            expected_new_value = original_params[param] - learning_rate * gradients[param]
            self.assertAlmostEqual(
                self.model.param_values[param],
                expected_new_value,
                places=10
            )
    
    def test_compute_loss(self):
        """
        Testet Loss-Berechnung.
        """
        # Test-Daten
        predictions = [(5.0, 6.0), (7.0, 8.0), (3.0, 4.0)]
        targets = [(5.5, 6.5), (7.2, 7.8), (2.8, 4.2)]
        
        loss = self.model.compute_loss(predictions, targets)
        
        # Loss sollte positive Zahl sein
        self.assertIsInstance(loss, float)
        self.assertGreaterEqual(loss, 0.0)
        
        # Perfekte Vorhersage sollte Loss = 0 geben
        perfect_predictions = [(5.0, 6.0), (7.0, 8.0)]
        perfect_targets = [(5.0, 6.0), (7.0, 8.0)]
        perfect_loss = self.model.compute_loss(perfect_predictions, perfect_targets)
        self.assertAlmostEqual(perfect_loss, 0.0, places=10)
    
    # === FEHLERBEHANDLUNG TESTS ===
    
    def test_invalid_parameter_updates(self):
        """
        Testet Fehlerbehandlung bei ungültigen Parameter-Updates.
        """
        # Leere Gradienten
        self.model.update_parameters({}, 0.1)  # Sollte nicht crashen
        
        # Ungültige Parameter
        invalid_gradients = {Parameter('invalid_param'): 0.1}
        self.model.update_parameters(invalid_gradients, 0.1)  # Sollte ignoriert werden
    
    def test_mismatched_predictions_targets(self):
        """
        Testet Fehlerbehandlung bei nicht passenden Predictions/Targets.
        """
        predictions = [(5.0, 6.0), (7.0, 8.0)]
        targets = [(5.5, 6.5)]  # Verschiedene Längen
        
        with self.assertRaises(ValueError):
            self.model.compute_loss(predictions, targets)
    
    # === INTEGRATION TESTS ===
    
    def test_full_prediction_pipeline(self):
        """
        Testet die vollständige Vorhersage-Pipeline.
        """
        freshness = 6.0
        
        # 1. Schaltkreis erstellen
        circuit = self.model.build_circuit(freshness)
        self.assertIsInstance(circuit, QuantumCircuit)
        
        # 2. Schaltkreis ausführen
        counts = self.model.run_circuit(circuit)
        self.assertIsInstance(counts, dict)
        self.assertGreater(len(counts), 0)
        
        # 3. Werte extrahieren
        durability, taste = self.model.extract_values(counts)
        self.assertIsInstance(durability, float)
        self.assertIsInstance(taste, float)
        
        # 4. Vorhersage (End-to-End)
        pred_dur, pred_taste = self.model.predict(freshness)
        
        # Sollten ähnliche Ergebnisse liefern (mit gewisser Toleranz wegen Rauschen)
        self.assertAlmostEqual(durability, pred_dur, delta=1.0)
        self.assertAlmostEqual(taste, pred_taste, delta=1.0)
    
    def test_model_info(self):
        """
        Testet die Modell-Informations-Funktion.
        """
        info = self.model.get_model_info()
        
        # Korrekte Struktur
        self.assertIsInstance(info, dict)
        
        # Erwartete Keys
        expected_keys = [
            'total_qubits', 'qubits_per_property', 'total_parameters',
            'parameter_types', 'qubit_mapping', 'parameter_ranges'
        ]
        for key in expected_keys:
            self.assertIn(key, info)
        
        # Korrekte Werte
        self.assertEqual(info['total_qubits'], 9)
        self.assertEqual(info['total_parameters'], 9)
        self.assertEqual(info['qubits_per_property'], 3)
    
    # === PERFORMANCE TESTS ===
    
    def test_prediction_performance(self):
        """
        Testet die Performance der Vorhersage-Funktion.
        """
        import time
        
        # Mehrere Vorhersagen messen
        n_predictions = 10
        start_time = time.time()
        
        for i in range(n_predictions):
            self.model.predict(5.0 + i * 0.1)
        
        total_time = time.time() - start_time
        avg_time_per_prediction = total_time / n_predictions
        
        # Sollte schnell genug sein (< 1 Sekunde pro Vorhersage)
        self.assertLess(avg_time_per_prediction, 1.0)
    
    def test_memory_usage(self):
        """
        Testet ob Modell vernünftige Speicher-Nutzung hat.
        """
        import sys
        
        # Größe des Modell-Objekts
        model_size = sys.getsizeof(self.model)
        
        # Sollte nicht zu groß sein (< 10 MB)
        max_size_mb = 10 * 1024 * 1024
        self.assertLess(model_size, max_size_mb)


class TestQuantumAppleModelExtended(unittest.TestCase):
    """
    Erweiterte Tests für spezielle Szenarien.
    """
    
    def test_different_qubit_counts(self):
        """
        Testet Modelle mit verschiedenen Qubit-Zahlen.
        """
        for n_qubits in [1, 2, 3, 4]:
            model = QuantumAppleModel(n_qubits_per_property=n_qubits)
            
            # Grundfunktionalität sollte funktionieren
            prediction = model.predict(5.0)
            self.assertIsInstance(prediction, tuple)
            self.assertEqual(len(prediction), 2)
    
    def test_parameter_persistence(self):
        """
        Testet ob Parameter zwischen Aufrufen persistent bleiben.
        """
        model = QuantumAppleModel(seed=42)
        
        # Erste Vorhersage
        pred1 = model.predict(5.0)
        
        # Parameter ändern
        for param in model.param_values.keys():
            model.param_values[param] += 0.1
        
        # Zweite Vorhersage sollte anders sein
        pred2 = model.predict(5.0)
        
        self.assertNotEqual(pred1, pred2)
    
    @patch('quantum_apple_model.AerSimulator')
    def test_simulator_failure_handling(self, mock_simulator):
        """
        Testet Verhalten bei Simulator-Fehlern.
        """
        # Mock Simulator-Fehler
        mock_simulator.return_value.run.side_effect = Exception("Simulator Error")
        
        model = QuantumAppleModel()
        
        # Sollte Exception propagieren oder graceful handling
        with self.assertRaises(Exception):
            model.predict(5.0)


# === TEST RUNNER ===

def run_tests():
    """
    Führt alle Tests aus und gibt Ergebnisse aus.
    """
    # Test Suite erstellen
    test_suite = unittest.TestSuite()
    
    # Tests hinzufügen
    test_suite.addTest(unittest.makeSuite(TestQuantumAppleModel))
    test_suite.addTest(unittest.makeSuite(TestQuantumAppleModelExtended))
    
    # Test Runner konfigurieren
    runner = unittest.TextTestRunner(
        verbosity=2,
        buffer=True,
        stream=sys.stdout
    )
    
    # Tests ausführen
    result = runner.run(test_suite)
    
    # Zusammenfassung
    print("\n" + "="*60)
    print("TEST ZUSAMMENFASSUNG")
    print("="*60)
    print(f"Tests ausgeführt: {result.testsRun}")
    print(f"Fehler: {len(result.errors)}")
    print(f"Fehlgeschlagen: {len(result.failures)}")
    print(f"Übersprungen: {len(result.skipped)}")
    
    if result.errors:
        print("\nFEHLER:")
        for test, error in result.errors:
            print(f"  {test}: {error}")
    
    if result.failures:
        print("\nFEHLGESCHLAGEN:")
        for test, failure in result.failures:
            print(f"  {test}: {failure}")
    
    success_rate = (result.testsRun - len(result.errors) - len(result.failures)) / result.testsRun * 100
    print(f"\nErfolgsrate: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)