import os
import json
import subprocess
import time
from colorama import Fore, Style, init
from chat import chat

# Automatically reset the console color after each print statement
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


def monitor_changes(prompt, chapter, topic, file_path='lesson'):

    message_history = [("user", f"{chapter=} {topic=}")]
    response = chat(
        prompt,
        message_history
    )
    print(Fore.GREEN + "Tutor: " + Fore.RESET + response)
    message_history.append(("assistant", response))

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
                print(Fore.GREEN + "User: " + user_feedback)
                message_history.append(("user", user_feedback))
            elif current_modified_time > last_modified_time:
                last_modified_time = current_modified_time
                print(Fore.YELLOW + "File modified")

                # open code
                with open(f"{file_path}.c") as f:
                    code = f.read()

                # compile code
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
            print(Fore.GREEN + "Tutor: " + Fore.RESET + response)
            message_history.append(("assistant", response))

            if "NEXT" in response:
                break

        except KeyboardInterrupt:
            print(Fore.RED + "KeyboardInterrupt")
            exit()


if __name__ == "__main__":
    with open('memory.json') as f:
        memory = json.load(f)
    with open('prompt.txt') as f:
        system_prompt = f.read()
    with open('chapters/chapter_titles.txt') as f:
        chapter_titles = f.read()

    chapter = memory['chapter']
    topic = memory['topic']

    with open(f"chapters/chapter{chapter}.txt") as f:
        topics = f.read()

    prompt = system_prompt + chapter_titles + topics

    while True:
        print(Fore.CYAN + f"Chapter {chapter}, Topic {topic}")

        monitor_changes(prompt, chapter, topic)

        topic += 1
        # memory['topic'] = topic

        # with open('memory.json', 'w') as f:
        #     json.dump(memory, f)
