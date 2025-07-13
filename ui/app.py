# ui/app.py
import sys
import os

# 👇 Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from main import run, OUTPUT_FILE
from utils.input_processor import process_user_input
import os
import re

st.set_page_config(page_title="AI Tutorial Generator", layout="centered")

st.title("🧠 AI-Powered Tutorial Generator")
st.markdown("Generate beginner tutorials using CrewAI agents and a local model.")

# Topic input
raw_topic = st.text_input("Enter Tutorial Topic")

# Show processed topic preview
if raw_topic:
    with st.spinner("Processing input..."):
        processed_topic = process_user_input(raw_topic)

    if processed_topic != raw_topic:
        st.info(f"📝 Processed topic: **{processed_topic}**")

# Initialize session state
if "tutorial_generated" not in st.session_state:
    st.session_state.tutorial_generated = False

if "final_topic" not in st.session_state:
    st.session_state.final_topic = ""

# Trigger button - only show if tutorial hasn't been generated yet
if not st.session_state.tutorial_generated:
    if st.button("🚀 Generate Tutorial"):
        # Process the input first
        st.session_state.final_topic = process_user_input(raw_topic)

        # Create a progress container
        progress_container = st.container()

        with progress_container:
            st.write(f"🎯 **Target Topic:** {st.session_state.final_topic}")

            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Step 1: Processing Input
            status_text.text("🔄 Processing and validating input...")
            progress_bar.progress(10)

            # Step 2: Initializing Agents
            status_text.text("🤖 Initializing AI agents and local LLM...")
            progress_bar.progress(25)

            # Step 3: Research Phase
            status_text.text(
                "🔍 Research Agent: Gathering information and key concepts..."
            )
            progress_bar.progress(40)

            # Step 4: Writing Phase
            status_text.text("✍️ Writer Agent: Creating tutorial content...")
            progress_bar.progress(65)

            # Step 5: Review Phase
            status_text.text("📋 Reviewer Agent: Checking quality and clarity...")
            progress_bar.progress(85)

            # Step 6: Finalizing
            status_text.text("🎨 Finalizing tutorial and saving output...")
            progress_bar.progress(95)

            # Run the actual generation
            run(st.session_state.final_topic)

            # Complete
            progress_bar.progress(100)
            status_text.text("✅ Tutorial generation completed!")

            # Small delay to show completion
            import time

            time.sleep(1)

            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

        # Hide the button by using session state
        st.session_state.tutorial_generated = True
        st.success("🎉 Tutorial Generated Successfully!")
        st.rerun()

# Show tutorial content if it has been generated
if st.session_state.tutorial_generated:
    # Display content
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

            # Create tabs for different views
            tab1, tab2 = st.tabs(["📖 Preview", "📝 Markdown Source"])

            with tab1:
                st.subheader("📘 Tutorial Preview")

                # Clean and process the content for better rendering
                if content.strip():
                    # Remove any potential BOM or invisible characters
                    content = content.encode("utf-8").decode("utf-8-sig")

                    # Remove markdown code block wrapper if present
                    if content.strip().startswith("```markdown"):
                        # Find the first ```markdown and remove it
                        content = content.strip()[11:]  # Remove ```markdown
                        # Find the last ``` and remove it
                        if content.strip().endswith("```"):
                            content = content.strip()[:-3]  # Remove closing ```

                    # Clean up any remaining formatting issues
                    content = content.strip()

                    # Use unsafe_allow_html=True for better rendering
                    st.markdown(content, unsafe_allow_html=True)
                else:
                    st.warning(
                        "The generated tutorial appears to be empty. Please try generating again."
                    )

                # Add a separator
                st.divider()

                # Show tutorial stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    word_count = len(content.split())
                    st.metric("Word Count", word_count)
                with col2:
                    line_count = len(content.split("\n"))
                    st.metric("Lines", line_count)
                with col3:
                    char_count = len(content)
                    st.metric("Characters", char_count)

            with tab2:
                st.subheader("📝 Raw Markdown")
                # Show raw markdown in a code block
                st.code(content, language="markdown", line_numbers=True)

        # Download button with processed topic name
        st.divider()

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write("**Ready to save your tutorial?**")
        with col2:
            with open(OUTPUT_FILE, "rb") as f:
                # Create a safe filename
                safe_filename = re.sub(r"[^\w\s-]", "", st.session_state.final_topic)
                safe_filename = re.sub(r"[-\s]+", "_", safe_filename)

                st.download_button(
                    label="💾 Download Tutorial",
                    data=f,
                    file_name=f"{safe_filename}_tutorial.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
        with col3:
            # Add a reset button to generate a new tutorial
            if st.button("🔄 Generate New", use_container_width=True):
                st.session_state.tutorial_generated = False
                st.rerun()
    else:
        st.error("❌ Output file not found. Please try generating the tutorial again.")
        # Add reset button in case of error
        if st.button("🔄 Try Again"):
            st.session_state.tutorial_generated = False
            st.rerun()
