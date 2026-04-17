import Link from "next/link";
import { Zap, Target, Sparkles, CheckCircle, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-black relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff08_1px,transparent_1px),linear-gradient(to_bottom,#ffffff08_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000,transparent)]" />
        <div className="absolute top-0 -left-4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
        <div className="absolute top-0 -right-4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
        <div className="absolute -bottom-8 left-20 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000" />
      </div>

      <div className="relative z-10">
        {/* Navigation */}
        <nav className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
          <div className="text-2xl font-bold">
            <span className="bg-gradient-to-b from-neutral-200 via-neutral-400 to-neutral-600 bg-clip-text text-transparent">
              RoleFit
            </span>
          </div>
          <div className="flex items-center gap-6">
            <a href="https://github.com/ispastro" target="_blank" rel="noopener noreferrer" className="text-neutral-400 hover:text-white transition-colors text-sm">
              GitHub
            </a>
            <Link 
              href="/tailor"
              className="px-6 py-2 bg-white hover:bg-neutral-100 text-black font-semibold rounded-lg transition-all hover:scale-105"
            >
              Get Started
            </Link>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="max-w-6xl mx-auto px-6 py-20 text-center space-y-8">
          <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-br from-neutral-800/40 via-neutral-700/20 to-transparent rounded-full blur-3xl pointer-events-none" />
          
          <div className="inline-block px-4 py-2 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-full text-sm text-neutral-300 mb-6">
            ⚡ Powered by Groq AI • Lightning Fast
          </div>

          <h1 className="text-7xl md:text-8xl font-bold tracking-tight leading-tight">
            <span className="bg-gradient-to-b from-white via-neutral-200 to-neutral-500 bg-clip-text text-transparent">
              Tailor Your Resume
            </span>
            <br />
            <span className="bg-gradient-to-b from-neutral-400 via-neutral-500 to-neutral-700 bg-clip-text text-transparent">
              In Seconds
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-neutral-400 max-w-3xl mx-auto leading-relaxed">
            Paste a job description. Get a perfectly tailored resume that matches the role.
            <span className="block text-neutral-500 text-lg mt-2">No manual editing. No keyword stuffing. Just results.</span>
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-6">
            <Link 
              href="/tailor"
              className="group px-8 py-4 bg-white hover:bg-neutral-100 text-black font-semibold rounded-lg transition-all duration-200 hover:scale-105 hover:shadow-2xl hover:shadow-white/20 flex items-center gap-2"
            >
              Start Tailoring Free
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <a 
              href="https://github.com/ispastro/RoleFit"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-neutral-900/50 backdrop-blur-sm border border-neutral-700 hover:border-neutral-500 text-white font-semibold rounded-lg transition-all hover:scale-105 flex items-center gap-2"
            >
              View on GitHub
            </a>
          </div>

          {/* Social Proof */}
          <div className="pt-12 flex items-center justify-center gap-8 text-sm text-neutral-500">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>No signup required</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>100% free</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>Open source</span>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="max-w-7xl mx-auto px-6 py-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Why RoleFit?
            </h2>
            <p className="text-xl text-neutral-400">
              Built by engineers, for engineers
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { 
                Icon: Zap, 
                title: "Lightning Fast", 
                desc: "Powered by Groq's ultra-fast AI inference. Tailor your resume in under 10 seconds.",
                gradient: "from-yellow-500/20 to-orange-500/20"
              },
              { 
                Icon: Target, 
                title: "Smart Matching", 
                desc: "Semantic understanding of job requirements. No keyword stuffing, just intelligent tailoring.",
                gradient: "from-blue-500/20 to-cyan-500/20"
              },
              { 
                Icon: Sparkles, 
                title: "Your Voice", 
                desc: "Maintains your writing style and LaTeX template. Only emphasizes what matters.",
                gradient: "from-purple-500/20 to-pink-500/20"
              }
            ].map((feature, i) => (
              <div 
                key={i} 
                className="group p-8 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-2xl hover:border-neutral-600 transition-all duration-300 hover:scale-105 relative overflow-hidden"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-300`} />
                <div className="relative z-10">
                  <div className="w-14 h-14 bg-white/10 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <feature.Icon className="w-7 h-7 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                  <p className="text-neutral-400 leading-relaxed">{feature.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* How It Works */}
        <div className="max-w-5xl mx-auto px-6 py-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              How It Works
            </h2>
            <p className="text-xl text-neutral-400">
              Three simple steps to your perfect resume
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { step: "1", title: "Paste Job Description", desc: "Copy the job posting you're applying for" },
              { step: "2", title: "AI Analyzes & Tailors", desc: "Our AI matches your experience to the role" },
              { step: "3", title: "Download & Apply", desc: "Get your tailored LaTeX resume instantly" }
            ].map((item, i) => (
              <div key={i} className="relative">
                <div className="flex flex-col items-center text-center space-y-4">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-white to-neutral-400 flex items-center justify-center text-2xl font-bold text-black">
                    {item.step}
                  </div>
                  <h3 className="text-xl font-semibold text-white">{item.title}</h3>
                  <p className="text-neutral-400">{item.desc}</p>
                </div>
                {i < 2 && (
                  <div className="hidden md:block absolute top-8 left-[60%] w-[80%] h-0.5 bg-gradient-to-r from-neutral-700 to-transparent" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="max-w-4xl mx-auto px-6 py-20">
          <div className="relative p-12 bg-gradient-to-br from-neutral-900/80 to-neutral-900/40 backdrop-blur-sm border border-neutral-800 rounded-3xl text-center overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 via-blue-500/10 to-pink-500/10" />
            <div className="relative z-10 space-y-6">
              <h2 className="text-4xl md:text-5xl font-bold text-white">
                Ready to Land Your Dream Job?
              </h2>
              <p className="text-xl text-neutral-300 max-w-2xl mx-auto">
                Join engineers who are getting more interviews with tailored resumes
              </p>
              <Link 
                href="/tailor"
                className="inline-flex items-center gap-2 px-8 py-4 bg-white hover:bg-neutral-100 text-black font-semibold rounded-lg transition-all duration-200 hover:scale-105 hover:shadow-2xl hover:shadow-white/20"
              >
                Start Tailoring Now
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="max-w-7xl mx-auto px-6 py-12 border-t border-neutral-900">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="text-neutral-500 text-sm">
              © 2026 RoleFit. Built with FastAPI, Next.js, and Groq AI.
            </div>
            <div className="flex items-center gap-6">
              <a href="https://github.com/ispastro" target="_blank" rel="noopener noreferrer" className="text-neutral-500 hover:text-white transition-colors">
                GitHub
              </a>
              <a href="https://haileasaye.me" target="_blank" rel="noopener noreferrer" className="text-neutral-500 hover:text-white transition-colors">
                Portfolio
              </a>
            </div>
          </div>
        </footer>
      </div>
    </main>
  );
}
