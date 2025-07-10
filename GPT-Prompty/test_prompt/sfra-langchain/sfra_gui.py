import streamlit as st
from sfra_analyzer import SFRAAnalyzer
from langchain_agent import build_agent_chain
import tempfile
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SFRA Analyzer AI", layout="wide")

st.title("⚡ SFRA Analyzer z GPT")
st.markdown("Wgraj plik CSV z pomiarem transformatora, a agent GPT oceni wynik i odpowie na pytania.")

# 1. Wgraj plik
uploaded_file = st.file_uploader("Wgraj plik CSV z pomiarem", type=["csv", "xlsx"])
if uploaded_file:
    # zapisz plik tymczasowo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # 2. Analiza SFRA
    try:
        analyzer = SFRAAnalyzer(tmp_path)
        analyzer.analyze()

        df = analyzer.load_data()
        analyzer.validate_columns(df)
        _, anomalies = analyzer.calibrate_thresholds(df)

        if anomalies.empty:
            st.success("✅ Nie wykryto anomalii. Pomiar mieści się w skalibrowanych progach.")
        else:
            prompt_text = analyzer.generate_prompt(anomalies.iloc[0])
            st.subheader("📋 Wygenerowany prompt:")
            st.code(prompt_text, language="markdown")

            st.markdown("---")
            st.subheader("🤖 Chat z agentem SFRA")
            chain = build_agent_chain(prompt_text)

            question = st.text_input("Zadaj pytanie do pomiaru SFRA:")
            if question:
                with st.spinner("Agent analizuje..."):
                    answer = chain.run(question=question)
                    st.success(answer)

    except Exception as e:
        st.error(f"Błąd: {e}")

