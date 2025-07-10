# Prompt Architect – metodologia projektowania promptów

Ten dokument opisuje podejście autora do projektowania, testowania i iteracji promptów dla modeli LLM takich jak GPT-4, Gemini, Mistral, Claude i DALL·E. Celem jest stworzenie **powtarzalnego, adaptowalnego i świadomego systemu komunikacji z AI**.



## 🧱 1. Architektura promptu

Każdy prompt opiera się na czterowarstwowym modelu:

| Warstwa               | Opis |
|-----------------------|------|
| **1. Behavior Prompt** | Określenie roli AI (np. „Zachowuj się jak rasowy rekruter”, „Ekspert BHP”). |
| **2. Zadanie Główne** | Konkretne polecenie (np. „Stwórz checklistę”, „Oceń mój poziom promptowania”). |
| **3. Kontekst Wejściowy** | Informacje dodatkowe: dane, ograniczenia, pliki, style wypowiedzi. |
| **4. Styl i Format Odpowiedzi** | Preferowany format: tabela, markdown, schemat, język formalny/luźny. |



## 🔁 2. Iteracja i testowanie (ACL loop)

Prompty są testowane i rozwijane zgodnie z pętlą korekcyjną:

1. **A (Ask)** – Zadaj prompt wstępny.
2. **C (Critic)** – Oceń jakość odpowiedzi (jasność, trafność, styl).
3. **L (Loop)** – Zmień prompt (zakres, styl, strukturę) i przetestuj ponownie.

Pętla ACL to systematyczna metoda doskonalenia promptów na podstawie realnego outputu, a nie intuicji.



## 🧠 3. Tryby pracy z modelem

| Tryb | Opis |
|------|------|
| **Zero-shot** | Model dostaje jednorazowy, kompletny prompt. Dla szybkich zadań. |
| **One-shot / few-shot** | Dostarczam przykład(y), aby nauczyć model struktury odpowiedzi. |
| **Prompt-as-a-system** | Projektuję cały system dialogowy: rola + iteracja + scenariusze + testy. |
| **Prompt-dialog / prompt-tool** | Model zachowuje się jak aplikacja: odpowiada, analizuje, raportuje, iteruje. |



## 🛠️ 4. Rodzaje promptów w repo

- **Techniczne**: audyt BHP, pomiary trafo, analiza dokumentów
- **Formalno-prawne**: odwołania, mandaty, argumentacja
- **Kreatywne**: tarot, narracja, autoanaliza osobowości
- **Metakognitywne**: ocena jakości pracy z AI, AOQ, RAM 2.0
- **Eksperymentalne**: testowanie granic modelu, prompt paradox, lustro Poppera



## 🧩 5. Styl i kontrola odpowiedzi

W promptach stosuję wyraźne **parametry kontroli stylu**:
- „odpowiedz jak ekspert, ale bez technobełkotu”
- „użyj markdown i tabel”
- „jeśli nie jesteś pewny – podaj warianty”

Stosuję też promptowe wskaźniki jakości: trafność, klarowność, struktura, rozdzielczość poznawcza.



