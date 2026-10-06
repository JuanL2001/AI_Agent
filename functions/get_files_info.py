import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        info = os.listdir(target_dir)
        directory_inf = []
        for name in info:
            file_name = name
            file_path = os.path.join(target_dir, name)
            dir_check = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            string = f"- {file_name}: file_size={file_size} bytes, is_dir={dir_check}"
            directory_inf.append(string)

        return "\n". join(directory_inf)

    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
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
        },
    },
}
