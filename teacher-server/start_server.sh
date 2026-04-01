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
echo "  Your LMS server is now running."
echo "=========================================================="
echo ""
echo "  A public URL will appear below. Copy the https://... URL"
echo "  and paste it into student-repo/.github/workflows/notify-teacher.yml"
echo "  (append /webhook to the end of it)."
echo ""
echo "  Press CTRL+C to shut everything down."
echo ""
echo "=========================================================="
echo ""

# 5. Use SSH tunnel via localhost.run (no install needed)
ssh -o StrictHostKeyChecking=no -R 80:localhost:5000 nokey@localhost.run

# When tunnel is closed (CTRL+C), clean up the python server
kill $SERVER_PID 2>/dev/null
echo "Server closed."
