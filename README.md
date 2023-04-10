# CodeTutorGPT

![Twitter Follow](https://img.shields.io/twitter/follow/dom_peely?style=social)

CodeTutorGPT is an interactive programming language tutor. It provides lessons, assigns coding tasks to test users' understanding, and offers tailored feedback on their progress.

![System diagram](https://pbs.twimg.com/media/FtXrE8FWAAsL6PH?format=png&name=large)

[Demo video](https://www.youtube.com/watch?v=oABUJiTbm-k)

## Features

- Encourages active learning
- Automatic code compilation and execution
- Code and error feedback
- User interaction through \`user_feedback.py\`

## How to Use

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the main script. `python src/main.py`
4. Modify the 'lesson.c' or 'lesson.py' file to complete the assigned tasks.
5. Use the 'user_feedback.py' chat or 'user_feedback.txt' to communicate with the tutor.
6. Monitor the output for feedback from the AI tutor.
7. To provide feedback or interact with the tutor, use `python src/user_feedback.py`.

## Dependencies

- GCC (for compiling C code)

## To-do

[ ] Config file to easily change language etc

[ ] Embedding spaces for languages/user context?

## License

This project is released under the MIT License.
