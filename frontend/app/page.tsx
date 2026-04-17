import Link from "next/link";
import { Zap, Target, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-black relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Grid */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff08_1px,transparent_1px),linear-gradient(to_bottom,#ffffff08_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000,transparent)]" />
        
        {/* Gradient Orbs */}
        <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob" />
        <div className="absolute top-0 -right-4 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000" />
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000" />
      </div>

      <div className="relative z-10 max-w-5xl mx-auto px-6 py-20">
        {/* Hero */}
        <div className="text-center space-y-8 mb-20 relative">
          {/* Large Circular Gradient Orb behind text */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-br from-neutral-800/40 via-neutral-700/20 to-transparent rounded-full blur-3xl pointer-events-none" />
          
          <div className="inline-block relative z-10">
            <h1 className="text-8xl font-bold tracking-tight">
              <span className="bg-gradient-to-b from-neutral-200 via-neutral-400 to-neutral-600 bg-clip-text text-transparent">
                RoleFit
              </span>
            </h1>
            <div className="flex items-center justify-center gap-3 mt-4">
              <p className="text-neutral-500 text-base">
                Tailor before you <span className="text-white font-medium">apply.</span>
              </p>
            </div>
          </div>
          
          <p className="text-2xl text-neutral-300 max-w-2xl mx-auto leading-relaxed relative z-10">
            Paste a job description. Get a perfectly tailored resume.
            <span className="block text-neutral-500 text-lg mt-2">In seconds.</span>
          </p>

          <Link 
            href="/tailor"
            className="relative z-10 inline-block px-8 py-4 bg-white hover:bg-neutral-100 text-black font-semibold rounded-lg transition-all duration-200 hover:scale-105 hover:shadow-2xl hover:shadow-white/20"
          >
            Start Tailoring →
          </Link>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-20">
          {[
            { Icon: Zap, title: "Lightning Fast", desc: "Powered by Groq's ultra-fast AI" },
            { Icon: Target, title: "Smart Matching", desc: "Semantic understanding, not keyword stuffing" },
            { Icon: Sparkles, title: "Your Voice", desc: "Maintains your style and template" }
          ].map((feature, i) => (
            <div key={i} className="p-6 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-xl hover:border-neutral-600 hover:bg-neutral-900/80 transition-all duration-300 hover:scale-105">
              <feature.Icon className="w-10 h-10 mb-3 text-white" />
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-neutral-400 text-sm">{feature.desc}</p>
            </div>
          ))}
        </div>

        {/* How it works */}
        <div className="text-center space-y-6">
          <h2 className="text-3xl font-bold text-white">How It Works</h2>
          <div className="flex flex-col md:flex-row items-center justify-center gap-4 text-neutral-400">
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded-full bg-white text-black flex items-center justify-center text-sm font-bold">1</span>
              <span>Paste job description</span>
            </div>
            <span className="hidden md:block">→</span>
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded-full bg-white text-black flex items-center justify-center text-sm font-bold">2</span>
              <span>AI analyzes & tailors</span>
            </div>
            <span className="hidden md:block">→</span>
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded-full bg-white text-black flex items-center justify-center text-sm font-bold">3</span>
              <span>Download LaTeX resume</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
