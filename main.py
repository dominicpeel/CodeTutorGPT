import os
import time
from colorama import Fore, init
from chat import chat
from languages import get_language

init(autoreset=True)

def context_agent(context_prompt, message_history):
    with open('user_context.txt', 'r') as f:
        user_context = f.read()
    history_string = ''
    for role, content in message_history[-5:]:
        if role == 'assistant':
            history_string += f"tutor: {content}, "
        else:
            history_string += f"student: {content}, "

    prompt = f"User context: {user_context}\nMessage history: {history_string} New user context:"
    new_context = chat(
        context_prompt,
        [("user", prompt)]
    ) 
    with open('user_context.txt', 'w') as f:
        f.write(new_context)
    return new_context 

def monitor(prompt, context_prompt, Language):
    message_history = []
    example = [
        ("assistant", "Welcome to CodeTutorGPT! What would you like to learn today?"),
        ("user", "pointers"),
        ("assistant", """Pointers are a fundamental concept in the C programming language. They allow you to manipulate memory directly, which can be incredibly powerful and efficient.

In C, a pointer is a variable that stores the memory address of another variable. You can use pointers to access and manipulate the value of the variable indirectly. Pointers are denoted by the * symbol and are declared with the data type of the variable they point to.

For example, to declare a pointer to an integer variable, you would write:

```
int *ptr;
```
This declares a pointer variable called ptr that can point to an integer value.

To get the address of a variable, you can use the & symbol. For example:

```
int num = 10;
int *ptr = &num;
```
This assigns the memory address of the integer variable num to the pointer ptr.

Now, let's try a coding task to test your understanding.

Write a program that declares an integer variable and a pointer to that variable. Assign a value to the integer variable, and then use the pointer to change the value of the integer variable to a new value. Finally, print the new value of the integer variable.

Save your program as 'lesson.c' and run it to see the output."""), 
 ('user', 'Run result: CompletedProcess(args=[\'./lesson\'], returncode=0, stdout=\'x = 5\\nx = 100\\n\', stderr=\'\')\nlesson.c: #include <stdio.h>\n\n#define PI 3.14159\n\nint main()\n{\n  int x = 5;\n  int *ptr = &x;\n  printf("x = %d\\n", x);\n  *ptr = 100;\n  printf("x = %d\\n", x);\n  return 0;\n}\n')    
    ]
    message_history.append(("assistant", 'Welcome to CodeTutorGPT! What would you like to learn today?'))
    print(Fore.CYAN + "Tutor: " + Fore.RESET + message_history[0][1])

    last_modified_time = Language.get_modified_time() 
    last_modified_user_feedback_time = os.path.getmtime('user_feedback.txt')
    while True:
        try:
            current_modified_time = Language.get_modified_time()
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

                print(Fore.YELLOW + "Program modified")

                message_history.append(("user", Language.run()))
            else:
                time.sleep(0.5)
                continue
            
            user_context = context_agent(context_prompt, message_history)
            response = chat(prompt+user_context, example+message_history)
            print(Fore.CYAN + "Tutor: " + Fore.RESET + Language.syntax_highlight(response)) 
            message_history.append(("assistant", response))
        except KeyboardInterrupt:
            print(Fore.RED + "KeyboardInterrupt")
            exit()


if __name__ == "__main__":
    with open('prompt.txt') as f:
        system_prompt = f.read()
    with open('context_prompt.txt') as f:
        context_prompt = f.read()

    language = 'python'
    Language = get_language(language)
    if Language is None:
        print(Fore.RED + f"Language {language} not supported")
        exit()

    prompt = system_prompt

    while True:
        monitor(prompt, context_prompt, Language)
