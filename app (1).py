
import streamlit as st
from google import genai
import os

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Interactive Study Assistant",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# GEMINI API
# --------------------------------------------------

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📚 Interactive Study Assistant")

st.write(
    "Your AI-powered study partner for learning, "
    "understanding, and revision."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("⚙️ Study Settings")

topic = st.sidebar.text_input(
    "📖 Study Topic",
    value="Python Programming"
)

study_mode = st.sidebar.selectbox(
    "🎯 Study Mode",
    [
        "Ask a Question",
        "Explain a Topic",
        "Generate Study Notes",
        "Important Points",
        "Give Examples"
    ]
)

difficulty = st.sidebar.selectbox(
    "📊 Explanation Level",
    [
        "Basic",
        "Medium",
        "Detailed"
    ]
)

# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------

if study_mode == "Ask a Question":

    user_question = st.text_area(
        "❓ Ask your question",
        placeholder="Example: What is inheritance in Python?"
    )

else:

    user_question = ""

# --------------------------------------------------
# START LEARNING
# --------------------------------------------------

if st.button(
    "🚀 Start Learning",
    use_container_width=True
):

    if not topic.strip():

        st.warning("Please enter a study topic.")

    elif (
        study_mode == "Ask a Question"
        and not user_question.strip()
    ):

        st.warning("Please enter your question.")

    else:

        # ------------------------------------------
        # PROMPT
        # ------------------------------------------

        if study_mode == "Ask a Question":

            prompt = f"""
You are an interactive study assistant.

Topic:
{topic}

Student Question:
{user_question}

Explanation Level:
{difficulty}

Explain the answer in simple student-friendly language.

Include:
1. Direct answer
2. Simple explanation
3. One example
4. Important point to remember
"""

        elif study_mode == "Explain a Topic":

            prompt = f"""
You are an interactive study assistant.

Explain this topic:

{topic}

Explanation Level:
{difficulty}

Include:
1. Definition
2. Main concepts
3. How it works
4. Simple example
5. Important points
6. Short summary

Use simple student-friendly language.
"""

        elif study_mode == "Generate Study Notes":

            prompt = f"""
You are an educational study assistant.

Create study notes for:

{topic}

Explanation Level:
{difficulty}

Include:
1. Introduction
2. Important definitions
3. Main concepts
4. Key points
5. Examples
6. Quick revision summary

Use simple student-friendly language.
"""

        elif study_mode == "Important Points":

            prompt = f"""
You are an educational study assistant.

Give the most important points about:

{topic}

Explanation Level:
{difficulty}

Include:
1. Important concepts
2. Important definitions
3. Key facts
4. Exam-focused points
5. Quick revision points

Use simple language.
"""

        else:

            prompt = f"""
You are an educational study assistant.

Give practical and real-world examples for:

{topic}

Explanation Level:
{difficulty}

For each example:
1. Situation
2. How the topic is used
3. Simple example
4. Why it is useful

Use student-friendly language.
"""

        # ------------------------------------------
        # GEMINI RESPONSE
        # ------------------------------------------

        try:

            with st.spinner(
                "🤖 Preparing your study material..."
            ):

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )

                answer = response.text

            st.session_state.study_result = answer

        except Exception as e:

            st.error(
                "Unable to generate study material."
            )

            st.error(str(e))

# --------------------------------------------------
# DISPLAY RESULT
# --------------------------------------------------

if "study_result" in st.session_state:

    st.subheader("📚 Study Assistant Response")

    st.markdown(
        st.session_state.study_result
    )

    st.divider()

    st.download_button(
        "⬇️ Download Study Material",
        data=st.session_state.study_result,
        file_name="study_material.txt",
        mime="text/plain",
        use_container_width=True
    )

# --------------------------------------------------
# CLEAR
# --------------------------------------------------

if "study_result" in st.session_state:

    if st.button(
        "🗑️ Clear Study Material",
        use_container_width=True
    ):

        del st.session_state.study_result

        st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Interactive Study Assistant | "
    "Streamlit + Google Gemini AI"
)
