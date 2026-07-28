import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path=os.path.abspath(working_directory)
        raw_path=os.path.join(abs_path, file_path)
        full_path=os.path.normpath(raw_path)
        is_valid=os.path.commonpath([full_path, abs_path])==abs_path
        if not is_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_path, "r") as file:
            contents=file.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if file.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return contents
    except Exception as e:
        
        return f"Error: {e}"