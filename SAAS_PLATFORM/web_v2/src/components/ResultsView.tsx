import { useState } from 'react'
import { motion } from 'framer-motion'
import { User, Target, FileText, Download, Share2, ChevronRight, Copy, Sparkles } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface ResultsViewProps {
    data: {
        persona: string
        estrategia: string
        roteiros: Array<{
            index: number
            tema: string
            visual: string
            texto: string
        }>
    }
}

export function ResultsView({ data }: ResultsViewProps) {
    const [activeTab, setActiveTab] = useState('persona')

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
        alert("Conteúdo copiado!");
    };

    return (
        <div className="max-w-6xl mx-auto px-6 py-20 antialiased">
            {/* Background Blobs for specific page */}
            <div className="fixed top-20 right-0 w-[500px] h-[500px] bg-primary/5 blur-[120px] -z-10 rounded-full" />

            <div className="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-16">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-4"
                >
                    <div className="flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-primary" />
                        <span className="text-[11px] font-bold text-slate-500 uppercase tracking-[0.2em]">Entrega Finalizada</span>
                    </div>
                    <h2 className="text-4xl md:text-5xl font-bold font-display tracking-tight text-slate-50">Sua Nova Estratégia</h2>
                    <p className="text-slate-400 text-lg max-w-xl">
                        Abaixo está o DNA da sua marca e os roteiros mestres gerados pela nossa IA.
                    </p>
                </motion.div>
                <div className="flex gap-4">
                    <button className="btn-secondary py-3 px-6 text-xs font-bold uppercase tracking-widest flex items-center gap-2">
                        <Download className="w-4 h-4" /> Exportar PDF
                    </button>
                    <button className="btn-primary py-3 px-6 text-xs font-bold uppercase tracking-widest flex items-center gap-2">
                        <Share2 className="w-4 h-4" /> Compartilhar
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-12 items-start">
                {/* Sidebar Nav */}
                <aside className="lg:col-span-1 space-y-3 sticky top-12">
                    <TabButton
                        active={activeTab === 'persona'}
                        onClick={() => setActiveTab('persona')}
                        icon={<User className="w-4 h-4" />}
                        label="Avatar & Identidade"
                    />
                    <TabButton
                        active={activeTab === 'estrategia'}
                        onClick={() => setActiveTab('estrategia')}
                        icon={<Target className="w-4 h-4" />}
                        label="Estratégia de Conteúdo"
                    />
                    <TabButton
                        active={activeTab === 'roteiros'}
                        onClick={() => setActiveTab('roteiros')}
                        icon={<FileText className="w-4 h-4" />}
                        label={`${data.roteiros.length} Roteiros Mestres`}
                    />
                </aside>

                {/* Content Area */}
                <main className="lg:col-span-3">
                    <motion.div
                        key={activeTab}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4 }}
                        className="card-premium p-8 md:p-14 min-h-[700px] prose prose-slate prose-invert prose-headings:font-display prose-headings:font-bold prose-p:text-slate-400 prose-p:leading-relaxed prose-strong:text-slate-200 prose-blockquote:border-primary/40 prose-blockquote:bg-slate-900/50 prose-blockquote:py-1 prose-blockquote:px-6 rounded-[2.5rem] max-w-none"
                    >
                        {activeTab === 'persona' && <ReactMarkdown>{data.persona}</ReactMarkdown>}
                        {activeTab === 'estrategia' && <ReactMarkdown>{data.estrategia}</ReactMarkdown>}
                        {activeTab === 'roteiros' && <ScriptsContent roteiros={data.roteiros} onCopy={copyToClipboard} />}
                    </motion.div>
                </main>
            </div>
        </div>
    )
}

function TabButton({ active, onClick, icon, label }: any) {
    return (
        <button
            onClick={onClick}
            className={`w-full flex items-center gap-4 py-4 px-5 rounded-2xl transition-all duration-300 border ${active
                ? 'bg-slate-900 border-slate-800 text-primary shadow-premium'
                : 'bg-transparent border-transparent text-slate-500 hover:text-slate-300 hover:bg-slate-900/50'
                }`}
        >
            <div className={`p-2 rounded-lg transition-colors ${active ? 'bg-primary/10 text-primary' : 'bg-slate-900/50 text-slate-600'}`}>
                {icon}
            </div>
            <span className={`text-[13px] font-bold tracking-tight transition-colors ${active ? 'text-slate-50' : ''}`}>
                {label}
            </span>
            {active && (
                <motion.div layoutId="tab-active-indicator" className="ml-auto">
                    <ChevronRight className="w-4 h-4" />
                </motion.div>
            )}
        </button>
    )
}

function ScriptsContent({ roteiros, onCopy }: any) {
    return (
        <div className="space-y-16 not-prose mt-4">
            {roteiros.map((script: any, i: number) => (
                <div key={i} className="group relative space-y-8 pb-16 border-b border-slate-900 last:border-0 last:pb-0">
                    <div className="flex justify-between items-start">
                        <div className="space-y-1">
                            <span className="text-[10px] font-bold text-primary uppercase tracking-[0.2em]">Roteiro de Alta Performance</span>
                            <h3 className="text-2xl font-bold font-display text-slate-100">{script.tema}</h3>
                        </div>
                        <button
                            onClick={() => onCopy(`${script.visual}\n\n${script.texto}`)}
                            className="p-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-500 hover:text-white hover:border-slate-700 transition-all group-hover:shadow-premium"
                        >
                            <Copy className="w-4 h-4" />
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="space-y-4">
                            <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                                <div className="w-1.5 h-1.5 rounded-full bg-primary" /> Direção Visual
                            </div>
                            <div className="p-6 bg-slate-950/50 border border-slate-900 rounded-3xl text-sm text-slate-400 leading-relaxed border-l-2 border-l-primary/50">
                                {script.visual}
                            </div>
                        </div>
                        <div className="space-y-4">
                            <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                                <div className="w-1.5 h-1.5 rounded-full bg-secondary" /> Script / Narração
                            </div>
                            <div className="p-6 bg-slate-950/50 border border-slate-900 rounded-3xl text-sm text-slate-300 italic leading-relaxed font-sans border-l-2 border-l-secondary/50">
                                "{script.texto}"
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}
