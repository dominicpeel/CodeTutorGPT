import os
import subprocess
import time
from colorama import Fore, init
import openai
from chat import chat
import pandas as pd
import ast
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = "gpt-3.5-turbo"
# model = "gpt-4"
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
    else:
        print(Fore.GREEN + "Program output:")
        print(run_result.stdout)
    return run_result

def monitor_changes(file_path='lesson'):
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
                return f"User: {user_feedback}" 
            elif current_modified_time > last_modified_time:
                last_modified_time = current_modified_time
                print(Fore.YELLOW + "File modified")

                # open code
                with open(f"{file_path}.c") as f:
                    code = f"Code:\n {f.read()}" 

                # compile code
                compile_result = compile_code(file_path)
                if compile_result["success"]:
                    run_result = run(file_path)
                    if run_result.returncode != 0:
                        return f"{code}\nExecution error: {run_result.stderr}"
                    return f"{code}\nExecution result: {run_result.stdout}" 
                else:
                    return f"{code}\nCompile error: {compile_result['compile_result'].stderr}"
            else:
                time.sleep(0.5)
                continue

        except KeyboardInterrupt:
            print(Fore.RED + "KeyboardInterrupt")
            exit()

def get_ada_embedding(text):
    text = text.replace("\n", " ")
    return openai.Embedding.create(
        input=[text], 
        model="text-embedding-ada-002"
    )["data"][0]["embedding"]

def getLanguageContext(query, k=2):
    embedded_query = get_ada_embedding(query) 

    try:
        language_df = pd.read_csv('data/embeddings.csv')
    except FileNotFoundError:
        print(Fore.RED + "No embeddings file found")
        exit() 

    language_embeddings = np.array(language_df['embedding'].apply(ast.literal_eval).tolist())
    
    # Calculate cosine similarity
    similarities = cosine_similarity([embedded_query], language_embeddings)[0]

    # Get the indices of the top k contexts
    top_k_indices = similarities.argsort()[-k:][::-1]

    # Return the top k contexts
    top_k_contexts = language_df.iloc[top_k_indices]['text']
    language_context_string = "\n".join(top_k_contexts)

    print(Fore.LIGHTBLUE_EX + "Language Context: " + Fore.RESET + language_context_string[:500] + "...")
    return language_context_string


def create_message(role, content):
    return {"role": role, "content": content}


def controller(controller_prompt, user_output, message_history):
    messages = []
    messages.append(create_message("system", controller_prompt))
    messages.append(create_message("user", user_output))

    getLangContext = 1
    controller_output = '' 
    while True:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )['choices'][0]['message']['content']
        
        print(Fore.CYAN + "Controller: " + Fore.RESET + response)

        command, arg = response.split(' ', 1)
        # parse controller response
        '''TO ADD
            - storeUserInfo 'text': Store user information in the user knowledge embedding space using the provided text.
            - getUserInfo 'query': Retrieve user information from the user knowledge embedding space based on the provided query.
        '''
        if command == "getLanguageContext":
            if getLangContext == 0:
                messages.append(create_message("user", "Error: getLanguageContext command used too many times"))
                print(Fore.RED + "getLanguageContext command used too many times") 
                continue
            getLangContext -= 1
            language_context = getLanguageContext(arg) 
            messages.append(create_message("user", language_context))
        elif command == "storeUserInfo":
            pass
        elif command == "getUserInfo":
            pass
        elif command == "sendPromptToUser":
            controller_output = arg[1:-1]
            break
        else:
            print(Fore.RED + "Unknown command")
            messages.append(create_message("user", "Error: Unknown command, please only use the following commands: getLanguageContext, sendPromptToUser")) 
            continue

    return controller_output

if __name__ == "__main__":
    with open('controller_prompt.txt') as f:
        controller_prompt = f.read()
    with open('tutor_prompt.txt') as f:
        tutor_prompt = f.read()

    message_history = [] 

    while True:
        user_output = monitor_changes()
        controller_output = controller(controller_prompt, user_output, message_history)
        print('Prompt sent to tutor...')
