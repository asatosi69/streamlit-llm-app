import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

def ask_llm(user_text: str, expert_type: str) -> str:
    if expert_type == "A：Python/Streamlit講師":
        system_prompt = (
            "あなたはPythonとStreamlitの専門講師です。"
            "初心者にも分かるように、手順を箇条書きで丁寧に説明し、"
            "必要なら短いサンプルコードも提示してください。"
        )
    else:
        system_prompt = (
            "あなたはプロダクト企画のメンターです。"
            "ユーザー課題の整理、仮説、優先順位、MVP設計の観点で、"
            "実務的に助言してください。"
        )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="これからユーザーの質問に答えてください。"),
        AIMessage(content="承知しました。質問をどうぞ。"),
        HumanMessage(content=user_text),
    ]

    result = llm.invoke(messages)
    return result.content


def main():
    st.set_page_config(page_title="LangChain × Streamlit Demo", page_icon="🤖", layout="centered")
    st.title("🤖 LangChain × Streamlit（専門家切り替えデモ）")

    st.markdown(
        """
このWebアプリは、入力フォームにテキストを送信すると、LangChain経由でLLMに問い合わせて回答を表示します。  
また、ラジオボタンで **LLMに振る舞わせる専門家** を切り替えできます。

### 使い方
1. ラジオボタンで専門家タイプ（A/B）を選択  
2. 入力フォームに質問や相談内容を入力  
3. 「送信」を押すと、回答が画面下に表示されます
"""
    )

    if not os.getenv("OPENAI_API_KEY"):
        st.warning("環境変数 `OPENAI_API_KEY` が設定されていません。設定後に再実行してください。")
        st.stop()

    expert_type = st.radio(
        "専門家タイプを選択してください",
        options=["A：Python/Streamlit講師", "B：プロダクト企画メンター"],
        horizontal=True,
    )

    user_text = st.text_input(
        "入力フォーム（質問を入力してください）",
        placeholder="例：Streamlitで入力フォームを作る方法は？",
    )

    if st.button("送信", type="primary", use_container_width=True):
        if not user_text.strip():
            st.error("テキストを入力してください。")
            st.stop()

        with st.spinner("LLMに問い合わせ中..."):
            try:
                answer = ask_llm(user_text=user_text, expert_type=expert_type)
            except Exception as e:
                st.error(f"LLM呼び出しでエラーが発生しました: {e}")
                st.stop()

        st.subheader("回答")
        st.write(answer)


if __name__ == "__main__":
    main()