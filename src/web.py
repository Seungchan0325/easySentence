import easySentence as easySentence
import streamlit as st

st.title("Easy Sentence Translator With AI")

# ./streamlit/secrets.toml 파일을 추가 해야함
#
# secrets.toml
#
# OPENAI_API_KEY = "YOUR OPENAI API KEY"
api_key: str = st.secrets.OPENAI_API_KEY

translator = easySentence.EasySentenceTranslator(api_key)

with st.form("form"):
    user_input = st.text_area("글을 입력해주세요 !")
    submit = st.form_submit_button("제출")

if submit and user_input:
    with st.spinner("문장 변환중입니다. 잠시만 기다려주세요..."):
        result = translator.translate(user_input)

    # '-------------' markdown 표
    st.write('-' * 50)
    for i in result:
        for j in i:
            st.write(j)
        st.write('-' * 50)