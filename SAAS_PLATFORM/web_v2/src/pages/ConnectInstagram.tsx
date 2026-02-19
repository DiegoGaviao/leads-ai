import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { Plus, Minus, Send, Link as LinkIcon, BarChart2, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = import.meta.env.VITE_API_URL || "https://leads-ai-v2.onrender.com";

export default function ManualDataEntryPage() {
    const navigate = useNavigate();
    const { plan, email, instagram, mission, enemy, pain, method, dream, dreamClient,
        toneVoice, brandValues, offerDetails, differentiation, posts: savedPosts, setPosts } = useOnboardingStore();

    const MAX_POSTS = plan === 'pro' ? 5 : 3;
    const [posts, setLocalPosts] = useState(savedPosts.length > 0 ? savedPosts.slice(0, MAX_POSTS) : [{ link: '', views: '', likes: '', comments: '', shares: '', saves: '', conversions: '' }]);
    const [isSaving, setIsSaving] = useState(false);
    const [isFinished, setIsFinished] = useState(false);

    const addPost = () => {
        if (posts.length < MAX_POSTS) {
            setLocalPosts([...posts, { link: '', views: '', likes: '', comments: '', shares: '', saves: '', conversions: '' }]);
        }
    };

    const removePost = (index: number) => {
        setLocalPosts(posts.filter((_, i) => i !== index));
    };

    const updatePost = (index: number, field: string, value: string) => {
        const newPosts = [...posts];
        newPosts[index] = { ...newPosts[index], [field]: value };
        setLocalPosts(newPosts);
    };

    const handleFinalize = async () => {
        try {
            setIsSaving(true);
            setPosts(posts);

            const res = await fetch(`${API_URL}/auth/onboarding/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email,
                    instagram,
                    mission,
                    enemy,
                    pain,
                    dream,
                    dreamClient,
                    method,
                    toneVoice,
                    brandValues,
                    offerDetails,
                    differentiation,
                    manual_posts: posts,
                    facebook_token: "manual_entry",
                    instagram_id: "manual_entry"
                })
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || "Falha ao salvar dados.");
            }

            setIsFinished(true);
        } catch (err: any) {
            console.error(err);
            alert(`Erro: ${err.message}`);
        } finally {
            setIsSaving(false);
        }
    };

    if (isFinished) {
        return (
            <div className="min-h-screen bg-slate-950 text-slate-50 flex flex-col items-center justify-center p-6 text-center antialiased">
                <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-[400px] bg-primary/10 blur-[120px] -z-10" />

                <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="card-premium max-w-lg w-full py-16">
                    <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-8 border border-primary/20">
                        <CheckCircle2 className="w-10 h-10 text-primary" />
                    </div>
                    <h1 className="text-3xl font-bold mb-4 font-display">Tudo pronto!</h1>
                    <p className="text-slate-400 text-base leading-relaxed mb-10 px-6">
                        Seus dados foram recebidos. O <b>Conselho de IAs</b> iniciou o processamento da sua estratégia agora mesmo.
                        <br /><br />
                        Em instantes, você receberá o relatório no e-mail <b>{email}</b>.
                    </p>
                    <button onClick={() => navigate('/')} className="text-primary hover:text-white font-bold tracking-widest uppercase text-[11px] transition-colors">
                        Voltar para o Início
                    </button>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950 text-slate-50 flex flex-col items-center py-20 px-6 antialiased">
            <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-[300px] bg-secondary/5 blur-[120px] -z-10" />

            {/* Header */}
            <div className="w-full max-w-3xl mb-16 text-center">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-slate-400 text-[10px] font-bold uppercase tracking-widest mb-6">
                    <BarChart2 className="w-3.5 h-3.5 text-primary" /> Passo Final: Performance
                </div>
                <h1 className="text-4xl font-bold mb-4 tracking-tight font-display">Dados Reais</h1>
                <p className="text-slate-400 text-lg leading-relaxed">
                    Adicione as métricas dos posts que melhor performaram para extrairmos os padrões de sucesso.
                </p>
            </div>

            <div className="w-full max-w-3xl space-y-8">
                <AnimatePresence>
                    {posts.map((post, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="card-premium relative group overflow-hidden"
                        >
                            <div className="flex justify-between items-center mb-10">
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-center text-[11px] font-bold text-slate-500">
                                        {index + 1}
                                    </div>
                                    <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">Análise de Conteúdo</span>
                                </div>
                                {posts.length > 1 && (
                                    <button
                                        onClick={() => removePost(index)}
                                        className="p-2 hover:bg-slate-800 text-slate-600 hover:text-white rounded-lg transition-all"
                                    >
                                        <Minus className="w-4 h-4" />
                                    </button>
                                )}
                            </div>

                            <div className="space-y-8">
                                <div className="space-y-3">
                                    <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-widest ml-1">Link do Post (Reels ou Carrossel)</label>
                                    <div className="relative group">
                                        <LinkIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-600 transition-colors group-focus-within:text-primary" />
                                        <input
                                            placeholder="https://www.instagram.com/p/..."
                                            value={post.link}
                                            onChange={(e) => updatePost(index, 'link', e.target.value)}
                                            className="w-full pl-12 pr-6 py-4 bg-slate-950 border border-slate-800 rounded-2xl outline-none focus:border-primary/50 transition-all text-sm placeholder-slate-800"
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 lg:grid-cols-3 gap-6">
                                    <MetricInput label="Visualizações" placeholder="0" value={post.views} onChange={(val: string) => updatePost(index, 'views', val)} />
                                    <MetricInput label="Curtidas" placeholder="0" value={post.likes} onChange={(val: string) => updatePost(index, 'likes', val)} />
                                    <MetricInput label="Comentários" placeholder="0" value={post.comments} onChange={(val: string) => updatePost(index, 'comments', val)} />
                                    <MetricInput label="Compartilhamentos" placeholder="0" value={post.shares} onChange={(val: string) => updatePost(index, 'shares', val)} />
                                    <MetricInput label="Salvamentos" placeholder="0" value={post.saves} onChange={(val: string) => updatePost(index, 'saves', val)} />
                                    <MetricInput label="Vendas/Leads" placeholder="0" value={post.conversions} onChange={(val: string) => updatePost(index, 'conversions', val)} highlight />
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                <button
                    onClick={addPost}
                    className="w-full py-4 bg-transparent border-2 border-dashed border-slate-900 rounded-2xl text-slate-600 hover:text-slate-400 hover:border-slate-800 transition-all flex items-center justify-center gap-2 group text-sm font-medium"
                >
                    <Plus className="w-4 h-4" /> Adicionar mais um Post
                </button>

                <div className="pt-16">
                    <button
                        onClick={handleFinalize}
                        disabled={isSaving || posts.some(p => !p.link)}
                        className="btn-primary w-full py-5 text-lg flex items-center justify-center gap-3 transition-all disabled:opacity-50"
                    >
                        {isSaving ? "Processando..." : (
                            <>
                                Gerar minha Estratégia <Send className="w-5 h-5" />
                            </>
                        )}
                    </button>
                    <p className="text-center text-slate-500 text-xs mt-6">
                        Sua estratégia será enviada em até 5 minutos para o e-mail cadastrado.
                    </p>
                </div>
            </div>
        </div>
    );
}

function MetricInput({ label, placeholder, value, onChange, highlight = false }: any) {
    return (
        <div className="space-y-2">
            <label className={`block text-[10px] font-bold uppercase tracking-widest text-center ${highlight ? 'text-primary' : 'text-slate-500'}`}>{label}</label>
            <input
                type="number"
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className={`w-full px-4 py-4 bg-slate-950 border rounded-2xl text-center outline-none transition-all text-sm ${highlight ? 'border-primary/30 focus:border-primary' : 'border-slate-900 focus:border-slate-700'}`}
            />
        </div>
    )
}
