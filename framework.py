import sys
from types import ModuleType, FunctionType
from typing import Any, Dict
from importlib import import_module, reload
import inspect
from pathlib import Path
import pandas as pd


preset_input_params = {
    "sod": pd.DataFrame(),
    "eod": pd.DataFrame(),
    "ca": pd.DataFrame(),
    "proforma": pd.DataFrame()
}

# later change this function to any ways how we wanted
def get_param_value(param: str):
    return preset_input_params[param]

def get_variables(module: ModuleType) -> Dict:
    needed_vars = [i for i in dir(module) if not(i.startswith("__") or i.endswith("__"))]
    return {k: v for k, v in vars(module).items() if k in needed_vars}


def execute_function(fn: FunctionType) -> Any:
    # figuring out input params
    fn_sign = inspect.signature(fn)
    fn_params = fn_sign.parameters
    # fn_return_type = fn_sign.return_annotation

    # checking all parameters valid?
    invalid_params = []
    for param_name in fn_params.keys():
        if param_name not in preset_input_params.keys():
            invalid_params.append(param_name)
    if invalid_params:
        raise Exception("Invalid parameters found")

    # constructing kwargs
    kwargs = {param: get_param_value(param) for param in fn_params.keys()}
    return fn.__call__(**kwargs)


def execute_script_functions(scripts_dir):
    sys_path_for_scripts: str = str(scripts_dir.parent)
    if sys_path_for_scripts in sys.path:
        sys.path.remove(sys_path_for_scripts)
    sys.path.append(sys_path_for_scripts)
    scripts = list(scripts_dir.glob("*.py"))
    imports = {script.stem: import_module(f"{scripts_dir.name}.{script.stem}") for script in scripts}
    # reloading modules if dynamically get the changes applied
    imports = {k: reload(v) for k, v in imports.items()}
    modules: Dict[str, Dict[str, Any]] = {k: get_variables(v) for k, v in imports.items()}

    # executing functions avaialbel in scripts
    outputs = {}

    for script_name, fn_dict in modules.items():
        fn_outputs = {}
        for k, v in fn_dict.items():
            if isinstance(v, FunctionType) and k.startswith("exec_"):
                try:
                    fn_outputs[k] = execute_function(fn=v)
                except Exception as e:
                    fn_outputs[k] = {"ERR": f"Unable to run function due to: {e}"}
        outputs[script_name] = fn_outputs

    return outputs

if __name__ == "__main__":
    scripts_dir = Path(__file__).parent / ".temp" / "scripts"
    outputs = execute_script_functions(scripts_dir)
    print(outputs)