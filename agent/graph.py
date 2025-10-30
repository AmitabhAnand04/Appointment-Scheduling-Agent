import os
import sqlite3
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from agent.state import AppointmentState 
AGENT_PROMPT=os.getenv("AGENT_PROMPT")
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

#Tool Nodes Start Here

#Tools Nodes End Here
tools = []
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
    return {"messages": state["messages"] + [state["email"]]+ [llm_with_tools.invoke(messages)]}

# Graph
builder = StateGraph(AppointmentState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
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