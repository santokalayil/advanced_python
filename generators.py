import time
from typing import Callable
import streamlit as st



def render_ui_with_steps(fn: Callable, **kwargs):
    with st.status(f"Execution in progress...", expanded=True, state="running"):
        for out in fn(**kwargs):
            if isinstance(out, dict):
                if "message" in out.keys():
                    msg = out["message"]
                    st.write(msg)
                elif "output" in out.keys():
                    output = out["output"]
                    return output
                else:
                    raise ValueError("The passed function yields dictionary with unknown keys: supporded keys are `message` and `output`")  
            else:
                raise ValueError("Invalid yields found! The passed function does not output a dictionary")
        else:
            raise Exception("Some issue. For loop should have broken if it was working properly")


def process():
    for i in range(10):
        time.sleep(2)
        yield {"message": f"Message {i+1} here"}
    yield {"output": 1000}

dummy_out = "<not_initialized>"
returned_out = dummy_out
if st.button(f"Executing Process"):
    returned_out = render_ui_with_steps(process)
    
if returned_out != dummy_out:
    st.info(f"OUTPUT RETURNED IS {returned_out}")
