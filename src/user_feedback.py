while True:
    user_feedback = input("User feedback: ")
    with open('data/user_feedback.txt', 'w') as f:
        f.write(user_feedback)