import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { ArrowRight } from 'lucide-react';
import { Logo } from '../components/Logo';

export default function OnboardingPage() {
    const navigate = useNavigate();
    const { setBasicInfo, setStrategy } = useOnboardingStore();
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);

    // Captura o plano via URL no mount
    React.useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const urlPlan = params.get('plan') as any;
        if (urlPlan && ['free', 'pro', 'master'].includes(urlPlan)) {
            setBasicInfo({ plan: urlPlan });
        }
    }, []);

    // Form State Local
    const [formData, setFormData] = useState({
        email: '', instagram: '', whatsapp: '',
        mission: '', enemy: '', pain: '', dream: '', dreamClient: '', method: '',
        toneVoice: '', brandValues: '', offerDetails: '', differentiation: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleNext = () => {
        if (step === 1) {
            if (!formData.email || !formData.instagram) return alert("Preencha email e instagram");
            setBasicInfo({
                email: formData.email,
                instagram: formData.instagram,
                whatsapp: formData.whatsapp
            });
            setStep(2);
        } else if (step === 2) {
            if (!formData.dreamClient || !formData.pain) return alert("Preencha os dados do seu público.");
            setStep(3);
        } else {
            if (!formData.mission || !formData.offerDetails) return alert("A Missão e Detalhes da Oferta são obrigatórios.");

            setLoading(true);
            setStrategy({
                mission: formData.mission,
                enemy: formData.enemy,
                pain: formData.pain,
                dream: formData.dream,
                dreamClient: formData.dreamClient,
                method: formData.method,
                toneVoice: formData.toneVoice,
                brandValues: formData.brandValues,
                offerDetails: formData.offerDetails,
                differentiation: formData.differentiation
            });

            setTimeout(() => {
                setLoading(false);
                navigate('/connect');
            }, 1000);
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-50 flex flex-col items-center justify-center p-6 antialiased">

            {/* Background Blobs */}
            <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-[400px] bg-primary/5 blur-[120px] -z-10" />

            {/* Header / Logo */}
            <div className="mb-12">
                <Logo />
            </div>

            {/* Progress Wrapper */}
            <div className="w-full max-w-xl mb-12 relative">
                <div className="flex items-center justify-between relative z-10 px-2">
                    <ProgressStep number={1} label="Identidade" active={step >= 1} current={step === 1} />
                    <ProgressStep number={2} label="Psicologia" active={step >= 2} current={step === 2} />
                    <ProgressStep number={3} label="Estratégia" active={step >= 3} current={step === 3} />
                </div>
                {/* Connecting lines */}
                <div className="absolute top-5 left-0 w-full h-[1px] bg-slate-800 -z-0">
                    <div className={`h-full bg-primary transition-all duration-500`} style={{ width: step === 1 ? '0%' : step === 2 ? '50%' : '100%' }} />
                </div>
            </div>

            <div className="card-premium max-w-2xl w-full shadow-2xl relative overflow-hidden">
                {/* Glow effect for cards */}
                <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 blur-3xl rounded-full" />

                {step === 1 && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="text-center">
                            <h2 className="text-2xl font-bold font-display mb-2">Primeiros Passos</h2>
                            <p className="text-slate-400 text-sm">Dados básicos para personalizarmos sua experiência.</p>
                        </div>

                        <div className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">Instagram (sem @)</label>
                                    <div className="flex group">
                                        <span className="inline-flex items-center px-4 rounded-l-2xl border border-r-0 border-slate-800 bg-slate-900/50 text-slate-500 transition-colors group-focus-within:border-primary/50 group-focus-within:text-primary">@</span>
                                        <input
                                            name="instagram"
                                            value={formData.instagram} onChange={handleChange}
                                            placeholder="seu_perfil"
                                            className="flex-1 px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-r-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 focus:bg-slate-900 transition-all text-sm"
                                        />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">WhatsApp</label>
                                    <input
                                        name="whatsapp"
                                        value={formData.whatsapp} onChange={handleChange}
                                        placeholder="Ex: 43 99999-9999"
                                        className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 focus:bg-slate-900 transition-all text-sm"
                                    />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">E-mail para Relatórios</label>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email} onChange={handleChange}
                                    placeholder="Ex: contato@suaempresa.com"
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 focus:bg-slate-900 transition-all text-sm"
                                />
                            </div>
                        </div>
                    </div>
                )}

                {step === 2 && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="text-center">
                            <h2 className="text-2xl font-bold font-display mb-2">Engenharia do Público</h2>
                            <p className="text-slate-400 text-sm">A IA precisa entender a mente de quem você quer atingir.</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">Público Alvo (Persona)</label>
                                <input
                                    name="dreamClient"
                                    value={formData.dreamClient} onChange={handleChange}
                                    placeholder="Ex: Empresários SaaS faturando +10k"
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 transition-all text-sm"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">O "Vilão" (Obstáculo)</label>
                                <input
                                    name="enemy"
                                    value={formData.enemy} onChange={handleChange}
                                    placeholder="Ex: A falta de tempo ou algoritmos"
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 transition-all text-sm"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">A Dor mais Profunda</label>
                                <input
                                    name="pain"
                                    value={formData.pain} onChange={handleChange}
                                    placeholder="O que tira o sono dele?"
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 transition-all text-sm"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">O Sonho (Destino final)</label>
                                <input
                                    name="dream"
                                    value={formData.dream} onChange={handleChange}
                                    placeholder="Como é a vida ideal dele?"
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 transition-all text-sm"
                                />
                            </div>
                            <div className="md:col-span-2 space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">Valores da Marca (Soul)</label>
                                <textarea
                                    name="brandValues"
                                    rows={2}
                                    value={formData.brandValues} onChange={handleChange}
                                    placeholder="Ex: Transparência, Velocidade, Resultados práticos..."
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 transition-all text-sm resize-none"
                                />
                            </div>
                        </div>
                    </div>
                )}

                {step === 3 && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="text-center">
                            <h2 className="text-2xl font-bold font-display mb-2">Diferenciação & Oferta</h2>
                            <p className="text-slate-400 text-sm">Como você se destaca e o que você entrega ao mundo.</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">Nome do Seu Método</label>
                                <input
                                    name="method"
                                    value={formData.method} onChange={handleChange}
                                    placeholder="Ex: Método Escala 10x"
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 transition-all text-sm"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">Tom de Voz</label>
                                <select
                                    name="toneVoice"
                                    value={formData.toneVoice} onChange={handleChange}
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white outline-none focus:border-primary/50 transition-all text-sm appearance-none"
                                >
                                    <option value="">Selecione um Tom</option>
                                    <option value="Autoridade (Sério e Direto)">Autoridade (Sério e Direto)</option>
                                    <option value="Amigável (Acessível e Inspirador)">Amigável (Inspirador)</option>
                                    <option value="Provocador (Quebra de Padrão)">Provocador (Quebra de Padrão)</option>
                                    <option value="Técnico (Focado em Dados)">Técnico (Dados)</option>
                                    <option value="Minimalista (Curto e Grosso)">Minimalista</option>
                                </select>
                            </div>
                            <div className="md:col-span-2 space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest text-slate-400">O que você vende? (Sua Oferta)</label>
                                <textarea
                                    name="offerDetails"
                                    rows={2}
                                    value={formData.offerDetails} onChange={handleChange}
                                    placeholder="Descreva seu produto, curso ou serviço principal..."
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 transition-all text-sm resize-none"
                                />
                            </div>
                            <div className="md:col-span-2 space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">Diferencial Único (Sua Unicidade)</label>
                                <input
                                    name="differentiation"
                                    value={formData.differentiation} onChange={handleChange}
                                    placeholder="Por que você e não a concorrência?"
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 transition-all text-sm"
                                />
                            </div>
                            <div className="md:col-span-2 space-y-2">
                                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-widest">Missão & Promessa Única</label>
                                <textarea
                                    name="mission"
                                    rows={2}
                                    value={formData.mission} onChange={handleChange}
                                    placeholder="Eu ajudo X a conseguir Y através de Z..."
                                    className="w-full px-4 py-4 bg-slate-900/50 border border-slate-800 rounded-2xl text-white placeholder-slate-700 outline-none focus:border-primary/50 transition-all text-sm resize-none"
                                />
                            </div>
                        </div>
                    </div>
                )}

                <div className="mt-12 flex justify-between items-center">
                    <p className="text-[11px] text-slate-600 font-medium">Leads AI &copy; 2026</p>
                    <button
                        onClick={handleNext}
                        disabled={loading}
                        className="btn-primary flex items-center gap-2 text-sm py-3 px-10"
                    >
                        {loading ? 'Processando DNA...' : (step < 3 ? 'Próximo Passo' : 'Gerar Estratégia')}
                        {!loading && <ArrowRight className="w-4 h-4" />}
                    </button>
                </div>
            </div>

            <p className="mt-8 text-xs text-slate-600 text-center max-w-xs leading-relaxed">
                Ao clicar em finalizar, nossa IA iniciará o processamento dos seus dados imediatamente para clonar sua voz de marca.
            </p>
        </div>
    );
}

function ProgressStep({ number, label, active, current }: { number: number, label: string, active: boolean, current: boolean }) {
    return (
        <div className="flex flex-col items-center gap-2 relative z-10 transition-all duration-300">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-xs border-2 transition-all ${current ? 'bg-primary border-primary text-slate-950 shadow-[0_0_15px_rgba(0,255,65,0.4)] ring-4 ring-primary/10' :
                active ? 'bg-slate-900 border-primary text-primary' :
                    'bg-slate-950 border-slate-800 text-slate-700'
                }`}>
                {number}
            </div>
            <span className={`text-[10px] uppercase tracking-widest font-bold transition-colors ${current ? 'text-primary' : active ? 'text-slate-400' : 'text-slate-700'
                }`}>{label}</span>
        </div>
    )
}
