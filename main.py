import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from uuid import uuid4
from agent.graph import react_graph  # ✅ Import your compiled graph

# -------------------- App Initialization --------------------
app = FastAPI(
    title="Appointment Scheduling Agent API",
    description="An intelligent assistant powered by Gemini + LangGraph for managing patient appointments.",
    version="1.0.0",
)

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


# -------------------- Helper --------------------
def invoke_graph(user_query: str, thread_id: str = None):
    """
    Invoke the compiled LangGraph agent graph with thread memory.
    """
    current_thread_id = thread_id or str(uuid4())
    human_message = HumanMessage(content=user_query)
    config = {"configurable": {"thread_id": current_thread_id}}

    # Call the compiled graph
    response = react_graph.invoke({"messages": [human_message]}, config)
    messages = response.get("messages", [])
    last_message = messages[-1] if messages else None
    # return last_message
    # content = getattr(last_message, "content", "")
    text = ""
    # if isinstance(last_message.get("content"), list) and len(last_message["content"]) > 0:
    #     first_item = last_message["content"][0]
    #     text = first_item.get("text", "")
    if last_message:
        content = last_message.content
        
        if isinstance(content, str):
            # Case 1: Simple string (direct model response)
            text = content
            
        elif isinstance(content, dict) and "text" in content:
            # Case 2: Dictionary with a direct 'text' key (common structured output)
            text = content["text"]
            
        elif isinstance(content, list) and content and isinstance(content[0], dict) and "text" in content[0]:
            # Case 3: List containing a dictionary, with 'text' inside the dictionary 
            # (This handles the specific format you provided: [{'type': 'text', 'text': '...'}])
            text = content[0]["text"]
            
        else:
            # Fallback: Convert to string to ensure nothing is lost, 
            # or handle edge cases where the content might be another type (like a ToolMessage object)
            text = str(content)
    print(text)


    # Prepare structured response
    return {
        "result": text,
        "message_state_length": len(messages),
        "all_messages_in_message_state": messages,
        "thread_id": current_thread_id
    }


# -------------------- API Endpoint --------------------
@app.post("/api/v1/chat")
async def chat_with_agent(request: Request):
    """
    POST endpoint to chat with the medical appointment assistant.

    Body:
    {
        "query": "I want to book an appointment with a cardiologist.",
        "thread_id": "optional-uuid"  // If continuing an existing conversation
    }
    """
    try:
        payload = await request.json()
        user_query = payload.get("query")
        thread_id = payload.get("thread_id")

        if not user_query:
            return JSONResponse(status_code=400, content={"error": "Missing 'query' field."})

        logging.info(f"Received query: {user_query} | Thread ID: {thread_id}")

        result = invoke_graph(user_query, thread_id)
        logging.info(f"Response generated for Thread {result['thread_id']}")

        # return JSONResponse(content=result)
        return result

    except Exception as e:
        logging.exception("Error during chat processing")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "message": "Internal server error"}
        )


# -------------------- Health Check --------------------
@app.get("/health")
async def health_check():
    """Simple health endpoint."""
    return {"status": "ok", "message": "Appointment Agent API is running."}


# -------------------- Run Command (for local testing) --------------------
# Use this only for local dev. In production, use gunicorn/uvicorn workers.
# Example: uvicorn main:app --host 0.0.0.0 --port 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
