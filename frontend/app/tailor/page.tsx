"use client";

import { useState } from "react";
import Link from "next/link";
import { Loader2, CheckCircle, ArrowLeft, Download } from "lucide-react";

export default function TailorPage() {
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!jobDescription.trim()) {
      setError("Please paste a job description");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/api/tailor`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: jobDescription })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMsg = errorData.detail || "Failed to tailor resume";
        throw new Error(errorMsg);
      }

      const data = await response.json();
      setResult(`${API_URL}${data.download_url}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Grid */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff08_1px,transparent_1px),linear-gradient(to_bottom,#ffffff08_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000,transparent)]" />
        
        {/* Large Circular Gradient Orb */}
        <div className="absolute top-40 left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-gradient-to-br from-neutral-800/30 via-neutral-700/15 to-transparent rounded-full blur-3xl pointer-events-none" />
        
        {/* Gradient Orbs */}
        <div className="absolute top-20 -left-4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob pointer-events-none" />
        <div className="absolute top-40 -right-4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000 pointer-events-none" />
        <div className="absolute bottom-20 left-1/3 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000 pointer-events-none" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="flex items-center justify-between mb-12 backdrop-blur-sm">
          <Link href="/" className="text-2xl font-bold hover:scale-105 transition-transform">
            <span className="bg-gradient-to-b from-neutral-200 via-neutral-400 to-neutral-600 bg-clip-text text-transparent">RoleFit</span>
          </Link>
          <Link href="/" className="text-neutral-400 hover:text-white text-sm flex items-center gap-1 transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back
          </Link>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6 relative">
          <div>
            <label className="block text-neutral-300 font-semibold mb-3">
              Paste Job Description
            </label>
            <div className="relative">
              {/* Glow effect on focus */}
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
            {/* Button shine effect */}
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

        {/* Error */}
        {error && (
          <div className="mt-6 p-4 bg-neutral-900/50 backdrop-blur-sm border border-neutral-700 rounded-lg text-neutral-300">
            {error}
          </div>
        )}

        {/* Success */}
        {result && (
          <div className="mt-6 p-6 bg-neutral-900/50 backdrop-blur-sm border border-neutral-700 rounded-lg relative overflow-hidden">
            {/* Success glow */}
            <div className="absolute inset-0 bg-gradient-to-r from-green-500/5 via-emerald-500/5 to-green-500/5 animate-pulse" />
            <div className="relative">
              <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-400" /> Resume Tailored Successfully!
              </h3>
              <a
                href={result}
                download
                className="inline-flex items-center gap-2 px-6 py-3 bg-white hover:bg-neutral-100 text-black font-semibold rounded-lg transition-all hover:scale-105 hover:shadow-2xl hover:shadow-white/20 group"
              >
                <Download className="w-4 h-4 group-hover:animate-bounce" /> Download Resume
              </a>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
