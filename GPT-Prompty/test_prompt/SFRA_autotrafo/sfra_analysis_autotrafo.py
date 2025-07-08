import sys
import logging
from pathlib import Path
from typing import List, Dict, Tuple

import pandas as pd

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SFRAAnalyzer:
    """
    Klasa do wczytywania, walidacji i analizy danych SFRA autotransformatora,
    z automatyczną korekcją progów detekcji anomalii.
    """

    def __init__(
        self,
        file_path: str,
        sep: str = ",",
        encoding: str = "utf-8",
        required_columns: List[str] = None,
        target_anomaly_rate: float = 0.05,
        sigma_step: float = 0.5,
        tol: float = 0.01,
        max_iter: int = 10
    ) -> None:
        self.file_path = Path(file_path)
        self.sep = sep
        self.encoding = encoding
        self.required_columns = required_columns or [
            "øA RATIO", "øA RATIO ERROR", "øA PHASE DEV", "øA RMS CURRENT",
            "øB RATIO", "øB RATIO ERROR", "øB PHASE DEV", "øB RMS CURRENT",
            "øC RATIO", "øC RATIO ERROR", "øC PHASE DEV", "øC RMS CURRENT",
        ]
        # parametry pętli korekcyjnej
        self.target_anomaly_rate = target_anomaly_rate
        self.sigma_step = sigma_step
        self.tol = tol
        self.max_iter = max_iter
        # do przechowywania wyników kalibracji
        self.sigma_multiplier = 2.0
        self.thresholds: Dict[str, float] = {}

    def load_data(self) -> pd.DataFrame:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Plik nie istnieje: {self.file_path}")
        try:
            df = pd.read_csv(self.file_path, sep=self.sep, encoding=self.encoding)
        except pd.errors.EmptyDataError:
            raise ValueError("Plik CSV jest pusty lub ma nieprawidłowy format")
        except pd.errors.ParserError as e:
            raise ValueError(f"Błąd parsowania CSV: {e}")

        if df.empty:
            raise ValueError("Wczytany DataFrame jest pusty")

        df.columns = df.columns.str.strip()
        logger.info(f"Wczytano {len(df)} wierszy z pliku {self.file_path}")
        logger.debug(f"Kolumny: {df.columns.tolist()}")
        return df

    def validate_columns(self, df: pd.DataFrame) -> None:
        missing = [col for col in self.required_columns if col not in df.columns]
        if missing:
            raise ValueError(
                f"Brakujące kolumny: {missing}. "
                f"Dostępne kolumny: {df.columns.tolist()}"
            )

    def _compute_thresholds(self, df: pd.DataFrame) -> None:
        """
        Na podstawie aktualnego sigma_multiplier liczy progi dla kolumn ERROR.
        """
        error_cols = [c for c in self.required_columns if c.endswith("ERROR")]
        stats = df[error_cols].agg(["mean", "std"])
        self.thresholds = {
            col: stats.at["mean", col] + self.sigma_multiplier * stats.at["std", col]
            for col in error_cols
        }
        logger.debug(f"Progi (σ={self.sigma_multiplier}): {self.thresholds}")

    def detect_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Zwraca podzbiór wierszy, w których któraś kolumna ERROR przekracza próg.
        """
        masks = []
        for col, thr in self.thresholds.items():
            masks.append(df[col] > thr)
        any_anomaly = pd.concat(masks, axis=1).any(axis=1)
        return df[any_anomaly]

    def calibrate_thresholds(self, df: pd.DataFrame) -> Tuple[Dict[str, float], pd.DataFrame]:
        """
        Pętla korekcyjna:
        - liczy progi na podstawie średniej + sigma_multiplier*std
        - sprawdza odsetek anomalii
        - dostosowuje sigma_multiplier aż odsetek anomalii ~ target_anomaly_rate
        """
        for i in range(self.max_iter):
            self._compute_thresholds(df)
            anomalies = self.detect_anomalies(df)
            rate = len(anomalies) / len(df)
            logger.info(
                f"Iteracja {i+1}: σ={self.sigma_multiplier:.2f}, "
                f"anomalii={len(anomalies)}/{len(df)} ({rate:.2%})"
            )
            if abs(rate - self.target_anomaly_rate) <= self.tol:
                break
            # jeśli jest za dużo anomalii → bardziej liberalny próg (większe sigma)
            if rate > self.target_anomaly_rate:
                self.sigma_multiplier += self.sigma_step
            else:
                # zbyt mało → zaostrzamy detekcję
                self.sigma_multiplier = max(self.sigma_step, self.sigma_multiplier - self.sigma_step)
        else:
            logger.warning("Osiągnięto maksymalną liczbę iteracji kalibracji")

        # finalne progi i zestaw wierszy-anomalii
        self._compute_thresholds(df)
        anomalies = self.detect_anomalies(df)
        return self.thresholds, anomalies

    def generate_prompt(self, sample: pd.Series) -> str:
        def val(key: str, suffix: str = "") -> str:
            return f"{sample.get(key, 'N/A')}{suffix}"

        return (
            "Dane z pomiaru SFRA autotransformatora AT-2 (Żukowice, 220/110kV):\n"
            f"- øA:\n"
            f"  - RATIO: {val('øA RATIO')}\n"
            f"  - ERROR: {val('øA RATIO ERROR', '%')}\n"
            f"  - PHASE DEV: {val('øA PHASE DEV', '°')}\n"
            f"  - RMS CURRENT: {val('øA RMS CURRENT', ' A')}\n"
            f"- øB:\n"
            f"  - RATIO: {val('øB RATIO')}\n"
            f"  - ERROR: {val('øB RATIO ERROR', '%')}\n"
            f"  - PHASE DEV: {val('øB PHASE DEV', '°')}\n"
            f"  - RMS CURRENT: {val('øB RMS CURRENT', ' A')}\n"
            f"- øC:\n"
            f"  - RATIO: {val('øC RATIO')}\n"
            f"  - ERROR: {val('øC RATIO ERROR', '%')}\n"
            f"  - PHASE DEV: {val('øC PHASE DEV', '°')}\n"
            f"  - RMS CURRENT: {val('øC RMS CURRENT', ' A')}\n\n"
            "Pomiar inspekcyjny. Oceń poprawność, wskaż anomalie i zaproponuj dalsze działania serwisowe."
        )

    def analyze(self) -> None:
        df = self.load_data()
        self.validate_columns(df)

        # 1) kalibracja progów
        thresholds, anomalies = self.calibrate_thresholds(df)

        # 2) podsumowanie
        logger.info("Ostateczne progi dla kolumn ERROR:")
        for col, thr in thresholds.items():
            logger.info(f"  {col}: {thr:.2f}%")

        logger.info(f"Znaleziono {len(anomalies)} wierszy-anomalii.")
        if not anomalies.empty:
            # wypisz kilka pierwszych przykładów
            logger.info("Przykłady anomalii (pierwsze 5 wierszy):")
            logger.info(anomalies[self.required_columns].head().to_string())

        # 3) wygeneruj prompt dla pierwszej anomalii, jeśli istnieje
        if not anomalies.empty:
            prompt = self.generate_prompt(anomalies.iloc[0])
            print("\n=== PROMPT DLA PIERWSZEJ ANOMALII ===\n")
            print(prompt)
        else:
            print("🚀 Nie wykryto anomalii – wszystkie pomiary mieszczą się w skalibrowanych progach.")


def main() -> None:
    file_path = sys.argv[1] if len(sys.argv) > 1 else "TTRU3_EXP_Export_2025-02-20T10_43_02.csv"
    analyzer = SFRAAnalyzer(file_path)

    try:
        analyzer.analyze()
    except Exception as e:
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
