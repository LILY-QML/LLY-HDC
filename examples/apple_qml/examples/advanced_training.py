#!/usr/bin/env python3
"""
Advanced Training Example - Erweiterte Trainingsstrategien

Dieses Beispiel demonstriert fortgeschrittene Trainingskonzepte:
- Hyperparameter-Optimierung
- Verschiedene Optimizer-Vergleiche
- Cross-Validation
- Ensemble-Methoden
- Regularisierung und Overfitting-Vermeidung
"""

import sys
import os
import logging
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import time

# Pfad zum src-Verzeichnis hinzufügen
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_apple_model import QuantumAppleModel
from data_generator import AppleDataGenerator
from trainer import QuantumTrainer, TrainingConfig
from visualizer import QuantumVisualizer

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HyperparameterOptimizer:
    """
    Hyperparameter-Optimierung für das QML-System.
    """
    
    def __init__(self, param_grid: dict):
        self.param_grid = param_grid
        self.results = []
    
    def grid_search(self, train_data, validation_data, n_trials: int = 3):
        """
        Grid Search über alle Hyperparameter-Kombinationen.
        """
        logger.info("Starte Hyperparameter Grid Search...")
        
        # Alle Kombinationen generieren
        param_names = list(self.param_grid.keys())
        param_values = list(self.param_grid.values())
        combinations = list(product(*param_values))
        
        logger.info(f"Teste {len(combinations)} Hyperparameter-Kombinationen")
        
        for i, param_combo in enumerate(combinations):
            logger.info(f"Kombination {i+1}/{len(combinations)}: {dict(zip(param_names, param_combo))}")
            
            # Mehrere Trials für robuste Ergebnisse
            trial_scores = []
            
            for trial in range(n_trials):
                try:
                    # Neues Modell für jeden Trial
                    model = QuantumAppleModel(n_qubits_per_property=3, seed=42+trial)
                    
                    # Training-Config erstellen
                    config = TrainingConfig(
                        epochs=param_combo[0] if 'epochs' in param_names else 30,
                        learning_rate=param_combo[1] if 'learning_rate' in param_names else 0.1,
                        batch_size=param_combo[2] if 'batch_size' in param_names else 5,
                        adaptive_lr=param_combo[3] if 'adaptive_lr' in param_names else True,
                        verbose=False
                    )
                    
                    # Training
                    trainer = QuantumTrainer(model, config)
                    trainer.train_gradient_descent(*train_data)
                    
                    # Validation
                    val_results = trainer.evaluate(*validation_data)
                    trial_scores.append(val_results['test_loss'])
                    
                except Exception as e:
                    logger.warning(f"Trial {trial+1} fehlgeschlagen: {e}")
                    trial_scores.append(float('inf'))
            
            # Durchschnittlicher Score
            avg_score = np.mean(trial_scores)
            std_score = np.std(trial_scores)
            
            self.results.append({
                'params': dict(zip(param_names, param_combo)),
                'score': avg_score,
                'std': std_score,
                'trials': trial_scores
            })
            
            logger.info(f"   Score: {avg_score:.6f} ± {std_score:.6f}")
        
        # Beste Konfiguration
        best_result = min(self.results, key=lambda x: x['score'])
        logger.info(f"Beste Konfiguration: {best_result['params']}")
        logger.info(f"Beste Score: {best_result['score']:.6f}")
        
        return best_result


