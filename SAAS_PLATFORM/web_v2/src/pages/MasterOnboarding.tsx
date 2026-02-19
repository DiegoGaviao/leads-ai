import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Phone, Mail, Send, CheckCircle2, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

const API_URL = import.meta.env.VITE_API_URL || "https://leads-ai-v2.onrender.com";

export default function MasterOnboardingPage() {
    const navigate = useNavigate();
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);

    const [formData, setFormData] = useState({
        contactMethod: 'whatsapp',
        contactValue: '',
        fbEmail: ''
    });

    const handleSubmit = async () => {
        setLoading(true);
        try {
            const res = await fetch(`${API_URL}/auth/master/notify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (res.ok) {
                setStep(2);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (step === 2) {
        return (
            <div className="min-h-screen bg-slate-950 text-slate-50 flex flex-col items-center justify-center p-6 text-center antialiased">
                <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-[400px] bg-primary/10 blur-[120px] -z-10" />

                <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="card-premium max-w-lg w-full py-16">
                    <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-8 border border-primary/20">
                        <CheckCircle2 className="w-10 h-10 text-primary" />
                    </div>
                    <h1 className="text-3xl font-bold mb-4 font-display">Tudo pronto!</h1>
                    <p className="text-slate-400 text-base leading-relaxed mb-10 px-6">
                        Recebemos sua solicitação. Nossa equipe entrará em contato via <b>{formData.contactMethod}</b> em breve para conectar sua conta e iniciar a análise profunda.
                    </p>
                    <button onClick={() => navigate('/')} className="text-primary hover:text-white font-bold tracking-widest uppercase text-[11px] transition-colors">
                        Voltar para a Home
                    </button>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950 text-slate-50 flex flex-col items-center justify-center p-6 antialiased">
            <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-3xl h-[400px] bg-primary/5 blur-[120px] -z-10" />

            <div className="card-premium max-w-xl w-full p-10 md:p-14">
                <div className="text-center mb-12">
                    <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-primary/20 shadow-premium">
                        <Sparkles className="w-8 h-8 text-primary" />
                    </div>
                    <h1 className="text-3xl font-bold mb-3 font-display tracking-tight">Conexão Master</h1>
                    <p className="text-slate-400 text-sm">Vamos habilitar sua análise total de dados.</p>
                </div>

                <div className="space-y-8">
                    <div className="space-y-3">
                        <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-widest ml-1">Como prefere ser contatado?</label>
                        <div className="grid grid-cols-2 gap-4">
                            <ContactTab
                                active={formData.contactMethod === 'whatsapp'}
                                onClick={() => setFormData({ ...formData, contactMethod: 'whatsapp' })}
                                icon={<Phone className="w-4 h-4" />}
                                label="WhatsApp"
                            />
                            <ContactTab
                                active={formData.contactMethod === 'email'}
                                onClick={() => setFormData({ ...formData, contactMethod: 'email' })}
                                icon={<Mail className="w-4 h-4" />}
                                label="E-mail"
                            />
                        </div>
                    </div>

                    <div className="space-y-3">
                        <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-widest ml-1">Seu {formData.contactMethod === 'whatsapp' ? 'WhatsApp' : 'E-mail'}</label>
                        <input
                            placeholder={formData.contactMethod === 'whatsapp' ? 'Ex: 43 99999-9999' : 'seu@email.com'}
                            value={formData.contactValue}
                            onChange={(e) => setFormData({ ...formData, contactValue: e.target.value })}
                            className="w-full px-5 py-4 bg-slate-950 border border-slate-900 rounded-2xl outline-none focus:border-primary/50 transition-all text-sm placeholder-slate-800"
                        />
                    </div>

                    <div className="space-y-3">
                        <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-widest ml-1">E-mail de Login do Facebook</label>
                        <input
                            placeholder="exemplo@login.com"
                            value={formData.fbEmail}
                            onChange={(e) => setFormData({ ...formData, fbEmail: e.target.value })}
                            className="w-full px-5 py-4 bg-slate-950 border border-slate-900 rounded-2xl outline-none focus:border-primary/50 transition-all text-sm placeholder-slate-800"
                        />
                        <p className="px-1 text-[10px] text-slate-600 leading-relaxed italic">Usado apenas para liberar permissão no Gerenciador de Anúncios.</p>
                    </div>

                    <button
                        onClick={handleSubmit}
                        disabled={loading || !formData.contactValue || !formData.fbEmail}
                        className="btn-primary w-full py-5 text-base flex items-center justify-center gap-3 transition-all disabled:opacity-50 mt-4"
                    >
                        {loading ? "Enviando..." : <>Solicitar Ativação Master <Send className="w-4 h-4" /></>}
                    </button>
                </div>
            </div>
        </div>
    );
}

function ContactTab({ active, onClick, icon, label }: any) {
    return (
        <button
            onClick={onClick}
            className={`flex items-center justify-center gap-2 p-4 rounded-2xl border transition-all text-sm font-bold ${active
                ? 'bg-slate-900 border-slate-800 text-slate-100 shadow-premium'
                : 'bg-transparent border-transparent text-slate-600 hover:text-slate-400 hover:bg-slate-950'}`}
        >
            {icon} {label}
        </button>
    )
}
