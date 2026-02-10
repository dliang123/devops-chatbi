"""FastAPI application for the BI chat agent."""

import logging
import sys
from typing import Any, cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.globals import set_debug
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

from .agent.baseAgent import State, graph

app = FastAPI()

# 2. 开启 LangChain 详细调试模式
# 这会在终端打印出所有 LLM 的输入输出和 Node 的跳转
set_debug(True)

# 3. 配置标准日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("uvicorn")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    """Request model for the chat endpoint."""

    message: str


# In-memory history for demonstration. In a real app, use a database or session management.
history: list[BaseMessage] = []


@app.post("/chat")
async def chat(request: ChatRequest) -> Any:
    """Handle chat requests and interact with the LangGraph agent.

    Args:
        request: The chat request containing the user's message.

    Returns:
        A dictionary containing the AI's response.
    """
    global history
    logging.info({"message": request.message})

    # Add the human message to history
    history.append(HumanMessage(content=request.message))

    # Invoke the Langgraph graph
    # Note: For a real application, you'd manage conversation history per user/session.
    # This simple example just passes the current message and expects the graph to handle state.
    config: RunnableConfig = {
        "recursion_limit": 50
    }  # Add recursion limit as it is important
    try:
        response = await graph.ainvoke(
            cast(Any, cast(State, {"messages": history})), config
        )

        # Extract the AI's response
        ai_message = response["messages"][-1]
        if isinstance(ai_message, AIMessage):
            history.append(ai_message)  # Add AI message to history
            logging.info({"response": ai_message.content})
            return {"response": ai_message.content}
        else:
            return {"response": "An unexpected response type was received."}
    except Exception as e:
        logger.error(f"!!! 发生未知错误: {str(e)}", exc_info=True)
        return {"error": str(e)}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint of the FastAPI application.

    Returns:
        A dictionary with a welcome message.
    """
    return {"message": "FastAPI is running!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.app.main:app", host="127.0.0.1", port=8000, reload=True)
