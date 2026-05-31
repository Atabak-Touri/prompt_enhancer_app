import streamlit as st
from google import genai

# 1. UI Setup: Wider layout and an icon
st.set_page_config(page_title="Prompt Enhancer Pro", page_icon="✨", layout="wide")

# 2. Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key:", type="password", help="Your key is not saved or stored anywhere.")
    
    st.markdown("---")
    
    st.subheader("Prompt Options")
    prompt_category = st.selectbox(
        "What type of task is this?",
        ["General", "Coding & Tech", "Business & Marketing", "Creative Writing"]
    )

# 3. Main Page Layout
st.title("✨ AI Prompt Enhancer Pro")
st.write("Turn your basic idea into a highly structured, professional prompt ready for any LLM.")

user_basic_prompt = st.text_area(
    "What do you want to ask the AI?", 
    placeholder="e.g., Write a report on applying AI in digital production management...", 
    height=150
)

# 4. Action Button with primary styling
if st.button("Enhance My Prompt", type="primary"):
    
    if not api_key:
        st.sidebar.error("⚠️ Please enter your API Key above.")
    elif not user_basic_prompt:
        st.warning("Please enter a basic prompt to enhance.")
    else:
        with st.spinner("Engineering your prompt..."):
            try:
                client = genai.Client(api_key=api_key)
                
                # Dynamic System Instructions based on user selection
                if prompt_category == "Coding & Tech":
                    focus = "Include sections for Tech Stack, Edge Cases, and Code Comments requirements."
                elif prompt_category == "Business & Marketing":
                    focus = "Include sections for Target Audience, Tone of Voice, and Key Performance Indicators."
                elif prompt_category == "Creative Writing":
                    focus = "Include sections for Narrative Tone, Character Background, and Pacing."
                else:
                    focus = "Include standard sections like Role, Context, Task, and Formatting Constraints."
                
                system_instruction = f"""
                You are an elite Prompt Engineer. Your task is to rewrite the user's basic request into a highly sophisticated, structured prompt ready to be pasted into an LLM.
                
                {focus}
                
                CRITICAL INSTRUCTIONS FOR YOU (THE PROMPT BUILDER):
                1. You are writing the prompt from the perspective of the user.
                2. DO NOT include meta-instructions meant for YOU inside the final generated prompt (e.g., do not write "Output ONLY the enhanced prompt" inside the generated text). 
                3. The final output must ONLY contain the instructions for the Target AI to follow.
                4. Output ONLY the final enhanced prompt. Do not include introductory or concluding conversational filler like "Here is the prompt."
                """

                
                full_prompt = f"{system_instruction}\n\nBasic request to enhance:\n{user_basic_prompt}"
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt
                )
                
                st.success("✨ Prompt Enhanced Successfully!")
                st.info("Click the copy icon in the top right corner of the box below to copy your prompt.")
                st.code(response.text, language="markdown")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")