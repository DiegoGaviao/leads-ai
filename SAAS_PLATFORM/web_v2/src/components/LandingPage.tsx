import { Brain, Rocket, Target } from 'lucide-react'
import { motion } from 'framer-motion'
import { Logo } from './Logo'

interface LandingPageProps {
    onStart: () => void
}

export function LandingPage({ onStart }: LandingPageProps) {
    return (
        <div className="relative overflow-hidden">
            {/* Soft Background Blobs */}
            <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/4 w-[800px] h-[800px] bg-primary/5 blur-[120px] rounded-full -z-10" />
            <div className="absolute bottom-0 left-0 translate-y-1/2 -translate-x-1/4 w-[600px] h-[600px] bg-secondary/5 blur-[120px] rounded-full -z-10" />

            {/* Navigation */}
            <nav className="flex items-center justify-between px-6 py-8 md:px-12 max-w-7xl mx-auto relative z-10">
                <Logo />
                <div className="flex items-center gap-6">
                    {/* Botões removidos para simplificação seguindo a versão final */}
                </div>
            </nav>

            {/* Hero Section */}
            <main className="px-6 pt-24 pb-40 max-w-7xl mx-auto text-center relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, ease: "easeOut" }}
                >
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/50 border border-slate-800 mb-8 backdrop-blur-sm">
                        <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                        <span className="text-[11px] font-bold text-slate-400 tracking-widest uppercase">
                            Nova Inteligência Generativa
                        </span>
                    </div>

                    <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold mb-8 tracking-tight leading-[1.05] font-display text-white">
                        Dados que viram<br />
                        <span className="text-primary italic">vendas reais.</span>
                    </h1>

                    <p className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto mb-12 leading-relaxed">
                        Esqueça a adivinhação. O Leads AI usa engenharia de retenção para revelar os padrões que sua audiência já aprovou no seu Instagram.
                    </p>

                    <div className="flex flex-col md:flex-row items-center justify-center gap-4">
                        {/* Botões de ação removidos seguindo a versão final */}
                    </div>
                </motion.div>

                {/* What it is / Methodology */}
                <div className="mt-48 grid grid-cols-1 lg:grid-cols-2 gap-20 text-left items-center">
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                    >
                        <h2 className="text-4xl md:text-5xl font-bold mb-8 font-display tracking-tight leading-tight">
                            Não é um gerador de roteiros.<br />
                            É o seu <span className="text-primary italic">Brain Trust</span> estratégico.
                        </h2>
                        <p className="text-slate-400 text-lg mb-8 leading-relaxed">
                            O <b>Leads AI</b> é uma inteligência de elite que vive dentro do seu perfil. Diferente de IAs genéricas, nós aplicamos engenharia reversa nos seus dados para descobrir o que sua audiência realmente aprova.
                        </p>
                        <div className="space-y-6">
                            <div className="flex gap-4">
                                <div className="w-10 h-10 shrink-0 bg-primary/10 rounded-lg flex items-center justify-center border border-primary/20 text-primary">
                                    <Target className="w-5 h-5" />
                                </div>
                                <div>
                                    <h4 className="font-bold text-slate-100 mb-1">Diagnóstico de DNA</h4>
                                    <p className="text-sm text-slate-500">Mapeamos seu tom de voz e os padrões que já geram picos de retenção no seu Instagram.</p>
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <div className="w-10 h-10 shrink-0 bg-secondary/10 rounded-lg flex items-center justify-center border border-secondary/20 text-secondary">
                                    <Rocket className="w-5 h-5" />
                                </div>
                                <div>
                                    <h4 className="font-bold text-slate-100 mb-1">Scripts Magnéticos</h4>
                                    <p className="text-sm text-slate-500">Receba roteiros prontos para gravar, com ganchos validados e CTAs que convertem seguidores em clientes.</p>
                                </div>
                            </div>
                        </div>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        className="relative group outline-none"
                    >
                        <div className="absolute inset-0 bg-primary/20 blur-[100px] rounded-full group-hover:bg-primary/30 transition-all duration-700 opacity-50" />
                        <div className="card-premium p-8 relative overflow-hidden flex flex-col gap-6">
                            <div className="flex items-center justify-between border-b border-white/5 pb-4">
                                <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Entrega Final</span>
                                <div className="px-2 py-0.5 bg-green-500/10 text-green-500 text-[10px] font-bold rounded border border-green-500/20">ESTRATÉGIA PRONTA</div>
                            </div>
                            <div className="space-y-4">
                                <div className="h-4 bg-slate-900 rounded-full w-3/4" />
                                <div className="h-4 bg-slate-900 rounded-full w-1/2" />
                                <div className="py-6 bg-primary/5 border border-primary/10 rounded-2xl flex items-center justify-center italic text-slate-400 text-sm px-6 text-center leading-relaxed">
                                    "O Leads AI transformou 50 posts aleatórios em um método replicável que triplicou minha autoridade em tempo recorde."
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-3 mt-4">
                                <div className="bg-slate-950 p-3 rounded-xl border border-white/5 text-center">
                                    <span className="block text-xl font-bold text-primary">85%</span>
                                    <span className="text-[10px] text-slate-500 uppercase font-bold tracking-tighter">Mais Retenção</span>
                                </div>
                                <div className="bg-slate-950 p-3 rounded-xl border border-white/5 text-center">
                                    <span className="block text-xl font-bold text-secondary">10h</span>
                                    <span className="text-[10px] text-slate-500 uppercase font-bold tracking-tighter">Salvas / Sem.</span>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                </div>

                {/* Impact Section */}
                <div className="mt-48 py-24 bg-gradient-to-b from-transparent via-primary/5 to-transparent rounded-[4rem]">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="max-w-4xl mx-auto text-center px-4"
                    >
                        <h2 className="text-3xl md:text-5xl font-bold mb-8 font-display">Liberte-se da Tela em Branco</h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-left mt-16">
                            <div className="space-y-4">
                                <div className="text-primary font-bold text-3xl font-display">01</div>
                                <h4 className="text-lg font-bold text-slate-100">Fim da Adivinhação</h4>
                                <p className="text-sm text-slate-500 leading-relaxed">Pare de postar e torcer. Use dados reais para saber o que postar antes mesmo de abrir a câmera.</p>
                            </div>
                            <div className="space-y-4">
                                <div className="text-secondary font-bold text-3xl font-display">02</div>
                                <h4 className="text-lg font-bold text-slate-100">Escala Sem Esforço</h4>
                                <p className="text-sm text-slate-500 leading-relaxed">Produza conteúdo de nível profissional em 15 minutos, mantendo a qualidade constante.</p>
                            </div>
                            <div className="space-y-4">
                                <div className="text-accent font-bold text-3xl font-display">03</div>
                                <h4 className="text-lg font-bold text-slate-100">Autoridade Inabalável</h4>
                                <p className="text-sm text-slate-500 leading-relaxed">Construa uma marca que as pessoas respeitam, com roteiros baseados no seu verdadeiro DNA.</p>
                            </div>
                        </div>
                    </motion.div>
                </div>

                {/* Pricing / Selection */}
                <div id="pricing" className="mt-48 scroll-mt-20">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-center mb-20"
                    >
                        <h2 className="text-3xl md:text-5xl font-bold mb-4 font-display">Acelere seu Crescimento</h2>
                        <p className="text-slate-400 text-lg">Estratégias validadas por dados, não por opiniões.</p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                        <PlanCard
                            title="Plano Starter"
                            price="R$ 0"
                            description="Valide seu potencial e receba um diagnóstico inicial do seu perfil."
                            features={["Análise de 3 Posts Recentes", "Identificação de Ganchos Fracos", "1 Roteiro Estratégico de Teste", "Acesso ao Conselho de IAs"]}
                            onAction={onStart}
                            buttonText="Começar Gratuitamente"
                        />

                        <PlanCard
                            title="Pro Strategy"
                            price="R$ 29,90"
                            description="Engenharia reversa completa dos seus vídeos para dominar seu nicho."
                            features={["Análise dos 5 Melhores Posts", "Raio-X de Padrões que Retém Públicos", "Matriz de Conteúdo: Ouro vs Lixo", "3 Roteiros Magnéticos Prontos"]}
                            onAction={() => window.location.href = 'https://mpago.la/2sM8erQ'}
                            buttonText="Desbloquear Agora"
                            paymentMethod="Pix & Cartão"
                        />

                        <PlanCard
                            title="Master Edition"
                            price="R$ 129,90"
                            description="Monitoramento profissional e escala contínua com suporte estratégico."
                            features={["Conexão via API Oficial (Meta)", "Histórico Completo de Métricas", "Análise de Sentimento da Audiência", "8 Roteiros Vendedores / Mês", "Consultoria VIP via WhatsApp"]}
                            onAction={() => window.location.href = 'https://mpago.la/31mTMpn'}
                            highlight
                            buttonText="Ativar Master"
                            paymentMethod="Pix & Cartão"
                        />
                    </div>
                </div>

                {/* Trust/Features */}
                <div className="mt-48 grid grid-cols-1 md:grid-cols-3 gap-10 text-left border-t border-slate-900 pt-20">
                    <FeatureItem
                        icon={<Brain className="w-5 h-5 text-primary" />}
                        title="Conselho de IAs (Brainstorming)"
                        description="DeepSeek, GPT-4 e Llama analisam seu conteúdo simultaneamente para garantir uma estratégia sem pontos cegos e ganchos irresistíveis."
                    />
                    <FeatureItem
                        icon={<Target className="w-5 h-5 text-secondary" />}
                        title="Engenharia de Retenção"
                        description="Identificamos matematicamente os segundos exatos onde seu público para de assistir e transformamos essas fraquezas em conversão."
                    />
                    <FeatureItem
                        icon={<Rocket className="w-5 h-5 text-accent" />}
                        title="DNA de Vendas"
                        description="Nossa IA clona seu tom de voz e aplica gatilhos mentais invisíveis, gerando roteiros que vendem sem parecerem propaganda."
                    />
                </div>
            </main>

            {/* Footer Background Glow */}
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-full h-[300px] bg-gradient-to-t from-primary/10 to-transparent -z-10 opacity-30" />
        </div>
    )
}

