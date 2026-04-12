from config_handler import prompts_conf
from path_tool import get_abs_path
from log_handler import logger

def load_system_prompt():
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts] yaml have not main_prompt_path config")
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except KeyError as e:
        logger.error(f"[load_system_prompts] anlyse system prompt error:{str(e)}")
        raise e
    
def load_rag_prompt():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompt] yaml have not rag_summarize_prompt_path config")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except KeyError as e:
        logger.error(f"[load_rag_prompt] anlyse system prompt error:{str(e)}")
        raise e

def load_report_prompt():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompt] yaml have not report_prompt_path config")
        raise e

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except KeyError as e:
        logger.error(f"[load_report_prompt] anlyse system prompt error:{str(e)}")
        raise e
    
if __name__ == "__main__":
    print(load_system_prompt())
    print(load_rag_prompt())
    print(load_report_prompt())