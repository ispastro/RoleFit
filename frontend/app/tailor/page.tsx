"use client";

import { useState, useCallback, useMemo } from "react";
import Link from "next/link";
import { Loader2, ArrowLeft, Download, RefreshCw, AlertCircle, FileText, ExternalLink, Copy, Check } from "lucide-react";

export default function TailorPage() {
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [latexCode, setLatexCode] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState("");
  const [inputMode, setInputMode] = useState<'file' | 'text'>('file');
  const [isDragging, setIsDragging] = useState(false);
  const [copied, setCopied] = useState(false);

  const API_URL = useMemo(
    () => process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
    []
  );

  const isFormValid = useMemo(
    () => jobDescription.trim().length > 0,
    [jobDescription]
  );

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isFormValid) {
      setError("Please paste a job description");
      return;
    }

    if (inputMode === 'file' && !resumeFile) {
      setError("Please upload your resume");
      return;
    }

    if (inputMode === 'text' && !resumeText.trim()) {
      setError("Please paste your resume");
      return;
    }

    setLoading(true);
    setError(null);
    setLatexCode(null);

    try {
      const formData = new FormData();
      formData.append('job_description', jobDescription);
      
      if (inputMode === 'file' && resumeFile) {
        formData.append('resume_file', resumeFile);
      } else if (inputMode === 'text') {
        formData.append('resume_text', resumeText);
      }

      const response = await fetch(`${API_URL}/api/tailor-latex`, {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to generate LaTeX code');
      }
      
      const data = await response.json();
      setLatexCode(data.latex_code);
    } catch (err) {
      console.error('Error:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate LaTeX code');
    } finally {
      setLoading(false);
    }
  }, [jobDescription, isFormValid, API_URL, inputMode, resumeFile, resumeText]);

  const handleReset = useCallback(() => {
    setLatexCode(null);
    setError(null);
    setJobDescription("");
    setResumeFile(null);
    setResumeText("");
    setCopied(false);
  }, []);

  const handleCopyLatex = useCallback(() => {
    if (latexCode) {
      navigator.clipboard.writeText(latexCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [latexCode]);

  const handleOpenOverleaf = useCallback(async () => {
    if (!latexCode) return;
    
    setLoading(true);
    
    try {
      // Create a form and submit to Overleaf
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = 'https://www.overleaf.com/docs';
      form.target = '_blank';
      
      // Add the LaTeX code as snip
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'snip';
      input.value = latexCode;
      form.appendChild(input);
      
      // Add engine
      const engineInput = document.createElement('input');
      engineInput.type = 'hidden';
      engineInput.name = 'engine';
      engineInput.value = 'pdflatex';
      form.appendChild(engineInput);
      
      document.body.appendChild(form);
      form.submit();
      document.body.removeChild(form);
    } catch (err) {
      console.error('Error opening Overleaf:', err);
      // Fallback: copy and open
      navigator.clipboard.writeText(latexCode);
      setCopied(true);
      window.open('https://www.overleaf.com/project', '_blank');
    } finally {
      setLoading(false);
    }
  }, [latexCode]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      const validExtensions = ['.pdf', '.docx', '.txt', '.md'];
      const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
      
      if (validExtensions.includes(fileExtension)) {
        setResumeFile(file);
        setInputMode('file');
      } else {
        setError('Invalid file type. Please upload PDF, DOCX, TXT, or MD files.');
      }
    }
  }, []);



  return (
    <main className="min-h-screen bg-black relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff08_1px,transparent_1px),linear-gradient(to_bottom,#ffffff08_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000,transparent)]" />
        <div className="absolute top-40 left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-gradient-to-br from-neutral-800/30 via-neutral-700/15 to-transparent rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-20 -left-4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob pointer-events-none" />
        <div className="absolute top-40 -right-4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000 pointer-events-none" />
        <div className="absolute bottom-20 left-1/3 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000 pointer-events-none" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        <div className="flex items-center justify-between mb-12 backdrop-blur-sm">
          <Link href="/" className="text-2xl font-bold hover:scale-105 transition-transform">
            <span className="bg-gradient-to-b from-neutral-200 via-neutral-400 to-neutral-600 bg-clip-text text-transparent">RoleFit</span>
          </Link>
          <Link href="/" className="text-neutral-400 hover:text-white text-sm flex items-center gap-1 transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back
          </Link>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 relative max-w-4xl mx-auto">
          <div>
            <label className="block text-neutral-300 font-semibold mb-3">
              Your Resume
            </label>
            
            <div className="flex gap-3 mb-3">
              <button
                type="button"
                onClick={() => setInputMode('file')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  inputMode === 'file'
                    ? 'bg-white text-black'
                    : 'bg-neutral-900/50 text-neutral-400 hover:text-neutral-200'
                }`}
              >
                Upload File
              </button>
              <button
                type="button"
                onClick={() => setInputMode('text')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  inputMode === 'text'
                    ? 'bg-white text-black'
                    : 'bg-neutral-900/50 text-neutral-400 hover:text-neutral-200'
                }`}
              >
                Paste Text
              </button>
            </div>

            {inputMode === 'file' ? (
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`relative border-2 border-dashed rounded-lg transition-all ${
                  isDragging
                    ? 'border-white bg-neutral-800/50'
                    : 'border-neutral-700 bg-neutral-900/50'
                }`}
              >
                <input
                  type="file"
                  accept=".pdf,.docx,.txt,.md"
                  onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  disabled={loading}
                />
                <div className="px-6 py-8 text-center">
                  {resumeFile ? (
                    <div className="space-y-2">
                      <FileText className="w-12 h-12 mx-auto text-green-400" />
                      <p className="text-neutral-200 font-medium">{resumeFile.name}</p>
                      <p className="text-neutral-500 text-sm">{(resumeFile.size / 1024).toFixed(2)} KB</p>
                      <button
                        type="button"
                        onClick={(e) => { e.stopPropagation(); setResumeFile(null); }}
                        className="text-neutral-400 hover:text-white text-sm underline"
                      >
                        Remove
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <Download className="w-12 h-12 mx-auto text-neutral-500" />
                      <p className="text-neutral-300">
                        <span className="font-semibold">Click to upload</span> or drag and drop
                      </p>
                      <p className="text-neutral-500 text-sm">PDF, DOCX, TXT, or MD (max 10MB)</p>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <textarea
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Paste your resume content here..."
                className="w-full h-64 px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-neutral-600 focus:ring-2 focus:ring-neutral-700/50 transition-all resize-none"
                disabled={loading}
              />
            )}
          </div>

          <div>
            <label className="block text-neutral-300 font-semibold mb-3">
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full job description here..."
              className="w-full h-64 px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-neutral-600 focus:ring-2 focus:ring-neutral-700/50 transition-all resize-none"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading || !jobDescription.trim()}
            className="relative w-full px-6 py-4 bg-white hover:bg-neutral-100 disabled:bg-neutral-800 disabled:text-neutral-600 text-black font-semibold rounded-lg transition-all duration-200 hover:scale-[1.02] hover:shadow-2xl hover:shadow-white/20 disabled:hover:scale-100 disabled:hover:shadow-none overflow-hidden group"
          >
            <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/20 to-transparent" />
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <Loader2 className="animate-spin h-5 w-5" />
                Tailoring your resume...
              </span>
            ) : (
              "Tailor Resume"
            )}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-900/20 backdrop-blur-sm border border-red-800/50 rounded-lg flex items-start gap-3 max-w-4xl mx-auto">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
            <p className="text-red-300 text-sm">{error}</p>
          </div>
        )}

        {latexCode && (
          <div className="mt-6 p-6 bg-neutral-900/50 backdrop-blur-sm border border-green-700 rounded-lg max-w-4xl mx-auto">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center">
                  <FileText className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-white font-semibold text-lg">LaTeX Code Generated!</h3>
                  <p className="text-green-300 text-sm">Compile on Overleaf to get your PDF</p>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <div className="bg-black/50 rounded-lg p-4 max-h-96 overflow-y-auto">
                <pre className="text-neutral-300 text-xs font-mono whitespace-pre-wrap break-words">{latexCode}</pre>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={handleCopyLatex}
                  className="px-6 py-3 bg-neutral-800 hover:bg-neutral-700 text-white font-semibold rounded-lg transition-all flex items-center justify-center gap-2"
                >
                  {copied ? (
                    <>
                      <Check className="w-5 h-5" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="w-5 h-5" />
                      Copy LaTeX Code
                    </>
                  )}
                </button>

                <button
                  onClick={handleOpenOverleaf}
                  className="px-6 py-3 bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-semibold rounded-lg transition-all flex items-center justify-center gap-2"
                >
                  <ExternalLink className="w-5 h-5" />
                  Open in Overleaf
                </button>
              </div>

              <div className="mt-4 p-4 bg-blue-900/20 border border-blue-800/50 rounded-lg">
                <p className="text-blue-300 text-sm">
                  <strong>How to compile:</strong>
                </p>
                <ol className="text-blue-300 text-sm mt-2 space-y-1 list-decimal list-inside">
                  <li>Click "Open in Overleaf" (creates project automatically)</li>
                  <li>Wait for Overleaf to load your project</li>
                  <li>Click "Recompile" if needed</li>
                  <li>Download your PDF from Overleaf</li>
                </ol>
              </div>

              <button
                onClick={handleReset}
                className="w-full px-6 py-3 bg-neutral-900/50 hover:bg-neutral-800 text-neutral-300 hover:text-white font-semibold rounded-lg transition-all flex items-center justify-center gap-2"
              >
                <RefreshCw className="w-4 h-4" /> Tailor Another Resume
              </button>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
