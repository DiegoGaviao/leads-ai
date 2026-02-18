import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { ArrowRight, Target, User } from 'lucide-react';

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
        mission: '', enemy: '', pain: '', dream: '', dreamClient: '', method: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleNext = () => {
        if (step === 1) {
            // Validação Banal
            if (!formData.email || !formData.instagram) return alert("Preencha email e instagram");
            setBasicInfo({
                email: formData.email,
                instagram: formData.instagram,
                whatsapp: formData.whatsapp
            });
            setStep(2);
        } else {
            // Finalizar Onboarding DNS -> Ir para Coleta de Dados Manuais
            if (!formData.mission) return alert("A Missão é obrigatória para a IA funcionar.");

            setLoading(true);
            setStrategy({
                mission: formData.mission,
                enemy: formData.enemy,
                pain: formData.pain,
                dream: formData.dream,
                dreamClient: formData.dreamClient,
                method: formData.method
            });

            // Simula salvamento rápido
            setTimeout(() => {
                setLoading(false);
                navigate('/connect'); // Vamos reaproveitar essa rota para a Coleta de Dados Manuais
            }, 1000);
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-6 font-['Inter']">

            {/* Progress Bar */}
            <div className="w-full max-w-2xl mb-8 flex items-center justify-between px-4">
                <div className={`flex flex-col items-center ${step >= 1 ? 'text-blue-500' : 'text-slate-600'}`}>
                    <div className={`w-10 h-10 rounded-full border-2 flex items-center justify-center font-bold mb-2 ${step >= 1 ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700'}`}>1</div>
                    <span className="text-xs font-medium uppercase tracking-wider">Identidade</span>
                </div>
                <div className={`flex-1 h-0.5 mx-4 ${step >= 2 ? 'bg-blue-500' : 'bg-slate-800'}`}></div>
                <div className={`flex flex-col items-center ${step >= 2 ? 'text-blue-500' : 'text-slate-600'}`}>
                    <div className={`w-10 h-10 rounded-full border-2 flex items-center justify-center font-bold mb-2 ${step >= 2 ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700'}`}>2</div>
                    <span className="text-xs font-medium uppercase tracking-wider">DNA da Marca</span>
                </div>
                <div className={`flex-1 h-0.5 mx-4 bg-slate-800`}></div>
                <div className={`flex flex-col items-center text-slate-600`}>
                    <div className="w-10 h-10 rounded-full border-2 border-slate-700 flex items-center justify-center font-bold mb-2 text-slate-500">3</div>
                    <span className="text-xs font-medium uppercase tracking-wider">Dados</span>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 max-w-2xl w-full shadow-2xl">

                {step === 1 && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="text-center mb-8">
                            <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-4 border border-blue-500/20">
                                <User className="w-8 h-8 text-blue-400" />
                            </div>
                            <h1 className="text-2xl font-bold text-white mb-2">Quem é você?</h1>
                            <p className="text-slate-400">Dados básicos para criar sua conta.</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-slate-400 mb-2">Seu Instagram (sem @)</label>
                                <div className="flex">
                                    <span className="inline-flex items-center px-3 rounded-l-lg border border-r-0 border-slate-700 bg-slate-800 text-slate-400">@</span>
                                    <input
                                        name="instagram"
                                        value={formData.instagram} onChange={handleChange}
                                        placeholder="seu_perfil"
                                        className="flex-1 min-w-0 block w-full px-3 py-3 bg-slate-950 border border-slate-700 rounded-r-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-400 mb-2">WhatsApp</label>
                                <input
                                    name="whatsapp"
                                    value={formData.whatsapp} onChange={handleChange}
                                    placeholder="43991817404"
                                    className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                                />
                            </div>
                            <div className="md:col-span-2">
                                <label className="block text-sm font-medium text-slate-400 mb-2">E-mail de Login do Facebook (Para liberarmos seu acesso)</label>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email} onChange={handleChange}
                                    placeholder="drmgaviao@gmail.com"
                                    className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                                />
                            </div>
                        </div>
                    </div>
                )}

                {step === 2 && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                        <div className="text-center mb-10">
                            <div className="w-20 h-20 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-3xl flex items-center justify-center mx-auto mb-6 border border-white/10 shadow-xl">
                                <Target className="w-10 h-10 text-indigo-400" />
                            </div>
                            <h1 className="text-3xl font-extrabold text-white mb-3 tracking-tight">Arquétipo & DNA</h1>
                            <p className="text-slate-400 max-w-md mx-auto leading-relaxed">Defina a essência da sua marca para que nosso robô aprenda a falar o seu dialeto.</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div className="space-y-2">
                                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Cliente dos Sonhos</label>
                                <input
                                    name="dreamClient"
                                    value={formData.dreamClient} onChange={handleChange}
                                    placeholder="Ex: Empresários que pensam fora da caixa..."
                                    className="w-full px-5 py-4 bg-slate-950/50 border border-slate-800 rounded-2xl text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all placeholder-slate-700"
                                />
                            </div>

                            <div className="space-y-2">
                                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Nome do Método/Empresa</label>
                                <input
                                    name="method"
                                    value={formData.method} onChange={handleChange}
                                    placeholder="Ex: Método Escala 10x"
                                    className="w-full px-5 py-4 bg-slate-950/50 border border-slate-800 rounded-2xl text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all placeholder-slate-700"
                                />
                            </div>

                            <div className="space-y-2">
                                <label className="block text-xs font-bold text-red-500/80 uppercase tracking-widest ml-1">O Inferno (A Dor maior)</label>
                                <input
                                    name="pain"
                                    value={formData.pain} onChange={handleChange}
                                    placeholder="O que tira o sono dele?"
                                    className="w-full px-5 py-4 bg-red-500/5 border border-red-500/10 rounded-2xl text-white focus:ring-2 focus:ring-red-500 outline-none transition-all placeholder-slate-700"
                                />
                            </div>

                            <div className="space-y-2">
                                <label className="block text-xs font-bold text-green-500/80 uppercase tracking-widest ml-1">O Céu (O Sonho)</label>
                                <input
                                    name="dream"
                                    value={formData.dream} onChange={handleChange}
                                    placeholder="Onde ele quer chegar?"
                                    className="w-full px-5 py-4 bg-green-500/5 border border-green-500/10 rounded-2xl text-white focus:ring-2 focus:ring-green-500 outline-none transition-all placeholder-slate-700"
                                />
                            </div>

                            <div className="md:col-span-2 space-y-2">
                                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Missão & Promessa (O que você resolve?)</label>
                                <textarea
                                    name="mission"
                                    rows={2}
                                    value={formData.mission} onChange={handleChange}
                                    placeholder="Transformo X em Y através da tecnologia Z..."
                                    className="w-full px-5 py-4 bg-slate-950/50 border border-slate-800 rounded-2xl text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all placeholder-slate-700 resize-none"
                                />
                            </div>

                            <div className="md:col-span-2 space-y-2">
                                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Inimigo Comum (Contra quem lutamos?)</label>
                                <input
                                    name="enemy"
                                    value={formData.enemy} onChange={handleChange}
                                    placeholder="Ex: O algoritmo, as taxas, os gurus mentirosos..."
                                    className="w-full px-5 py-4 bg-slate-950/50 border border-slate-800 rounded-2xl text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all placeholder-slate-700"
                                />
                            </div>
                        </div>
                    </div>
                )}

                <div className="mt-8 pt-6 border-t border-slate-800 flex justify-end">
                    <button
                        onClick={handleNext}
                        disabled={loading}
                        className="group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-3 px-8 rounded-xl flex items-center gap-2 transition-all shadow-lg hover:shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? 'Salvando...' : (step === 1 ? 'Próximo Passo' : 'Finalizar Setup')}
                        {!loading && <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />}
                    </button>
                </div>

            </div>
        </div>
    );
}
