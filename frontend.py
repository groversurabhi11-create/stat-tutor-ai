import streamlit as st
import requests

# Initialize Streamlit app with tabs for different modes
st.set_page_config(page_title="Stat Tutor AI", layout="wide")

st.title("Stat Tutor AI")

if "question" not in st.session_state:
    st.session_state.question = None

if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0

st.sidebar.title("Your Progress")

st.sidebar.write(f"Attempts: {st.session_state.attempts}")
st.sidebar.write(f"Score: {st.session_state.score}")

if st.session_state.attempts > 0:
    accuracy = st.session_state.score / st.session_state.attempts
    st.sidebar.write(f"Accuracy: {accuracy:.2%}")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Explain", "Practice", "Evaluate"])

with tab1:
    st.header("Explain Mode")
    topic = st.text_input("Enter a statistics concept you would like to understand")
    if st.button("Explain"):
        resp = requests.post("http://localhost:8000/explain", json={"topic": topic})
        data = resp.json()
        st.write(data["data"]["explanation"])

with tab2:
    st.header("Practice Mode")
    topic = st.text_input("Enter a statistics topic for practice")
    difficulty = st.selectbox("Select difficulty", ["easy", "medium", "hard"])
    if st.button("Get Problem"):
        resp = requests.post("http://localhost:8000/practice", json={"topic": topic, "difficulty": difficulty})
        result = resp.json()

        st.session_state.question = result["data"]["question"]
        st.session_state.correct_answer = result["data"]["correct_answer"]

        st.write("Question:")
        st.write(st.session_state.question)
        st.session_state.attempts = 0
        st.session_state.score = 0
        ## Persist model response in session state to allow for evaluation in the next tab
    if "question" in st.session_state:
        st.write("Current Question:")
        st.write(st.session_state.question)
    

with tab3:
    st.header("Evaluate Mode")

    if st.session_state.question is None:
        st.warning("Generate a practice question first.")
    else:
        st.write("Question:")
        st.write(st.session_state.question)

        student_answer = st.text_area("Enter the student's answer")

        if st.button("Evaluate"):
            if not student_answer.strip():
                st.warning("Please enter an answer before evaluating.")
            else:
                resp = requests.post(
                    "http://localhost:8000/evaluate",
                    json={
                        "question": st.session_state.question,
                        "student_answer": student_answer,
                        "correct_answer": st.session_state.correct_answer,
                    },
                )

                data = resp.json()

                st.write(data["data"]["evaluation"])

                st.session_state.attempts += 1

                if data["data"]["evaluation"]["correct"]:
                    st.session_state.score += 1

                st.write(f"Attempts: {st.session_state.attempts}")
                st.write(f"Score: {st.session_state.score}")