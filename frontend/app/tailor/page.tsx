"use client";

import { useState } from "react";
import Link from "next/link";
import { Loader2, CheckCircle, ArrowLeft, Download } from "lucide-react";

export default function TailorPage() {
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

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
      const response = await fetch("http://localhost:8000/api/tailor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: jobDescription })
      });

      if (!response.ok) throw new Error("Failed to tailor resume");

      const data = await response.json();
      setResult(data.download_url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black">
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="flex items-center justify-between mb-12">
          <Link href="/" className="text-2xl font-bold text-white">
            RoleFit
          </Link>
          <Link href="/" className="text-neutral-400 hover:text-neutral-300 text-sm flex items-center gap-1">
            <ArrowLeft className="w-4 h-4" /> Back
          </Link>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-neutral-300 font-semibold mb-3">
              Paste Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full job description here..."
              className="w-full h-96 px-4 py-3 bg-neutral-900 border border-neutral-800 rounded-lg text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-white focus:ring-2 focus:ring-white/20 transition-all resize-none"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading || !jobDescription.trim()}
            className="w-full px-6 py-4 bg-white hover:bg-neutral-100 disabled:bg-neutral-800 disabled:text-neutral-600 text-black font-semibold rounded-lg transition-all duration-200 disabled:hover:scale-100"
          >
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
          <div className="mt-6 p-4 bg-neutral-900 border border-neutral-700 rounded-lg text-neutral-300">
            {error}
          </div>
        )}

        {/* Success */}
        {result && (
          <div className="mt-6 p-6 bg-neutral-900 border border-neutral-700 rounded-lg">
            <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
              <CheckCircle className="w-5 h-5" /> Resume Tailored Successfully!
            </h3>
            <a
              href={result}
              download
              className="inline-flex items-center gap-2 px-6 py-3 bg-white hover:bg-neutral-100 text-black font-semibold rounded-lg transition-all"
            >
              <Download className="w-4 h-4" /> Download Resume
            </a>
          </div>
        )}
      </div>
    </main>
  );
}
