import os
import re
import json
import subprocess
import tempfile
import shutil
import requests
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file in the same directory
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

app = Flask(__name__)

# ─── Configuration ────────────────────────────────────────────────────────────
TEACHER_DIR       = os.path.dirname(os.path.abspath(__file__))
HIDDEN_TESTS_DIR  = os.path.join(TEACHER_DIR, 'hidden-tests')
GITHUB_TOKEN      = os.getenv("GITHUB_PAT")          # Your GitHub Personal Access Token
GITHUB_API_BASE   = "https://api.github.com"
# ──────────────────────────────────────────────────────────────────────────────


def post_commit_comment(repo: str, commit_sha: str, body: str):
    """Post a comment on a specific commit via the GitHub API."""
    if not GITHUB_TOKEN:
        print("⚠️  GITHUB_PAT not set in .env — skipping GitHub comment.")
        return

    url     = f"{GITHUB_API_BASE}/repos/{repo}/commits/{commit_sha}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept":        "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = requests.post(url, headers=headers, json={"body": body})

    if resp.status_code == 201:
        print(f"✅  Comment posted on commit {commit_sha[:7]}")
    else:
        print(f"❌  Failed to post comment ({resp.status_code}): {resp.text}")


def parse_maven_results(stdout: str):
    """
    Parse `mvn test` stdout into structured info.
    Returns a dict with keys:
        passed, failed, errors, skipped, total, failures (list of test names)
    """
    result = {
        "passed":   0,
        "failed":   0,
        "errors":   0,
        "skipped":  0,
        "total":    0,
        "failures": [],          # individual failed/errored test names
        "raw_summary": [],       # "Tests run: ..." lines
    }

    for line in stdout.splitlines():
        # Summary lines look like:
        #   Tests run: 5, Failures: 1, Errors: 0, Skipped: 0
        m = re.search(
            r"Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+),\s*Skipped:\s*(\d+)",
            line,
        )
        if m:
            total    = int(m.group(1))
            failures = int(m.group(2))
            errors   = int(m.group(3))
            skipped  = int(m.group(4))
            passed   = total - failures - errors - skipped

            result["total"]   += total
            result["failed"]  += failures
            result["errors"]  += errors
            result["skipped"] += skipped
            result["passed"]  += passed
            result["raw_summary"].append(line.strip())

        # Individual failure lines look like:
        #   testRobotMovement(oop.workshop.RobotTest)  Time elapsed: ...  <<< FAILURE!
        #   testRobotMovement(oop.workshop.RobotTest)  Time elapsed: ...  <<< ERROR!
        if "<<< FAILURE!" in line or "<<< ERROR!" in line:
            test_match = re.match(r"\s*([\w]+)\([\w.]+\)", line)
            if test_match:
                result["failures"].append(test_match.group(1))

    return result


def build_github_comment(repo: str, commit_sha: str, stats: dict, overall_passed: bool) -> str:
    """Build a nicely formatted Markdown comment body for GitHub."""
    short_sha = commit_sha[:7]
    status_icon = "✅" if overall_passed else "❌"
    headline   = "All tests passed!" if overall_passed else "Some tests failed."

    lines = [
        f"## {status_icon} Teacher Bot — Grading Report (`{short_sha}`)",
        "",
        f"**{headline}**",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| ✅ Passed  | {stats['passed']}  |",
        f"| ❌ Failed  | {stats['failed']}  |",
        f"| 💥 Errors  | {stats['errors']}  |",
        f"| ⏭️ Skipped | {stats['skipped']} |",
        f"| 📦 Total   | {stats['total']}   |",
    ]

    if stats["failures"]:
        lines += [
            "",
            "### ❌ Failing Tests",
            "",
        ]
        for name in stats["failures"]:
            lines.append(f"- `{name}`")

    lines += [
        "",
        "---",
        "*Automated grading by Teacher Bot · Push a new commit to re-run the tests.*",
    ]

    return "\n".join(lines)


