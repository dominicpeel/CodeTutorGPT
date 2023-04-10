import subprocess
import os
import re
from pygments import highlight
from pygments.formatters import TerminalFormatter
from colorama import Fore, init

init(autoreset=True)

# base language class
class Language:
    def __init__(self):
        self.lexer = self.init_lexer() 

    def init_lexer(self):
        raise NotImplementedError("Subclasses must implement this method")

    def syntax_highlight(self, text):
        if self.lexer is None:
            return text

        code_regex = r'```(.*?)```'
        highlighted_text = ""

        last_match_end = 0
        for match in re.finditer(code_regex, text, re.DOTALL):
            code = match.group(1)
            highlighted_code = highlight(code, self.lexer(), TerminalFormatter())

            highlighted_text += text[last_match_end:match.start()] + highlighted_code
            last_match_end = match.end()

        highlighted_text += text[last_match_end:]
        return highlighted_text

    def get_modified_time(self):
        return NotImplementedError("Subclasses must implement this method")

    def run(self):
        raise NotImplementedError("Subclasses must implement this method")

# C language class
class CLanguage(Language):
    def init_lexer(self):
        from pygments.lexers import CLexer
        return CLexer

    def get_modified_time(self):
        return os.path.getmtime("lessons/lesson.c")

    def run(self):
        file_path = "lessons/lesson"
        with open(f"{file_path}.c", "r") as f:
            code = f.read()

        compile_result = subprocess.run(
            ["gcc", "-o", file_path, f"{file_path}.c"], 
            capture_output=True, 
            text=True
        )
        if compile_result.returncode != 0:
            print(Fore.RED + "Compilation failed:")
            print(compile_result.stderr)
            return f"Code: {code}\nCompilation failed: {compile_result}"

        run_result = subprocess.run(
            [f"./{file_path}"], 
            capture_output=True, 
            text=True
        )

        if run_result.returncode != 0:
            print(Fore.RED + "Program execution failed:")
            print(run_result.returncode)
            print(run_result.stderr)
        else:
            print(Fore.GREEN + "Program output:")
            print(run_result.stdout)

        return f"Code: {code}\nProgram output: {run_result}"

# Python language class
class PythonLanguage(Language):
    def init_lexer(self):
        from pygments.lexers import PythonLexer
        return PythonLexer

    def get_modified_time(self):
        return os.path.getmtime("lessons/lesson.py")

    def run(self):
        file_path = "lessons/lesson"
        with open(f"{file_path}.py", "r") as f:
            code = f.read()

        run_result = subprocess.run(
            ["python", f"{file_path}.py"], 
            capture_output=True, 
            text=True
        )

        if run_result.returncode != 0:
            print(Fore.RED + "Program execution failed:")
            print(run_result.returncode)
            print(run_result.stderr)
        else:
            print(Fore.GREEN + "Program output:")
            print(run_result.stdout)

        return f"Code: {code}\nProgram output: {run_result}"

def get_language(language_name):
    if language_name == "c":
        return CLanguage()
    elif language_name == "python":
        return PythonLanguage()
    else:
        return None
