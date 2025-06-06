"""
Quantum Trainer - Training und Optimierung für das Apfel QML-System

Dieses Modul implementiert verschiedene Trainingsstrategien für das
parametrisierte Quantenschaltkreis-Modell. Es bietet sowohl gradientenbasierte
als auch gradientenfreie Optimierungsverfahren.

Hauptfunktionalitäten:
- Gradient Descent mit finite differences
- Scipy-basierte Optimizer (COBYLA, SPSA)
- Adaptive Learning Rate Strategien
- Umfassende Evaluation und Metriken
- Trainings-Monitoring und Visualisierung
"""

import numpy as np
from typing import List, Tuple, Dict, Optional, Callable, Union
import logging
from dataclasses import dataclass, field
import time
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from qiskit.circuit import Parameter

# Logging konfigurieren
logger = logging.getLogger(__name__)


@dataclass
class TrainingConfig:
    """
    Konfiguration für Training-Parameter.
    
    Attributes:
        epochs: Anzahl Trainings-Epochen
        learning_rate: Initiale Lernrate
        batch_size: Größe der Mini-Batches
        patience: Early Stopping Geduld
        min_delta: Minimale Verbesserung für Early Stopping
        adaptive_lr: Ob adaptive Lernrate verwendet werden soll
        lr_decay: Lernraten-Abfall-Faktor
        gradient_clipping: Maximaler Gradient für Clipping
    """
    epochs: int = 50
    learning_rate: float = 0.1
    batch_size: int = 5
    patience: int = 10
    min_delta: float = 1e-6
    adaptive_lr: bool = True
    lr_decay: float = 0.95
    gradient_clipping: Optional[float] = None
    verbose: bool = True


@dataclass
class TrainingMetrics:
    """
    Metriken für Training-Monitoring.
    
    Attributes:
        loss_history: Verlauf der Loss-Werte
        learning_rates: Verlauf der Lernraten
        gradient_norms: Verlauf der Gradient-Normen
        training_time: Gesamte Trainingszeit
        convergence_epoch: Epoche der Konvergenz
        best_loss: Beste erreichte Loss
        best_params: Parameter bei bester Loss
    """
    loss_history: List[float] = field(default_factory=list)
    learning_rates: List[float] = field(default_factory=list)
    gradient_norms: List[float] = field(default_factory=list)
    training_time: float = 0.0
    convergence_epoch: Optional[int] = None
    best_loss: float = float('inf')
    best_params: Optional[Dict] = None


