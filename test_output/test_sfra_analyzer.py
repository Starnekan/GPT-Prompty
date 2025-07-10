# test_output/test_sfra_analyzer.py
import pandas as pd
import pytest
from test_prompt.sfra_langchain.sfra_analyzer import SFRAAnalyzer

def test_load_data(tmp_path):
    # stwórz prosty CSV
    data = "A,B\n1,2\n3,4"
    file = tmp_path / "test.csv"
    file.write_text(data)
    analyzer = SFRAAnalyzer(str(file))
    df = analyzer.load_data()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["A", "B"]
