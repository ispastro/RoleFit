import Link from "next/link";
import { Zap, Target, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-black">
      <div className="max-w-5xl mx-auto px-6 py-20">
        {/* Hero */}
        <div className="text-center space-y-8 mb-20">
          <div className="inline-block">
            <h1 className="text-7xl font-bold text-white">
              RoleFit
            </h1>
            <p className="text-neutral-500 text-sm mt-2">AI Resume Tailoring</p>
          </div>
          
          <p className="text-2xl text-neutral-300 max-w-2xl mx-auto leading-relaxed">
            Paste a job description. Get a perfectly tailored resume.
            <span className="block text-neutral-500 text-lg mt-2">In seconds.</span>
          </p>

          <Link 
            href="/tailor"
            className="inline-block px-8 py-4 bg-white hover:bg-neutral-100 text-black font-semibold rounded-lg transition-all duration-200"
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
            <div key={i} className="p-6 bg-neutral-900 border border-neutral-800 rounded-xl hover:border-neutral-700 transition-colors">
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
