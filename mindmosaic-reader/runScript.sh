#!/bin/bash

# ===============================================
# MindMosaic Local Reader Runner
# Runs both FastAPI backend and React frontend
# ===============================================

set -e  # Exit immediately on error

# ---- Configuration ----
BACKEND_DIR="./backend"
FRONTEND_DIR="./frontend"
BACKEND_PORT=8000
FRONTEND_PORT=3000
PY_ENV_NAME="myenv"

echo "🔧 Setting up MindMosaic Reader environment..."

# ---- CLEANUP EXISTING PROCESSES ----
echo ""
echo "🧹 Cleaning up existing processes..."

# Kill any existing processes on our ports
echo "   Stopping any existing backend on port $BACKEND_PORT..."
lsof -ti:$BACKEND_PORT | xargs kill -9 2>/dev/null || true

echo "   Stopping any existing frontend on port $FRONTEND_PORT..."
lsof -ti:$FRONTEND_PORT | xargs kill -9 2>/dev/null || true

# Kill any existing node/npm processes that might be related
echo "   Stopping any existing Node.js processes..."
pkill -f "react-scripts" 2>/dev/null || true
pkill -f "npm start" 2>/dev/null || true

echo "   Stopping any existing Python/FastAPI processes..."
pkill -f "uvicorn.*app:app" 2>/dev/null || true

# Small delay to ensure processes are fully terminated
sleep 2

# ---- BACKEND SETUP ----
echo ""
echo "🚀 Setting up FastAPI backend..."
cd "$BACKEND_DIR"

# Create Python virtual environment if missing
if [ ! -d "$PY_ENV_NAME" ]; then
  echo "⚙️  Creating Python virtual environment ($PY_ENV_NAME)..."
  python3 -m venv "$PY_ENV_NAME"
fi

# Activate the environment
source "$PY_ENV_NAME/bin/activate"

# Install dependencies
echo "📦 Installing Python dependencies (FastAPI, Uvicorn, Pydantic, Groq)..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run backend in background
echo "▶️  Launching backend on port $BACKEND_PORT..."
uvicorn app:app --host 127.0.0.1 --port "$BACKEND_PORT" --reload &
BACKEND_PID=$!

cd ..

# ---- FRONTEND SETUP ----
echo ""
echo "🌐 Setting up React frontend..."
cd "$FRONTEND_DIR"

# Ensure package.json exists (create minimal one if missing without touching src/)
if [ ! -f "package.json" ]; then
  echo "⚙️  No package.json found — creating a minimal React setup (src/ preserved)..."
  cat > package.json <<'JSON'
{
  "name": "mindmosaic-reader-frontend",
  "private": true,
  "version": "0.1.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
JSON
  echo "✅ Created minimal package.json"
fi

# Install node dependencies if missing
if [ ! -d "node_modules" ]; then
  echo "📦 Installing npm dependencies..."
  npm install
fi

# Warn if likely entrypoint files are missing (we do not create them to avoid altering src logic)
if [ ! -f "src/index.js" ] && [ ! -f "src/main.jsx" ]; then
  echo "⚠️  Note: No src/index.js or src/main.jsx found. react-scripts may fail to start."
  echo "   Your existing src files are preserved; add an entrypoint if needed."
fi

# Run frontend in background
echo "▶️  Launching frontend on port $FRONTEND_PORT..."
PORT="$FRONTEND_PORT" BROWSER=none npm start &
FRONTEND_PID=$!

cd ..

# ---- CLEANUP HANDLER ----
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    
    # Kill our specific processes
    if [ ! -z "$BACKEND_PID" ]; then
        echo "   Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "   Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Force kill any remaining processes on our ports
    echo "   Force stopping any remaining processes on ports $BACKEND_PORT and $FRONTEND_PORT..."
    lsof -ti:$BACKEND_PORT | xargs kill -9 2>/dev/null || true
    lsof -ti:$FRONTEND_PORT | xargs kill -9 2>/dev/null || true
    
    echo "✅ Cleanup complete"
}

trap cleanup EXIT INT TERM

echo ""
echo "✅ MindMosaic Reader is now running!"
echo "   Backend → http://127.0.0.1:$BACKEND_PORT"
echo "   Frontend → http://localhost:$FRONTEND_PORT"
echo ""
echo "Press Ctrl+C to stop both servers."

# Keep script alive so trap works
wait
