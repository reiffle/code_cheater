import os
from openai.types.chat import ChatCompletionFunctionToolParam

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path=os.path.abspath(working_directory)
        raw_path=os.path.join(abs_path, directory)
        full_path=os.path.normpath(raw_path)
        is_valid=os.path.commonpath([full_path, abs_path])==abs_path
        if not is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory\n'
        file_info=[]
        file_list=os.listdir(full_path)
        for file in file_list:
            file_dict={}
            file_dict["name"]=file
            is_path=os.path.join(full_path, file)
            file_dict["size"]=os.path.getsize(is_path)
            file_dict["is_directory"]=os.path.isdir(is_path)
            file_info.append(file_dict)
        info_str="\n".join(map(lambda x: f"- {x["name"]}: file_size={x["size"]}, is_dir={x["is_directory"]}", file_info)) 
        intro_str=""
        if directory==".":
            intro_str="Result for current directory:\n"
        else:
            intro_str=f"Result for '{directory}' directory:\n"
        return intro_str + info_str + "\n"
    except Exception as e:
        return f"Error: {e}\n"

#JSON descriptor for LLM
schema_get_files_info: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["directory"],
        },
    },
}
