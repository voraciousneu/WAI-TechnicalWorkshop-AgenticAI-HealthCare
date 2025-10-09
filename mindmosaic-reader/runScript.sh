#!/bin/bash

# ===============================================
# MindMosaic Local Reader Runner
# Runs both FastAPI backend and React frontend
# ===============================================

# Stop on first error
set -e

# ---- Configuration ----
BACKEND_DIR="./backend"
FRONTEND_DIR="./frontend"
BACKEND_PORT=8000
FRONTEND_PORT=3000

# ---- Start Backend ----
echo "Starting FastAPI backend..."
cd "$BACKEND_DIR"

# Ensure dependencies
if ! python3 -m venv myenv 2>/dev/null; then
    echo "Creating Python virtual environment..."
    python3 -m venv myenv
fi

source myenv/bin/activate
pip install -q fastapi uvicorn pydantic

# Run backend in background
uvicorn app:app --host 127.0.0.1 --port "$BACKEND_PORT" --reload &
BACKEND_PID=$!

cd ..

# ---- Start Frontend ----
echo "🌐 Starting React frontend..."
cd "$FRONTEND_DIR"

# Install node dependencies if missing
if [ ! -d "node_modules" ]; then
  echo "📦 Installing npm dependencies..."
  npm install
fi

# Run frontend (non-blocking)
npm start -- --port "$FRONTEND_PORT" &
FRONTEND_PID=$!

cd ..

# ---- Cleanup on exit ----
trap "echo '🛑 Shutting down...'; kill $BACKEND_PID $FRONTEND_PID" EXIT

echo ""
echo "✅ MindMosaic Reader is running!"
echo "   Backend: http://127.0.0.1:$BACKEND_PORT"
echo "   Frontend: http://localhost:$FRONTEND_PORT"
echo ""
echo "Press Ctrl+C to stop both servers."

# Keep script alive to manage both processes
wait


