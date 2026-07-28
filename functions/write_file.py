import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path=os.path.abspath(working_directory)
        raw_path=os.path.join(abs_path, file_path)
        full_path=os.path.normpath(raw_path)
        is_valid=os.path.commonpath([full_path, abs_path])==abs_path
        if not is_valid:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        part_path=os.path.dirname(full_path)
        os.makedirs(part_path, exist_ok=True) #create directories if they don't exist yet
        with open(full_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"