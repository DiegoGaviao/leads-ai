import { ArrowRight, Sparkles, Brain, BarChart3, Zap } from 'lucide-react'
import { motion } from 'framer-motion'

interface LandingPageProps {
    onStart: () => void
}

export function LandingPage({ onStart }: LandingPageProps) {
    return (
        <div className="relative">
            {/* Navigation */}
            <nav className="flex items-center justify-between px-6 py-8 md:px-12 max-w-7xl mx-auto">
                <div className="flex items-center gap-2">
                    <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
                        <Sparkles className="text-white w-6 h-6" />
                    </div>
                    <span className="text-xl font-bold tracking-tight">Leads AI</span>
                </div>
                <button onClick={onStart} className="btn-secondary hidden md:block">
                    Entrar
                </button>
            </nav>

            {/* Hero */}
            <main className="px-6 pt-20 pb-32 max-w-7xl mx-auto text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <span className="px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-bold tracking-widest uppercase border border-primary/20 mb-8 inline-block">
                        Inteligência de Conteúdo com Alma
                    </span>
                    <h1 className="text-6xl md:text-8xl font-extrabold mb-8 tracking-tighter leading-[1.1]">
                        Pare de adivinhar.<br />
                        <span className="gradient-text">Domine o algoritmo.</span>
                    </h1>
                    <p className="text-muted-foreground text-lg md:text-xl max-w-2xl mx-auto mb-12 leading-relaxed">
                        Nós não comparamos você com os outros. Analisamos os seus próprios dados para revelar o padrão exato que sua audiência já aprovou.
                    </p>

                    <div className="flex flex-col md:flex-row items-center justify-center gap-4">
                        <button onClick={onStart} className="btn-primary flex items-center gap-2 w-full md:w-auto text-lg group">
                            Começar agora <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </button>
                        <button className="btn-secondary w-full md:w-auto text-lg">
                            Ver demonstração
                        </button>
                    </div>
                </motion.div>

                {/* Features Preview */}
                <div className="mt-40 grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
                    <FeatureCard
                        icon={<Brain className="w-6 h-6 text-primary" />}
                        title="Conselho de IAs"
                        description="DeepSeek, OpenAI e HuggingFace trabalham juntos para criar sua estratégia."
                    />
                    <FeatureCard
                        icon={<BarChart3 className="w-6 h-6 text-secondary" />}
                        title="Análise Estatística"
                        description="Identificamos matematicamente quais posts geram retenção e vendas reais."
                    />
                    <FeatureCard
                        icon={<Zap className="w-6 h-6 text-accent" />}
                        title="Roteiros Prontos"
                        description="Receba 5 roteiros otimizados baseados no seu histórico de sucesso."
                    />
                </div>
            </main>
        </div>
    )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="glass p-8 rounded-2xl"
        >
            <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center mb-6 border border-white/10">
                {icon}
            </div>
            <h3 className="text-xl font-bold mb-3">{title}</h3>
            <p className="text-muted-foreground leading-relaxed">{description}</p>
        </motion.div>
    )
}
