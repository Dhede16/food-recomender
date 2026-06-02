#!/bin/bash
echo "🍽️  Starting MakanKost App..."

# Start backend
echo "▶ Starting FastAPI backend on port 8000..."
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start frontend
echo "▶ Starting Vue.js frontend on port 5173..."
cd ../frontend && npm install --silent && npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ App running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   Swagger:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID; echo 'Servers stopped.'" SIGINT
wait
