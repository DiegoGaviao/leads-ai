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
                    <div className="flex flex-col">
                        <span className="text-xl font-bold tracking-tight">Leads AI</span>
                        <span className="text-[10px] text-muted-foreground font-mono leading-none">v2.0.3-STABLE</span>
                    </div>
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

                {/* Pricing Section */}
                <div id="pricing" className="mt-40 scroll-mt-20">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <h2 className="text-4xl md:text-5xl font-extrabold mb-4">Escolha seu Nível</h2>
                        <p className="text-muted-foreground text-lg">Deixe os dados guiarem seu crescimento.</p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                        {/* Trial Plan */}
                        <div className="glass p-8 rounded-3xl border border-white/5 flex flex-col items-start text-left relative overflow-hidden group">
                            <div className="mb-8">
                                <span className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-4 block">Trial Grátis</span>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-4xl font-extrabold">R$ 0</span>
                                </div>
                                <p className="text-sm text-muted-foreground mt-4 leading-relaxed">
                                    Experimente a tecnologia sem riscos e descubra seus primeiros padrões.
                                </p>
                            </div>

                            <button
                                onClick={() => window.location.href = '/projetos/leads-ai/setup?plan=free'}
                                className="w-full py-4 rounded-xl bg-white/5 border border-white/10 font-bold hover:bg-white/10 transition-all mb-8"
                            >
                                Começar Grátis
                            </button>

                            <ul className="space-y-4 text-sm text-muted-foreground w-full">
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-primary" /> Análise de 3 Posts
                                </li>
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-primary" /> Diagnóstico de Ganchos
                                </li>
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-primary" /> 1 Ideia de Roteiro
                                </li>
                            </ul>
                        </div>

                        {/* Pro Plan */}
                        <div className="glass p-8 rounded-3xl border-2 border-primary/50 flex flex-col items-start text-left relative overflow-hidden group bg-primary/5">
                            <div className="absolute top-4 right-4 px-3 py-1 bg-primary text-[10px] font-bold uppercase tracking-widest rounded-full">
                                Mais Popular
                            </div>
                            <div className="mb-8">
                                <span className="text-sm font-bold text-primary uppercase tracking-widest mb-4 block">Pro Strategy</span>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-4xl font-extrabold">R$ 29,90</span>
                                    <span className="text-muted-foreground text-sm">/único</span>
                                </div>
                                <p className="text-sm text-muted-foreground mt-4 leading-relaxed">
                                    Engenharia reversa completa para escalar seu perfil.
                                </p>
                            </div>

                            <button
                                onClick={() => window.location.href = 'https://mpago.la/2sM8erQ'}
                                className="w-full py-4 rounded-xl bg-primary text-white font-bold hover:bg-primary-hover transition-all mb-8 shadow-lg shadow-primary/20"
                            >
                                Desbloquear Estratégia
                            </button>

                            <ul className="space-y-4 text-sm w-full">
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-primary" /> Análise de 5 Melhores Posts
                                </li>
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-primary" /> Raio-X de Padrões Visuais
                                </li>
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-primary" /> Gráfico "Ouro vs Lixo"
                                </li>
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-primary" /> 3 Roteiros Prontos para Gravar
                                </li>
                            </ul>
                        </div>

                        {/* Master Plan */}
                        <div className="glass p-8 rounded-3xl border border-white/5 flex flex-col items-start text-left relative overflow-hidden group">
                            <div className="mb-8">
                                <span className="text-sm font-bold text-secondary uppercase tracking-widest mb-4 block">Master Data</span>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-4xl font-extrabold">R$ 129,90</span>
                                    <span className="text-muted-foreground text-sm">/mês</span>
                                </div>
                                <p className="text-sm text-muted-foreground mt-4 leading-relaxed">
                                    Conectamos todos os seus posts e dados ao sistema para uma análise completa.
                                </p>
                            </div>

                            <button
                                onClick={() => window.location.href = 'https://mpago.la/31mTMpn'}
                                className="w-full py-4 rounded-xl bg-white/5 border border-white/10 font-bold hover:bg-white/10 transition-all mb-8"
                            >
                                Assinar Master
                            </button>

                            <ul className="space-y-4 text-sm text-muted-foreground w-full">
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-secondary" /> Conexão Total com Instagram
                                </li>
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-secondary" /> Análise de Todo Histórico
                                </li>
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-secondary" /> 2 Roteiros Semanais (8/mês)
                                </li>
                                <li className="flex items-center gap-3">
                                    <Zap className="w-4 h-4 text-secondary" /> Relatório de Evolução Mensal
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

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
