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


# ============================ IMPORTANT KNOWLEDGE ==========================
"""
Generator Type Hinting + how it works + how yield, send and return can be used
to make sure full potential of python is being used
"""

from typing import Generator, TypeAlias

YieldType: TypeAlias = str
SendType: TypeAlias = str
ReturnType: TypeAlias = str

def generator() -> Generator[YieldType, SendType, ReturnType]:
    result1 = yield "santo"
    print(result1, "is yielded")
    result2: str = yield "sajan"
    print(result1, result2, "are yielded")
    result3: str = yield "saly"
    print(result1, result2, result3, "are yielded")
    return "complete"

gen = generator()

value_yielded = next(gen)
print(f"Received (value_yielded) BEFORE while loop")
while True:
    try:
        value_yielded = gen.send(value_yielded)
        print (f"Received (value yielded) inside while loop")
    except StopIteration as e:
        print("StopIteration occured")
        print(f"RETURNED the value {e.value}")
        break

"""OUTPUT

Received (value_yielded) BEFORE while loop
santo is yielded
Received (value yielded) inside while loop
santo sajan are yielded
Received (value yielded) inside while loop
santo sajan saly are yielded
StopIteration occured
RETURNED the value complete

"""
