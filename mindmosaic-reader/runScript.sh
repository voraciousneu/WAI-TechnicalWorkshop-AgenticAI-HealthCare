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
echo "📦 Installing Python dependencies (FastAPI, Uvicorn, Pydantic)..."
pip install -q --upgrade pip
pip install -q fastapi uvicorn pydantic

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
trap "echo '🛑 Shutting down servers...'; kill $BACKEND_PID $FRONTEND_PID" EXIT

echo ""
echo "✅ MindMosaic Reader is now running!"
echo "   Backend → http://127.0.0.1:$BACKEND_PORT"
echo "   Frontend → http://localhost:$FRONTEND_PORT"
echo ""
echo "Press Ctrl+C to stop both servers."

# Keep script alive so trap works
wait
