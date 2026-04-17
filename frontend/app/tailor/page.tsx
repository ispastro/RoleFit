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

    setLoading(true);
    setError(null);
    setResult(null);
    setTexContent(null);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000);

      const response = await fetch(`${API_URL}/api/tailor`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: jobDescription }),
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
  }, [jobDescription, isFormValid, API_URL]);

  const handleReTailor = useCallback(() => {
    setViewMode("preview");
    setResult(null);
    setTexContent(null);
    setError(null);
  }, []);

  const handleCompileToPDF = useCallback(async () => {
    if (!texContent) return;
    
    setPdfGenerating(true);
    setError(null);
    
    try {
      // Fallback: Open Overleaf since latex.js doesn't support complex packages
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = 'https://www.overleaf.com/docs';
      form.target = '_blank';
      
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'snip';
      input.value = texContent;
      
      const nameInput = document.createElement('input');
      nameInput.type = 'hidden';
      nameInput.name = 'snip_name';
      nameInput.value = 'resume.tex';
      
      form.appendChild(input);
      form.appendChild(nameInput);
      document.body.appendChild(form);
      form.submit();
      document.body.removeChild(form);
      
      setPdfGenerating(false);
    } catch (err) {
      console.error('PDF generation error:', err);
      setError('Failed to open Overleaf. Please download LaTeX file instead.');
      setPdfGenerating(false);
    }
  }, [texContent]);

  const handleViewModeChange = useCallback((mode: ViewMode) => {
    setViewMode(mode);
  }, []);

  return (
    <main className="min-h-screen bg-black relative overflow-hidden">
      {/* Animated Background */}
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
              Paste Job Description
            </label>
            <div className="relative">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-neutral-600 to-neutral-800 rounded-lg blur opacity-0 group-focus-within:opacity-30 transition duration-300" />
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the full job description here..."
                className="relative w-full h-96 px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-neutral-600 focus:ring-2 focus:ring-neutral-700/50 transition-all resize-none"
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
                aria-pressed={viewMode === "preview"}
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
                aria-pressed={viewMode === "download"}
              >
                <Download className="w-4 h-4 inline mr-2" /> Download
              </button>
            </div>

            {viewMode === "preview" && texContent && (
              <div className="p-6 bg-neutral-900/50 backdrop-blur-sm border border-neutral-700 rounded-lg relative overflow-hidden">
                <div className="relative">
                  <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-green-400" /> Resume Preview
                  </h3>
                  <div className="bg-black/50 rounded-lg p-4 max-h-96 overflow-y-auto">
                    <pre className="text-neutral-300 text-xs font-mono whitespace-pre-wrap">{texContent}</pre>
                  </div>
                  <div className="mt-4 flex gap-3">
                    <button
                      onClick={handleReTailor}
                      className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-neutral-800 hover:bg-neutral-700 text-white font-semibold rounded-lg transition-all"
                    >
                      <RefreshCw className="w-4 h-4" /> Re-Tailor
                    </button>
                    <button
                      onClick={handleCompileToPDF}
                      disabled={pdfGenerating}
                      className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-500 disabled:bg-green-800 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all hover:scale-105 hover:shadow-2xl hover:shadow-green-500/20 disabled:hover:scale-100 group"
                    >
                      {pdfGenerating ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" /> Generating PDF...
                        </>
                      ) : (
                        <>
                          <FileText className="w-4 h-4 group-hover:animate-pulse" /> Compile to PDF
                        </>
                      )}
                    </button>
                    <a
                      href={result}
                      download
                      className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-white hover:bg-neutral-100 text-black font-semibold rounded-lg transition-all hover:scale-105 hover:shadow-2xl hover:shadow-white/20 group"
                    >
                      <Download className="w-4 h-4 group-hover:animate-bounce" /> Download LaTeX
                    </a>
                  </div>
                </div>
              </div>
            )}

            {viewMode === "download" && (
              <div className="p-6 bg-neutral-900/50 backdrop-blur-sm border border-neutral-700 rounded-lg relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-green-500/5 via-emerald-500/5 to-green-500/5 animate-pulse" />
                <div className="relative">
                  <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-green-400" /> Resume Tailored Successfully!
                  </h3>
                  <div className="flex gap-3">
                    <button
                      onClick={handleReTailor}
                      className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-neutral-800 hover:bg-neutral-700 text-white font-semibold rounded-lg transition-all"
                    >
                      <RefreshCw className="w-4 h-4" /> Re-Tailor
                    </button>
                    <button
                      onClick={handleCompileToPDF}
                      disabled={pdfGenerating}
                      className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-500 disabled:bg-green-800 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all hover:scale-105 hover:shadow-2xl hover:shadow-green-500/20 disabled:hover:scale-100 group"
                    >
                      {pdfGenerating ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" /> Generating PDF...
                        </>
                      ) : (
                        <>
                          <FileText className="w-4 h-4 group-hover:animate-pulse" /> Compile to PDF
                        </>
                      )}
                    </button>
                    <a
                      href={result}
                      download
                      className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-white hover:bg-neutral-100 text-black font-semibold rounded-lg transition-all hover:scale-105 hover:shadow-2xl hover:shadow-white/20 group"
                    >
                      <Download className="w-4 h-4 group-hover:animate-bounce" /> Download LaTeX
                    </a>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
