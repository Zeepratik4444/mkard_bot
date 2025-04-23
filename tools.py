from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent, ToolExecutor
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import os
from database import check_user, create_user, book_appointment

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# 1. Define tools using LangChain's decorator
@tool
def CheckUser(phone: str) -> str:
    return check_user(phone)

@tool
def CreateUser(data: str) -> str:
    """data: 'Full Name, Address, Email, Zip Code, City, Phone, Service'"""
    parts = data.split(",")
    if len(parts) < 7:
        return "Invalid user data"
    return create_user(*[p.strip() for p in parts])

@tool
def BookAppointment(data: str) -> str:
    """data: 'Phone Number, Date, Time'"""
    parts = data.split(",")
    if len(parts) < 3:
        return "Invalid appointment data"
    return book_appointment(*[p.strip() for p in parts])

# 2. Tool Executor
tools = [CheckUser, CreateUser, BookAppointment]
tool_executor = ToolExecutor(tools)

# 3. LLM
llm = ChatGroq(model="LLaMA3-8b-8192")

# 4. System Prompt
system_prompt = """
You are a friendly assistant helping users book landscaping appointments.

Steps:
1. Ask for the user's phone number. Use CheckUser.
2. If not found, collect Full Name, Address, Email, Zip Code, City, Phone, Service, and use CreateUser.
3. Ask for appointment date and time. Use BookAppointment.
4. Confirm the booking and exit.

Only use tools when needed. Respond short, helpful, and conversational.
"""

# 5. Agent
agent_runnable = create_react_agent(llm, tools, system_prompt)

# 6. Define LangGraph State
def run_agent(data):
    result = agent_runnable.invoke(data)
    return {"messages": data["messages"] + [result]}

# 7. Build Graph
graph = StateGraph()

graph.add_node("agent", RunnableLambda(run_agent))
graph.set_entry_point("agent")
graph.add_edge("agent", END)

graph_chatbot = graph.compile()

# 8. REPL for testing
def run_chat():
    print("Welcome to MKARD Landscaping 🌳 (LangGraph powered)")
    messages = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("🤖 Goodbye!")
            break
        messages.append(HumanMessage(content=user_input))
        state = {"messages": messages}
        result = graph_chatbot.invoke(state)
        ai_msg = result["messages"][-1]
        print(f"🤖 {ai_msg.content}")
        messages = result["messages"]

# Run it
if __name__ == "__main__":
    run_chat()
