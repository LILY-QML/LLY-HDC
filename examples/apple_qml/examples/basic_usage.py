#!/usr/bin/env python3
"""
Basic Usage Example - Einfaches Beispiel für das Apfel QML-System

Dieses Skript demonstriert die grundlegende Verwendung des Apfel QML-Systems:
1. Modell-Erstellung und Konfiguration
2. Datengenerierung  
3. Training mit verschiedenen Strategien
4. Evaluation und Visualisierung

Ideal für erste Schritte und zum Verständnis der Basis-Funktionalitäten.
"""

import sys
import os
import logging

# Pfad zum src-Verzeichnis hinzufügen
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_apple_model import QuantumAppleModel
from data_generator import AppleDataGenerator
from trainer import QuantumTrainer, TrainingConfig
from visualizer import QuantumVisualizer

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Hauptfunktion für das Basic Usage Beispiel.
    
    Führt einen kompletten Workflow vom Modell-Setup bis zur Evaluation durch.
    """
    logger.info("=== Apfel QML-System: Basic Usage Example ===")
    
    # === 1. MODELL-ERSTELLUNG ===
    logger.info("\n1. Erstelle Quantum Apple Model...")
    
    # Modell mit 3 Qubits pro Eigenschaft initialisieren
    model = QuantumAppleModel(
        n_qubits_per_property=3,
        seed=42  # Für reproduzierbare Ergebnisse
    )
    
    # Modell-Informationen anzeigen
    model_info = model.get_model_info()
    logger.info(f"   - Qubits gesamt: {model_info['total_qubits']}")
    logger.info(f"   - Parameter gesamt: {model_info['total_parameters']}")
    logger.info(f"   - Qubit-Mapping: {model_info['qubit_mapping']}")
    
    # === 2. DATENGENERIERUNG ===
    logger.info("\n2. Generiere Trainingsdaten...")
    
    # Data Generator mit konfigurierbarem Rauschen
    data_gen = AppleDataGenerator(
        seed=42,
        noise_level=0.1  # 10% Rauschen für Realismus
    )
    
    # Verschiedene Datentypen generieren
    logger.info("   - Generiere realistische Daten...")
    freshness_values, targets = data_gen.generate_realistic_data(n_samples=40)
    
    # Daten aufteilen
    train_fresh, train_targets, test_fresh, test_targets = data_gen.split_data(
        freshness_values, targets, 
        train_ratio=0.8,
        stratify=True  # Gleichmäßige Verteilung über Frische-Bereiche
    )
    
    logger.info(f"   - Training: {len(train_fresh)} Samples")
    logger.info(f"   - Test: {len(test_fresh)} Samples")
    
    # Datenstatistiken berechnen
    data_stats = data_gen.get_statistics(freshness_values, targets)
    logger.info(f"   - Korrelation Frische↔Haltbarkeit: {data_stats['correlations']['freshness_durability']:.3f}")
    logger.info(f"   - Korrelation Frische↔Geschmack: {data_stats['correlations']['freshness_taste']:.3f}")
    
    # === 3. TRAINING ===
    logger.info("\n3. Trainiere das Modell...")
    
    # Training-Konfiguration
    config = TrainingConfig(
        epochs=30,
        learning_rate=0.15,
        batch_size=8,
        patience=15,
        adaptive_lr=True,
        verbose=True
    )
    
    # Trainer initialisieren
    trainer = QuantumTrainer(model, config)
    
    # Training mit Gradient Descent
    logger.info("   - Starte Gradient Descent Training...")
    training_metrics = trainer.train_gradient_descent(train_fresh, train_targets)
    
    logger.info(f"   - Training abgeschlossen nach {len(training_metrics.loss_history)} Epochen")
    logger.info(f"   - Beste Loss: {training_metrics.best_loss:.6f}")
    logger.info(f"   - Trainingszeit: {training_metrics.training_time:.2f}s")
    
    # === 4. EVALUATION ===
    logger.info("\n4. Evaluiere das trainierte Modell...")
    
    # Evaluation auf Testdaten
    test_results = trainer.evaluate(test_fresh, test_targets)
    
    logger.info("   Test-Ergebnisse:")
    logger.info(f"   - Test Loss: {test_results['test_loss']:.6f}")
    logger.info(f"   - MAE Haltbarkeit: {test_results['mae_durability']:.4f}")
    logger.info(f"   - MAE Geschmack: {test_results['mae_taste']:.4f}")
    logger.info(f"   - R² Haltbarkeit: {test_results['r2_durability']:.4f}")
    logger.info(f"   - R² Geschmack: {test_results['r2_taste']:.4f}")
    
    # === 5. VISUALISIERUNG ===
    logger.info("\n5. Erstelle Visualisierungen...")
    
    # Visualizer initialisieren
    visualizer = QuantumVisualizer()
    
    # Ausgabeordner erstellen
    output_dir = "../outputs/basic_usage"
    os.makedirs(output_dir, exist_ok=True)
    
    # Training-Verlauf visualisieren
    logger.info("   - Training-Verlauf...")
    trainer.plot_training_history(filename=f"{output_dir}/training_history.png")
    
    # Vorhersagen visualisieren
    logger.info("   - Vorhersage-Analyse...")
    trainer.plot_predictions(
        test_fresh, test_targets, test_results['predictions'],
        filename=f"{output_dir}/predictions.png"
    )
    
    # Systemarchitektur visualisieren
    logger.info("   - Systemarchitektur...")
    visualizer.visualize_system_architecture(
        filename=f"{output_dir}/architecture.png"
    )
    
    # 3D-Vorhersageraum
    logger.info("   - 3D-Vorhersageraum...")
    visualizer.visualize_3d_prediction_space(
        model, filename=f"{output_dir}/3d_predictions.png"
    )
    
    # === 6. INTERAKTIVE VORHERSAGEN ===
    logger.info("\n6. Teste interaktive Vorhersagen...")
    
    test_inputs = [1.5, 3.0, 5.0, 7.5, 9.0]
    
    print("\n" + "="*60)
    print("INTERAKTIVE VORHERSAGEN")
    print("="*60)
    print(f"{'Frische':<10} {'Haltbarkeit':<12} {'Geschmack':<10} {'Bewertung'}")
    print("-"*60)
    
    for freshness in test_inputs:
        durability, taste = model.predict(freshness)
        
        # Einfache Bewertung basierend auf Durchschnitt
        avg_score = (durability + taste) / 2
        if avg_score >= 7:
            rating = "Ausgezeichnet ⭐⭐⭐"
        elif avg_score >= 5:
            rating = "Gut ⭐⭐"
        else:
            rating = "Schlecht ⭐"
        
        print(f"{freshness:<10.1f} {durability:<12.2f} {taste:<10.2f} {rating}")
    
    print("="*60)
    
    # === 7. ZUSAMMENFASSUNG ===
    logger.info("\n7. Training-Zusammenfassung...")
    
    summary = trainer.get_training_summary()
    
    print(f"\nTRAINING-ZUSAMMENFASSUNG:")
    print(f"- Konfiguration: {summary['training_config']}")
    print(f"- Ergebnisse: Epochen={summary['training_results']['total_epochs']}, "
          f"Zeit={summary['training_results']['training_time']:.2f}s")
    print(f"- Performance: Beste Loss={summary['training_results']['best_loss']:.6f}")
    print(f"- Optimierung: Ø Gradient={summary['optimization_stats']['avg_gradient_norm']:.6f}")
    
    # === 8. ERFOLG ===
    logger.info("\n✅ Basic Usage Example erfolgreich abgeschlossen!")
    logger.info(f"📁 Alle Visualisierungen wurden in '{output_dir}/' gespeichert")
    logger.info("🚀 Das trainierte Modell ist einsatzbereit für weitere Experimente!")
    
    return model, trainer, test_results


if __name__ == "__main__":
    try:
        model, trainer, results = main()
        print(f"\n🎉 Beispiel erfolgreich beendet!")
        print(f"📊 Test-Performance: MAE(H)={results['mae_durability']:.3f}, MAE(G)={results['mae_taste']:.3f}")
        
    except Exception as e:
        logger.error(f"❌ Fehler im Basic Usage Example: {e}")
        raise