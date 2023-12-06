import streamlit as st
import openai

st.cache_data.clear()

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

openai.api_key = st.session_state.openai_api_key

if "text_error" not in st.session_state:
    st.session_state.text_error = None

if "text" not in st.session_state:
    st.session_state.text = None

if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

with st.sidebar:
    api_key_insert = st.form(key="api_key_insert")
    openai_api_key = api_key_insert.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    api_key_form_submitted = api_key_insert.form_submit_button("Submit")

    if api_key_form_submitted:
        st.session_state.openai_api_key = openai_api_key
        openai.api_key = st.session_state.openai_api_key
        st.success("Your OpenAI API key was subbitted successfully.")

def generate_flower_recommendation(occasion, recipient_name, favorite_color, relationship):
    # Customize the prompt based on your requirements
    prompt = f"Recommend me a flower that are suitable for {occasion} and {favorite_color} for {recipient_name} who is my {relationship}. and write 5 notes for me to tell {recipient_name} why I chose this flower for this {occasion}."

    # Call OpenAI API for recommendation
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        top_p=0.7,
        max_tokens=450,
        messages=[
            {"role": "system", "content": "You are a flowers recommendation bot. You will help users find the best flowers for their important person."},
            {"role": "user", "content": f"You will help users find the best flowers and make notes from the context:{prompt}."},
        ]
    )
    
    return response.choices[0].message.content

st.title("Compatibility")

