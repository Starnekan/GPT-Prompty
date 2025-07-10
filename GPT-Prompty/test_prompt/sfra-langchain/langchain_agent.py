from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def build_agent_chain(prompt_text: str):
    template = PromptTemplate(
        input_variables=["question"],
        template="""
Jesteś specjalistą od diagnostyki transformatorów. Odpowiadasz na pytania techniczne na podstawie raportu z analizy SFRA.

Raport z analizy:
\"\"\"
{prompt_text}
\"\"\"

Pytanie użytkownika: {{question}}
Odpowiedź:
"""
    )

    llm = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=template.partial(prompt_text=prompt_text))
    return chain

