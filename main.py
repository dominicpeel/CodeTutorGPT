import os
import subprocess
import time
from colorama import Fore, init
from chat import chat
import re
from pygments import highlight
from pygments.lexers import CLexer 
from pygments.formatters import TerminalFormatter

init(autoreset=True)

def compile_code(file_path):
    compile_result = subprocess.run(
        ["gcc", "-o", file_path, f"{file_path}.c"], capture_output=True, text=True)
    if compile_result.returncode != 0:
        print(Fore.RED + "Compilation failed:")
        print(compile_result.stderr)
        return {"success": False, "compile_result": compile_result}
    return {"success": True}

def run(file_path):
    run_result = subprocess.run(
        [f"./{file_path}"], capture_output=True, text=True)
    if run_result.returncode != 0:
        print(Fore.RED + "Program execution failed:")
        print(run_result.returncode)
        print(run_result.stderr)
        # feed stderr and code to GPT-4
    else:
        print(Fore.GREEN + "Program output:")
        print(run_result.stdout)
    return run_result

def format_response(text):
    code_regex = r'```(.*?)```'
    highlighted_text = ""

    last_match_end = 0
    for match in re.finditer(code_regex, text, re.DOTALL):
        code = match.group(1)
        highlighted_code = highlight(code, CLexer(), TerminalFormatter())

        highlighted_text += text[last_match_end:match.start()] + highlighted_code
        last_match_end = match.end()

    highlighted_text += text[last_match_end:]
    return highlighted_text

def monitor(prompt, file_path='lesson'):
    message_history = [("assistant", 'Welcome to CodeTutorGPT! What would you like to learn today?')]
    print(Fore.CYAN + "Tutor: " + Fore.RESET + message_history[0][1])

    last_modified_time = os.path.getmtime(f"{file_path}.c")
    last_modified_user_feedback_time = os.path.getmtime('user_feedback.txt')
    while True:
        try:
            current_modified_time = os.path.getmtime(f"{file_path}.c")
            current_modified_user_feedback_time = os.path.getmtime(
                'user_feedback.txt')
            if current_modified_user_feedback_time > last_modified_user_feedback_time:
                last_modified_user_feedback_time = current_modified_user_feedback_time
                print(Fore.YELLOW + "User feedback file modified")
                with open('user_feedback.txt') as f:
                    user_feedback = f.read()
                print(Fore.GREEN + "User: " + Fore.RESET + user_feedback)
                message_history.append(("user", user_feedback))
            elif current_modified_time > last_modified_time:
                last_modified_time = current_modified_time
                print(Fore.YELLOW + "File modified")

                with open(f"{file_path}.c") as f:
                    code = f.read()

                compile_result = compile_code(file_path)
                if compile_result["success"]:
                    run_result = run(file_path)
                    message_history.append(
                        ("user", f"Run result: {run_result}\nlesson.c: {code}"))
                else:
                    message_history.append(
                        ("user", f"Failed to compile: {compile_result['compile_result']}\nlesson.c: {code}"))

                response = chat(
                    prompt,
                    message_history
                )
            else:
                time.sleep(0.5)
                continue

            response = chat(prompt, message_history)
            print(Fore.CYAN + "Tutor: " + Fore.RESET + format_response(response)) 
            message_history.append(("assistant", response))
        except KeyboardInterrupt:
            print(Fore.RED + "KeyboardInterrupt")
            exit()


if __name__ == "__main__":
    with open('prompt.txt') as f:
        system_prompt = f.read()
    with open('chapters.txt') as f:
        chapters = f.read()

    prompt = system_prompt + chapters

    while True:
        monitor(prompt)
