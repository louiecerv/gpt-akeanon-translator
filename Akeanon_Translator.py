import streamlit as st
import openai
import pandas as pd

from openai import AsyncOpenAI
from openai import OpenAI

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=st.secrets["API_key"],
)

context = "You are a language assistant"

async def generate_response(question, context):
    model = "ft:gpt-3.5-turbo-1106:west-visayas-state-university::9JDQf0yI"
    
    completion = await client.chat.completions.create(model=model, 
        messages=[{"role": "user", "content": question}, 
                {"role": "system", "content": context}])
    return completion.choices[0].message.content

async def app():
    st.subheader("Translect: Akeanon-English / English Akeanon Translator")

    text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
    CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University
    """
    st.write(text)

    text = """This is a simple translator that translates English to Akeanon and vice versa.
    The app is based on a research project to develop a mobile tranlation app for various Visayan languages."""
    st.write(text)
    df = pd.read_csv("akeanon-sentences.csv", header=0)

    with st.expander("Click to display the training dataset"):
        st.write(df)

    # Define the options for the show selection
    show_options = ["English to Akeanon", "Akeanon to English"]

    # Use st.selectbox to create the show option box
    selected_show = st.selectbox("Select the translation task", show_options)

    # Process the selected option
    if selected_show:  # Check if user selected something
        if selected_show == "English to Akeanon":
            task = "translate to akeanon:"
        elif selected_show == "Akeanon to English":
            task = "translate to enlish:"

    # Text input for user question
    question = st.text_input("Enter the sentence to translate:")
    prompt = task + " " + question
    # Button to generate response
    if st.button("Translate"):
        if question and context:
            response = await generate_response(prompt, context)
            st.write("Response:")
            st.write(response)
        else:
            st.error("Please enter both question and context.")

#run the app
if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