def compare_optimizers(train_data, test_data):
    """
    Vergleicht verschiedene Optimierungsverfahren.
    """
    logger.info("Vergleiche verschiedene Optimizer...")
    
    optimizers = [
        ('Gradient Descent', 'gradient_descent'),
        ('COBYLA', 'cobyla'),
        ('Nelder-Mead', 'nelder_mead'),
        ('Powell', 'powell')
    ]
    
    results = {}
    
    for name, method in optimizers:
        logger.info(f"Teste {name}...")
        
        # Neues Modell für fairen Vergleich
        model = QuantumAppleModel(n_qubits_per_property=3, seed=42)
        trainer = QuantumTrainer(model)
        
        start_time = time.time()
        
        try:
            if method == 'gradient_descent':
                config = TrainingConfig(epochs=25, learning_rate=0.15, verbose=False)
                trainer.config = config
                metrics = trainer.train_gradient_descent(*train_data)
            else:
                metrics = trainer.train_scipy_optimizer(*train_data, method=method.upper(), maxiter=50)
            
            training_time = time.time() - start_time
            
            # Test-Evaluation
            test_results = trainer.evaluate(*test_data)
            
            results[name] = {
                'final_loss': metrics.best_loss,
                'test_loss': test_results['test_loss'],
                'mae_durability': test_results['mae_durability'],
                'mae_taste': test_results['mae_taste'],
                'training_time': training_time,
                'iterations': len(metrics.loss_history),
                'converged': metrics.convergence_epoch is not None
            }
            
            logger.info(f"   {name}: Loss={test_results['test_loss']:.6f}, Zeit={training_time:.2f}s")
            
        except Exception as e:
            logger.warning(f"   {name} fehlgeschlagen: {e}")
            results[name] = {'error': str(e)}
    
    return results


def cross_validation(freshness_data, target_data, k_folds: int = 5):
    """
    K-Fold Cross-Validation für robuste Performance-Evaluation.
    """
    logger.info(f"Führe {k_folds}-Fold Cross-Validation durch...")
    
    n_samples = len(freshness_data)
    fold_size = n_samples // k_folds
    
    cv_scores = []
    fold_results = []
    
    for fold in range(k_folds):
        logger.info(f"Fold {fold+1}/{k_folds}")
        
        # Test-Indizes für aktuellen Fold
        test_start = fold * fold_size
        test_end = test_start + fold_size if fold < k_folds-1 else n_samples
        
        # Daten aufteilen
        test_indices = list(range(test_start, test_end))
        train_indices = [i for i in range(n_samples) if i not in test_indices]
        
        train_fresh = [freshness_data[i] for i in train_indices]
        train_targets = [target_data[i] for i in train_indices]
        test_fresh = [freshness_data[i] for i in test_indices]
        test_targets = [target_data[i] for i in test_indices]
        
        # Training
        model = QuantumAppleModel(n_qubits_per_property=3, seed=42+fold)
        config = TrainingConfig(epochs=20, learning_rate=0.15, verbose=False)
        trainer = QuantumTrainer(model, config)
        
        trainer.train_gradient_descent(train_fresh, train_targets)
        
        # Evaluation
        results = trainer.evaluate(test_fresh, test_targets)
        cv_scores.append(results['test_loss'])
        fold_results.append(results)
        
        logger.info(f"   Fold {fold+1} Loss: {results['test_loss']:.6f}")
    
    # Zusammenfassung
    mean_score = np.mean(cv_scores)
    std_score = np.std(cv_scores)
    
    logger.info(f"Cross-Validation Ergebnis: {mean_score:.6f} ± {std_score:.6f}")
    
    return {
        'mean_score': mean_score,
        'std_score': std_score,
        'fold_scores': cv_scores,
        'fold_results': fold_results
    }


