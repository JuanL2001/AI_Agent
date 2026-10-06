import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args != None:
            command.extend(args)
        run = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
        output_str = []
        if run.returncode != 0:
            output_str.append(f"Process exited with code {run.returncode}")
        if run.stdout == "" and run.stderr == "":
            output_str.append("No output produced")
        if run.stdout != "":
            output_str.append(f"STDOUT: {run.stdout}")
        if run.stderr != "":
            output_str.append(f"STDERR: {run.stderr}")
        return "\n".join(output_str)

    except Exception as e:
       return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}
