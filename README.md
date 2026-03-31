# Local Java LMS Workshop System

This repository contains two main sections for your Java OOP Workshop:

## 1. `student-repo/`
These are the files you will upload to your public GitHub repository. Your students will **fork** your repository and fill in the missing code.

It contains:
- The 7 OOP units as incomplete code files, with simple instructions in the comments.
- A `pom.xml` for Java compilation and running JUnit tests (provided by the teacher).
- A `.github/workflows/notify-teacher.yml` file. This GitHub Action automatically triggers every time a student commits, sending their code link to your local machine!

## 2. `teacher-server/`
These are the files you keep on your personal PC. They contain the testing server, the hidden tests, and the final answer keys.

### How to run the local LMS grading server:
1. Make sure Python 3 is installed.
2. Install the requirements: `pip install -r requirements.txt`
3. Run the Python flask server: `python server.py`
4. The server runs on port 5000. Use ngrok to expose your local port so GitHub can reach it:
   ```bash
   ngrok http 5000
   ```
5. Copy the generated `https://...ngrok-free.app` URL and update the `TEACHER_WEBHOOK_URL` variable inside `student-repo/.github/workflows/notify-teacher.yml`. Then push `student-repo` to GitHub.

### How it works:
- Student forks your repo on GitHub.
- Student writes code and pushes it to their fork.
- The GitHub action defined in `notify-teacher.yml` runs on the student's repository and sends a POST request to your `ngrok` URL containing the student's repo name and commit.
- Your local Python server receives the request, `git clone`s the student's repository into a temporary folder, copies the tests from `teacher-server/hidden-tests` into it, and runs `mvn test`.
- The test results are instantly displayed on your local terminal!

### Answers
If you ever need the completed code, it is available inside `teacher-server/answers/oop/workshop`.

Good luck with the workshop!
