from .groq_client import GroqClient
import json
import re
import os
import logging

logger = logging.getLogger(__name__)

class LatexResumeGenerator:
    def __init__(self):
        self.client = GroqClient()
        # Get absolute path to templates directory
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.template_path = os.path.join(backend_dir, 'templates', 'resume_template.tex')
    
    def generate_tailored_latex(self, resume_text: str, job_description: str) -> str:
        """
        Extract data, optimize with signal amplification, then humanize.
        """
        
        # Load template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # PASS 1: Signal Amplification
        amplification_prompt = """You are an advanced resume optimization engine specializing in candidate differentiation and signal amplification.

Your task is to take a resume and push it to a top-tier level by making the candidate stand out among highly competitive applicants.

GOAL:
Transform the resume from "good match" to "top 5% standout candidate" by amplifying strong signals, increasing perceived impact, and highlighting engineering depth.

STEP 1: Identify High-Value Signals
- Scan all experience and projects
- Detect the most impressive elements:
  - real-time systems
  - scalability challenges
  - concurrency / race conditions
  - performance optimization
  - system design decisions
  - full-stack ownership
- Rank bullets into:
  - HIGH SIGNAL (rare, complex, impressive)
  - MEDIUM SIGNAL (solid but common)
  - LOW SIGNAL (generic tasks)

STEP 2: Aggressive Amplification of High-Signal Bullets
For HIGH SIGNAL bullets:
- Rewrite to emphasize:
  - system complexity
  - engineering difficulty
  - real-world constraints
  - architectural thinking
- Use language like:
  - "engineered", "designed", "architected", "optimized"
- Add:
  - concurrency, scalability, performance, reliability
- Make these bullets clearly stronger than others

STEP 3: Upgrade Medium-Signal Bullets
- Add:
  - technical depth
  - clearer system context
- Avoid generic phrasing like:
  - "worked on", "helped", "assisted"
- Convert into ownership-driven statements

STEP 4: Minimize or Remove Low-Signal Content
- Compress or remove generic bullets that do not add differentiation
- Prioritize quality over quantity

STEP 5: Inject Implicit Impact (Without Fabrication)
- If no metrics exist, add realistic impact framing:
  - "improving system responsiveness"
  - "ensuring low-latency communication"
  - "supporting concurrent users"
- DO NOT invent fake numbers

STEP 6: Create "Standout Moments"
- Ensure each role has at least 1–2 bullets that:
  - feel significantly more advanced than typical junior work
  - demonstrate deep technical understanding
- These should grab recruiter attention within 5–10 seconds

STEP 7: Strengthen Technical Identity
- Ensure the candidate clearly reads as:
  - Full-Stack Engineer (not frontend-heavy)
- Balance frontend + backend signals in experience

STEP 8: Final Polish
- Keep bullets concise but dense in value
- Avoid fluff or repetitive wording
- Maintain ATS-friendly formatting
- Ensure strong, confident tone

CONSTRAINTS:
- Do NOT fabricate experience or metrics
- Do NOT exaggerate beyond believable scope
- Do NOT introduce buzzword stuffing
- Keep everything grounded and technically credible

OUTPUT FORMAT (JSON):
{
  "name": "Full Name",
  "phone": "Phone Number",
  "email": "Email",
  "github": "GitHub username",
  "website": "Website URL",
  "experience": [
    {
      "company": "Company Name",
      "dates": "Month YYYY -- Month YYYY",
      "title": "Job Title (optimized if needed)",
      "location": "City, Country",
      "bullets": ["HIGH SIGNAL bullets first, amplified with technical depth and impact"]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "bullets": ["Reframed to show engineering complexity and real-world value"]
    }
  ],
  "education": [
    {
      "school": "University",
      "dates": "Month YYYY -- Month YYYY",
      "degree": "Degree",
      "location": "City, Country"
    }
  ],
  "skills": [
    {"category": "Languages", "items": "Reordered by job relevance"},
    {"category": "Frontend", "items": "Aligned with job requirements"},
    {"category": "Backend", "items": "Balanced with frontend for full-stack identity"}
  ]
}

Return ONLY valid JSON, no markdown, no explanations."""

        amplification_message = f"""RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Analyze the resume and job description. Transform this resume into a top 5% standout candidate by:
1. Identifying and amplifying HIGH SIGNAL technical achievements
2. Adding engineering depth and system complexity
3. Creating standout moments that grab attention
4. Balancing full-stack identity
5. Ensuring every bullet demonstrates strong technical ownership

Return optimized data as JSON only."""

        logger.info("PASS 1: Signal amplification...")
        amplified_response = self.client.chat(amplification_prompt, amplification_message)
        amplified_data = self._extract_json(amplified_response)
        
        # PASS 2: Humanization
        humanization_prompt = """You are a resume output quality control system inside an AI resume builder pipeline.

Your role is NOT to generate or improve content creatively.

Your role is to enforce structure, clarity, and human readability on already-generated resume text.

You are the final step before output is delivered to the user.

YOUR CORE RESPONSIBILITY:
Act as a strict quality gate that ensures the resume is:
- concise
- readable
- non-repetitive
- human-like
- technically accurate in tone

STEP 1: Detect Over-Expansion
Identify and flag:
- bullets containing multiple unrelated ideas
- sentences with stacked clauses
- excessive explanation of obvious concepts

Fix by:
- splitting into 2 bullets OR
- removing secondary ideas

STEP 2: Enforce Signal-to-Noise Ratio
Remove or reduce:
- filler phrases (e.g. "ensuring seamless experience", "high-quality", "robust system design")
- repeated adjectives and buzzwords
- vague claims without technical meaning

Keep only content that communicates:
- what was built
- what system behavior existed
- what technical challenge was solved

STEP 3: Enforce One-Idea Rule per Bullet
Each bullet must contain:
- one core technical action
- optional secondary constraint OR impact

If more than one core idea exists → split or simplify.

STEP 4: Normalize Verb Usage
Ensure diversity of action verbs:
- avoid repeating "designed", "implemented", "built" across multiple bullets
- replace with natural variation:
  - engineered
  - developed
  - led
  - optimized
  - delivered
  - created

STEP 5: Preserve High-Value Technical Signals
Do NOT remove or weaken:
- real-time systems
- concurrency handling
- WebSockets
- race conditions
- system architecture decisions
- performance optimization

These are HIGH VALUE signals and must remain visible.

STEP 6: Enforce Natural Human Tone
Ensure the final resume:
- does NOT sound overly polished or repetitive
- does NOT use identical sentence structures repeatedly
- feels like written by a real engineer, not an LLM

Allow slight variation in tone and length.

STEP 7: Remove AI Patterns
Detect and eliminate:
- repeated sentence templates
- overly symmetrical bullet structure
- excessive use of "ensuring", "leveraging", "optimized"

Replace with more natural phrasing or remove if unnecessary.

FINAL OUTPUT REQUIREMENTS:
- Reduced verbosity (clean and tight)
- High readability (scan-friendly)
- Strong technical clarity
- Natural human tone
- No loss of core engineering meaning
- Balanced importance across bullets (not everything sounds "important")

FINAL TEST:
If a recruiter reads the resume in under 10 seconds, they should:
- understand what systems were built
- understand technical depth without reading twice
- not suspect AI-generated writing patterns

OUTPUT FORMAT (JSON):
Same structure as input, but with quality-controlled, concise, human-readable content.

Return ONLY valid JSON, no markdown, no explanations."""

        humanization_message = f"""AMPLIFIED RESUME DATA:
{json.dumps(amplified_data, indent=2)}

Apply quality control:
1. Detect and fix over-expansion
2. Enforce signal-to-noise ratio (remove filler)
3. Enforce one-idea rule per bullet
4. Normalize verb usage (vary action verbs)
5. Preserve high-value technical signals
6. Enforce natural human tone
7. Remove AI patterns

Make it concise, readable, and authentically human.

Return quality-controlled data as JSON only."""

        logger.info("PASS 2: Humanization...")
        humanized_response = self.client.chat(humanization_prompt, humanization_message)
        final_data = self._extract_json(humanized_response)
        
        # Fill template manually
        latex_code = self._fill_template(template, final_data)
        
        logger.info(f"Final LaTeX length: {len(latex_code)} characters")
        
        return latex_code
    
    def _extract_json(self, text: str) -> dict:
        """Extract JSON from AI response."""
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # Find JSON object
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start == -1 or end == 0:
            raise ValueError("No JSON found in response")
        
        json_str = text[start:end]
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            logger.error(f"JSON string: {json_str[:500]}")
            raise ValueError(f"Invalid JSON from AI: {e}")
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        if not text:
            return ""
        text = str(text)
        text = text.replace('\\', '\\textbackslash{}')
        text = text.replace('&', '\\&')
        text = text.replace('%', '\\%')
        text = text.replace('$', '\\$')
        text = text.replace('#', '\\#')
        text = text.replace('_', '\\_')
        text = text.replace('{', '\\{')
        text = text.replace('}', '\\}')
        text = text.replace('~', '\\textasciitilde{}')
        text = text.replace('^', '\\textasciicircum{}')
        return text
    
    def _fill_template(self, template: str, data: dict) -> str:
        """Manually fill template with extracted data."""
        # Fill basic info
        template = template.replace('{{NAME}}', self._escape_latex(data.get('name', 'Name')))
        template = template.replace('{{PHONE}}', self._escape_latex(data.get('phone', '')))
        template = template.replace('{{EMAIL}}', self._escape_latex(data.get('email', '')))
        template = template.replace('{{GITHUB}}', self._escape_latex(data.get('github', '')))
        template = template.replace('{{WEBSITE}}', self._escape_latex(data.get('website', '')))
        
        # Fill experience
        exp_entries = []
        for exp in data.get('experience', []):
            entry = f"""\n  \\resumeSubheading
      {{{self._escape_latex(exp.get('company', ''))}}}{{{self._escape_latex(exp.get('dates', ''))}}}
      {{{self._escape_latex(exp.get('title', ''))}}}{{{self._escape_latex(exp.get('location', ''))}}}
      \\resumeItemListStart"""
            for bullet in exp.get('bullets', []):
                entry += f"\n        \\resumeItem{{{self._escape_latex(bullet)}}}"
            entry += "\n      \\resumeItemListEnd\n"
            exp_entries.append(entry)
        template = template.replace('{{EXPERIENCE_ENTRIES}}', ''.join(exp_entries))
        
        # Fill projects
        proj_entries = []
        for proj in data.get('projects', []):
            entry = f"""\n    \\resumeProjectHeading{{\\textbf{{{self._escape_latex(proj.get('name', ''))}}}}}{{}}\n      \\resumeItemListStart"""
            for bullet in proj.get('bullets', []):
                entry += f"\n        \\resumeItem{{{self._escape_latex(bullet)}}}"
            entry += "\n      \\resumeItemListEnd\n"
            proj_entries.append(entry)
        template = template.replace('{{PROJECT_ENTRIES}}', ''.join(proj_entries))
        
        # Fill education
        edu_entries = []
        for edu in data.get('education', []):
            entry = f"""\n  \\resumeSubheading
      {{{self._escape_latex(edu.get('school', ''))}}}{{{self._escape_latex(edu.get('dates', ''))}}}
      {{{self._escape_latex(edu.get('degree', ''))}}}{{{self._escape_latex(edu.get('location', ''))}}}"""
            edu_entries.append(entry)
        template = template.replace('{{EDUCATION_ENTRIES}}', ''.join(edu_entries))
        
        # Fill skills
        skills_content = []
        for skill in data.get('skills', []):
            skills_content.append(f"\\textbf{{{self._escape_latex(skill.get('category', ''))}}}: {self._escape_latex(skill.get('items', ''))} \\vspace{{2pt}} \\\\")
        template = template.replace('{{SKILLS_CONTENT}}', '\n'.join(skills_content))
        
        return template

    
    def evaluate_resume(self, resume_text: str, job_description: str) -> dict:
        """
        Evaluate resume quality with structured scoring.
        """
        
        evaluation_prompt = """You are an elite resume evaluation engine.

Your task is to analyze a resume and produce a structured, multi-dimensional evaluation.

You must NOT rewrite the resume.

You only score and critique it.

SCORING DIMENSIONS:

1. Technical Depth (25%)
- real engineering complexity
- distributed systems, real-time systems, concurrency, scaling
- depth of system design thinking

2. Impact Clarity (20%)
- clarity of outcomes
- specificity of contribution
- measurable or observable improvements

3. Structure & Readability (20%)
- one idea per bullet rule
- scan speed and cognitive load
- consistency of formatting

4. ATS Match Quality (20%)
- keyword alignment with modern software roles
- stack relevance
- job-readiness alignment

5. Human Authenticity (15%)
- detect AI-like writing patterns
- repetition of phrases
- unnatural symmetry
- lack of variation

RULES:
- Do NOT rewrite the resume
- Do NOT improve wording
- Only evaluate and critique
- Be strict and engineering-minded, not generous

OUTPUT FORMAT (JSON):
{
  "total_score": 87,
  "breakdown": {
    "technical_depth": 90,
    "impact_clarity": 85,
    "structure_readability": 88,
    "ats_match": 83,
    "human_authenticity": 89
  },
  "strengths": [
    "Strong real-time system experience",
    "Good concurrency handling signals"
  ],
  "weaknesses": [
    "Some bullets are still generic (low specificity)",
    "Missing measurable impact in 2 roles"
  ],
  "critical_fixes_for_builder": [
    "Inject concurrency + scale context into WebSocket bullet",
    "Replace generic verbs with system-specific actions"
  ]
}

Return ONLY valid JSON, no markdown, no explanations."""

        evaluation_message = f"""RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Evaluate this resume strictly. Provide scores, strengths, weaknesses, and actionable fixes.

Return evaluation as JSON only."""

        response = self.client.chat(evaluation_prompt, evaluation_message)
        logger.info(f"Evaluation response length: {len(response)} characters")
        
        # Extract JSON from response
        evaluation = self._extract_json(response)
        
        return evaluation

    
    def inject_missing_signals(self, resume_data: dict, evaluation: dict) -> dict:
        """
        Inject missing technical signals based on evaluation weaknesses.
        """
        
        injection_prompt = """You are an elite resume enhancement engine focused ONLY on injecting missing technical signals.

You do NOT rewrite resumes.
You do NOT expand unnecessarily.
You do NOT add filler or marketing language.

Your ONLY job is to strengthen weak technical areas while preserving clarity and brevity.

PRIMARY GOAL:
Improve engineering signal strength WITHOUT increasing verbosity or reducing readability.

CORE RULES:

1. Minimal Intervention Rule
Only modify bullets that are:
- weak in technical depth
- missing system-level clarity
- under-specified compared to the candidate's actual experience

Do NOT touch already strong bullets.

2. Signal Injection Rule
When improving a bullet:
ONLY add missing technical dimensions such as:

- concurrency
- real-time systems
- state synchronization
- scalability constraints
- latency/performance considerations
- architecture boundaries

Do NOT add:
- buzzwords
- generic adjectives
- marketing phrases
- vague claims

3. Preservation Rule
Maintain:
- original meaning
- original structure style
- original length as much as possible

No bullet should grow significantly longer.

4. Natural Integration Rule
Injected technical signals must:
- feel naturally part of the sentence
- not appear appended or forced
- blend into existing engineering description

5. Anti-Overfitting Rule
Do NOT:
- make every bullet "advanced"
- upgrade everything to "senior-level language"
- repeat the same technical terms across bullets

Maintain variation.

6. Priority Order for Signal Injection

Inject only if missing:

HIGH PRIORITY:
- concurrency / race conditions
- real-time systems
- distributed state
- WebSockets / event-driven systems
- performance constraints

MEDIUM PRIORITY:
- caching strategies
- scalability design
- API architecture
- database optimization

LOW PRIORITY:
- tooling details (only if necessary)

7. Constraint Awareness
Respect existing constraints:
- do not contradict original experience level
- do not inflate job scope
- do not invent systems not implied

OUTPUT FORMAT (JSON):
{
  "enhanced_resume": {
    // Same structure as input, with only weak bullets improved
  },
  "changes": [
    {
      "location": "Experience > Company Name > Bullet 2",
      "original": "Original bullet text",
      "enhanced": "Enhanced bullet text",
      "injected_signals": ["concurrency", "real-time"],
      "reason": "Missing system-level context"
    }
  ]
}

FINAL TEST:
After injection:
- resume must still be readable in < 10 seconds
- no increase in fluff
- technical depth must be visibly improved
- no AI-generated tone increase

Return ONLY valid JSON, no markdown, no explanations."""

        injection_message = f"""RESUME DATA:
{json.dumps(resume_data, indent=2)}

EVALUATION REPORT:
{json.dumps(evaluation, indent=2)}

Based on the weaknesses and critical fixes identified:
1. Identify weak bullets that need technical signal injection
2. Inject ONLY missing high-priority signals (concurrency, real-time, scalability)
3. Preserve original meaning and length
4. Make changes feel natural and integrated
5. Do NOT touch already strong bullets

Return enhanced resume with change log as JSON only."""

        response = self.client.chat(injection_prompt, injection_message)
        logger.info(f"Signal injection response length: {len(response)} characters")
        
        # Extract JSON from response
        result = self._extract_json(response)
        
        return result
