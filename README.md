# CodeTutorGPT

This project is an interactive programming language tutor, designed to teach users a language through a series of interactive lessons. The AI tutor provides explanations, examples, and tasks for users to complete in order to gain a deeper understanding of the language. The project's folder structure, scripts, and files are outlined below.

[Demo video](https://www.youtube.com/watch?v=oABUJiTbm-k)

## To-do

[ ] Add memory/context of user's current knowledge.

[ ] Support for multiple languages, make it more modular to allow for easy adding of new languages

[ ] Embedding spaces for languages/user context?

# CodeTutorGPT

CodeTutorGPT is an interactive programming language tutor based on the book It provides concise lessons, assigns coding tasks to test users' understanding, and offers tailored feedback on their progress.

## Features

- Encourages active learning
- Automatic code compilation and execution
- Code and error feedback
- User interaction through `user_feedback.py`

## How to Use

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the main script. `python main.py`
4. Modify the 'lesson.c' file to complete the assigned tasks.
5. User the 'user_feedback.py' chat or 'user_feedback.txt' to communicate with the tutor.
6. Monitor the output for feedback from the AI tutor.
7. To provide feedback or interact with the tutor, use `user_feedback.py`.

## Dependencies

- GCC (for compiling C code)

## License

This project is released under the MIT License.
