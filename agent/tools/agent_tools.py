from langchain.tools import tool
from rag.rag_service import RagSummarize

import random
import os

from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path
from utils.log_handler import logger

rag = RagSummarize()

user_ids = ["1001","1002","1003","1004","1005","1006","1007","1008","1009", "1010"]
months = ["2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12"]
external_data = {}

@tool(description="search refrence content")
def rag_summarize(query: str)->str:
    return rag.rag_summarize(query)

@tool(description="search today weather")
def get_weater(city:str)->str:
    return f"{city} weather is sunny"

@tool(description="get user localtion")
def get_user_location(city: str)->str:
    return random.choice(["hangzhou", "nantong", "wenzhou"])

@tool(description="get user id, return string")
def get_user_id()->str:
    return random.choice(user_ids)

@tool(description="get current month, return string")
def get_current_month()->str:
    return random.choice()

def generate_external_data():
    '''
    return {
        "user_id":{
            "mounth":{}
        }
    }
    '''
    if not external_data:
        abs_external_data = get_abs_path(agent_conf["external_data_path"])
        if not os.path.exists(abs_external_data):
            raise FileNotFoundError(f"external data {external_data} is not exist")
        with open(abs_external_data, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                line = line.strip()
                line_array: list[str] = line.split(",")
                
                user_id: str = line_array[0].replace('"', "")
                feater: str = line_array[1].replace('"', "")
                efficiency: str = line_array[2].replace('"', "")
                consumables: str = line_array[3].replace('"', "")
                comparision: str = line_array[4].replace('"', "")
                time: str = line_array[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id]={}
                external_data[user_id][time] = {
                    "feater":feater,
                    "efficiency":efficiency,
                    "consumables":consumables,
                    "comparision":comparision,
                }



@tool(description="get external user use info, return string, if not info return null")
def fetch_external_data(user_id: str, month:str)->str:
    generate_external_data()
    try:
        return external_data[user_id][month]
    except:
        logger.warning(f"[fetch_external_data] miss user:{user_id} in {month} recorde")
        return ""

if __name__ == "__main__":
    print(fetch_external_data("1002", "2025-04"))