class QuantumTrainer:
    """
    Trainer für das Quantum Apple Model.
    
    Diese Klasse implementiert verschiedene Optimierungsstrategien für
    das parametrisierte Quantenschaltkreis-Modell. Sie bietet sowohl
    einfache gradientenbasierte Verfahren als auch fortgeschrittene
    scipy-basierte Optimizer.
    
    Attributes:
        model: Das zu trainierende QuantumAppleModel
        config: Training-Konfiguration
        metrics: Training-Metriken und Verlauf
        optimizer_state: Zustand des Optimizers
    """
    
    def __init__(self, model, config: Optional[TrainingConfig] = None):
        """
        Initialisiert den Quantum Trainer.
        
        Args:
            model: QuantumAppleModel Instanz zum Trainieren
            config: Training-Konfiguration (falls None, wird Standard verwendet)
        """
        self.model = model
        self.config = config or TrainingConfig()
        self.metrics = TrainingMetrics()
        self.optimizer_state = {}
        
        logger.info(f"QuantumTrainer initialisiert mit {len(model.param_values)} Parametern")
        logger.info(f"Training Config: Epochen={self.config.epochs}, "
                   f"LR={self.config.learning_rate}, Batch={self.config.batch_size}")
    
    def compute_gradients(self, freshness_batch: List[float], 
                         targets_batch: List[Tuple[float, float]], 
                         epsilon: float = 0.01) -> Dict[Parameter, float]:
        """
        Berechnet numerische Gradienten mittels Finite Differences.
        
        Diese Methode implementiert die Parameter-Shift-Regel für
        parametrisierte Quantenschaltkreise. Für jeden Parameter wird
        der Gradient durch zentrale Differenzen approximiert.
        
        Args:
            freshness_batch: Batch von Frische-Werten
            targets_batch: Batch von Ziel-Werten
            epsilon: Schrittgröße für finite differences
            
        Returns:
            Dict: Parameter → Gradient Zuordnung
        """
        gradients = {}
        
        # Basis-Loss für Referenz berechnen
        base_loss = self._evaluate_batch(freshness_batch, targets_batch)
        
        logger.debug(f"Berechne Gradienten für {len(self.model.param_values)} Parameter")
        
        # Für jeden Parameter den Gradienten berechnen
        for param in self.model.param_values.keys():
            # Ursprünglichen Wert speichern
            original_value = self.model.param_values[param]
            
            # Vorwärts-Schritt: Parameter um epsilon erhöhen
            self.model.param_values[param] = original_value + epsilon
            loss_plus = self._evaluate_batch(freshness_batch, targets_batch)
            
            # Rückwärts-Schritt: Parameter um epsilon verringern
            self.model.param_values[param] = original_value - epsilon  
            loss_minus = self._evaluate_batch(freshness_batch, targets_batch)
            
            # Zentrale Differenz berechnen
            gradient = (loss_plus - loss_minus) / (2 * epsilon)
            gradients[param] = gradient
            
            # Parameter zurücksetzen
            self.model.param_values[param] = original_value
            
            logger.debug(f"Gradient {param}: {gradient:.6f}")
        
        # Gradient-Norm für Monitoring berechnen
        gradient_norm = np.sqrt(sum(g**2 for g in gradients.values()))
        self.metrics.gradient_norms.append(gradient_norm)
        
        logger.debug(f"Gradient-Norm: {gradient_norm:.6f}")
        
        return gradients
    
    def _evaluate_batch(self, freshness_batch: List[float], 
                       targets_batch: List[Tuple[float, float]]) -> float:
        """
        Evaluiert die Loss-Funktion für einen Batch.
        
        Args:
            freshness_batch: Batch von Frische-Werten
            targets_batch: Batch von Ziel-Werten
            
        Returns:
            float: Durchschnittliche Loss für den Batch
        """
        predictions = []
        
        # Vorhersagen für alle Samples im Batch
        for freshness in freshness_batch:
            try:
                pred = self.model.predict(freshness)
                predictions.append(pred)
            except Exception as e:
                logger.warning(f"Vorhersage-Fehler für Frische {freshness}: {e}")
                # Fallback-Vorhersage
                predictions.append((5.0, 5.0))
        
        # Loss berechnen
        loss = self.model.compute_loss(predictions, targets_batch)
        return loss
    
    def _apply_gradient_clipping(self, gradients: Dict[Parameter, float]) -> Dict[Parameter, float]:
        """
        Wendet Gradient Clipping an, falls konfiguriert.
        
        Args:
            gradients: Ursprüngliche Gradienten
            
        Returns:
            Dict: Geclippte Gradienten
        """
        if self.config.gradient_clipping is None:
            return gradients
        
        # Gradient-Norm berechnen
        gradient_norm = np.sqrt(sum(g**2 for g in gradients.values()))
        
        if gradient_norm > self.config.gradient_clipping:
            # Gradienten skalieren
            scale_factor = self.config.gradient_clipping / gradient_norm
            clipped_gradients = {
                param: grad * scale_factor 
                for param, grad in gradients.items()
            }
            
            logger.debug(f"Gradienten geclippt: Norm {gradient_norm:.6f} "
                        f"→ {self.config.gradient_clipping}")
            
            return clipped_gradients
        
        return gradients
    
    def _update_learning_rate(self, epoch: int, current_loss: float) -> float:
        """
        Aktualisiert die Lernrate basierend auf Training-Verlauf.
        
        Args:
            epoch: Aktuelle Epoche
            current_loss: Aktuelle Loss
            
        Returns:
            float: Neue Lernrate
        """
        if not self.config.adaptive_lr:
            return self.config.learning_rate
        
        # Exponentieller Abfall
        new_lr = self.config.learning_rate * (self.config.lr_decay ** epoch)
        
        # Plateau-Detection: Falls Loss nicht sinkt, Lernrate reduzieren
        if len(self.metrics.loss_history) > 5:
            recent_losses = self.metrics.loss_history[-5:]
            if all(abs(loss - current_loss) < self.config.min_delta for loss in recent_losses):
                new_lr *= 0.5
                logger.info(f"Plateau erkannt, Lernrate reduziert auf {new_lr:.6f}")
        
        return new_lr
    
    def _check_early_stopping(self, current_loss: float, epoch: int) -> bool:
        """
        Prüft Early Stopping Kriterien.
        
        Args:
            current_loss: Aktuelle Loss
            epoch: Aktuelle Epoche
            
        Returns:
            bool: True falls Training gestoppt werden soll
        """
        # Update beste Loss
        if current_loss < self.metrics.best_loss:
            self.metrics.best_loss = current_loss
            self.metrics.best_params = self.model.param_values.copy()
            self.metrics.convergence_epoch = epoch
            self.optimizer_state['patience_counter'] = 0
        else:
            self.optimizer_state['patience_counter'] = self.optimizer_state.get('patience_counter', 0) + 1
        
        # Early Stopping Check
        if self.optimizer_state['patience_counter'] >= self.config.patience:
            logger.info(f"Early Stopping bei Epoche {epoch} "
                       f"(Geduld: {self.config.patience})")
            return True
        
        return False
    
    def train_gradient_descent(self, train_freshness: List[float], 
                              train_targets: List[Tuple[float, float]]) -> TrainingMetrics:
        """
        Trainiert das Modell mit Gradient Descent.
        
        Diese Methode implementiert Mini-Batch Gradient Descent mit
        verschiedenen Verbesserungen wie adaptive Lernrate, Gradient
        Clipping und Early Stopping.
        
        Args:
            train_freshness: Trainings-Frische-Werte
            train_targets: Trainings-Ziel-Werte
            
        Returns:
            TrainingMetrics: Umfassende Training-Metriken
        """
        logger.info(f"Starte Gradient Descent Training mit {len(train_freshness)} Samples")
        
        # Training-Timer starten
        start_time = time.time()
        
        # Optimizer-State initialisieren
        self.optimizer_state = {'patience_counter': 0}
        
        n_samples = len(train_freshness)
        current_lr = self.config.learning_rate
        
        for epoch in range(self.config.epochs):
            epoch_start_time = time.time()
            epoch_loss = 0.0
            n_batches = 0
            
            # Mini-Batches erstellen
            for i in range(0, n_samples, self.config.batch_size):
                batch_freshness = train_freshness[i:i+self.config.batch_size]
                batch_targets = train_targets[i:i+self.config.batch_size]
                
                # Gradienten berechnen
                gradients = self.compute_gradients(batch_freshness, batch_targets)
                
                # Gradient Clipping anwenden
                gradients = self._apply_gradient_clipping(gradients)
                
                # Parameter aktualisieren
                self.model.update_parameters(gradients, current_lr)
                
                # Batch-Loss für Monitoring
                batch_loss = self._evaluate_batch(batch_freshness, batch_targets)
                epoch_loss += batch_loss
                n_batches += 1
            
            # Durchschnittliche Epoche-Loss
            avg_epoch_loss = epoch_loss / n_batches if n_batches > 0 else epoch_loss
            self.metrics.loss_history.append(avg_epoch_loss)
            
            # Lernrate aktualisieren
            current_lr = self._update_learning_rate(epoch, avg_epoch_loss)
            self.metrics.learning_rates.append(current_lr)
            
            # Logging
            epoch_time = time.time() - epoch_start_time
            if self.config.verbose and epoch % 10 == 0:
                logger.info(f"Epoche {epoch}: Loss={avg_epoch_loss:.6f}, "
                           f"LR={current_lr:.6f}, Zeit={epoch_time:.2f}s")
            
            # Early Stopping Check
            if self._check_early_stopping(avg_epoch_loss, epoch):
                break
        
        # Training abschließen
        self.metrics.training_time = time.time() - start_time
        
        # Beste Parameter laden
        if self.metrics.best_params:
            self.model.param_values = self.metrics.best_params.copy()
        
        logger.info(f"Training abgeschlossen nach {len(self.metrics.loss_history)} Epochen")
        logger.info(f"Beste Loss: {self.metrics.best_loss:.6f}")
        logger.info(f"Trainingszeit: {self.metrics.training_time:.2f}s")
        
        return self.metrics
    
    def train_scipy_optimizer(self, train_freshness: List[float], 
                             train_targets: List[Tuple[float, float]],
                             method: str = 'COBYLA',
                             maxiter: int = 100) -> TrainingMetrics:
        """
        Trainiert das Modell mit scipy-basierten Optimizern.
        
        Diese Methode nutzt fortgeschrittene Optimizer aus scipy.optimize
        für gradientenfreie Optimierung. Besonders geeignet für noisy
        Objective Functions wie bei Quantenschaltkreisen.
        
        Args:
            train_freshness: Trainings-Frische-Werte  
            train_targets: Trainings-Ziel-Werte
            method: Optimierungsverfahren ('COBYLA', 'Nelder-Mead', 'Powell')
            maxiter: Maximale Anzahl Iterationen
            
        Returns:
            TrainingMetrics: Training-Metriken
        """
        logger.info(f"Starte {method} Optimierung mit {maxiter} max. Iterationen")
        
        start_time = time.time()
        
        # Parameter als Array für scipy
        param_keys = list(self.model.param_values.keys())
        initial_params = np.array([self.model.param_values[key] for key in param_keys])
        
        # Iteration Counter
        self.optimizer_state = {'iteration': 0}
        
        def objective_function(params_array: np.ndarray) -> float:
            """
            Objective Function für scipy Optimizer.
            
            Args:
                params_array: Parameter als NumPy Array
                
            Returns:
                float: Loss-Wert
            """
            # Parameter ins Model laden
            for i, key in enumerate(param_keys):
                self.model.param_values[key] = params_array[i]
            
            # Loss berechnen
            loss = self._evaluate_batch(train_freshness, train_targets)
            
            # Metrics aktualisieren
            self.metrics.loss_history.append(loss)
            self.optimizer_state['iteration'] += 1
            
            # Update beste Parameter
            if loss < self.metrics.best_loss:
                self.metrics.best_loss = loss
                self.metrics.best_params = self.model.param_values.copy()
                self.metrics.convergence_epoch = self.optimizer_state['iteration']
            
            # Logging
            if self.config.verbose and self.optimizer_state['iteration'] % 10 == 0:
                logger.info(f"Iteration {self.optimizer_state['iteration']}: "
                           f"Loss={loss:.6f}")
            
            return loss
        
        # Constraints für parameter bounds (0 bis 2π)
        bounds = [(0, 2*np.pi) for _ in param_keys] if method in ['L-BFGS-B', 'TNC'] else None
        
        try:
            # Optimierung ausführen
            result = minimize(
                objective_function,
                initial_params,
                method=method,
                bounds=bounds,
                options={'maxiter': maxiter}
            )
            
            # Ergebnisse verarbeiten
            if result.success:
                # Finale Parameter setzen
                for i, key in enumerate(param_keys):
                    self.model.param_values[key] = result.x[i]
                
                self.metrics.best_params = self.model.param_values.copy()
                self.metrics.best_loss = result.fun
                
                logger.info(f"{method} Optimierung erfolgreich abgeschlossen")
                logger.info(f"Finale Loss: {result.fun:.6f}")
                logger.info(f"Iterationen: {result.nit}")
                
            else:
                logger.warning(f"{method} Optimierung fehlgeschlagen: {result.message}")
                
        except Exception as e:
            logger.error(f"Fehler bei {method} Optimierung: {e}")
        
        # Training abschließen
        self.metrics.training_time = time.time() - start_time
        
        logger.info(f"Scipy Optimierung abgeschlossen nach "
                   f"{self.metrics.training_time:.2f}s")
        
        return self.metrics
    
    def evaluate(self, test_freshness: List[float], 
                test_targets: List[Tuple[float, float]]) -> Dict:
        """
        Evaluiert das trainierte Modell auf Testdaten.
        
        Args:
            test_freshness: Test-Frische-Werte
            test_targets: Test-Ziel-Werte
            
        Returns:
            Dict: Umfassende Evaluation-Metriken
        """
        logger.info(f"Evaluiere Modell auf {len(test_freshness)} Test-Samples")
        
        # Beste Parameter laden falls verfügbar
        if self.metrics.best_params:
            self.model.param_values = self.metrics.best_params.copy()
        
        # Vorhersagen erstellen
        predictions = []
        for freshness in test_freshness:
            try:
                pred = self.model.predict(freshness)
                predictions.append(pred)
            except Exception as e:
                logger.warning(f"Vorhersage-Fehler für Test-Sample {freshness}: {e}")
                predictions.append((5.0, 5.0))  # Fallback
        
        # Metriken berechnen
        test_loss = self.model.compute_loss(predictions, test_targets)
        
        # Mean Absolute Error für jede Eigenschaft
        mae_durability = np.mean([
            abs(pred[0] - target[0]) 
            for pred, target in zip(predictions, test_targets)
        ])
        
        mae_taste = np.mean([
            abs(pred[1] - target[1]) 
            for pred, target in zip(predictions, test_targets)
        ])
        
        # Root Mean Square Error
        rmse_durability = np.sqrt(np.mean([
            (pred[0] - target[0])**2 
            for pred, target in zip(predictions, test_targets)
        ]))
        
        rmse_taste = np.sqrt(np.mean([
            (pred[1] - target[1])**2 
            for pred, target in zip(predictions, test_targets)
        ]))
        
        # R² Score approximation
        def r2_score(y_true: List[float], y_pred: List[float]) -> float:
            y_true_mean = np.mean(y_true)
            ss_tot = sum((y - y_true_mean)**2 for y in y_true)
            ss_res = sum((y_true[i] - y_pred[i])**2 for i in range(len(y_true)))
            return 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        
        true_durability = [t[0] for t in test_targets]
        pred_durability = [p[0] for p in predictions]
        true_taste = [t[1] for t in test_targets]
        pred_taste = [p[1] for p in predictions]
        
        r2_durability = r2_score(true_durability, pred_durability)
        r2_taste = r2_score(true_taste, pred_taste)
        
        evaluation_results = {
            'test_loss': test_loss,
            'mae_durability': mae_durability,
            'mae_taste': mae_taste,
            'rmse_durability': rmse_durability,
            'rmse_taste': rmse_taste,
            'r2_durability': r2_durability,
            'r2_taste': r2_taste,
            'predictions': predictions,
            'n_test_samples': len(test_freshness)
        }
        
        # Logging der Ergebnisse
        logger.info("Evaluation-Ergebnisse:")
        logger.info(f"  Test Loss: {test_loss:.6f}")
        logger.info(f"  MAE Haltbarkeit: {mae_durability:.4f}")
        logger.info(f"  MAE Geschmack: {mae_taste:.4f}")
        logger.info(f"  RMSE Haltbarkeit: {rmse_durability:.4f}")
        logger.info(f"  RMSE Geschmack: {rmse_taste:.4f}")
        logger.info(f"  R² Haltbarkeit: {r2_durability:.4f}")
        logger.info(f"  R² Geschmack: {r2_taste:.4f}")
        
        return evaluation_results
    
    def plot_training_history(self, filename: Optional[str] = None, 
                             figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Visualisiert den detaillierten Trainingsverlauf.
        
        Args:
            filename: Dateiname zum Speichern (optional)
            figsize: Größe der Figure
            
        Returns:
            plt.Figure: Matplotlib Figure
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Training Verlauf - Detailanalyse', fontsize=16, fontweight='bold')
        
        # 1. Loss Verlauf
        ax1 = axes[0, 0]
        if self.metrics.loss_history:
            ax1.plot(self.metrics.loss_history, linewidth=2, color='darkblue')
            ax1.axhline(y=self.metrics.best_loss, color='red', linestyle='--', 
                       label=f'Beste Loss: {self.metrics.best_loss:.4f}')
            ax1.set_xlabel('Iteration')
            ax1.set_ylabel('Loss')
            ax1.set_title('Loss Verlauf')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.set_yscale('log')
        
        # 2. Learning Rate Verlauf
        ax2 = axes[0, 1]
        if self.metrics.learning_rates:
            ax2.plot(self.metrics.learning_rates, linewidth=2, color='green')
            ax2.set_xlabel('Iteration')
            ax2.set_ylabel('Learning Rate')
            ax2.set_title('Learning Rate Anpassung')
            ax2.grid(True, alpha=0.3)
            ax2.set_yscale('log')
        
        # 3. Gradient Normen
        ax3 = axes[1, 0]
        if self.metrics.gradient_norms:
            ax3.plot(self.metrics.gradient_norms, linewidth=2, color='orange')
            ax3.set_xlabel('Iteration')
            ax3.set_ylabel('Gradient Norm')
            ax3.set_title('Gradient Magnitude')
            ax3.grid(True, alpha=0.3)
            ax3.set_yscale('log')
        
        # 4. Konvergenz-Analyse
        ax4 = axes[1, 1]
        if len(self.metrics.loss_history) > 10:
            # Gleitender Durchschnitt
            window_size = min(10, len(self.metrics.loss_history) // 4)
            moving_avg = np.convolve(self.metrics.loss_history, 
                                   np.ones(window_size)/window_size, 
                                   mode='valid')
            
            ax4.plot(self.metrics.loss_history, alpha=0.3, label='Raw Loss')
            ax4.plot(range(window_size-1, len(self.metrics.loss_history)), 
                    moving_avg, linewidth=2, label=f'MA({window_size})')
            
            if self.metrics.convergence_epoch:
                ax4.axvline(x=self.metrics.convergence_epoch, color='red', 
                           linestyle=':', label=f'Konvergenz @ {self.metrics.convergence_epoch}')
            
            ax4.set_xlabel('Iteration')
            ax4.set_ylabel('Loss')
            ax4.set_title('Konvergenz-Analyse')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            logger.info(f"Training-Verlauf gespeichert als {filename}")
        
        return fig
    
    def plot_predictions(self, test_freshness: List[float], 
                        test_targets: List[Tuple[float, float]],
                        predictions: List[Tuple[float, float]],
                        filename: Optional[str] = None) -> plt.Figure:
        """
        Visualisiert Vorhersagen vs. Zielwerte mit detaillierter Analyse.
        
        Args:
            test_freshness: Test-Frische-Werte
            test_targets: Test-Ziel-Werte  
            predictions: Modell-Vorhersagen
            filename: Dateiname zum Speichern (optional)
            
        Returns:
            plt.Figure: Matplotlib Figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Vorhersage-Analyse', fontsize=16, fontweight='bold')
        
        # Daten extrahieren
        target_durability = [t[0] for t in test_targets]
        pred_durability = [p[0] for p in predictions]
        target_taste = [t[1] for t in test_targets]
        pred_taste = [p[1] for p in predictions]
        
        # 1. Haltbarkeit: Vorhersage vs. Target
        ax1 = axes[0, 0]
        ax1.scatter(test_freshness, target_durability, label='Ziel', alpha=0.7, s=80, c='blue')
        ax1.scatter(test_freshness, pred_durability, label='Vorhersage', alpha=0.7, s=100, 
                   c='red', marker='x')
        
        # Verbindungslinien für bessere Visualisierung
        for i in range(len(test_freshness)):
            ax1.plot([test_freshness[i], test_freshness[i]], 
                    [target_durability[i], pred_durability[i]], 
                    'k-', alpha=0.3, linewidth=1)
        
        ax1.set_xlabel('Frische')
        ax1.set_ylabel('Haltbarkeit')
        ax1.set_title('Haltbarkeit: Ziel vs. Vorhersage')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, 11)
        ax1.set_ylim(0, 11)
        
        # 2. Geschmack: Vorhersage vs. Target
        ax2 = axes[0, 1]
        ax2.scatter(test_freshness, target_taste, label='Ziel', alpha=0.7, s=80, c='blue')
        ax2.scatter(test_freshness, pred_taste, label='Vorhersage', alpha=0.7, s=100, 
                   c='red', marker='x')
        
        for i in range(len(test_freshness)):
            ax2.plot([test_freshness[i], test_freshness[i]], 
                    [target_taste[i], pred_taste[i]], 
                    'k-', alpha=0.3, linewidth=1)
        
        ax2.set_xlabel('Frische')
        ax2.set_ylabel('Geschmack')
        ax2.set_title('Geschmack: Ziel vs. Vorhersage')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 11)
        ax2.set_ylim(0, 11)
        
        # 3. Haltbarkeit: Scatter Plot (Ideal vs. Predicted)
        ax3 = axes[1, 0]
        ax3.scatter(target_durability, pred_durability, alpha=0.7, s=80)
        
        # Ideale Linie (perfekte Vorhersage)
        min_val, max_val = 1, 10
        ax3.plot([min_val, max_val], [min_val, max_val], 'r--', 
                linewidth=2, label='Perfekte Vorhersage')
        
        ax3.set_xlabel('Ziel Haltbarkeit')
        ax3.set_ylabel('Vorhergesagte Haltbarkeit')
        ax3.set_title('Haltbarkeit: Ideal vs. Predicted')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(1, 10)
        ax3.set_ylim(1, 10)
        
        # 4. Geschmack: Scatter Plot (Ideal vs. Predicted)
        ax4 = axes[1, 1]
        ax4.scatter(target_taste, pred_taste, alpha=0.7, s=80)
        ax4.plot([min_val, max_val], [min_val, max_val], 'r--', 
                linewidth=2, label='Perfekte Vorhersage')
        
        ax4.set_xlabel('Ziel Geschmack')
        ax4.set_ylabel('Vorhergesagter Geschmack')
        ax4.set_title('Geschmack: Ideal vs. Predicted')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_xlim(1, 10)
        ax4.set_ylim(1, 10)
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            logger.info(f"Vorhersage-Analyse gespeichert als {filename}")
        
        return fig
    
    def get_training_summary(self) -> Dict:
        """
        Erstellt eine umfassende Zusammenfassung des Trainings.
        
        Returns:
            Dict: Training-Zusammenfassung mit allen relevanten Metriken
        """
        summary = {
            'training_config': {
                'epochs': self.config.epochs,
                'learning_rate': self.config.learning_rate,
                'batch_size': self.config.batch_size,
                'adaptive_lr': self.config.adaptive_lr
            },
            'training_results': {
                'total_epochs': len(self.metrics.loss_history),
                'training_time': self.metrics.training_time,
                'convergence_epoch': self.metrics.convergence_epoch,
                'final_loss': self.metrics.loss_history[-1] if self.metrics.loss_history else None,
                'best_loss': self.metrics.best_loss,
                'loss_improvement': (
                    self.metrics.loss_history[0] - self.metrics.best_loss 
                    if self.metrics.loss_history else 0
                ),
                'converged': self.metrics.convergence_epoch is not None
            },
            'optimization_stats': {
                'avg_gradient_norm': np.mean(self.metrics.gradient_norms) if self.metrics.gradient_norms else 0,
                'final_gradient_norm': self.metrics.gradient_norms[-1] if self.metrics.gradient_norms else 0,
                'avg_learning_rate': np.mean(self.metrics.learning_rates) if self.metrics.learning_rates else 0,
                'parameter_count': len(self.model.param_values)
            }
        }
        
        return summary