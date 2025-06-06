"""
Apple Data Generator - Synthetische Datenerzeugung für QML-Training

Dieses Modul stellt verschiedene Methoden zur Erzeugung synthetischer
Trainingsdaten für das Apfel QML-System bereit. Es implementiert realistische
Beziehungen zwischen Frische, Haltbarkeit und Geschmack.

Die Klasse bietet verschiedene Datentypen:
- Lineare Beziehungen für einfache Tests
- Nichtlineare komplexe Beziehungen  
- Realistische Daten mit Rauschen und physikalischen Constraints
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
import logging
import matplotlib.pyplot as plt
from dataclasses import dataclass

# Logging konfigurieren
logger = logging.getLogger(__name__)


@dataclass
class AppleDataSample:
    """
    Datenstruktur für einen einzelnen Apfel-Datenpunkt.
    
    Attributes:
        freshness: Frische-Wert (1-10)
        durability: Haltbarkeits-Wert (1-10)  
        taste: Geschmacks-Wert (1-10)
        metadata: Zusätzliche Informationen (optional)
    """
    freshness: float
    durability: float
    taste: float
    metadata: Optional[Dict] = None


class AppleDataGenerator:
    """
    Generator für synthetische Apfel-Trainingsdaten.
    
    Diese Klasse implementiert verschiedene Strategien zur Erzeugung
    realistischer Trainingsdaten für das QML-System. Die Daten folgen
    physikalisch plausiblen Beziehungen zwischen den Apfel-Eigenschaften.
    
    Attributes:
        seed: Zufallsseed für Reproduzierbarkeit
        noise_level: Globales Rausch-Level (0.0 - 1.0)
        data_history: Historie aller erzeugten Datensätze
    """
    
    def __init__(self, seed: Optional[int] = None, noise_level: float = 0.1):
        """
        Initialisiert den Data Generator.
        
        Args:
            seed: Zufallsseed für reproduzierbare Ergebnisse
            noise_level: Globales Rausch-Level (0.0 = kein Rauschen, 1.0 = viel Rauschen)
        """
        self.seed = seed
        self.noise_level = max(0.0, min(1.0, noise_level))  # Clamp zwischen 0 und 1
        self.data_history = []
        
        if seed is not None:
            np.random.seed(seed)
            
        logger.info(f"AppleDataGenerator initialisiert mit Seed={seed}, "
                   f"Noise Level={noise_level}")
    
    def generate_simple_linear_data(self, n_samples: int = 10) -> Tuple[List[float], List[Tuple[float, float]]]:
        """
        Erzeugt einfache lineare Trainingsdaten für Basistests.
        
        Diese Methode erstellt Daten mit klaren linearen Beziehungen:
        - Haltbarkeit = 0.8 * Frische + 1.0  
        - Geschmack = 0.9 * Frische + 0.5
        
        Ideal für erste Tests und Debugging des Modells.
        
        Args:
            n_samples: Anzahl zu erzeugender Datenpunkte
            
        Returns:
            Tuple: (freshness_values, targets) wobei targets = [(durability, taste), ...]
        """
        logger.info(f"Generiere {n_samples} einfache lineare Datenpunkte")
        
        freshness_values = []
        targets = []
        
        # Gleichmäßig verteilte Frische-Werte über den gesamten Bereich
        for i in range(n_samples):
            if n_samples == 1:
                freshness = 5.0  # Fallback für einen einzelnen Punkt
            else:
                freshness = 1 + (9 / (n_samples - 1)) * i
            
            # Einfache lineare Beziehungen
            durability = freshness * 0.8 + 1.0
            taste = freshness * 0.9 + 0.5
            
            # Leichtes Rauschen hinzufügen
            if self.noise_level > 0:
                durability += np.random.normal(0, 0.1 * self.noise_level)
                taste += np.random.normal(0, 0.1 * self.noise_level)
            
            # Werte in gültigen Bereich clippen
            durability = np.clip(durability, 1, 10)
            taste = np.clip(taste, 1, 10)
            
            freshness_values.append(freshness)
            targets.append((durability, taste))
        
        # Datensatz zur Historie hinzufügen
        dataset_info = {
            'type': 'linear',
            'n_samples': n_samples,
            'noise_level': self.noise_level,
            'data': list(zip(freshness_values, targets))
        }
        self.data_history.append(dataset_info)
        
        logger.debug(f"Lineare Daten generiert: Frische [{min(freshness_values):.1f}, {max(freshness_values):.1f}]")
        
        return freshness_values, targets
    
    def generate_realistic_data(self, n_samples: int = 20) -> Tuple[List[float], List[Tuple[float, float]]]:
        """
        Erzeugt realistische Trainingsdaten mit physikalisch plausiblen Beziehungen.
        
        Dieses Modell implementiert komplexere, realistische Beziehungen:
        - Hohe Frische → Hohe Haltbarkeit (mit Sättigung)
        - Geschmack hat optimale Reife-Zone (nicht linear)
        - Zufällige Variationen simulieren natürliche Unterschiede
        - Korrelations-Rauschen zwischen den Eigenschaften
        
        Args:
            n_samples: Anzahl zu erzeugender Datenpunkte
            
        Returns:
            Tuple: (freshness_values, targets) mit realistischen Beziehungen
        """
        logger.info(f"Generiere {n_samples} realistische Datenpunkte")
        
        freshness_values = []
        targets = []
        
        for _ in range(n_samples):
            # Zufällige Frische mit Bevorzugung mittlerer Werte (natürlicher)
            freshness = np.random.beta(2, 2) * 9 + 1  # Beta-Verteilung für natürlichere Verteilung
            
            # === HALTBARKEIT: Starke Korrelation mit Frische ===
            # Basis: Exponentielles Wachstum mit Sättigung
            durability_base = 10 * (1 - np.exp(-freshness / 4))
            
            # Zufällige Variation basierend auf "Apfel-Sorte"
            variety_factor = np.random.normal(1.0, 0.15 * self.noise_level)
            durability = durability_base * variety_factor
            
            # Umwelt-Rauschen (Lagerung, Transport, etc.)
            environmental_noise = np.random.normal(0, 0.5 * self.noise_level)
            durability += environmental_noise
            
            # === GESCHMACK: Komplexere nichtlineare Beziehung ===
            # Optimaler Geschmack bei mittlerer Reife (Gauss-ähnlich)
            optimal_freshness = 7.0  # Optimaler Reife-Punkt
            freshness_deviation = abs(freshness - optimal_freshness)
            
            # Basis-Geschmack: Peak bei optimaler Frische
            taste_base = 8.5 - 1.5 * (freshness_deviation / 3.0) ** 2
            
            # Sorte beeinflusst auch Geschmack (korreliert mit Haltbarkeit)
            taste_variety_factor = 0.7 + 0.6 * (variety_factor - 0.7)
            taste = taste_base * taste_variety_factor
            
            # Individuelle Geschmacks-Variation
            taste += np.random.normal(0, 1.0 * self.noise_level)
            
            # Sehr frische Äpfel können sauer sein (niedrigerer Geschmack)
            if freshness > 9:
                sourness_penalty = (freshness - 9) * 2
                taste -= sourness_penalty
            
            # Sehr alte Äpfel haben schlechten Geschmack
            if freshness < 3:
                staleness_penalty = (3 - freshness) * 1.5  
                taste -= staleness_penalty
            
            # === CROSS-KORRELATIONEN ===
            # Sehr schlechte Haltbarkeit → schlechter Geschmack
            if durability < 3:
                taste *= 0.7
            
            # Sehr gute Haltbarkeit kann Geschmack leicht verbessern
            if durability > 8:
                taste *= 1.1
            
            # Werte in gültigen Bereich clippen
            durability = np.clip(durability, 1, 10)
            taste = np.clip(taste, 1, 10)
            
            freshness_values.append(freshness)
            targets.append((durability, taste))
        
        # Datensatz zur Historie hinzufügen
        dataset_info = {
            'type': 'realistic',
            'n_samples': n_samples,
            'noise_level': self.noise_level,
            'data': list(zip(freshness_values, targets))
        }
        self.data_history.append(dataset_info)
        
        # Statistiken loggen
        durabilities = [t[0] for t in targets]
        tastes = [t[1] for t in targets]
        
        logger.info(f"Realistische Daten generiert:")
        logger.info(f"  Frische: {np.mean(freshness_values):.2f} ± {np.std(freshness_values):.2f}")
        logger.info(f"  Haltbarkeit: {np.mean(durabilities):.2f} ± {np.std(durabilities):.2f}")
        logger.info(f"  Geschmack: {np.mean(tastes):.2f} ± {np.std(tastes):.2f}")
        
        return freshness_values, targets
    
    def generate_nonlinear_data(self, n_samples: int = 15) -> Tuple[List[float], List[Tuple[float, float]]]:
        """
        Erzeugt nichtlineare Trainingsdaten mit komplexen mathematischen Beziehungen.
        
        Diese Methode testet die Fähigkeit des QML-Modells, komplexere
        nichtlineare Funktionen zu lernen:
        - Haltbarkeit: Exponentieller Anstieg  
        - Geschmack: Sinusoidale Modulation
        
        Args:
            n_samples: Anzahl zu erzeugender Datenpunkte
            
        Returns:
            Tuple: (freshness_values, targets) mit nichtlinearen Beziehungen
        """
        logger.info(f"Generiere {n_samples} nichtlineare Datenpunkte")
        
        freshness_values = []
        targets = []
        
        for _ in range(n_samples):
            # Zufällige Frische über gesamten Bereich  
            freshness = np.random.uniform(1, 10)
            
            # === NICHTLINEARE HALTBARKEIT ===
            # Exponentieller Anstieg mit Sättigung
            durability = 10 * (1 - np.exp(-freshness / 5))
            
            # === NICHTLINEARE GESCHMACK ===
            # Sinusoidale Modulation mit Trend
            base_taste = 5 + 3 * np.sin(freshness * np.pi / 8)
            freshness_trend = freshness / 10  # Leichter linearer Trend
            taste = base_taste + 2 * freshness_trend
            
            # Rauschen hinzufügen
            durability += np.random.normal(0, 0.3 * self.noise_level)
            taste += np.random.normal(0, 0.3 * self.noise_level)
            
            # Werte begrenzen
            durability = np.clip(durability, 1, 10)
            taste = np.clip(taste, 1, 10)
            
            freshness_values.append(freshness)
            targets.append((durability, taste))
        
        # Datensatz zur Historie hinzufügen
        dataset_info = {
            'type': 'nonlinear',
            'n_samples': n_samples,
            'noise_level': self.noise_level,
            'data': list(zip(freshness_values, targets))
        }
        self.data_history.append(dataset_info)
        
        logger.debug(f"Nichtlineare Daten generiert mit {n_samples} Punkten")
        
        return freshness_values, targets
    
    def split_data(self, freshness: List[float], targets: List[Tuple[float, float]], 
                   train_ratio: float = 0.8, 
                   stratify: bool = False) -> Tuple[List[float], List[Tuple[float, float]], 
                                                   List[float], List[Tuple[float, float]]]:
        """
        Teilt Daten in Trainings- und Testset auf.
        
        Args:
            freshness: Liste der Frische-Werte
            targets: Liste der (Haltbarkeit, Geschmack) Ziele
            train_ratio: Anteil der Trainingsdaten (0.0 - 1.0)
            stratify: Ob stratifizierte Aufteilung verwendet werden soll
            
        Returns:
            Tuple: (train_freshness, train_targets, test_freshness, test_targets)
        """
        if not (0.0 < train_ratio < 1.0):
            raise ValueError("train_ratio muss zwischen 0 und 1 liegen")
        
        n_samples = len(freshness)
        n_train = int(n_samples * train_ratio)
        
        logger.info(f"Teile {n_samples} Samples auf: {n_train} Training, "
                   f"{n_samples - n_train} Test")
        
        if stratify:
            # Stratifizierte Aufteilung nach Frische-Bereichen
            # Teile in 3 Bereiche: niedrig (1-4), mittel (4-7), hoch (7-10)
            indices_low = [i for i, f in enumerate(freshness) if f <= 4]
            indices_mid = [i for i, f in enumerate(freshness) if 4 < f <= 7]
            indices_high = [i for i, f in enumerate(freshness) if f > 7]
            
            # Proportionale Aufteilung aus jedem Bereich
            train_indices = []
            for indices_group in [indices_low, indices_mid, indices_high]:
                if indices_group:
                    np.random.shuffle(indices_group)
                    n_train_group = int(len(indices_group) * train_ratio)
                    train_indices.extend(indices_group[:n_train_group])
            
            test_indices = [i for i in range(n_samples) if i not in train_indices]
            
            logger.debug(f"Stratifizierte Aufteilung: "
                        f"Niedrig={len(indices_low)}, Mittel={len(indices_mid)}, "
                        f"Hoch={len(indices_high)}")
        else:
            # Einfache zufällige Aufteilung
            indices = np.random.permutation(n_samples)
            train_indices = indices[:n_train]
            test_indices = indices[n_train:]
        
        # Daten aufteilen
        train_freshness = [freshness[i] for i in train_indices]
        train_targets = [targets[i] for i in train_indices]
        test_freshness = [freshness[i] for i in test_indices]
        test_targets = [targets[i] for i in test_indices]
        
        return train_freshness, train_targets, test_freshness, test_targets
    
    def add_noise(self, freshness: List[float], targets: List[Tuple[float, float]], 
                  noise_type: str = 'gaussian') -> Tuple[List[float], List[Tuple[float, float]]]:
        """
        Fügt verschiedene Arten von Rauschen zu bestehenden Daten hinzu.
        
        Args:
            freshness: Ursprüngliche Frische-Werte
            targets: Ursprüngliche Ziel-Werte
            noise_type: Art des Rauschens ('gaussian', 'uniform', 'outliers')
            
        Returns:
            Tuple: Verrauschte (freshness, targets)
        """
        logger.info(f"Füge {noise_type} Rauschen hinzu")
        
        noisy_freshness = freshness.copy()
        noisy_targets = [(d, t) for d, t in targets]
        
        if noise_type == 'gaussian':
            # Gausssches Rauschen
            for i in range(len(noisy_targets)):
                d, t = noisy_targets[i]
                d += np.random.normal(0, 0.3 * self.noise_level)
                t += np.random.normal(0, 0.3 * self.noise_level)
                noisy_targets[i] = (np.clip(d, 1, 10), np.clip(t, 1, 10))
                
        elif noise_type == 'uniform':
            # Gleichverteiltes Rauschen
            for i in range(len(noisy_targets)):
                d, t = noisy_targets[i]
                d += np.random.uniform(-0.5, 0.5) * self.noise_level
                t += np.random.uniform(-0.5, 0.5) * self.noise_level
                noisy_targets[i] = (np.clip(d, 1, 10), np.clip(t, 1, 10))
                
        elif noise_type == 'outliers':
            # Einzelne starke Outliers
            n_outliers = max(1, int(len(targets) * 0.1))  # 10% Outliers
            outlier_indices = np.random.choice(len(targets), n_outliers, replace=False)
            
            for i in outlier_indices:
                d, t = noisy_targets[i]
                # Starke zufällige Abweichung
                d += np.random.normal(0, 2.0)
                t += np.random.normal(0, 2.0)
                noisy_targets[i] = (np.clip(d, 1, 10), np.clip(t, 1, 10))
                
            logger.debug(f"{n_outliers} Outliers zu Indizes {outlier_indices} hinzugefügt")
        
        return noisy_freshness, noisy_targets
    
    def visualize_data(self, freshness: List[float], targets: List[Tuple[float, float]], 
                      title: str = "Apfel-Daten Visualisierung",
                      filename: Optional[str] = None) -> plt.Figure:
        """
        Visualisiert die erzeugten Daten in informativen Plots.
        
        Args:
            freshness: Frische-Werte  
            targets: Ziel-Werte (Haltbarkeit, Geschmack)
            title: Titel für die Visualisierung
            filename: Dateiname zum Speichern (optional)
            
        Returns:
            plt.Figure: Matplotlib Figure mit den Plots
        """
        logger.info(f"Visualisiere Datensatz mit {len(freshness)} Punkten")
        
        durability = [t[0] for t in targets]
        taste = [t[1] for t in targets]
        
        # Figure mit mehreren Subplots erstellen
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # 1. Haltbarkeit vs Frische
        ax1 = axes[0, 0]
        scatter1 = ax1.scatter(freshness, durability, alpha=0.7, s=50, c=freshness, cmap='viridis')
        ax1.set_xlabel('Frische')
        ax1.set_ylabel('Haltbarkeit')
        ax1.set_title('Frische → Haltbarkeit')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, 11)
        ax1.set_ylim(0, 11)
        plt.colorbar(scatter1, ax=ax1, label='Frische')
        
        # 2. Geschmack vs Frische  
        ax2 = axes[0, 1]
        scatter2 = ax2.scatter(freshness, taste, alpha=0.7, s=50, c=freshness, cmap='plasma')
        ax2.set_xlabel('Frische')
        ax2.set_ylabel('Geschmack')
        ax2.set_title('Frische → Geschmack')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 11)
        ax2.set_ylim(0, 11)
        plt.colorbar(scatter2, ax=ax2, label='Frische')
        
        # 3. Haltbarkeit vs Geschmack (Korrelation)
        ax3 = axes[1, 0]
        scatter3 = ax3.scatter(durability, taste, alpha=0.7, s=50, c=freshness, cmap='coolwarm')
        ax3.set_xlabel('Haltbarkeit')
        ax3.set_ylabel('Geschmack')
        ax3.set_title('Haltbarkeit ↔ Geschmack')
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(0, 11)
        ax3.set_ylim(0, 11)
        plt.colorbar(scatter3, ax=ax3, label='Frische')
        
        # 4. Histogramme aller Eigenschaften
        ax4 = axes[1, 1]
        ax4.hist(freshness, bins=15, alpha=0.7, label='Frische', color='green')
        ax4.hist(durability, bins=15, alpha=0.7, label='Haltbarkeit', color='blue')
        ax4.hist(taste, bins=15, alpha=0.7, label='Geschmack', color='orange')
        ax4.set_xlabel('Wert')
        ax4.set_ylabel('Häufigkeit')
        ax4.set_title('Verteilungen')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            logger.info(f"Visualisierung gespeichert als {filename}")
        
        return fig
    
    def get_statistics(self, freshness: List[float], 
                      targets: List[Tuple[float, float]]) -> Dict:
        """
        Berechnet umfassende Statistiken für einen Datensatz.
        
        Args:
            freshness: Frische-Werte
            targets: Ziel-Werte
            
        Returns:
            Dict: Umfassende Statistiken
        """
        durability = [t[0] for t in targets]
        taste = [t[1] for t in targets]
        
        def calc_stats(values: List[float]) -> Dict:
            return {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values),
                'median': np.median(values),
                'q25': np.percentile(values, 25),
                'q75': np.percentile(values, 75)
            }
        
        # Korrelationen berechnen
        corr_fresh_dur = np.corrcoef(freshness, durability)[0, 1]
        corr_fresh_taste = np.corrcoef(freshness, taste)[0, 1]
        corr_dur_taste = np.corrcoef(durability, taste)[0, 1]
        
        statistics = {
            'n_samples': len(freshness),
            'freshness': calc_stats(freshness),
            'durability': calc_stats(durability),
            'taste': calc_stats(taste),
            'correlations': {
                'freshness_durability': corr_fresh_dur,
                'freshness_taste': corr_fresh_taste,
                'durability_taste': corr_dur_taste
            },
            'data_quality': {
                'freshness_in_range': all(1 <= f <= 10 for f in freshness),
                'durability_in_range': all(1 <= d <= 10 for d in durability),
                'taste_in_range': all(1 <= t <= 10 for t in taste),
                'no_nan_values': not any(np.isnan([freshness + durability + taste]).flatten())
            }
        }
        
        logger.info(f"Statistiken berechnet für {len(freshness)} Samples")
        
        return statistics
    
    def export_data(self, freshness: List[float], targets: List[Tuple[float, float]], 
                   filename: str, format: str = 'csv') -> None:
        """
        Exportiert Daten in verschiedenen Formaten.
        
        Args:
            freshness: Frische-Werte
            targets: Ziel-Werte
            filename: Dateiname für Export
            format: Exportformat ('csv', 'json', 'numpy')
        """
        logger.info(f"Exportiere {len(freshness)} Datenpunkte als {format}")
        
        if format == 'csv':
            import csv
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['freshness', 'durability', 'taste'])
                for f, (d, t) in zip(freshness, targets):
                    writer.writerow([f, d, t])
                    
        elif format == 'json':
            import json
            data = {
                'metadata': {
                    'n_samples': len(freshness),
                    'generator_seed': self.seed,
                    'noise_level': self.noise_level
                },
                'samples': [
                    {'freshness': f, 'durability': d, 'taste': t}
                    for f, (d, t) in zip(freshness, targets)
                ]
            }
            with open(filename, 'w') as jsonfile:
                json.dump(data, jsonfile, indent=2)
                
        elif format == 'numpy':
            data_array = np.array([[f, d, t] for f, (d, t) in zip(freshness, targets)])
            np.save(filename, data_array)
        
        logger.info(f"Daten erfolgreich exportiert nach {filename}")
    
    def get_data_history(self) -> List[Dict]:
        """
        Gibt die Historie aller erzeugten Datensätze zurück.
        
        Returns:
            List[Dict]: Historie der Datensatz-Generierung
        """
        return self.data_history.copy()