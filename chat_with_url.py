import streamlit as st
from package.search_utils import scrape_jina_ai
from broai.llm_management.ollama import BedrockOllamaChat
from broai.prompt_management.core import PromptGenerator
from broai.prompt_management.interface import Persona
# import os

if "model_name" not in st.session_state:
    st.session_state["model_name"] = "us.meta.llama3-2-11b-instruct-v1:0"


prompt_dir = "./agent_prompts"
model = BedrockOllamaChat()
st.set_page_config(
    page_title="BroGPT",
    page_icon="🚀",
)
with st.sidebar:
    st.title("Chat Settings")

    # Mode selector
    chat_mode = st.radio("Mode", ["Talk with Bot", "Talk with URL"])
    st.radio("Model name", ["us.meta.llama3-2-1b-instruct-v1:0", "us.meta.llama3-2-3b-instruct-v1:0", "us.meta.llama3-2-11b-instruct-v1:0", "us.meta.llama3-3-70b-instruct-v1:0"], key="model_name")
    st.write(st.session_state.model_name)
    st.markdown("---")
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
    with st.expander("System Prompt"):
        name = st.text_input("Agent Name", "Andy Bro")
        description = st.text_area("Agent Character", "You are chill, friendly and supportive.")
        instruction = st.text_area("Agent Instructions", "Do everything to help a user.")
        structured_output = st.text_area("Agent Structured Output Format", "Return only plain text.")
        filename = st.text_input("Filename", "")

        pg = PromptGenerator(
            persona=Persona(name=name, description=description),
            instruction=instruction if len(instruction)!=0 else None,
            structured_output=structured_output if len(structured_output)!=0 else None,
        )
        if st.button("Save Agent Prompt") and len(filename)!=0:
            with open(f"{prompt_dir}/{filename}", "w") as f:
                f.write(pg.as_prompt())
            st.write(f"successfully saved in {filename}")

    url = st.text_input(
        "Enter url here below",
        "https://www....",
        key="placeholder",
    )
    if st.button("Scrape"):
        if url and url != "https://www....":
            with st.spinner("Scraping..."):
                scraped_text = scrape_jina_ai(url)
                st.session_state.scraped_text = scraped_text
                st.session_state.scraped_url = url
            with open("temp.md", "w") as f:
                f.write(scraped_text)
        else:
            st.warning("Please enter a valid URL.")

    if "scraped_text" in st.session_state:
        st.write("### Scraped Result")
        st.markdown(st.session_state.scraped_text)

# -- Main Chat UI --
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"][0]["text"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append(model.UserMessage(text=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 👇 Adjust system prompt based on mode
            if chat_mode == "Talk with URL" and "scraped_text" in st.session_state:
                full_prompt = f"{pg.as_prompt()}\n\nKnowledge:\n{st.session_state.scraped_text}"
            else:
                full_prompt = pg.as_prompt()
            model.model_name = st.session_state.model_name
            response = model.run(system_prompt=full_prompt, messages=st.session_state.messages)
            st.markdown(response)

    st.session_state.messages.append(model.AIMessage(text=response))

