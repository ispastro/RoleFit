# 🎯 RoleFit - AI Resume Tailoring

**Paste a job description. Get a perfectly tailored resume. In seconds.**

Built with FastAPI, Next.js, and Groq AI.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Groq API Key ([Get one free](https://console.groq.com))

### Setup

1. **Clone & Install**
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

2. **Configure API Key**
```bash
cd backend
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

3. **Run Development**
```bash
# From root directory
dev.bat  # Windows

# Or manually:
# Terminal 1: cd backend && uvicorn api:app --reload
# Terminal 2: cd frontend && npm run dev
```

4. **Open App**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
RoleFit/
├── backend/           # FastAPI + AI Engine
│   ├── src/
│   │   ├── domain/           # Business logic
│   │   ├── infrastructure/   # AI & parsers
│   │   └── presentation/     # CLI
│   ├── latex/         # Your resume template
│   ├── output/        # Generated resumes
│   └── api.py         # FastAPI server
│
├── frontend/          # Next.js UI
│   ├── app/
│   │   ├── page.tsx          # Landing
│   │   └── tailor/page.tsx   # Main app
│   └── package.json
│
└── dev.bat           # Start both servers
```

---

## 🎯 How It Works

1. **Paste** job description in the UI
2. **AI analyzes** requirements using Groq (Llama 3.3 70B)
3. **Tailors** your resume sections to match
4. **Compiles** to PDF via cloud API
5. **Download** ready-to-apply PDF

---

## 🛠️ Tech Stack

**Backend:**
- FastAPI (API)
- Groq AI (LLM)
- LaTeX Online API (PDF compilation)
- Python 3.13

**Frontend:**
- Next.js 16
- TypeScript
- Tailwind CSS 4
- Lucide Icons
- Geist Font

---

## 📝 API Endpoints

- `POST /api/tailor` - Tailor resume
- `GET /api/download/{filename}` - Download PDF
- `GET /health` - Health check
- `GET /docs` - Interactive API docs

---

## 🔥 Features

- ⚡ Lightning fast (Groq inference)
- 🎨 Clean, minimalist UI with Aurora-style design
- 🔒 Secure (API key in .env)
- 📱 Responsive design
- 🎯 Smart AI matching
- ✨ Preserves your voice
- 📄 Automatic PDF generation (no LaTeX installation needed)
- 🌐 Deploy anywhere

---

## 🚀 Deployment

No LaTeX installation required! The app uses a free cloud API for PDF compilation.

**Deploy to:**
- Vercel (Frontend)
- Railway/Render (Backend)
- AWS/GCP/Azure
- Docker

---

## 📄 License

MIT

---

**Built by engineers, for engineers.** 🚀
