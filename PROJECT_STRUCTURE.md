# 📁 RoleFit - Clean Project Structure

## Overview
Minimal, production-ready structure with only essential files.

---

## Directory Tree

```
RoleFit/
├── backend/                          # FastAPI Backend
│   ├── src/
│   │   └── infrastructure/
│   │       ├── ai/
│   │       │   ├── groq_client.py           # Groq API wrapper
│   │       │   └── latex_resume_generator.py # 3-pass AI pipeline
│   │       └── parsers/
│   │           ├── file_extractor.py        # PDF/DOCX/TXT/MD parser
│   │           └── plaintext_parser.py      # Text processing
│   ├── templates/
│   │   └── resume_template.tex              # LaTeX template
│   ├── .env                                  # API keys (gitignored)
│   ├── .env.example                          # Template for .env
│   ├── api_latex.py                          # FastAPI server
│   └── requirements.txt                      # Python dependencies
│
├── frontend/                         # Next.js Frontend
│   ├── app/
│   │   ├── components/
│   │   │   └── ui.tsx                       # Reusable UI components
│   │   ├── tailor/
│   │   │   └── page.tsx                     # Main app page
│   │   ├── favicon.ico
│   │   ├── globals.css                      # Global styles
│   │   ├── layout.tsx                       # Root layout
│   │   └── page.tsx                         # Landing page
│   ├── .env.local                            # Environment variables
│   ├── next.config.ts                        # Next.js config
│   ├── package.json                          # Node dependencies
│   ├── postcss.config.mjs                    # PostCSS config
│   └── tsconfig.json                         # TypeScript config
│
├── dev.bat                           # Start both servers (Windows)
└── README.md                         # Main documentation
```

---

## Core Files

### Backend

| File | Purpose | Lines |
|------|---------|-------|
| `api_latex.py` | FastAPI server with 2 endpoints | ~120 |
| `latex_resume_generator.py` | 3-pass AI pipeline + evaluation | ~800 |
| `groq_client.py` | Groq API wrapper | ~50 |
| `file_extractor.py` | Multi-format resume parser | ~100 |
| `resume_template.tex` | LaTeX template with placeholders | ~150 |

### Frontend

| File | Purpose | Lines |
|------|---------|-------|
| `app/tailor/page.tsx` | Main UI (upload, display, Overleaf) | ~400 |
| `app/page.tsx` | Landing page | ~100 |
| `app/components/ui.tsx` | Reusable components | ~50 |

---

## API Endpoints

### `POST /api/tailor-latex`
- **Input**: `job_description` (form), `resume_file` or `resume_text` (form)
- **Output**: `{ "latex_code": "...", "message": "..." }`
- **Purpose**: Generate tailored LaTeX code

### `POST /api/evaluate-resume`
- **Input**: `resume_text` (form), `job_description` (form)
- **Output**: Structured evaluation JSON with scores
- **Purpose**: Evaluate resume quality (5 dimensions)

### `GET /health`
- **Output**: `{ "status": "healthy", "service": "RoleFit LaTeX API" }`
- **Purpose**: Health check

---

## Dependencies

### Backend (Python 3.8+)
```
fastapi
uvicorn
groq
pypdf2
python-docx
python-multipart
```

### Frontend (Node.js 18+)
```
next (16.x)
react (19.x)
typescript
tailwindcss (4.x)
lucide-react
```

---

## Removed Files (Cleanup)

### Backend
- ❌ `api.py` - Old patch-based API
- ❌ `output/` - Test output directory
- ❌ `src/domain/` - Unused domain layer
- ❌ `src/presentation/cli.py` - Unused CLI
- ❌ `src/infrastructure/ai/content_patcher.py` - Old approach
- ❌ `src/infrastructure/ai/content_rewriter.py` - Old approach
- ❌ `src/infrastructure/ai/job_analyzer.py` - Unused
- ❌ `src/infrastructure/ai/resume_analyzer.py` - Unused
- ❌ `src/infrastructure/parsers/json_generator.py` - Unused
- ❌ `src/infrastructure/parsers/markdown_generator.py` - Unused

### Frontend
- ❌ `components/ResumeTemplate.tsx` - Unused component
- ❌ `components/ResumeTemplateClean.tsx` - Unused component
- ❌ `public/*.svg` - Default Next.js SVGs
- ❌ `AGENTS.md`, `CLAUDE.md` - Unused docs

### Root
- ❌ `test_setup.py` - Old test script
- ❌ `FINAL_SYSTEM.md` - Outdated docs
- ❌ `OVERLEAF_WORKFLOW.md` - Outdated docs
- ❌ `QUICK_REFERENCE.md` - Outdated docs

---

## File Count Summary

### Before Cleanup
- Backend: ~25 files
- Frontend: ~30 files
- Root: ~8 files
- **Total: ~63 files**

### After Cleanup
- Backend: ~10 files
- Frontend: ~15 files
- Root: ~2 files
- **Total: ~27 files** (57% reduction)

---

## Key Features

✅ **Minimal Dependencies** - Only essential packages
✅ **Clean Architecture** - Infrastructure layer only
✅ **Single Responsibility** - Each file has one clear purpose
✅ **No Dead Code** - All files actively used
✅ **Production Ready** - Deployable as-is

---

## Development Workflow

```bash
# 1. Setup
cd backend && python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
cd ../frontend && npm install

# 2. Configure
cd backend && cp .env.example .env
# Add GROQ_API_KEY to .env

# 3. Run
cd .. && dev.bat

# 4. Open
http://localhost:3000
```

---

## Deployment

### Backend (Railway/Render)
- Root: `backend/`
- Start: `uvicorn api_latex:app --host 0.0.0.0 --port $PORT`
- Env: `GROQ_API_KEY`

### Frontend (Vercel)
- Root: `frontend/`
- Framework: Next.js
- Env: `NEXT_PUBLIC_API_URL`

---

**Clean, minimal, production-ready!** 🚀
