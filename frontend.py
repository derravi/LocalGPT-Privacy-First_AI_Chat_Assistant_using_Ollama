import streamlit as st
import requests

API_URL = "http://127.0.0.1:9000"

st.title("Local GPT Chat")

# ==============================
# Session Create
# ==============================

st.sidebar.header("Create Chat Session")

session_title = st.sidebar.text_input("Session Title")

if st.sidebar.button("Create Session"):

    response = requests.post(
        f"{API_URL}/create_session",
        params={"title": session_title}
    )

    data = response.json()

    st.session_state["session_id"] = data["session_id"]

    st.sidebar.success(f"Session Created: {data['session_id']}")


# ==============================
# Chat Section
# ==============================

st.header("Ask Question")

prompt = st.text_input("Enter your prompt")

if st.button("Send Prompt"):

    if "session_id" not in st.session_state:
        st.error("Please create a session first!")

    elif prompt == "":
        st.warning("Please enter a prompt")

    else:

        response = requests.post(
            f"{API_URL}/answer",
            params={"session_id": st.session_state["session_id"]},
            json={
                "input_text": [prompt]
            }
        )

        data = response.json()

        answer = data["responses"][0]["answer"]

        st.subheader("Answer")
        st.write(answer)


# ==============================
# History
# ==============================

st.header("Chat History")

if st.button("Load History"):

    response = requests.get(f"{API_URL}/history")

    data = response.json()

    for i in data:
        st.write("Prompt:", i["original_text"])
        st.write("Answer:", i["answer_text"])
        st.write("Time:", i["date_and_time"])
        st.write("---")