import streamlit as st
from streamlit_chat import message
import requests


import yaml
import openai

import databutton as db

openai.api_key = db.secrets.get("OPENAI_API_KEY")


st.set_page_config(
    page_title="TobyGPT"
)

st.image("https://cdn-icons-png.flaticon.com/512/3649/3649460.png")


model_engine = "gpt-3.5-turbo"


# This is where we set the personality and style of our chatbot
prompt_template = """
    You are a helpful online chatbot named Toby asked to assist job-seekers in their job-application under H&H power. Your replies are respectful and specific.
    """

# When calling ChatGPT, we   need to send the entire chat history together
# with the instructions. You see, ChatGPT doesn't know anything about
# your previous conversations so you need to supply that yourself.
# Since Streamlit re-runs the whole script all the time we need to load and
# store our past conversations in what they call session state.
# prompt = st.session_state.get("prompt", None)

if 'prompt' not in st.session_state:
    # This is the format OpenAI expects
    st.session_state['prompt'] = []
    
    # initiate the information that the bot knows about talent recruitment
    st.session_state.prompt.append({"role": "system", "content": prompt_template})
    st.session_state.prompt.append({"role": "system", "content": "You are Toby, you match job-seekers with available jobs in a Filipino power generation company. You may ask them on their experiences, or educational background."})
    st.session_state.prompt.append({"role": "system", "content": """H&H company is a power generation company with a porfolio of 500 MW. Currently their assets include 300 MW of coal power plants and 200 MW of solar plants across the Philippines """})
    st.session_state.prompt.append({"role": "system", "content": """The available jobs in the company are a Data Scientist position for an entry level, a Business Development manager for expansion projects, an accounting specialist that is an expert in tax and a graphic designer under the creatives team. """})
    st.session_state.prompt.append({"role": "system", "content": "The Data scientist's  responsibilities are to create models for price forecasting of electricity and demand. They are also tasked to compute monthly Fuel cost of the coal plant"})
    st.session_state.prompt.append({"role": "system", "content": "The Business development manager is responsible for leading the projects for solar plant construction, creating financial models, and talking to shareholders about the returns of the projects"})
    st.session_state.prompt.append({"role": "system", "content": "The accounting specialist needed will deal with taxes. He/she must be verse in tax compliance laws and would make sure that taxes are paid on time."})
    st.session_state.prompt.append({"role": "system", "content": "The graphic designer's job are to create logos, posters or graphic artwork needed for presentation purposes in both shareholder setting and online setting."})
    st.session_state.prompt.append({"role": "system", "content": "If a person is interested in a position, tell them they could email their resume to harvey.de.leon@powercompany.com.ph"})
    st.session_state.prompt.append({"role": "system", "content": "If a person is qualified for a position, suggest to them the job vacancy otherwise, tell them their qualification does not currenly match current job openings but feel free to try again next time"})
    st.session_state.prompt.append({"role": "system", "content": "If a person asks for the salary of the positions then here's what you tell them. The salary for the data scientist is Php 35,000 to Php 80,000 per month depending on the experience. The salary for the Business Development Manager ranges from Php 80,000 to Php 120,000 per month. The salary for the accounting specialist ranges from Php 44,000 to Php 70,000 per month and the graphic designer's position has a salary of Php 50,000 to Php 70,000 per month. "})
    st.session_state.prompt.append({"role": "system", "content": "Aside from being a match maker for applicants, some applicants can ask you for an update of their job applications.As of right now, you could choose to tell them that their application hasn't been viewed yet, its being evaluated by the person in charge, their application has been rejected but has not email it to them or that they are scheduling for an interview but has not decided yet on the date. Pick among these choices randomly"})
    # for onboarding
    st.session_state.prompt.append({"role": "system", "content": "You will also provide newly hired employees assistance for the onboarding process with the documents needed for identification and paperworks to be submitted before they report to the office."})
    st.session_state.prompt.append({"role": "system", "content": "Advise the new employee about the standard flow for the different periods of the onboarding process, however, assure the new employee that an HR representative will be in touch during the whole onboarding process."})
    st.session_state.prompt.append({"role": "system", "content": "On the first day of work, newly hired employees will be required to report to the IT department for the arrangement of their new workstation, HR department for a formal onboarding meeting, and department head for an introduction."})
    st.session_state.prompt.append({"role": "system", "content": "On the first week of work, newly hired employees will be informed of regular 1:1 meeting schedules and performance objectives and will be given check ins and feedbacks on their initial work."})
    st.session_state.prompt.append({"role": "system", "content": "On the first three months of work, the newly hired employees will continue to have regular 1:1 meetings and 30-day check in for immediate concerns, and will be asked to give feedback on the onboarding process."})
    st.session_state.prompt.append({"role": "system", "content": "Answer specific questions related to the specified job descriptions. For other concerns regarding the tasks, advise the new employee to coordinate with their department head."})
    
# Send an API request and get a response, note that the interface and parameters have changed compared to the old model

def get_response(input_text):
    
    st.session_state.prompt.append({"role": "user", "content": input_text})

    messages = st.session_state.prompt
    response = openai.ChatCompletion.create(model=model_engine,messages=messages)
    output = response['choices'][0]['message']['content']
    
    
    # When we get an answer back we add that to the message history
    st.session_state.prompt.append({"role": "assistant", "content": output})
    return output


st.header("Toby GPT")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ","Hello, I have questions regarding human resources.", key="input")
    return input_text 


user_input = get_text()

if user_input:
    output = get_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


# this is to reprint the chat history
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        