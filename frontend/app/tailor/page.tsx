"use client";

import { useState, useCallback, useMemo } from "react";
import Link from "next/link";
import { Loader2, CheckCircle, ArrowLeft, Download, Eye, RefreshCw, AlertCircle, FileText } from "lucide-react";

type ViewMode = "preview" | "download";

export default function TailorPage() {
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [texContent, setTexContent] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>("preview");
  const [pdfGenerating, setPdfGenerating] = useState(false);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState("");
  const [inputMode, setInputMode] = useState<'file' | 'text'>('file');
  const [isDragging, setIsDragging] = useState(false);

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
    setResult(null);
    setTexContent(null);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000);

      const formData = new FormData();
      formData.append('job_description', jobDescription);
      
      if (inputMode === 'file' && resumeFile) {
        formData.append('resume_file', resumeFile);
      } else if (inputMode === 'text') {
        formData.append('resume_text', resumeText);
      }

      const response = await fetch(`${API_URL}/api/tailor`, {
        method: "POST",
        body: formData,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to tailor resume");
      }

      const data = await response.json();
      
      if (!data.download_url || !data.tex_content) {
        throw new Error("Invalid response from server");
      }

      setResult(`${API_URL}${data.download_url}`);
      setTexContent(data.tex_content);
      setViewMode("preview");
    } catch (err) {
      if (err instanceof Error) {
        if (err.name === "AbortError") {
          setError("Request timed out. Please try again.");
        } else {
          setError(err.message);
        }
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }, [jobDescription, isFormValid, API_URL, inputMode, resumeFile, resumeText]);

  const handleReTailor = useCallback(() => {
    setViewMode("preview");
    setResult(null);
    setTexContent(null);
    setError(null);
  }, []);

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

  const handleCompileToPDF = useCallback(async () => {
    if (!texContent) return;
    
    setPdfGenerating(true);
    setError(null);
    
    try {
      const { marked } = await import('marked');
      const { default: html2pdf } = await import('html2pdf.js');
      
      const htmlContent = marked.parse(texContent);
      
      const container = document.createElement('div');
      container.innerHTML = htmlContent as string;
      container.style.padding = '40px';
      container.style.fontFamily = 'Arial, sans-serif';
      container.style.lineHeight = '1.6';
      container.style.color = '#000';
      
      await html2pdf(container, {
        margin: 0.5,
        filename: 'resume_tailored.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
      });
      
      setPdfGenerating(false);
    } catch (err) {
      console.error('PDF generation error:', err);
      setError('Failed to generate PDF. Please try again.');
      setPdfGenerating(false);
    }
  }, [texContent]);

  const handleViewModeChange = useCallback((mode: ViewMode) => {
    setViewMode(mode);
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

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-12">
        <div className="flex items-center justify-between mb-12 backdrop-blur-sm">
          <Link href="/" className="text-2xl font-bold hover:scale-105 transition-transform">
            <span className="bg-gradient-to-b from-neutral-200 via-neutral-400 to-neutral-600 bg-clip-text text-transparent">RoleFit</span>
          </Link>
          <Link href="/" className="text-neutral-400 hover:text-white text-sm flex items-center gap-1 transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back
          </Link>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 relative">
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
                        onClick={() => setResumeFile(null)}
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
              <div className="relative">
                <textarea
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  placeholder="Paste your resume content here..."
                  className="w-full h-64 px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-neutral-600 focus:ring-2 focus:ring-neutral-700/50 transition-all resize-none"
                  disabled={loading}
                />
              </div>
            )}
          </div>

          <div>
            <label className="block text-neutral-300 font-semibold mb-3">
              Paste Job Description
            </label>
            <div className="relative">
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the full job description here..."
                className="w-full h-96 px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-neutral-600 focus:ring-2 focus:ring-neutral-700/50 transition-all resize-none"
                disabled={loading}
              />
            </div>
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
          <div className="mt-6 p-4 bg-red-900/20 backdrop-blur-sm border border-red-800/50 rounded-lg flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
            <p className="text-red-300 text-sm">{error}</p>
          </div>
        )}

        {result && (
          <div className="mt-6 space-y-4">
            <div className="flex gap-3">
              <button
                onClick={() => handleViewModeChange("preview")}
                className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all ${
                  viewMode === "preview"
                    ? "bg-white text-black"
                    : "bg-neutral-900/50 text-neutral-300 hover:bg-neutral-900/80"
                }`}
              >
                <Eye className="w-4 h-4 inline mr-2" /> Preview
              </button>
              <button
                onClick={() => handleViewModeChange("download")}
                className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all ${
                  viewMode === "download"
                    ? "bg-white text-black"
                    : "bg-neutral-900/50 text-neutral-300 hover:bg-neutral-900/80"
                }`}
              >
                <Download className="w-4 h-4 inline mr-2" /> Download
              </button>
            </div>

            {viewMode === "preview" && texContent && (
              <div className="p-6 bg-neutral-900/50 backdrop-blur-sm border border-neutral-700 rounded-lg">
                <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-400" /> Resume Preview
                </h3>
                <div className="bg-black/50 rounded-lg p-4 max-h-96 overflow-y-auto">
                  <pre className="text-neutral-300 text-xs font-mono whitespace-pre-wrap">{texContent}</pre>
                </div>
                <div className="mt-4 flex gap-3">
                  <button
                    onClick={handleReTailor}
                    className="flex-1 px-6 py-3 bg-neutral-800 hover:bg-neutral-700 text-white font-semibold rounded-lg transition-all"
                  >
                    <RefreshCw className="w-4 h-4 inline mr-2" /> Re-Tailor
                  </button>
                  <button
                    onClick={handleCompileToPDF}
                    disabled={pdfGenerating}
                    className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-500 disabled:bg-green-800 text-white font-semibold rounded-lg transition-all hover:scale-105 group"
                  >
                    {pdfGenerating ? (
                      <>
                        <Loader2 className="w-4 h-4 inline mr-2 animate-spin" /> Generating...
                      </>
                    ) : (
                      <>
                        <FileText className="w-4 h-4 inline mr-2" /> Download PDF
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}

            {viewMode === "download" && (
              <div className="p-6 bg-neutral-900/50 backdrop-blur-sm border border-neutral-700 rounded-lg">
                <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-400" /> Resume Tailored Successfully!
                </h3>
                <div className="flex gap-3">
                  <button
                    onClick={handleReTailor}
                    className="flex-1 px-6 py-3 bg-neutral-800 hover:bg-neutral-700 text-white font-semibold rounded-lg transition-all"
                  >
                    <RefreshCw className="w-4 h-4 inline mr-2" /> Re-Tailor
                  </button>
                  <button
                    onClick={handleCompileToPDF}
                    disabled={pdfGenerating}
                    className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-500 disabled:bg-green-800 text-white font-semibold rounded-lg transition-all hover:scale-105 group"
                  >
                    {pdfGenerating ? (
                      <>
                        <Loader2 className="w-4 h-4 inline mr-2 animate-spin" /> Generating...
                      </>
                    ) : (
                      <>
                        <FileText className="w-4 h-4 inline mr-2" /> Download PDF
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
