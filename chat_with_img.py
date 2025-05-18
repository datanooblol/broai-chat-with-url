import streamlit as st
from broai.prompt_management.core import PromptGenerator
from broai.llm_management.ollama import BedrockOllamaChat
from broai.prompt_management.interface import Persona
from PIL import Image
import io
import boto3
client = boto3.client("bedrock-runtime", region_name="us-west-2")

model = BedrockOllamaChat()
if "model_name" not in st.session_state:
    st.session_state["model_name"] = "us.meta.llama3-2-11b-instruct-v1:0"


def get_image_bytes(filename):
    MAX_PIXELS = 600 * 600  # 1 million pixels
    # Open and resize image if needed
    with Image.open(filename) as img:
        while img.width * img.height > MAX_PIXELS:
            img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
        # Save to in-memory buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()  # This is ready to send to boto3
    return image_bytes

# def get_image_bytes(filename):
#     with open(filename, "rb") as image_file:
#         image_bytes = image_file.read()
#     return image_bytes


def UserMessage(text, image_bytes=None, image_format=None):
    content = [{"text": text}]
    if image_bytes:
        image = {"image": {"format": image_format, "source": {"bytes": image_bytes}}}
        content.append(image)
    return {"role": "user", "content": content}


def AIMessage(text):
    return {"role": "assistant", "content": [{"text": text}]}


def extract_response(response):
    return response["output"]["message"]["content"][0]["text"]


def chat(client, model_name, system_prompt, messages):
    response = client.converse(
        modelId=model_name,
        messages=messages,
        # system=[{"text": system_prompt}]
    )
    return extract_response(response)

if "filename" not in st.session_state:
    st.session_state["filename"] = None

prompt_dir = "./agent_prompts"
# model = BedrockOllamaChat()
st.set_page_config(
    page_title="BroGPT",
    page_icon="🚀",
)
with st.sidebar:
    st.title("Chat Settings")
    st.radio("Model name", ["us.meta.llama3-2-11b-instruct-v1:0"], key="model_name")
    st.write(st.session_state.model_name)
    st.markdown("---")
    uploaded_file = st.file_uploader("Talk to Image")
    if uploaded_file:
        image_bytes = uploaded_file.read()
        image_format = uploaded_file.name.split(".")[-1]
        filename = f"./img/temp.{image_format}"
        st.session_state.filename = filename
        with open(filename, "wb") as f:
            f.write(image_bytes)
        st.image(image_bytes)
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

# -- Main Chat UI --
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"][0]["text"])

if prompt := st.chat_input("What is up?"):
    if st.session_state.filename:
        image_bytes = get_image_bytes(st.session_state.filename)
        user_msg = model.UserMessage(
            text=prompt,
            image_bytes=image_bytes,
            image_format=st.session_state.filename.split(".")[-1]
        )
    else:
        user_msg = UserMessage(text=prompt)
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_prompt = pg.as_prompt()
            # response = chat(
            #     client,
            #     model_name=st.session_state.model_name,
            #     system_prompt=full_prompt,
            #     messages=st.session_state.messages+[user_msg]
            # )
            model.model_name = st.session_state.model_name
            response = model.run(system_prompt=full_prompt, messages=st.session_state.messages+[user_msg])
            st.markdown(response)
    st.session_state.messages.append(UserMessage(text=prompt))
    st.session_state.messages.append(AIMessage(text=response))
    

