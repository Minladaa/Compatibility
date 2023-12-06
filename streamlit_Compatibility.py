import streamlit as st
import openai
import pandas as pd
import json

st.cache_data.clear()

# OpenAI part

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
        st.success("Your OpenAI API key was submitted successfully.")

def compatibility_analyzer(user_personality_type, user_zodiac_sign, their_personality_type, their_zodiac_sign):
    # Customize the prompt based on your requirements
    prompt = f"You are a compatibility analyzer bot. You will analze the compatibility of the user and the other person based on their personality types and zodiac signs. The user is an {user_personality_type} and a {user_zodiac_sign}. The other person is an {their_personality_type} and a {their_zodiac_sign}. 
    List the analytics in a JSON array.
    First, return one of these phases defining the compatibility: 1. 'You guys could rock the world together!💓' If there are only minor challenges and many stong strengths,. 2. 'You guys could give it a go!💛'If there are some average challenges and some average strengths. 3. 'This seems unlikely...😿' If there are  major challenges and not so stong strengths. Next, return strengths. Next, return challenges. Next, return potential dynamics. Lastly, return some additional tips."

    # Call OpenAI API for recommendation
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        top_p=0.7,
        max_tokens=450,
        messages=[
            {"role": "system", "content": "You are a compatibility analyzer bot. You will analze the compatibility of the user and the other person based on their personality types and zodiac signs."},
            {"role": "user", "content": f"You will tell users the analytics of the compatibility between them and the other person from the context:{prompt}."},
        ]
    )
    
    analytics_dictionary = response.choices[0].message.content
    return analytics_dictionary

sd = json.loads(analytics_dictionary)
analytics_df = pd.DataFrame.from_dict(sd)
analytics_df

# Streamlit part

st.title("Your compatibility with your crush👀")
st.markdown("This app will analyze the compatibility between you and someone that you have chosen based on personality types and zodiac signs.💌")

    # User input
st.markdown("## Tell me about yourself.💫")
user_personality_type = st.selectbox("Your personality type:", ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"])
st.write("If you don't know your personality type or want to know more about your personality type,\n check out this [link](https://www.16personalities.com/)")
user_zodiac_sign = st.selectbox("Your zodiac sign:", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])
st.write("If you don't know your zodiac sign or want to know more about your zodiac sign,\n check out this [link](https://www.zodiacsign.com/)")
st.markdown("## Now, tell me about the other person.👀")
their_personality_type = st.selectbox("Their personality type:", ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"])
their_zodiac_sign = st.selectbox("Their zodiac sign:", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])

    # Analyze the compatibility
if st.button("Tell me the compatibility!"):
    if user_personality_type and user_zodiac_sign and their_personality_type and their_zodiac_sign:
        Analytics = compatibility_analyzer(user_personality_type, user_zodiac_sign, their_personality_type, their_zodiac_sign)
        st.success(f"Analyzed the compatibility: {analytics_df}")
    else:
        st.warning("Tell me about yourself and the other person first!")
