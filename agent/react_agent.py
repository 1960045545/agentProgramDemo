from langchain.agents import create_agent

from model.factory import chat_model
from utils.prompt_loader import load_system_prompt
from agent.tools.agent_tools import (rag_summarize, get_user_id, get_weater, 
                                     get_user_location, get_current_month,
                                     fetch_external_data, fill_context_for_report)
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch

class ReactAgent():
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_user_id, get_weater, 
                                     get_user_location, get_current_month,
                                     fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    def executer_stream(self, query: str):
        input = {
            "messages":[
                {"role":"user", "content":query}
            ]
        }
        for chunk in self.agent.stream(input, 
                          stream_mode="values", 
                          context={"report":False}
                          ):
            laste_msg = chunk["messages"][-1]
            if laste_msg.content:
                yield laste_msg.content.strip()+"\n"

if __name__ == "__main__":
    agent = ReactAgent()
    for chunk in agent.executer_stream("robot in my area tempory how to fix"):
        print(chunk, end="", flush=True)