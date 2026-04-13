from agent.react_agent import ReactAgent
import streamlit as st
import time

st.title("intellgent robot")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()
if "msg" not in st.session_state:
    st.session_state["msg"] = []

for msg in st.session_state["msg"]:
    st.chat_message(msg["role"]).write(msg["content"])

# user input prompt
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["msg"].append({
        "role":"user",
        "content":prompt,
    })
    response_msgs = []
    with st.spinner("think...."):
        res_stream = st.session_state["agent"].executer_stream(prompt)
        
        def capture(generator, cache_lsit):
            for chunk in generator:
                cache_lsit.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_msgs))
        st.session_state["msg"].append({"role":"assistant", "content": response_msgs[-1]})
        st.rerun()
