# 🧪 Test Prompt: SFRA Analysis – Autotransformator AT-2

Ten notebook demonstruje użycie promptu **„Asystent Diagnostyki i Analizy Transformatorów Energetycznych”** na przykładzie pomiaru SFRA autotransformatora 220/110kV, Żukowice.

## 📄 Dane wejściowe

- **Plik CSV**: `TTRU3_EXP_Export_2025-02-20T10_43_02.csv`
- **Typ pomiaru**: Sweep Frequency Response Analysis (SFRA)
- **Obiekt**: Autotransformator AT-2
- **Lokalizacja**: Żukowice
- **Charakter pomiaru**: Inspekcyjny

## 🔍 Zakres testu

- Wczytanie danych CSV z pomiarów SFRA
- Ekstrakcja kluczowych parametrów diagnostycznych (RATIO, ERROR, PHASE DEV, CURRENT)
- Wygenerowanie tekstowego promptu w formacie GPT
- Wklejenie wyników do modelu w celu uzyskania oceny stanu transformatora

## 📂 Pliki

- `sfra_analysis_autotrafo.ipynb` – notebook Jupyter z pełnym testem
- `TTRU3_EXP_Export_2025-02-20T10_43_02.csv` – dane pomiarowe

## ✅ Status

Test został przygotowany do analizy i gotowy do użycia w folderze `test_prompt/` lub `showcase/`.
