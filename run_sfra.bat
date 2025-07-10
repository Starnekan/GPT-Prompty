@echo off
REM — Zmiana na dysk G:
G:
REM — Przejście do katalogu projektu
cd /d %~dp0
cd GPT_Prompty

REM — Aktywacja venv
call venv\Scripts\activate.bat

REM — Przejście do folderu z GUI
cd test_prompt\sfra_langchain

REM — Uruchomienie Streamlit
streamlit run sfra_gui.py

REM — Zatrzymaj okno, by zobaczyć logi po zamknięciu
pause
