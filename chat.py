from langchain_groq import ChatGroq
from database import check_user,create_user,book_appointment
from flask import Flask, request, jsonify
import sqlite3
from dotenv import load_dotenv
import os
load_dotenv()

os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
model_name="Llama3-8b-8192"
llm=ChatGroq(model=model_name)
app = Flask(__name__)
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import Runnable  # Assuming you're using LangChain's Runnable LLM
import threading

# Replace with your actual LLM (like ChatGroq, OpenAI, etc.)
# For example:
# from langchain_groq import ChatGroq
# llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
# System prompt
system = """
You are a helpful assistant who helps users book appointments for MKARD Landscaping & Tree Care Services.
When starting greet them with welcome and ask to book appointment and ask the question one by one.
Ask for a phone number to check if the user already exists in the database.
If not, collect their full name, address, email, zipcode, city, service request, and phone number.
Ask the same in a conversational manner and collect data one after one.
Also, check if the requested appointment slot is free. 
If not, offer alternative free slots for that day and once done ask do you want to exit? if yes then close chat.
Give them a brief about the appointment and then exit.
Don't answer questions out of this scope, just say 'I don't know about it.'
Please keep it short and precise.
"""
system="""You are a helpful assistant for MKARD Landscaping & Tree Care Services. 
Your job is to help users book appointments in a friendly and conversational way.

Start with a welcome message and ask the user if they'd like to book an appointment.

1. Ask for their phone number to check if they already exist in the database.
2. If the user does not exist, collect their:
- Full Name
- Address
- Email
- Zip Code
- City
- Phone Number
- Service Request
Ask one question at a time, keeping the conversation natural and short.

3. Ask the user for their preferred appointment date and time.
- Check the database to see if that slot is available.
- If it's not available, suggest alternative free slots for that day.

4. Once the appointment is booked, provide a brief summary with the date, time, and service.

5. Then ask, “Would you like to exit the chat?” If yes, end the conversation politely.

If the user asks something out of scope, respond with:
> "I don't know about it."

Keep responses short, friendly, and focused on completing the appointment booking.
"""
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


prompt=ChatPromptTemplate.from_messages([
("system","""You are a helpful assistant for MKARD Landscaping & Tree Care Services. 
Your job is to help users book appointments in a friendly and conversational way.

Start with a welcome message and ask the user if they'd like to book an appointment.

1. Ask for their phone number to check if they already exist in the database.
2. If the user does not exist, collect their:
- Full Name
- Address
- Email
- Zip Code
- City
- Phone Number
- Service Request
Ask one question at a time, keeping the conversation natural and short.

3. Ask the user for their preferred appointment date and time.
- Check the database to see if that slot is available.
- If it's not available, suggest alternative free slots for that day.

4. Once the appointment is booked, provide a brief summary with the date, time, and service.

5. Then ask, “Would you like to exit the chat?” If yes, end the conversation politely.

If the user asks something out of scope, respond with:
> "I don't know about it."

Keep responses short, friendly, and focused on completing the appointment booking.
Use the provided tools for searching, creating and booking appointments
"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])



# Chat history
messages = [SystemMessage(content=prompt)]

def chatbot(query, messages):
    messages.append(HumanMessage(content=query))
    result = llm.invoke(messages)
    messages.append(AIMessage(content=result.content))
    print(f"🤖 {result.content}")
    return result.content

def input_with_timeout(prompt, timeout):
    user_input = [None]
    def get_input():
        user_input[0] = input(prompt)
    t = threading.Thread(target=get_input)
    t.start()
    t.join(timeout)
    if t.is_alive():
        print("\n⏳ Timeout reached. No input received.")
        return None
    return user_input[0]

def run_chat():
    print("Welcome to MKARD Landscaping & Tree Care Services! Type 'exit' anytime to quit.\n")
    while True:
        user_input = input_with_timeout("You: ", timeout=300)
        if user_input is None or user_input.strip().lower() in ['exit', 'quit', 'done', 'complete']:
            print("🤖 Thank you! Have a great day. 🌿")
            break
        chatbot(user_input, messages)

# Run the chatbot loop
run_chat()

