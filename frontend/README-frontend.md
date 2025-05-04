# VoiceUp Analytics & Compliance: Frontend
This document outlines the setup and testing of the frontend for the VoiceUp Analytics & Compliance project. The frontend is built with React, TypeScript, and Material-UI, providing a dashboard for compliance scores, a conversations list, and per-message emotion analysis.

# Project Structure

frontend/src/App.tsx: Main app with routing.
frontend/src/routes/Dashboard.tsx: Compliance score chart.
frontend/src/routes/Conversations.tsx: Conversations list.
frontend/src/routes/ConversationDetail.tsx: Conversation details with emotions.
frontend/src/components/MessageList.tsx: Displays messages with emotions.
frontend/src/utils/api.ts: API utility functions.
frontend/src/types/index.ts: TypeScript interfaces.

# Prerequisites

Node.js 16+: Install from https://nodejs.org/.
PowerShell: For running commands on Windows.
Project Directory: C:\Users\hp\Desktop\voice-analytics\frontend.
Backend Running: Flask server at http://127.0.0.1:5000.

# Setup Instructions
1. Navigate to Frontend Directory
cd C:\Users\hp\Desktop\voice-analytics\frontend

2. Install Dependencies
npm install

3. Clear Cache
Remove-Item -Recurse -Force C:\Users\hp\Desktop\voice-analytics\frontend\node_modules\.vite
Remove-Item -Recurse -Force C:\Users\hp\Desktop\voice-analytics\frontend\dist

4. Run Frontend
npm run dev

Expected output:
VITE v4.x.x  ready in xxx ms
Local:   http://localhost:3000/

Testing Frontend
Open http://localhost:3000 in a browser and verify:

Dashboard (/): Displays compliance score chart.
Conversations (/conversations): Lists conversations with compliance scores.
Conversation Detail (/conversations/2): Shows per-message emotions (e.g., “positive (99.9%)”) and conversation analysis.

# Troubleshooting

Blank Page: Check browser console (F12 → Console) for errors like Failed to fetch.
API Errors: Ensure Flask server is running (http://127.0.0.1:5000).
Dependencies: Run npm install if modules are missing.

