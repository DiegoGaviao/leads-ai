import { useState, type ReactNode } from 'react'
import { motion } from 'framer-motion'
import { User, Target, FileText, Download, Share2, ChevronRight, Copy, Sparkles } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { useNavigate } from 'react-router-dom'

interface ResultsViewProps {
    data: {
        persona: string
        estrategia: string
        roteiros: Array<{
            index: number
            tema: string
            visual: string
            texto: string
            image_url?: string
            visual_prompts?: string[]
        }>
    }
}

export function ResultsView({ data }: ResultsViewProps) {
    const [activeTab, setActiveTab] = useState('persona')
    const navigate = useNavigate()

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
        alert("Conteúdo copiado!");
    };

    return (
        <div className="mx-auto max-w-6xl px-5 py-12 antialiased md:px-8 md:py-16">
            <div className="fixed top-24 right-0 -z-10 h-[400px] w-[400px] rounded-full bg-emerald-500/[0.04] blur-[100px]" />

            <div className="mb-12 flex flex-col justify-between gap-8 md:mb-16 md:flex-row md:items-end">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-4"
                >
                    <div className="flex items-center gap-2">
                        <Sparkles className="h-5 w-5 text-emerald-600" />
                        <span className="text-[11px] font-bold uppercase tracking-[0.2em] text-slate-500">Entrega finalizada</span>
                    </div>
                    <h2 className="font-display text-3xl font-bold tracking-tight text-slate-900 md:text-4xl lg:text-5xl">Sua nova estratégia</h2>
                    <p className="max-w-xl text-lg text-slate-600">
                        DNA da marca, roteiros e criativos visuais gerados para você publicar mais rápido.
                    </p>
                </motion.div>
                <div className="flex flex-wrap gap-3">
                    <button type="button" className="btn-secondary flex items-center gap-2 py-3 px-5 text-xs font-bold uppercase tracking-widest">
                        <Download className="h-4 w-4" /> Exportar PDF
                    </button>
                    <button
                        type="button"
                        onClick={() => navigate('/posts')}
                        className="btn-secondary flex items-center gap-2 py-3 px-5 text-xs font-bold uppercase tracking-widest"
                    >
                        <FileText className="h-4 w-4" /> Ver tabela de posts
                    </button>
                    <button type="button" className="btn-primary flex items-center gap-2 py-3 px-5 text-xs font-bold uppercase tracking-widest">
                        <Share2 className="h-4 w-4" /> Compartilhar
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 items-start gap-10 lg:grid-cols-4 lg:gap-12">
                <aside className="sticky top-0 space-y-2 lg:col-span-1 lg:top-12">
                    <TabButton
                        active={activeTab === 'persona'}
                        onClick={() => setActiveTab('persona')}
                        icon={<User className="h-4 w-4" />}
                        label="Avatar & identidade"
                    />
                    <TabButton
                        active={activeTab === 'estrategia'}
                        onClick={() => setActiveTab('estrategia')}
                        icon={<Target className="h-4 w-4" />}
                        label="Estratégia de conteúdo"
                    />
                    <TabButton
                        active={activeTab === 'roteiros'}
                        onClick={() => setActiveTab('roteiros')}
                        icon={<FileText className="h-4 w-4" />}
                        label={`${data.roteiros.length} roteiros mestres`}
                    />
                </aside>

                <main className="lg:col-span-3">
                    <motion.div
                        key={activeTab}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4 }}
                        className="card-premium min-h-[560px] max-w-none rounded-[2rem] p-6 md:p-12 lg:min-h-[700px] prose prose-slate max-w-none prose-headings:font-display prose-headings:font-bold prose-headings:text-slate-900 prose-p:text-slate-600 prose-p:leading-relaxed prose-strong:text-slate-800 prose-blockquote:border-emerald-500/40 prose-blockquote:bg-slate-50 prose-blockquote:py-1 prose-blockquote:px-6"
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

function TabButton({ active, onClick, icon, label }: { active: boolean; onClick: () => void; icon: ReactNode; label: string }) {
    return (
        <button
            type="button"
            onClick={onClick}
            className={`flex w-full items-center gap-4 rounded-2xl border py-4 px-5 transition-all duration-300 ${
                active
                    ? 'border-emerald-200 bg-emerald-50 text-emerald-900 shadow-sm'
                    : 'border-transparent bg-transparent text-slate-500 hover:bg-slate-100 hover:text-slate-800'
            }`}
        >
            <div className={`rounded-lg p-2 transition-colors ${active ? 'bg-white text-emerald-700 shadow-sm' : 'bg-slate-100 text-slate-500'}`}>
                {icon}
            </div>
            <span className={`text-[13px] font-bold tracking-tight ${active ? 'text-slate-900' : ''}`}>
                {label}
            </span>
            {active && (
                <motion.div layoutId="tab-active-indicator" className="ml-auto">
                    <ChevronRight className="h-4 w-4 text-emerald-600" />
                </motion.div>
            )}
        </button>
    )
}

function ScriptsContent({ roteiros, onCopy }: { roteiros: any[]; onCopy: (t: string) => void }) {
    return (
        <div className="not-prose mt-4 space-y-16">
            {roteiros.map((script: any, i: number) => (
                <div key={i} className="group relative space-y-8 border-b border-slate-200 pb-16 last:border-0 last:pb-0">
                    <div className="flex items-start justify-between">
                        <div className="space-y-1">
                            <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-emerald-700">Roteiro de alta performance</span>
                            <h3 className="font-display text-2xl font-bold text-slate-900">{script.tema}</h3>
                        </div>
                        <button
                            type="button"
                            onClick={() => onCopy(`${script.visual}\n\n${script.texto}`)}
                            className="rounded-xl border border-slate-200 bg-white p-3 text-slate-500 shadow-sm transition-all hover:border-slate-300 hover:text-slate-900"
                        >
                            <Copy className="h-4 w-4" />
                        </button>
                    </div>

                    <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
                        <div className="space-y-4">
                            {script.image_url ? (
                                <>
                                    <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-slate-500">
                                        <div className="h-1.5 w-1.5 rounded-full bg-emerald-600" /> Criativo (IA)
                                    </div>
                                    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-slate-50 shadow-sm">
                                        <img
                                            src={script.image_url}
                                            alt={`Criativo: ${script.tema}`}
                                            className="h-auto w-full object-cover"
                                            loading="lazy"
                                        />
                                    </div>
                                </>
                            ) : null}
                            <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-slate-500">
                                <div className="h-1.5 w-1.5 rounded-full bg-emerald-500" /> Direção visual
                            </div>
                            <div className="rounded-3xl border border-slate-200 border-l-4 border-l-emerald-500/60 bg-slate-50 p-6 text-sm leading-relaxed text-slate-700">
                                {script.visual}
                            </div>
                        </div>
                        <div className="space-y-4">
                            <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-slate-500">
                                <div className="h-1.5 w-1.5 rounded-full bg-emerald-800/70" /> Script / narração
                            </div>
                            <div className="rounded-3xl border border-slate-200 border-l-4 border-l-emerald-500/40 bg-white p-6 font-sans text-sm italic leading-relaxed text-slate-700">
                                &ldquo;{script.texto}&rdquo;
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}
