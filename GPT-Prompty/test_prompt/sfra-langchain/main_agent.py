import sys
from sfra_analyzer import SFRAAnalyzer
from langchain_agent import build_agent_chain
from dotenv import load_dotenv

load_dotenv()

def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "dane_pomiarowe/pomiar1.csv"
    analyzer = SFRAAnalyzer(file_path)
    try:
        analyzer.analyze()
        # prompt na podstawie 1. anomalii
        df = analyzer.load_data()
        analyzer.validate_columns(df)
        _, anomalies = analyzer.calibrate_thresholds(df)
        if anomalies.empty:
            print("Brak anomalii, koniec sesji.")
            return
        prompt_text = analyzer.generate_prompt(anomalies.iloc[0])

        chain = build_agent_chain(prompt_text)

        print("\n🔧 Agent SFRA gotowy. Zadawaj pytania (lub wpisz 'exit'):\n")
        while True:
            q = input("🧠> ")
            if q.lower() in ["exit", "quit"]:
                break
            response = chain.run(question=q)
            print("📡", response.strip())

    except Exception as e:
        print("❌ Błąd analizy:", e)

if __name__ == "__main__":
    main()