class EnsembleModel:
    """
    Ensemble von mehreren QML-Modellen für verbesserte Performance.
    """
    
    def __init__(self, n_models: int = 5):
        self.n_models = n_models
        self.models = []
        self.trainers = []
    
    def train_ensemble(self, train_data):
        """
        Trainiert ein Ensemble von Modellen mit verschiedenen Initialisierungen.
        """
        logger.info(f"Trainiere Ensemble mit {self.n_models} Modellen...")
        
        for i in range(self.n_models):
            logger.info(f"Trainiere Modell {i+1}/{self.n_models}")
            
            # Verschiedene Seeds für Diversität
            model = QuantumAppleModel(n_qubits_per_property=3, seed=42+i*10)
            
            # Leicht verschiedene Hyperparameter
            lr = 0.1 + (i * 0.02)  # 0.1 bis 0.18
            config = TrainingConfig(
                epochs=25,
                learning_rate=lr,
                batch_size=5 + (i % 3),  # 5, 6, 7
                verbose=False
            )
            
            trainer = QuantumTrainer(model, config)
            trainer.train_gradient_descent(*train_data)
            
            self.models.append(model)
            self.trainers.append(trainer)
    
    def predict_ensemble(self, freshness: float):
        """
        Ensemble-Vorhersage durch Mittelung aller Modelle.
        """
        predictions = []
        
        for model in self.models:
            try:
                pred = model.predict(freshness)
                predictions.append(pred)
            except:
                continue
        
        if not predictions:
            return (5.0, 5.0)  # Fallback
        
        # Mittelwert aller Vorhersagen
        avg_durability = np.mean([p[0] for p in predictions])
        avg_taste = np.mean([p[1] for p in predictions])
        
        return (avg_durability, avg_taste)
    
    def evaluate_ensemble(self, test_data):
        """
        Evaluiert das Ensemble-Modell.
        """
        test_freshness, test_targets = test_data
        
        ensemble_predictions = []
        for freshness in test_freshness:
            pred = self.predict_ensemble(freshness)
            ensemble_predictions.append(pred)
        
        # Loss berechnen
        total_loss = 0
        for pred, target in zip(ensemble_predictions, test_targets):
            loss_dur = (pred[0] - target[0])**2
            loss_taste = (pred[1] - target[1])**2
            total_loss += loss_dur + loss_taste
        
        ensemble_loss = total_loss / len(test_targets)
        
        # MAE berechnen
        mae_dur = np.mean([abs(pred[0] - target[0]) 
                          for pred, target in zip(ensemble_predictions, test_targets)])
        mae_taste = np.mean([abs(pred[1] - target[1]) 
                            for pred, target in zip(ensemble_predictions, test_targets)])
        
        return {
            'ensemble_loss': ensemble_loss,
            'mae_durability': mae_dur,
            'mae_taste': mae_taste,
            'predictions': ensemble_predictions
        }


