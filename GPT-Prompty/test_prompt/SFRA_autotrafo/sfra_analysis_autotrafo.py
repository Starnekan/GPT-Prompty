import pandas as pd

# Ścieżka do pliku CSV
file_path = "TTRU3_EXP_Export_2025-02-20T10_43_02.csv"

# Wczytanie danych
df = pd.read_csv(file_path, sep=",", encoding="utf-8")
df.columns = df.columns.str.strip()

# Pobranie przykładowego wiersza
sample_row = df.iloc[0]

# Generowanie promptu
prompt_input = f"""Dane z pomiaru SFRA autotransformatora AT-2 (Żukowice, 220/110kV):

- øA:
  - RATIO: {sample_row['øA RATIO']}
  - ERROR: {sample_row['øA RATIO ERROR']}%
  - PHASE DEV: {sample_row['øA PHASE DEV']}°
  - RMS CURRENT: {sample_row['øA RMS CURRENT']} A

- øB:
  - RATIO: {sample_row['øB RATIO']}
  - ERROR: {sample_row['øB RATIO ERROR']}%
  - PHASE DEV: {sample_row['øB PHASE DEV']}°
  - RMS CURRENT: {sample_row['øB RMS CURRENT']} A

- øC:
  - RATIO: {sample_row['øC RATIO']}
  - ERROR: {sample_row['øC RATIO ERROR']}%
  - PHASE DEV: {sample_row['øC PHASE DEV']}°
  - RMS CURRENT: {sample_row['øC RMS CURRENT']} A

Pomiar inspekcyjny. Oceń poprawność, wskaż anomalie i zaproponuj dalsze działania serwisowe.
"""

print(prompt_input)

# Miejsce na odpowiedź GPT (ręczne wklejenie):
print("\n🔍 Wklej tutaj odpowiedź GPT na powyższy prompt.\n")
