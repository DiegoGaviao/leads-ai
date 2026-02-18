import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Phone, Mail, Send, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';

const API_URL = import.meta.env.VITE_API_URL || "https://leads-ai-backend.onrender.com";

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
            // Salva no banco e notifica admin
            const res = await fetch(`${API_URL}/auth/master/notify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (res.ok) {
                setStep(2); // Sucesso
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (step === 2) {
        return (
            <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-6 text-center">
                <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} className="w-20 h-20 bg-green-500/20 rounded-full flex items-center justify-center mb-6">
                    <CheckCircle2 className="w-12 h-12 text-green-500" />
                </motion.div>
                <h1 className="text-3xl font-bold mb-4 tracking-tight text-white">Pronto, mestre!</h1>
                <p className="text-slate-400 max-w-md text-lg leading-relaxed">
                    Recebemos seus dados. Nossa equipe entrará em contato em breve via <b>{formData.contactMethod}</b> para conectar sua conta e iniciar a análise profunda de todo o seu histórico.
                </p>
                <button onClick={() => navigate('/')} className="mt-8 text-blue-400 hover:text-blue-300 font-medium">Voltar para a Home</button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-6 font-['Inter']">
            <div className="w-full max-w-xl bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl">
                <div className="text-center mb-10">
                    <div className="w-16 h-16 bg-blue-500/10 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-blue-500/20">
                        <CheckCircle2 className="w-8 h-8 text-blue-400" />
                    </div>
                    <h1 className="text-3xl font-bold mb-2 tracking-tight">Bem-vindo ao Master Data</h1>
                    <p className="text-slate-400">Vamos conectar seus dados para análise total.</p>
                </div>

                <div className="space-y-6">
                    <div>
                        <label className="block text-sm font-bold text-slate-300 mb-2 uppercase tracking-wider">Como prefere ser contatado?</label>
                        <div className="grid grid-cols-2 gap-4">
                            <button
                                onClick={() => setFormData({ ...formData, contactMethod: 'whatsapp' })}
                                className={`flex items-center justify-center gap-2 p-4 rounded-xl border transition-all ${formData.contactMethod === 'whatsapp' ? 'bg-blue-600 border-blue-500 text-white' : 'bg-slate-950 border-slate-800 text-slate-500'}`}
                            >
                                <Phone className="w-4 h-4" /> WhatsApp
                            </button>
                            <button
                                onClick={() => setFormData({ ...formData, contactMethod: 'email' })}
                                className={`flex items-center justify-center gap-2 p-4 rounded-xl border transition-all ${formData.contactMethod === 'email' ? 'bg-blue-600 border-blue-500 text-white' : 'bg-slate-950 border-slate-800 text-slate-500'}`}
                            >
                                <Mail className="w-4 h-4" /> E-mail
                            </button>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-bold text-slate-300 mb-2 uppercase tracking-wider">Seu {formData.contactMethod === 'whatsapp' ? 'WhatsApp' : 'E-mail'}</label>
                        <input
                            placeholder={formData.contactMethod === 'whatsapp' ? '43 99181-7404' : 'seu@email.com'}
                            value={formData.contactValue}
                            onChange={(e) => setFormData({ ...formData, contactValue: e.target.value })}
                            className="w-full px-4 py-4 bg-slate-950 border border-slate-800 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-bold text-slate-300 mb-2 uppercase tracking-wider text-slate-300">E-mail de Login no Facebook</label>
                        <p className="text-xs text-slate-500 mb-2">Pode ser o mesmo que você usa para acessar o Gerenciador de Anúncios.</p>
                        <input
                            placeholder="exemplo@login.com"
                            value={formData.fbEmail}
                            onChange={(e) => setFormData({ ...formData, fbEmail: e.target.value })}
                            className="w-full px-4 py-4 bg-slate-950 border border-slate-800 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                        />
                    </div>

                    <button
                        onClick={handleSubmit}
                        disabled={loading || !formData.contactValue || !formData.fbEmail}
                        className="w-full py-5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-lg rounded-2xl shadow-xl shadow-blue-500/20 flex items-center justify-center gap-2 transition-all hover:scale-[1.02] disabled:opacity-50"
                    >
                        {loading ? "Enviando..." : <>Solicitar Conexão Master <Send className="w-5 h-5" /></>}
                    </button>
                </div>
            </div>
        </div>
    );
}