def main():
    """
    Hauptfunktion für Advanced Training Example.
    """
    logger.info("=== Advanced Training Example ===")
    
    # === 1. DATEN GENERIEREN ===
    logger.info("\n1. Generiere erweiterte Datensätze...")
    
    data_gen = AppleDataGenerator(seed=42, noise_level=0.15)
    
    # Größeres Dataset für robuste Evaluation
    freshness_data, target_data = data_gen.generate_realistic_data(n_samples=100)
    
    # Standard Train/Test Split
    train_fresh, train_targets, test_fresh, test_targets = data_gen.split_data(
        freshness_data, target_data, train_ratio=0.7
    )
    
    # Validation Set
    val_fresh, val_targets, test_fresh, test_targets = data_gen.split_data(
        test_fresh, test_targets, train_ratio=0.5
    )
    
    logger.info(f"   Training: {len(train_fresh)} Samples")
    logger.info(f"   Validation: {len(val_fresh)} Samples") 
    logger.info(f"   Test: {len(test_fresh)} Samples")
    
    # === 2. HYPERPARAMETER-OPTIMIERUNG ===
    logger.info("\n2. Hyperparameter-Optimierung...")
    
    param_grid = {
        'epochs': [20, 30, 40],
        'learning_rate': [0.1, 0.15, 0.2],
        'batch_size': [4, 6, 8],
        'adaptive_lr': [True, False]
    }
    
    optimizer = HyperparameterOptimizer(param_grid)
    best_config = optimizer.grid_search(
        (train_fresh, train_targets),
        (val_fresh, val_targets),
        n_trials=2  # Reduziert für Demo
    )
    
    # === 3. OPTIMIZER-VERGLEICH ===
    logger.info("\n3. Optimizer-Vergleich...")
    
    optimizer_results = compare_optimizers(
        (train_fresh, train_targets),
        (test_fresh, test_targets)
    )
    
    # Ergebnisse anzeigen
    print("\nOPTIMIZER-VERGLEICH:")
    print("-" * 80)
    print(f"{'Optimizer':<15} {'Test Loss':<12} {'MAE(H)':<10} {'MAE(G)':<10} {'Zeit(s)':<10}")
    print("-" * 80)
    
    for name, results in optimizer_results.items():
        if 'error' not in results:
            print(f"{name:<15} {results['test_loss']:<12.6f} "
                  f"{results['mae_durability']:<10.4f} {results['mae_taste']:<10.4f} "
                  f"{results['training_time']:<10.2f}")
    
    # === 4. CROSS-VALIDATION ===
    logger.info("\n4. Cross-Validation...")
    
    cv_results = cross_validation(freshness_data, target_data, k_folds=5)
    
    # === 5. ENSEMBLE-MODELL ===
    logger.info("\n5. Ensemble-Modell...")
    
    ensemble = EnsembleModel(n_models=3)  # Kleiner für Demo
    ensemble.train_ensemble((train_fresh, train_targets))
    
    ensemble_results = ensemble.evaluate_ensemble((test_fresh, test_targets))
    
    logger.info(f"Ensemble Performance:")
    logger.info(f"   Loss: {ensemble_results['ensemble_loss']:.6f}")
    logger.info(f"   MAE Haltbarkeit: {ensemble_results['mae_durability']:.4f}")
    logger.info(f"   MAE Geschmack: {ensemble_results['mae_taste']:.4f}")
    
    # === 6. VISUALISIERUNG ===
    logger.info("\n6. Erstelle erweiterte Visualisierungen...")
    
    output_dir = "../outputs/advanced_training"
    os.makedirs(output_dir, exist_ok=True)
    
    # Hyperparameter-Heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Grid Search Ergebnisse visualisieren
    if optimizer.results:
        scores = [r['score'] for r in optimizer.results]
        param_labels = [str(r['params']) for r in optimizer.results]
        
        ax.barh(range(len(scores)), scores)
        ax.set_yticks(range(len(scores)))
        ax.set_yticklabels([f"Config {i+1}" for i in range(len(scores))])
        ax.set_xlabel('Validation Loss')
        ax.set_title('Hyperparameter Grid Search Ergebnisse')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/hyperparameter_search.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    # Cross-Validation Boxplot
    if cv_results['fold_scores']:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.boxplot([cv_results['fold_scores']], labels=['CV Scores'])
        ax.set_ylabel('Test Loss')
        ax.set_title('Cross-Validation Score Distribution')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/cross_validation.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    # === 7. ZUSAMMENFASSUNG ===
    logger.info("\n7. Zusammenfassung der erweiterten Trainingsmethoden...")
    
    print("\n" + "="*80)
    print("ERWEITERTE TRAININGS-ZUSAMMENFASSUNG")
    print("="*80)
    
    print(f"\n📊 Hyperparameter-Optimierung:")
    print(f"   Beste Konfiguration: {best_config['params']}")
    print(f"   Beste Validation Loss: {best_config['score']:.6f}")
    
    print(f"\n🔄 Cross-Validation:")
    print(f"   Durchschnittliche Loss: {cv_results['mean_score']:.6f} ± {cv_results['std_score']:.6f}")
    
    print(f"\n🎯 Ensemble-Modell:")
    print(f"   Ensemble Loss: {ensemble_results['ensemble_loss']:.6f}")
    print(f"   Verbesserung ggü. Einzelmodell: {cv_results['mean_score'] - ensemble_results['ensemble_loss']:.6f}")
    
    best_single_optimizer = min(optimizer_results.items(), 
                               key=lambda x: x[1].get('test_loss', float('inf')))
    print(f"\n🏆 Bester Einzeloptimizer: {best_single_optimizer[0]}")
    print(f"   Test Loss: {best_single_optimizer[1]['test_loss']:.6f}")
    
    logger.info("\n✅ Advanced Training Example erfolgreich abgeschlossen!")
    logger.info(f"📁 Visualisierungen wurden in '{output_dir}/' gespeichert")
    
    return {
        'best_hyperparams': best_config,
        'optimizer_comparison': optimizer_results,
        'cross_validation': cv_results,
        'ensemble_results': ensemble_results
    }


if __name__ == "__main__":
    try:
        results = main()
        print("\n🎉 Advanced Training erfolgreich abgeschlossen!")
        
    except Exception as e:
        logger.error(f"❌ Fehler im Advanced Training: {e}")
        raise