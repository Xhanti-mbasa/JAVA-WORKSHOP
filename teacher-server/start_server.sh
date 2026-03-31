#!/bin/bash

echo "Starting your LMS Grading Bot..."

# Ensure we are in the correct directory
cd "$(dirname "$0")"

# 1. Activate the virtual environment
if [ ! -d "../venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ../venv
fi
source ../venv/bin/activate

# 2. Install requirements if not already installed
echo "Checking requirements..."
pip install -r requirements.txt -q

# 3. Kill any previously running server on port 5000 to avoid conflicts
fuser -k 5000/tcp 2>/dev/null

# 4. Start the python server secretly in the background
echo "Starting Python Server..."
python3 server.py &
SERVER_PID=$!

echo "Python server started in background (PID: $SERVER_PID)"
echo ""
echo "=========================================================="
echo "= SECURE PUBLIC URL (localtunnel)                       ="
echo "=========================================================="
echo "Starting localtunnel. Please copy the URL below and paste"
echo "it into your student-repo/.github/workflows/notify-teacher.yml"
echo "It usually looks like https://<random-words>.loca.lt"
echo ""
echo "Press CTRL+C anytime to securely shut down everything."
echo "=========================================================="
echo ""

# 5. Bring up localtunnel in the foreground so they can see the link and stop the script easily
npx localtunnel --port 5000

# When localtunnel is closed (CTRL+C), clean up the python server
kill $SERVER_PID
echo "Server closed."
