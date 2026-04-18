# 🎯 RoleFit - AI Resume Tailoring

**Upload your resume. Paste a job description. Get a perfectly tailored resume. In seconds.**

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
│   │   │   ├── ai/          # Groq AI services
│   │   │   └── parsers/     # File extractors
│   │   └── presentation/     # CLI
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

1. **Upload/Paste** your resume (PDF, DOCX, TXT, MD)
2. **Paste** job description
3. **AI analyzes** requirements using Groq (Llama 3.3 70B)
4. **Tailors** resume:
   - **Skills**: Reordered + adds missing skills from job
   - **Experience**: Keywords added (preserves original tech stacks)
   - **Projects/Education**: Unchanged
5. **Download PDF** (in-browser conversion)

---

## 🛠️ Tech Stack

**Backend:**
- FastAPI (API)
- Groq AI (Llama 3.3 70B)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)
- Python 3.13

**Frontend:**
- Next.js 16
- TypeScript
- Tailwind CSS 4
- marked (Markdown parser)
- html2pdf.js (PDF generation)
- Lucide Icons

---

## 📝 API Endpoints

- `POST /api/tailor` - Tailor resume (multipart/form-data)
  - `job_description`: string (required)
  - `resume_file`: file (optional - PDF/DOCX/TXT/MD)
  - `resume_text`: string (optional - pasted text)
- `GET /api/download/{filename}` - Download tailored resume
- `GET /health` - Health check
- `GET /docs` - Interactive API docs

---

## 🔥 Features

- ⚡ Lightning fast (Groq inference)
- 📤 Upload resume (PDF, DOCX, TXT, MD) or paste text
- 🎨 Clean, minimalist UI with Aurora-style design
- 🔒 Secure (API key in .env)
- 📱 Responsive design
- 🎯 Smart AI matching
- ✨ Preserves structure and truth
- 📄 In-browser PDF generation (no external services)
- 🌐 Deploy anywhere

---

## 🧠 AI Logic

**Skills Section:**
- Reorders existing skills to match job
- **Adds missing skills from job** (you're applying, so you can learn them)
- Groups related skills

**Experience Section:**
- Adds relevant keywords naturally
- **Never adds new tech stacks** (keeps it truthful)
- Rewords to emphasize relevance

**Projects & Education:**
- Completely unchanged

---

## 🚀 Deployment

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
