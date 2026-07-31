import os
import subprocess
from openai.types.chat import ChatCompletionFunctionToolParam


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    abs_path=os.path.abspath(working_directory)
    raw_path=os.path.join(abs_path, file_path)
    full_path=os.path.normpath(raw_path)
    is_valid=os.path.commonpath([full_path, abs_path])==abs_path
    try:
        if not is_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python3", full_path]
        if args:
            command.extend(list(args))
        result=subprocess.run(command, capture_output=True, text=True, cwd=abs_path, timeout=30)
        final_list=[]
        if result.returncode!=0:
            final_list.append(f"Process exited with code {result.returncode}")
        if result.stderr=="" and result.stdout=="":
            final_list.append("No output produced")
        if result.stdout:
            final_list.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            final_list.append(f"STDERR: {result.stderr}")
        return "\n".join(final_list)
    except Exception as e:
        return f"Error: executing Python file: {e}"

#JSON descriptor for LLM
schema_run_python_file: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file from the specified file path, relative to the working directory, along with any additional arguments required. The result is returned as a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path, relative to the working directory, to a python file.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Arguments supplied to the python file to be run.",
                }
            },

        "required": ["file_path"],
        },
    },
}