@app.route('/', methods=['GET'])
def index():
    return "LMS Bot Server is running! Configure your GitHub webhook to point to /webhook."


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    if not data:
        return {"status": "error", "message": "No data received"}, 400

    repo   = data.get('repo')
    branch = data.get('branch', 'main')
    commit = data.get('commit', 'HEAD')

    if not repo:
        return {"status": "error", "message": "Repository not specified"}, 400

    print(f"\n--- New submission from {repo} ---")
    print(f"    Branch : {branch}")
    print(f"    Commit : {commit}")

    overall_passed = False
    stats = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_url = f"https://github.com/{repo}.git"

        # ── Clone student repo ──────────────────────────────────────────────
        print(f"\n[1/3] Cloning {clone_url} ...")
        try:
            subprocess.run(
                ["git", "clone", clone_url, temp_dir],
                check=True, capture_output=True
            )
        except subprocess.CalledProcessError as e:
            print("❌  Clone failed:")
            print(e.stderr.decode('utf-8'))
            _comment_error(repo, commit, "Could not clone your repository. Is it public?")
            return {"status": "error", "message": "Failed to clone repo"}, 500

        # Detect if the project lives inside a student-repo/ sub-folder
        project_dir = temp_dir
        if os.path.exists(os.path.join(temp_dir, 'student-repo')):
            project_dir = os.path.join(temp_dir, 'student-repo')

        # ── Inject hidden tests ─────────────────────────────────────────────
        print("[2/3] Injecting hidden tests ...")
        student_test_dir = os.path.join(project_dir, 'src', 'test')
        os.makedirs(student_test_dir, exist_ok=True)

        shutil.copytree(
            os.path.join(HIDDEN_TESTS_DIR, 'src', 'test', 'java'),
            os.path.join(student_test_dir, 'java'),
            dirs_exist_ok=True,
        )

        # ── Run Maven tests ─────────────────────────────────────────────────
        print("[3/3] Running Maven tests ...")
        try:
            result = subprocess.run(
                ["mvn", "test"],
                cwd=project_dir,
                capture_output=True,
                text=True,
            )
            overall_passed = (result.returncode == 0)
            stats = parse_maven_results(result.stdout)

            # Print summary to teacher terminal
            print("\n─── RESULTS ───────────────────────────────────────")
            for summary_line in stats["raw_summary"]:
                print("  " + summary_line)
            if stats["failures"]:
                print("  Failing tests:")
                for name in stats["failures"]:
                    print(f"    • {name}")
            verdict = "✅  PASSED" if overall_passed else "❌  FAILED"
            print(f"\n  Overall: {verdict}")
            print("────────────────────────────────────────────────────\n")

        except FileNotFoundError:
            print("❌  Maven (mvn) is not installed or not in PATH.")
            _comment_error(repo, commit, "Server error: Maven is not installed on the teacher's machine.")
            return {"status": "error", "message": "mvn not found"}, 500
        except Exception as e:
            print(f"❌  Unexpected error: {e}")
            _comment_error(repo, commit, f"Server error: {e}")
            return {"status": "error", "message": str(e)}, 500

    # ── Post GitHub commit comment ──────────────────────────────────────────
    comment_body = build_github_comment(repo, commit, stats, overall_passed)
    post_commit_comment(repo, commit, comment_body)

    return {"status": "success", "passed": overall_passed}


def _comment_error(repo: str, commit: str, message: str):
    """Post a simple error comment if grading could not complete."""
    body = (
        "## ⚠️ Teacher Bot — Grading Error\n\n"
        f"{message}\n\n"
        "Please contact your teacher if this problem persists."
    )
    post_commit_comment(repo, commit, body)


if __name__ == '__main__':
    print("Teacher Server started.")
    if not GITHUB_TOKEN:
        print("⚠️  WARNING: GITHUB_PAT is not set in teacher-server/.env")
        print("    Grading will still run, but no commit comments will be posted.")
    print("\nForward port 5000 using ngrok:")
    print("  ngrok http 5000")
    print("Update the URL in student-repo/.github/workflows/notify-teacher.yml\n")
    app.run(host='0.0.0.0', port=5000)
