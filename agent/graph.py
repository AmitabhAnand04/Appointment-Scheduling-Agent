import os
import sqlite3
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from agent.state import AppointmentState 
from tools.find_patient import find_patient
from tools.create_patient import create_patient
from tools.get_doctors_by_speciality import search_doctors
from tools.get_available_slots import get_available_slots
from tools.book_appointment import book_appointment
from tools.cancel_appointment import cancel_appointment
from tools.reschedule_appointment import reschedule_appointment
from tools.helper_tools import fill_state_tool, extract_state_tool, get_current_datetime_tool
from prompt import AGENT_PROMPT
# AGENT_PROMPT=os.getenv("AGENT_PROMPT")
llm = ChatGoogleGenerativeAI(model=os.getenv("AGENT_LLM"))

# Define path depending on environment
if os.getenv("WEBSITE_SITE_NAME"):
    # Running on Azure Web App
    db_path = "/home/chat_memory.db"
else:
    # Running locally
    db_path = "chat_memory.db"

print(f"DB Path = {db_path}")
conn = sqlite3.connect(db_path, check_same_thread=False)

tools = [find_patient, create_patient, search_doctors, get_available_slots, book_appointment, cancel_appointment, reschedule_appointment, fill_state_tool, extract_state_tool, get_current_datetime_tool]
llm_with_tools = llm.bind_tools(tools)
# System message
sys_msg = SystemMessage(
    content= AGENT_PROMPT
)
# Node
def assistant(state: AppointmentState):
    # print("Assistant node started!!")
    messages = [sys_msg] + state["messages"]
    # for m in messages:
    #     m.pretty_print()
    return {"messages": state["messages"] + [llm_with_tools.invoke(messages)]}

# Graph
builder = StateGraph(AppointmentState)

# Define nodes: these do the work
builder.add_node("assistant", assistant, include_signature=False)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
# builder.add_edge("tools", "assistant")
builder.add_edge("tools", "assistant")
builder.add_edge("assistant", END)
memory = SqliteSaver(conn)
react_graph = builder.compile(checkpointer=memory)