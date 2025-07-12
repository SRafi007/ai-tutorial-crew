import sys
import os

# 👇 Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from main import run, OUTPUT_FILE
import os

st.set_page_config(page_title="AI Tutorial Generator", layout="centered")

st.title("🧠 AI-Powered Python Tutorial Generator")
st.markdown("Generate beginner Python tutorials using CrewAI agents and a local model.")

# Optional topic input (just for UI, not wired into agents yet)
topic = st.text_input("Enter Tutorial Topic", "Python Lists")

# Trigger button
if st.button("🚀 Generate Tutorial"):
    with st.spinner("Agents are working..."):
        run(topic)  # <-- pass input to backend

    st.success("✅ Tutorial Generated!")

    # Display content
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            st.subheader("📘 Tutorial Output")
            st.code(content, language="markdown")

        # Download button
        with open(OUTPUT_FILE, "rb") as f:
            st.download_button(
                label="💾 Download Markdown",
                data=f,
                file_name="python_tutorial.md",
                mime="text/markdown",
            )
    else:
        st.error("Output file not found.")
