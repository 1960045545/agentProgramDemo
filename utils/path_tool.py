import os

def get_project_root()->str:
    cur_path = os.path.abspath(__file__)
    cur_dir = os.path.dirname(cur_path) #os.path.dirname等同与../
    return os.path.dirname(cur_dir)

def get_abs_path(relative_path: str)->str:
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)


if __name__ == "__main__":
    print(get_abs_path("config\config.ini"))
