import os

import streamlit as st
from streamlit_chat import message

from pdf_reader import PDFReader
from QA_response_generator import QAResponseGenerator

PDF_DATA_DIR = "./pdf_data/"

os.makedirs(PDF_DATA_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file, save_dir):
    try:
        with open(os.path.join(save_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getvalue())
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def upload_pdf_file():
    uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        if save_uploaded_file(uploaded_file, PDF_DATA_DIR):
            st.success(f"File {uploaded_file.name} saved at {PDF_DATA_DIR}")
        else:
            st.error("The file could not be saved.")

def display_chat(chat_history):
    for i, chat in enumerate(reversed(chat_history)):
        if "user" in chat:
            message(chat["user"], is_user=True, key=str(i)) 
        else:
            message(chat["bot"], key="bot_"+str(i))

def main():
    st.title('PDF Q&A app')

    upload_pdf_file()
    file_name = st.sidebar.selectbox("Choose a file", os.listdir(PDF_DATA_DIR)) 
    choice = st.radio("参照情報を表示:", ["表示する", "表示しない"])
    question = st.text_input("Your question")

    # メインの画面に質問送信ボタンを設定
    submit_question = st.button("質問")
    clear_chat = st.sidebar.button("履歴消去")

    # チャット履歴を保存
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if clear_chat:
        st.session_state["chat_history"] = []

    pdf_reader = PDFReader()
    response_generator = QAResponseGenerator("gpt-3.5-turbo", pdf_reader)
    # ボタンがクリックされた場合の処理
    if submit_question:
        if question:  # 質問が入力されている場合
            response, source = response_generator.generate(question, file_name)
            if choice == "表示する":
                response += f"\n\n参照した情報は次の通りです:\n{source}"

            # 質問と応答をチャット履歴に追加
            st.session_state["chat_history"].append({"user": question})
            st.session_state["chat_history"].append({"bot": response})

    display_chat(st.session_state["chat_history"])

if __name__ == "__main__":
    main()
