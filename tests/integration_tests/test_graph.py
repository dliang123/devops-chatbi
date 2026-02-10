import pytest
from agent.graph import State, graph
from langchain_core.messages import HumanMessage

pytestmark = pytest.mark.anyio


# @pytest.mark.langsmith
async def test_agent_simple_passthrough() -> None:
    # inputs = {"changeme": "some_val"}
    inputs: State = {"messages": [HumanMessage(content="北京天气怎么样？")]}
    res = await graph.ainvoke(inputs)
    assert res is not None
