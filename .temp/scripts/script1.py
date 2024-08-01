from typing import Dict
import pandas as pd

# input_files = {
#     "sod": ""
# }
# reports = {}

def do_something():
    print("doing something")

# give comment what function does
def exec_this_check(sod: pd.DataFrame) -> Dict:
    do_something()
    report = {"check1": pd.DataFrame()} 
    return report
    

