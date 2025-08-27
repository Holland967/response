from openai import OpenAI
import streamlit as st

if "r_text" not in st.session_state:
    st.session_state.r_text = []
if "c_text" not in st.session_state:
    st.session_state.c_text = []
if "resp_id" not in st.session_state:
    st.session_state.resp_id = None

with st.sidebar:
    api_key = st.text_input("API KEY", "", type="password", key="api_key")
    clear_btn = st.button("Clear", key="clear_btn")
    st.markdown("---")
    model_list = [
      "doubao-seed-1-6-250615",
      "doubao-seed-1-6-thinking-250715",
      "doubao-seed-1-6-vision-250815"
    ]
    model = st.selectbox("Models", model_list, key="model")
    instruct = st.text_area("Instruct", "", key="instruct")
    max_tokens = st.slider("Max Tokens", 1, 32768, 16384, 1, key="tokens")
    temperature = st.slider("Temperature", 0.00, 2.00, 1.00, 0.01, key="temp")
    top_p = st.slider("Top P", 0.00, 1.00, 0.70, 0.01, key="top_p")

if api_key:
    client = OpenAI(
      base_url="https://ark.cn-beijing.volces.com/api/v3",
      api_key=api_key
    )

if clear_btn:
    st.session_state.r_text = []
    st.session_state.c_text = []
    st.session_state.resp_id = None
    st.rerun()

index = 0
for i in st.session_state.c_text:
    if i["role"] == "user":
        with st.chat_message("user"):
            st.markdown(i["content"])
        if st.session_state.r_text:
            if index < len(st.session_state.r_text):
                with st.expander("Thinking", False):
                    st.markdown(st.session_state.r_text[index])
                index += 1
    elif i["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(i["content"])

if prompt := st.chat_input("Say something", key="prompt"):
    st.session_state.c_text.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    if st.session_state.resp_id is None:
        response = client.responses.create(
            model=model,
            input=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=True
        )
    else:
        response = client.responses.create(
            model=model,
            previous_response_id=st.session_state.resp_id,
            input=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=True
        )

    c_text = ""
    r_text = ""

    with st.expander("Thinking", True):
        r_placeholder = st.empty()
    with st.chat_message("assistant"):
        c_placeholder = st.empty()
  
    try:
        for event in response:
            if event.type == "response.reasoning_summary_text.delta":
                r_text += event.delta
                r_placeholder.markdown(event.delta)
            elif event.type == "response.output_text.delta":
                c_text += event.delta
                c_placeholder.markdown(event.delta)
            elif event.type == "response.completed":
                st.session_state.resp_id = event.response.id
        st.session_state.r_text.append(r_text)
        st.session_state.c_text.append({"role": "assistant", "content": c_text})
        st.rerun()
    except Exception as e:
        st.error(e)
