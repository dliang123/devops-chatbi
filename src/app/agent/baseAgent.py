"""LangGraph agent for BI chat functionality."""

import os
from typing import Annotated, Any, Literal, TypedDict, cast

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI
from langgraph.graph import (
    START,  # type: ignore
    StateGraph,
)
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pydantic import SecretStr


# 1. 定义状态 (State)
class State(TypedDict):
    """Represents the state of the LangGraph agent during a conversation."""

    messages: Annotated[list[BaseMessage], add_messages]
    current_intent: str | None
    generated_sql: str | None
    sql_check_result: str | None
    analysis_result: str | None


# 2. 定义工具 (Tools)
@tool(
    "recognize_intent",
    description="识别用户查询的意图，例如“销售额查询”、“用户增长分析”等。",
)
def recognize_intent(user_query: str) -> str:
    """识别用户查询的意图，例如“销售额查询”、“用户增长分析”等."""
    if "销售额" in user_query:
        return "sales_query"
    elif "用户增长" in user_query:
        return "user_growth_analysis"
    else:
        return "unknown_intent"


@tool("generate_sql", description="根据用户意图和查询生成 SQL 语句。")
def generate_sql(intent: str, user_query: str) -> str:
    """根据用户意图和查询生成 SQL 语句."""
    if intent == "sales_query":
        # In a real scenario, this would be more sophisticated, possibly using another LLM call or a rule-based system
        return "SELECT SUM(amount) FROM sales WHERE date >= 'last_week';"
    elif intent == "user_growth_analysis":
        return "SELECT region, COUNT(user_id) FROM users GROUP BY region;"
    else:
        return "SELECT 'Error: Could not generate SQL for unknown intent.'"


@tool("sql_checker", description="检查生成的 SQL 语句的语法和有效性.")
def sql_checker(sql_query: str) -> str:
    """检查生成的 SQL 语句的语法和有效性."""
    if "Error" in sql_query:
        return "SQL_ERROR: Generated SQL contains errors."
    elif "DROP TABLE" in sql_query.upper():  # Simple check for dangerous commands
        return "SQL_ERROR: Potentially dangerous SQL command."
    return "SQL_VALID"


@tool(
    "data_analyzer", description="执行 SQL 查询并对结果进行数据分析，返回自然语言摘要."
)
def data_analyzer(sql_query: str) -> str:
    """执行 SQL 查询并对结果进行数据分析，返回自然语言摘要."""
    if "SUM(amount)" in sql_query:
        return "上周销售额为 100 万美元，同比增长 10%。"
    elif "COUNT(user_id)" in sql_query:
        return "所有区域的用户增长都呈现稳定上升趋势，尤其是在亚太地区增长显著。"
    else:
        return "无法提供详细分析，请检查查询。"


tools: list[BaseTool] = [recognize_intent, generate_sql, sql_checker, data_analyzer]

tool_node = ToolNode(tools)


# 3. 初始化 Qwen 模型并绑定工具
def get_model() -> Runnable[Any, Any]:
    """Initialize and return the ChatOpenAI model bound with available tools."""
    load_dotenv()
    print("DASHSCOPE_API_KEY:" + os.getenv("DASHSCOPE_API_KEY", ""))
    print("DASHSCOPE_BASE_URL:" + os.getenv("DASHSCOPE_BASE_URL", ""))
    return ChatOpenAI(
        model=os.getenv("DASHSCOPE_MODEL", "qwen-plus"),
        api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY", "")),
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        temperature=0,
    ).bind_tools(tools)


# 4. 定义节点逻辑
def call_model(state: State) -> dict[str, list[AIMessage]]:
    """Call the language model with the current conversation history."""
    messages = state["messages"]

    response = get_model().invoke(messages)
    return {"messages": [response]}


def should_continue_after_intent(
    state: State,
) -> Literal["generate_sql_node", "__end__"]:
    """Determine the next step after intent recognition.

    If the intent is recognized and not 'unknown_intent', proceeds to SQL generation;
    otherwise, the graph ends.
    """
    # Assuming the intent recognition tool's output is captured in the messages.
    # We need to extract the intent from the last tool_call_result or from a specific state field
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        # Assuming the first tool call is recognize_intent
        for tool_call in last_message.tool_calls:
            if cast(Any, tool_call).name == "recognize_intent":
                # This is a simplified way to get the output. In a real scenario,
                # the tool node would execute and put the result in the state.
                # For now, let's just check the intent from a mock state field
                # or infer from the tool call itself if we were to process it here.
                pass  # The actual execution and state update will happen in the tool_node

    # For now, let's just use a placeholder for `current_intent` for routing
    if state.get("current_intent") and state["current_intent"] != "unknown_intent":
        return "generate_sql_node"
    return "__end__"  # End if intent is unknown or not set


