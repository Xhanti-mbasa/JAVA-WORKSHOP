import os
import json
import subprocess
import tempfile
import shutil
from flask import Flask, request

app = Flask(__name__)

# Directory where the hidden test cases are stored locally
TEACHER_DIR = os.path.dirname(os.path.abspath(__file__))
HIDDEN_TESTS_DIR = os.path.join(TEACHER_DIR, 'hidden-tests')

@app.route('/', methods=['GET'])
def index():
    return "LMS Bot Server is running! Configure your GitHub webhook to point to /webhook."

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    if not data:
        return {"status": "error", "message": "No data received"}, 400
        
    repo = data.get('repo')
    branch = data.get('branch', 'main')
    commit = data.get('commit', 'HEAD')
    
    if not repo:
        return {"status": "error", "message": "Repository not specified"}, 400
        
    print(f"\n--- New code submitted from {repo} ---\nCommit: {commit}")
    
    # Create a temporary directory to clone and test
    with tempfile.TemporaryDirectory() as temp_dir:
        clone_url = f"https://github.com/{repo}.git"
        
        # Clone the student repo
        print(f"Cloning {clone_url}...")
        try:
            subprocess.run(["git", "clone", clone_url, temp_dir], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print("Failed to clone repository!")
            print(e.stderr.decode('utf-8'))
            return {"status": "error", "message": "Failed to clone repo"}, 500
            
        # Copy hidden tests into the student's repo
        student_test_dir = os.path.join(temp_dir, 'src', 'test')
        if not os.path.exists(student_test_dir):
            os.makedirs(student_test_dir)
            
        print("Copying hidden tests...")
        shutil.copytree(os.path.join(HIDDEN_TESTS_DIR, 'src', 'test', 'java'), 
                        os.path.join(student_test_dir, 'java'), 
                        dirs_exist_ok=True)
                        
        # Run maven tests
        print("Running tests with Maven...")
        try:
            result = subprocess.run(["mvn", "test"], cwd=temp_dir, capture_output=True, text=True)
            
            # Print output for the teacher to see
            print("--- MAVEN TEST RESULTS ---")
            
            # Extract just the summarized output or print all
            lines = result.stdout.split('\n')
            for line in lines:
                if "Tests run:" in line or "BUILD" in line:
                    print(line)
                    
            if result.returncode == 0:
                print("Student passed the tests!")
            else:
                print("Student failed some tests.")
                print("Error Details:")
                error_lines = result.stdout.split('\n')
                printing_errors = False
                for line in error_lines:
                    if "<<< FAILURE!" in line or "<<< ERROR!" in line:
                        print(line)
                        
        except FileNotFoundError:
            print("Maven (mvn) is not installed or not in PATH.")
        except Exception as e:
            print(f"Error running tests: {e}")
            
    print("--------------------------------------\n")
    return {"status": "success", "message": "Tests executed"}

if __name__ == '__main__':
    print("Teacher Server started. Forward port 5000 using ngrok:")
    print("ngrok http 5000")
    print("Make sure to update the URL in your student-repo/.github/workflows/lms-webhook.yml")
    app.run(host='0.0.0.0', port=5000)
