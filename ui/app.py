# ui/app.py
import sys
import os

# 👇 Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from main import run, OUTPUT_FILE
from utils.input_processor import process_user_input
import os

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

# Trigger button
if st.button("🚀 Generate Tutorial"):
    # Process the input first
    final_topic = process_user_input(raw_topic)

    # Create a progress container
    progress_container = st.container()

    with progress_container:
        st.write(f"🎯 **Target Topic:** {final_topic}")

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
        status_text.text("🔍 Research Agent: Gathering information and key concepts...")
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
        run(final_topic)

        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Tutorial generation completed!")

        # Small delay to show completion
        import time

        time.sleep(1)

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

    st.success("🎉 Tutorial Generated Successfully!")

    # Display content
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

            # Create tabs for different views
            tab1, tab2 = st.tabs(["📖 Preview", "📝 Markdown Source"])

            with tab1:
                st.subheader("📘 Tutorial Preview")
                # Display markdown content as rendered markdown
                st.markdown(content)

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
                st.code(content, language="markdown")

        # Download button with processed topic name
        st.divider()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Ready to save your tutorial?**")
        with col2:
            with open(OUTPUT_FILE, "rb") as f:
                st.download_button(
                    label="💾 Download Tutorial",
                    data=f,
                    file_name=f"{final_topic.replace(' ', '_').replace('/', '_')}_tutorial.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
    else:
        st.error("❌ Output file not found. Please try generating the tutorial again.")
