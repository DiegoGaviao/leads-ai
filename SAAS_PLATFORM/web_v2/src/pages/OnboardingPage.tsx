import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { ArrowRight, Target, User } from 'lucide-react';

export default function OnboardingPage() {
    const navigate = useNavigate();
    const { setBasicInfo, setStrategy } = useOnboardingStore();
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);

    // Form State Local
    const [formData, setFormData] = useState({
        email: '', instagram: '', whatsapp: '',
        mission: '', enemy: '', pain: '', method: ''
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
            // Finalizar Onboarding Manual -> Ir para Conexão
            if (!formData.mission) return alert("A Missão é obrigatória para a IA funcionar.");

            setLoading(true);
            setStrategy({
                mission: formData.mission,
                enemy: formData.enemy,
                pain: formData.pain,
                method: formData.method
            });

            // Simula salvamento rápido (na prática salva no próximo passo junto com Auth)
            setTimeout(() => {
                setLoading(false);
                navigate('/connect'); // Próxima etapa: Conectar Facebook
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
                    <span className="text-xs font-medium uppercase tracking-wider">Alma da Marca</span>
                </div>
                <div className={`flex-1 h-0.5 mx-4 bg-slate-800`}></div>
                <div className={`flex flex-col items-center text-slate-600`}>
                    <div className="w-10 h-10 rounded-full border-2 border-slate-700 flex items-center justify-center font-bold mb-2 text-slate-500">3</div>
                    <span className="text-xs font-medium uppercase tracking-wider">Conexão</span>
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
                            <p className="text-slate-400">Vamos começar pelo básico para personalizar sua experiência.</p>
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
                                <label className="block text-sm font-medium text-slate-400 mb-2">Seu WhatsApp</label>
                                <input
                                    name="whatsapp"
                                    value={formData.whatsapp} onChange={handleChange}
                                    placeholder="(11) 99999-9999"
                                    className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                                />
                            </div>
                            <div className="md:col-span-2">
                                <label className="block text-sm font-medium text-slate-400 mb-2">E-mail de Acesso</label>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email} onChange={handleChange}
                                    placeholder="voce@exemplo.com"
                                    className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                                />
                            </div>
                        </div>
                    </div>
                )}

                {step === 2 && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="text-center mb-8">
                            <div className="w-16 h-16 bg-purple-500/10 rounded-full flex items-center justify-center mx-auto mb-4 border border-purple-500/20">
                                <Target className="w-8 h-8 text-purple-400" />
                            </div>
                            <h1 className="text-2xl font-bold text-white mb-2">Calibrando a IA</h1>
                            <p className="text-slate-400">Para a IA não soar robótica, ela precisa entender sua alma.</p>
                        </div>

                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-bold text-slate-300 mb-2">Qual é sua MISSÃO em uma frase?</label>
                                <p className="text-xs text-slate-500 mb-2">Ex: "Ajudar mulheres a recuperar a autoestima através da moda."</p>
                                <textarea
                                    name="mission"
                                    value={formData.mission} onChange={handleChange}
                                    rows={2}
                                    className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-bold text-slate-300 mb-2">Quem é o INIMIGO?</label>
                                    <p className="text-xs text-slate-500 mb-2">Ex: "A procrastinação", "A indústria da dieta".</p>
                                    <input
                                        name="enemy"
                                        value={formData.enemy} onChange={handleChange}
                                        className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-bold text-slate-300 mb-2">Qual a DOR principal?</label>
                                    <p className="text-xs text-slate-500 mb-2">Ex: "Sentir que trabalha muito e não sai do lugar".</p>
                                    <input
                                        name="pain"
                                        value={formData.pain} onChange={handleChange}
                                        className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-bold text-slate-300 mb-2">Nome do seu Método/Produto (Opcional)</label>
                                <input
                                    name="method"
                                    value={formData.method} onChange={handleChange}
                                    placeholder="Ex: Método Turbo 5k"
                                    className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
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