def should_continue_after_sql_check(
    state: State,
) -> Literal["analyze_data_node", "generate_sql_node", "__end__"]:
    """Determine the next step after SQL checking.

    If the SQL is valid, proceeds to data analysis; if there are errors, attempts
    to re-generate SQL. Otherwise, the graph ends.
    """
    # We assume sql_check_result is set by a previous step (tool_node executing sql_checker)
    if state.get("sql_check_result") == "SQL_VALID":
        return "analyze_data_node"
    elif state.get("sql_check_result") == "SQL_ERROR":
        # If SQL has errors, try generating it again (simple retry mechanism)
        return "generate_sql_node"
    return "__end__"  # Fallback


# 5. 构建图 (Graph)
workflow = StateGraph(State)

# 定义节点
workflow.add_node("agent", call_model)  # The primary agent node that can call tools
workflow.add_node(
    "recognize_intent_tool", tool_node
)  # Tool node specifically for intent recognition
workflow.add_node(
    "generate_sql_tool", tool_node
)  # Tool node specifically for SQL generation
workflow.add_node(
    "check_sql_tool", tool_node
)  # Tool node specifically for SQL checking
workflow.add_node(
    "analyze_data_tool", tool_node
)  # Tool node specifically for data analysis


workflow.add_edge(START, "agent")

# Agent decides which tool to call.
# The `agent` node is responsible for invoking the tools.
# We'll need a conditional edge from 'agent' to 'recognize_intent_tool'
# for the initial tool call based on the input message.
# For simplicity, let's assume the first step is always intent recognition.
# We need to update `should_continue` logic to handle specific tool calls.

# Revised workflow:
# START -> agent (receives user query)
# agent -> recognize_intent_tool (agent calls recognize_intent)
# recognize_intent_tool -> agent (tool result comes back to agent)
# agent (now with intent) -> generate_sql_tool (agent calls generate_sql)
# generate_sql_tool -> agent (tool result comes back to agent)
# agent (now with SQL) -> check_sql_tool (agent calls sql_checker)
# check_sql_tool -> agent (tool result comes back to agent)
# agent (now with SQL check result) -> analyze_data_tool (if valid) OR generate_sql_tool (if error)
# analyze_data_tool -> agent (tool result comes back to agent)
# agent -> END (presents final answer)


def route_agent_to_tools(
    state: State,
) -> Literal[
    "recognize_intent_tool",
    "generate_sql_tool",
    "check_sql_tool",
    "analyze_data_tool",
    "__end__",
]:
    """Routes the agent's tool calls to the appropriate tool nodes."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        # Based on the tool call, route to the appropriate tool node
        # if cast(Any, last_message.tool_calls[0]).name == "recognize_intent":
        if last_message.tool_calls[0]["name"] == "recognize_intent":
            return "recognize_intent_tool"
        elif last_message.tool_calls[0]["name"] == "generate_sql":
            return "generate_sql_tool"
        elif last_message.tool_calls[0]["name"] == "sql_checker":
            return "check_sql_tool"
        elif last_message.tool_calls[0]["name"] == "data_analyzer":
            return "analyze_data_tool"
        else:
            return "__end__"  # Should not happen if tools are well-defined
    return "__end__"  # If agent doesn't call a tool, it's done or an error


def route_tools_to_agent_or_end(state: State) -> Literal["agent", "__end__"]:
    """Routes the result of a tool execution back to the agent for further processing or ends the graph."""
    # After a tool executes, the result comes back to the agent
    # The agent then decides the next step (another tool call or end)
    # For now, let's just route everything back to the agent for decision making
    return "agent"


workflow.add_conditional_edges("agent", route_agent_to_tools)
workflow.add_edge("recognize_intent_tool", "agent")
workflow.add_edge("generate_sql_tool", "agent")
workflow.add_edge("check_sql_tool", "agent")
workflow.add_edge("analyze_data_tool", "agent")

# The agent itself will decide when to end by not making any tool calls.
# The conditional edges from 'agent' will handle the flow.


# 编译 Graph
graph = workflow.compile()
