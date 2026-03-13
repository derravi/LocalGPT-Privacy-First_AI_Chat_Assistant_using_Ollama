import streamlit as st
import requests

API_URL = "http://127.0.0.1:9000"

st.title("LocalGPT Chat")

#Session ID
session_id = st.number_input("Session ID",min_value=1,step=1)

#prompt input
user_prompt = st.text_area("Enter Your Prompt here...")

if st.button("Send"):
    payload = {
        "input_text" : [user_prompt],
    }

    response = requests.post(
        f"{API_URL}/answer?session_id={session_id}",
        json=payload
    )

    if response.status_code == 200:

        data = response.json()

        for i in data["responses"]:
            st.write("### Prompt")
            st.write(i["Prompt"])

            st.write("### Answer")
            st.write(r["Answer"])
    else:
        st.error("Error connecting to API.")