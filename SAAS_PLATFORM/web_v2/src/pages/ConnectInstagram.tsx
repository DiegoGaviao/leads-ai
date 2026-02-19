import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { Plus, Minus, Send, Link as LinkIcon, BarChart2, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = import.meta.env.VITE_API_URL || "https://leads-ai-v2.onrender.com";

export default function ManualDataEntryPage() {
    const navigate = useNavigate();
    const { plan, email, instagram, mission, enemy, pain, method, dream, dreamClient, posts: savedPosts, setPosts } = useOnboardingStore();

    // Limite baseado no plano
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
            setPosts(posts); // Atualiza o store global

            // Salva no backend
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
                    manual_posts: posts,
                    facebook_token: "manual_entry",
                    instagram_id: "manual_entry"
                })
            });

            if (!res.ok) throw new Error("Falha ao salvar dados.");

            setIsFinished(true);
        } catch (err) {
            console.error(err);
            alert("Erro ao salvar dados. Verifique sua conexão.");
        } finally {
            setIsSaving(false);
        }
    };

    if (isFinished) {
        return (
            <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-6 text-center font-['Inter']">
                <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} className="w-20 h-20 bg-blue-500/10 rounded-full flex items-center justify-center mb-8 border border-blue-500/20">
                    <CheckCircle2 className="w-10 h-10 text-blue-400" />
                </motion.div>
                <h1 className="text-4xl font-extrabold mb-4 tracking-tight text-white">Tudo pronto!</h1>
                <p className="text-slate-400 max-w-lg text-lg leading-relaxed">
                    Seus dados foram recebidos com sucesso. O <b>Conselho de IAs</b> iniciou o processamento do seu relatório agora mesmo.
                    <br /><br />
                    Em alguns minutos, você receberá um e-mail em <b>{email}</b> com sua estratégia completa!
                </p>
                <button onClick={() => navigate('/')} className="mt-12 text-blue-400 hover:text-blue-300 font-bold tracking-wide uppercase text-sm">Voltar para a Home</button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center py-12 px-6 font-['Inter']">

            {/* Header */}
            <div className="w-full max-w-3xl mb-12 text-center">
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold uppercase tracking-widest mb-6">
                    <BarChart2 className="w-4 h-4" /> Passo Final: Performance
                </div>
                <h1 className="text-4xl font-extrabold mb-4 tracking-tight text-white">Quais posts queremos analisar?</h1>
                <p className="text-slate-400 text-lg leading-relaxed">
                    Adicione os links e as métricas dos posts que você quer que nosso Robô analise para extrair o DNA do seu sucesso.
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
                            className="bg-slate-900/50 border border-slate-800 rounded-3xl p-8 relative group overflow-hidden shadow-xl"
                        >
                            <div className="absolute top-0 left-0 w-1.5 h-full bg-indigo-500/50" />

                            <div className="flex justify-between items-center mb-8">
                                <span className="text-sm font-bold text-slate-500 uppercase tracking-widest">Análise #{index + 1}</span>
                                {posts.length > 1 && (
                                    <button
                                        onClick={() => removePost(index)}
                                        className="p-2 hover:bg-red-500/10 text-slate-500 hover:text-red-400 rounded-xl transition-all"
                                    >
                                        <Minus className="w-5 h-5" />
                                    </button>
                                )}
                            </div>

                            <div className="space-y-6">
                                <div>
                                    <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-3 ml-1">Link do Post</label>
                                    <div className="relative">
                                        <LinkIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-600" />
                                        <input
                                            placeholder="https://www.instagram.com/p/..."
                                            value={post.link}
                                            onChange={(e) => updatePost(index, 'link', e.target.value)}
                                            className="w-full pl-12 pr-5 py-4 bg-slate-950 border border-slate-800 rounded-2xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all placeholder-slate-800"
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                                    <div>
                                        <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 ml-1 text-center">Visualizações</label>
                                        <input
                                            type="number"
                                            placeholder="Ex: 5000"
                                            value={post.views}
                                            onChange={(e) => updatePost(index, 'views', e.target.value)}
                                            className="w-full px-5 py-4 bg-slate-950/80 border border-slate-800 rounded-2xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-center"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 ml-1 text-center">Curtidas</label>
                                        <input
                                            type="number"
                                            placeholder="Ex: 250"
                                            value={post.likes}
                                            onChange={(e) => updatePost(index, 'likes', e.target.value)}
                                            className="w-full px-5 py-4 bg-slate-950/80 border border-slate-800 rounded-2xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-center"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 ml-1 text-center">Comentários</label>
                                        <input
                                            type="number"
                                            placeholder="Ex: 45"
                                            value={post.comments}
                                            onChange={(e) => updatePost(index, 'comments', e.target.value)}
                                            className="w-full px-5 py-4 bg-slate-950/80 border border-slate-800 rounded-2xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-center"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 ml-1 text-center">Compartilhamentos</label>
                                        <input
                                            type="number"
                                            placeholder="Ex: 30"
                                            value={post.shares}
                                            onChange={(e) => updatePost(index, 'shares', e.target.value)}
                                            className="w-full px-5 py-4 bg-slate-950/80 border border-slate-800 rounded-2xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-center"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 ml-1 text-center">Salvamentos</label>
                                        <input
                                            type="number"
                                            placeholder="Ex: 120"
                                            value={post.saves}
                                            onChange={(e) => updatePost(index, 'saves', e.target.value)}
                                            className="w-full px-5 py-4 bg-slate-950/80 border border-slate-800 rounded-2xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-center"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-[10px] font-bold text-green-500/80 uppercase tracking-widest mb-2 ml-1 text-center">Vendas/Leads</label>
                                        <input
                                            type="number"
                                            placeholder="Ex: 12"
                                            value={post.conversions}
                                            onChange={(e) => updatePost(index, 'conversions', e.target.value)}
                                            className="w-full px-5 py-4 bg-green-500/5 border border-green-500/10 rounded-2xl focus:ring-2 focus:ring-green-500 outline-none transition-all text-center placeholder-green-900/50"
                                        />
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                <button
                    onClick={addPost}
                    className="w-full py-4 bg-slate-900 border border-dashed border-slate-700 rounded-2xl text-slate-400 hover:text-white hover:border-blue-500/50 hover:bg-blue-500/5 transition-all flex items-center justify-center gap-2 group"
                >
                    <Plus className="w-5 h-5 group-hover:rotate-90 transition-transform" /> Adicionar mais um Post
                </button>

                <div className="pt-12">
                    <button
                        onClick={handleFinalize}
                        disabled={isSaving || posts.some(p => !p.link)}
                        className="w-full py-5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-xl rounded-2xl shadow-xl shadow-blue-500/20 flex items-center justify-center gap-3 transition-all disabled:opacity-50 disabled:grayscale"
                    >
                        {isSaving ? "Processando..." : (
                            <>
                                Finalizar e Gerar Estratégia <Send className="w-6 h-6" />
                            </>
                        )}
                    </button>
                    <p className="text-center text-slate-500 text-sm mt-6">
                        Ao clicar, nosso robô iniciará a análise e você receberá o relatório completo no e-mail cadastrado.
                    </p>
                </div>
            </div>
        </div>
    );
}
