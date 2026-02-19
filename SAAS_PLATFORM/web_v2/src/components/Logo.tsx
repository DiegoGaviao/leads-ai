import { motion } from 'framer-motion'

export function Logo({ className = "", withText = true }: { className?: string, withText?: boolean }) {
    return (
        <div className={`flex items-center gap-3 ${className}`}>
            <div className="relative group">
                {/* Glow Effect */}
                <div className="absolute inset-0 bg-primary/40 blur-xl rounded-full group-hover:bg-primary/60 transition-all duration-500 opacity-50" />

                {/* SVG Icon Concept: Combination of 'L' + Growth Arrow + Tech Nodes */}
                <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="relative z-10">
                    {/* Background Shape */}
                    <rect width="40" height="40" rx="12" fill="#0D0D0D" />
                    <rect width="40" height="40" rx="12" stroke="#1A1A1A" strokeWidth="1" />

                    {/* The "L" and Growth Stroke */}
                    <motion.path
                        d="M12 28V12M12 28H28M12 28L28 12M28 12L22 12M28 12L28 18"
                        stroke="#00FF41"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        initial={{ pathLength: 0, opacity: 0 }}
                        animate={{ pathLength: 1, opacity: 1 }}
                        transition={{ duration: 1.5, ease: "easeInOut" }}
                    />

                    {/* AI Nodes */}
                    <circle cx="12" cy="12" r="2" fill="#00FF41" />
                    <circle cx="28" cy="28" r="2" fill="#00FF41" />
                    <circle cx="28" cy="12" r="2" fill="#FFFFFF" />
                </svg>
            </div>

            {withText && (
                <div className="flex flex-col">
                    <span className="text-xl font-bold tracking-tight font-display text-white">
                        LEADS<span className="text-primary italic">AI</span>
                    </span>
                    <span className="text-[9px] text-slate-500 font-bold uppercase tracking-[0.3em]">
                        by Dhawk Labs
                    </span>
                </div>
            )}
        </div>
    )
}
