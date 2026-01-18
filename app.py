import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

def ask_llm(user_text: str, expert_type: str) -> str:
    """
    入力テキスト(user_text) と ラジオ選択(expert_type) を受け取り、
    LLMの回答テキストを返す関数
    """
    # 専門家タイプごとにシステムメッセージを切り替え
    if expert_type == "A：Python/Streamlit講師":
        system_prompt = (
            "あなたはPythonとStreamlitの専門講師です。"
            "初心者にも分かるように、手順を箇条書きで丁寧に説明し、"
            "必要なら短いサンプルコードも提示してください。"
        )
    else:  # "B：プロダクト企画メンター"
        system_prompt = (
            "あなたはプロダクト企画のメンターです。"
            "ユーザー課題の整理、仮説、優先順位、MVP設計の観点で、"
            "実務的に助言してください。"
        )

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    # Lesson8形式（System/Human/AIメッセージ）を踏襲
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="これからユーザーの質問に答えてください。"),
        AIMessage(content="承知しました。質問をどうぞ。"),
        HumanMessage(content=user_text),
    ]

    result = llm(messages)

    # result は AIMessage 互換のことが多いので content を優先して返す
    return getattr(result, "content", str(result))


def main():
    st.set_page_config(page_title="LangChain × Streamlit Demo", page_icon="🤖", layout="centered")

    st.title("🤖 LangChain × Streamlit（専門家切り替えデモ）")

    # 概要・操作方法（要件）
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

    # APIキーの確認（OpenAI）
    # 環境変数 OPENAI_API_KEY が入っている想定。未設定なら案内表示。
    if not os.getenv("OPENAI_API_KEY"):
        st.warning(
            "環境変数 `OPENAI_API_KEY` が設定されていません。"
            "設定後に再実行してください。"
        )
        st.stop()

    # ラジオボタン（要件：専門家の種類を選択）
    expert_type = st.radio(
        "専門家タイプを選択してください",
        options=["A：Python/Streamlit講師", "B：プロダクト企画メンター"],
        horizontal=True,
    )

    # 入力フォーム（要件：1つ用意）
    user_text = st.text_input("入力フォーム（質問を入力してください）", placeholder="例：Streamlitでフォーム送信後に画面を更新する方法は？")

    # 送信ボタン
    send = st.button("送信", type="primary", use_container_width=True)

    if send:
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