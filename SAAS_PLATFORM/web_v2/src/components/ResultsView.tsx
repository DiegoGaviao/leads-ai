import { useState } from 'react'
import { motion } from 'framer-motion'
import { User, Target, FileText, Download, Share2, ChevronRight, Copy } from 'lucide-react'
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

    return (
        <div className="max-w-6xl mx-auto px-6 py-20">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <h2 className="text-4xl font-bold mb-2">Sua Estratégia Pronta</h2>
                    <p className="text-muted-foreground italic">"Conteúdo com alma fundamentado em dados."</p>
                </motion.div>
                <div className="flex gap-3">
                    <button className="btn-secondary py-2 px-4 text-sm flex items-center gap-2">
                        <Download className="w-4 h-4" /> PDF
                    </button>
                    <button className="btn-primary py-2 px-4 text-sm flex items-center gap-2">
                        <Share2 className="w-4 h-4" /> Compartilhar
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-12">
                {/* Sidebar Nav */}
                <aside className="lg:col-span-1 space-y-2">
                    <TabButton
                        active={activeTab === 'persona'}
                        onClick={() => setActiveTab('persona')}
                        icon={<User className="w-5 h-5" />}
                        label="Identidade & Persona"
                    />
                    <TabButton
                        active={activeTab === 'estrategia'}
                        onClick={() => setActiveTab('estrategia')}
                        icon={<Target className="w-5 h-5" />}
                        label="Estratégia Única"
                    />
                    <TabButton
                        active={activeTab === 'roteiros'}
                        onClick={() => setActiveTab('roteiros')}
                        icon={<FileText className="w-5 h-5" />}
                        label={`${data.roteiros.length} Roteiros Mestres`}
                    />
                </aside>

                {/* Content Area */}
                <main className="lg:col-span-3">
                    <motion.div
                        key={activeTab}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="glass rounded-3xl p-8 md:p-12 min-h-[600px] prose prose-invert max-w-none"
                    >
                        {activeTab === 'persona' && <ReactMarkdown>{data.persona}</ReactMarkdown>}
                        {activeTab === 'estrategia' && <ReactMarkdown>{data.estrategia}</ReactMarkdown>}
                        {activeTab === 'roteiros' && <ScriptsContent roteiros={data.roteiros} />}
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
            className={`w-full flex items-center gap-4 p-4 rounded-xl transition-all ${active
                    ? 'bg-primary text-white shadow-lg shadow-primary/20'
                    : 'hover:bg-white/5 text-muted-foreground hover:text-white'
                }`}
        >
            {icon}
            <span className="font-bold">{label}</span>
            {active && <ChevronRight className="w-4 h-4 ml-auto" />}
        </button>
    )
}

function ScriptsContent({ roteiros }: any) {
    return (
        <div className="space-y-12 not-prose">
            {roteiros.map((script: any, i: number) => (
                <div key={i} className="p-6 bg-white/5 rounded-2xl border border-white/5 space-y-4 relative">
                    <div className="flex justify-between items-center">
                        <span className="px-3 py-1 rounded-full bg-primary/20 text-primary text-xs font-bold uppercase tracking-wider">REEL #{script.index || i + 1}</span>
                        <button className="text-muted-foreground hover:text-white transition-colors"><Copy className="w-5 h-5" /></button>
                    </div>
                    <h5 className="text-xl font-bold">{script.tema}</h5>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                        <div className="space-y-2">
                            <p className="text-muted-foreground font-bold uppercase text-[10px] tracking-widest">Visual</p>
                            <div className="p-3 bg-black/30 rounded-lg border border-white/5 leading-relaxed">{script.visual}</div>
                        </div>
                        <div className="space-y-2">
                            <p className="text-muted-foreground font-bold uppercase text-[10px] tracking-widest">Fala / Texto</p>
                            <div className="p-3 bg-black/30 rounded-lg border border-white/5 italic leading-relaxed">"{script.texto}"</div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}
