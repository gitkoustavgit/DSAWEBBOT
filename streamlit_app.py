import streamlit as st
from main import answer_with_context, explain_code, debug_code 

st.set_page_config(page_title="GenAI Tutor", layout="centered")

st.markdown("""
    <style>
        .stApp {
            background-color: #000000;
            color: white;
        }
        .centered-title {
            text-align: center;
            color: #FFC966;
            font-size: 40px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .stTextArea textarea {
            min-height: 200px !important;
        }
        .stTextInput>div>div>input,
        .stTextArea textarea {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #FFA500;
            color: black;
            font-weight: bold;
            border-radius: 8px;
            border: none;
        }
        .stSidebar {
            background-color: #111111;
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 3rem;
            padding-bottom: 2rem;
        }
        div[data-baseweb="radio"] label {
            display: block;
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🧭 Navigation")
mode = st.sidebar.radio("✨ What's on your mind today?", [
    "💬 Just here to clarify some doubts..",
    "👨‍💻 Need some help with coding? I got you covered!",
    "🐞 Your code has an error? Lemme fix it for you!!"
])

st.markdown('<div class="centered-title">🧠 GenAI Tutor</div>', unsafe_allow_html=True)

if mode == "💬 Just here to clarify some doubts..":
    st.subheader("🔍 Ask a Web Dev / DSA Question")
    history = []
    user_query = st.text_area("Your Question", height=200)

    if st.button("Get Answer"):
        if user_query:
            response = answer_with_context(user_query, history)
            st.markdown("### 🤖 Answer")
            st.write(response)
            history.append({"user": user_query, "bot": response})

elif mode == "👨‍💻 Need some help with coding? I got you covered!":
    st.subheader("📘 Paste Code for Explanation or Type in the Question to be solved")
    code_snippet = st.text_area("Paste your code here", height=250)
    lang = st.text_input("Language (e.g., HTML, Python, JS)")

    if st.button("Explain Code"):
        if code_snippet:
            explanation = explain_code(code_snippet, lang)
            st.markdown("### ✏️ Explanation")
            st.write(explanation)

elif mode == "🐞 Your code has an error? Lemme fix it for you!!":
    st.subheader("🛠️ Paste Code to Find and Fix Bugs")
    code_to_debug = st.text_area("Paste your code here", height=250)
    lang = st.text_input("Language (e.g., Python, C++, Java)")

    if st.button("Debug Code"):
        if code_to_debug:
            debugged = debug_code(code_to_debug, lang)
            st.markdown("### ✅ Debugging Output")
            st.write(debugged)