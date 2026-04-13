from typing import Callable

from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langgraph.runtime import Runtime
from langchain.agents import AgentState

from utils.log_handler import logger
from utils.prompt_loader import load_report_prompt, load_system_prompt

@wrap_tool_call
def monitor_tool(
    # request data wrap
    request: ToolCallRequest,
    # excute function
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
)->ToolMessage | Command:
    logger.info(f"[tool monitor] excute tools{request.tool_call['name']}")
    logger.info(f"[tool monitor] excute tools{request.tool_call['args']}")
    try:
        res = handler(request)
        logger.info(f"[tool monitor] tool {request.tool_call["name"]} use success")
        if request.tool_call["name"] == "fill_context_for_report":
            request.runtime.context["report"] = True
    except Exception as e:
        logger.error(f"[tool monitor] tool {request.tool_call["name"]} use error, reason is {str(e)}")
        raise e
    return res

@before_model
def log_before_model(
    # recoder whole agent state
    state:AgentState,
    # recoder agent context info
    runtime: Runtime,
):
    logger.info(f"[before model] next use model, bring {len(state["messages"])} message")
    logger.debug(f"[before model] msg: {state["messages"][-1].content.strip()}, msg type: {type(state["messages"][-1]).__name__}")

@dynamic_prompt # before evert time use prompt, use this function
def report_prompt_switch(
    request: ModelRequest
):
    is_report = request.runtime.context.get("report", False)
    if is_report:
        return load_report_prompt()
    return load_system_prompt()
