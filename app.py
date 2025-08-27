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

.
