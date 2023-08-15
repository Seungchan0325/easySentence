import easySentence
import streamlit as st

st.title("Easy Sentence Translator With AI")

translator = easySentence.EasySentenceTranslator("OPENAI API KEY")

with st.form("form"):
    user_input = st.text_area("글을 입력해주세요 !")
    submit = st.form_submit_button("제출")

if submit and user_input:
    with st.spinner("문장 변환중입니다. 잠시만 기다려주세요..."):
        result = translator.translate(user_input)

    for i in result:
        for j in i:
            st.write(j)
        st.write('-' * 50)