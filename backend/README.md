# 🎯 RoleFit - AI Resume Tailoring Agent

**The smartest way to tailor your resume.** Just paste a job description, and RoleFit's AI agent automatically customizes your resume to perfectly match the role - while keeping your template and voice intact.

## 🚀 Features

- **Smart AI Agent**: Multi-step reasoning powered by Groq (Llama 3.3 70B)
- **Zero Prompts**: Just paste the job description - no manual work
- **Preserves Structure**: Keeps your LaTeX template exactly as is
- **Maintains Voice**: Rewrites content in YOUR style
- **ATS-Optimized**: Automatically includes relevant keywords
- **Lightning Fast**: Groq's ultra-fast inference

## 📋 Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Get Groq API Key:**
   - Go to https://console.groq.com
   - Create a free account
   - Generate an API key

3. **Configure API Key:**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your key
GROQ_API_KEY=your_actual_groq_api_key_here
```

## 🎯 Usage

**It's this simple:**

```bash
python main.py
```

Then:
1. Paste the job description
2. Press Enter twice
3. Wait ~30 seconds
4. Get your tailored resume in `output/tailored_resume.tex`

**That's it!** No prompts, no configuration, no manual editing.

## 📁 Project Structure

```
RoleFit/
├── latex/
│   └── haile_resume.tex          # Your original resume
├── output/
│   └── tailored_resume.tex       # Generated tailored resume
├── agent.py                       # Main orchestrator
├── job_analyzer.py                # Analyzes job requirements
├── resume_analyzer.py             # Analyzes your resume
├── content_rewriter.py            # Rewrites sections
├── latex_parser.py                # Parses LaTeX structure
├── latex_generator.py             # Generates new LaTeX
├── groq_client.py                 # Groq API wrapper
└── main.py                        # Entry point
```

## 🧠 How It Works

RoleFit uses a **multi-agent architecture**:

1. **Job Analyzer Agent**: Extracts requirements, skills, keywords from job description
2. **Resume Analyzer Agent**: Understands your strengths and writing style
3. **Content Rewriter Agent**: Tailors each section to match the job
4. **LaTeX Generator**: Rebuilds your resume with new content

All powered by **Groq's Llama 3.3 70B** for intelligent reasoning.

## 🎨 Customization

Want to use your own resume template? Just replace `latex/haile_resume.tex` with your LaTeX resume. RoleFit works with any LaTeX resume structure!

## 🔥 Why RoleFit?

- ✅ **No manual work** - Just paste job description
- ✅ **Preserves your template** - LaTeX structure stays intact
- ✅ **Maintains your voice** - Sounds like YOU, not AI
- ✅ **Smart matching** - Semantic understanding, not keyword stuffing
- ✅ **Fast** - Groq's inference is lightning quick
- ✅ **Free** - Groq offers generous free tier

## 📝 Example

**Input:** Paste job description for "Senior Full-Stack Engineer at Tech Startup"

**Output:** Your resume automatically tailored with:
- Emphasized full-stack experience
- Highlighted relevant tech stack
- Reordered projects to show most relevant first
- Added keywords naturally
- Quantified achievements matching job requirements

**Time:** ~30 seconds

## 🛠️ Requirements

- Python 3.8+
- Groq API key (free)
- Your resume in LaTeX format

## 📄 License

MIT

---

**Built by engineers, for engineers.** 🚀