function PlanCard({ title, price, description, features, onAction, highlight = false, buttonText, paymentMethod }: any) {
    return (
        <div className={`card-premium flex flex-col items-start text-left relative overflow-hidden group ${highlight ? 'border-primary/40 ring-1 ring-primary/20 bg-slate-950' : 'bg-slate-950/50'}`}>
            {highlight && (
                <div className="absolute top-4 right-4 px-2.5 py-1 bg-primary text-slate-950 text-[10px] font-bold uppercase tracking-widest rounded-lg">
                    Mais Completo
                </div>
            )}

            <div className="mb-6 w-full">
                <span className={`text-xs font-bold uppercase tracking-[0.2em] mb-4 block ${highlight ? 'text-primary' : 'text-slate-500'}`}>{title}</span>
                <p className="text-sm text-slate-400 leading-relaxed min-h-[40px]">
                    {description}
                </p>
            </div>

            <ul className="space-y-4 text-[13px] text-slate-400 w-full mb-8 flex-1 border-t border-slate-900 pt-8">
                {features.map((f: string, i: number) => (
                    <li key={i} className="flex items-center gap-3">
                        <div className={`w-1 h-1 rounded-full ${highlight ? 'bg-primary' : 'bg-slate-700'}`} /> {f}
                    </li>
                ))}
            </ul>

            <div className="w-full pt-6 border-t border-slate-900 mb-8 mt-auto">
                <div className="flex items-center justify-between">
                    <div className="flex items-baseline gap-1">
                        <span className="text-4xl font-bold font-display tracking-tight">{price}</span>
                        {price !== "R$ 0" && <span className="text-slate-500 text-sm font-medium">/único</span>}
                    </div>
                    {paymentMethod && (
                        <div className="flex items-center gap-1.5 px-2.5 py-1 bg-slate-900 border border-slate-800 rounded-lg">
                            <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">{paymentMethod}</span>
                        </div>
                    )}
                </div>
            </div>

            <button
                onClick={onAction}
                className={`w-full py-4 rounded-2xl font-bold transition-all text-sm ${highlight ? 'bg-primary text-slate-950 shadow-glow hover:bg-primary/90' : 'bg-slate-800 text-slate-100 hover:bg-slate-700'}`}
            >
                {buttonText}
            </button>
        </div>
    )
}

function FeatureItem({ icon, title, description }: any) {
    return (
        <div className="space-y-4">
            <div className="w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center">
                {icon}
            </div>
            <h3 className="text-lg font-bold font-display">{title}</h3>
            <p className="text-slate-400 text-sm leading-relaxed">{description}</p>
        </div>
    )
}
