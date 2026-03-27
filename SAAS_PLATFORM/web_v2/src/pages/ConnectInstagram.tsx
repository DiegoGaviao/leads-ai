import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { Plus, Minus, Send, Link as LinkIcon, BarChart2, CheckCircle2, ShieldCheck } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = import.meta.env.VITE_API_URL || "https://leads-ai-v2.onrender.com";

export default function ConnectInstagramPage() {
    const navigate = useNavigate();
    const { plan, email, instagram, whatsapp, mission, enemy, pain, method, dream, dreamClient,
        toneVoice, brandValues, offerDetails, differentiation, posts: savedPosts, setPosts } = useOnboardingStore();

    const MAX_POSTS = plan === 'master' ? 10 : plan === 'pro' ? 5 : 3;

    const emptyPost = () => ({
        link: '',
        views: '',
        likes: '',
        comments: '',
        shares: '',
        saves: '',
        conversions: '',
        creativeTheme: '',
    });

    const [posts, setLocalPosts] = useState(() => {
        const base =
            savedPosts.length > 0 ? savedPosts.slice(0, MAX_POSTS) : [emptyPost()];
        return base.map((p) => ({ ...emptyPost(), ...p }));
    });
    const [isSaving, setIsSaving] = useState(false);
    const [isFinished, setIsFinished] = useState(false);
    /** Modo manual permanece como fallback caso a conexão automática falhe. */
    const [showManualMode, setShowManualMode] = useState(true);
    const [isConnecting, setIsConnecting] = useState(false);

    const handleFacebookAutoConnect = () => {
        // Fallback importante para não "travar" o botão caso o env não tenha sido embutido no build.
        // O app_id também existe como default no backend (FacebookClient).
        const DEFAULT_FACEBOOK_APP_ID = '880409131510410';
        const facebookAppId = (import.meta.env.VITE_FACEBOOK_APP_ID || DEFAULT_FACEBOOK_APP_ID).trim();
        if (!facebookAppId) {
            alert('Facebook app_id inválido/vazio. Configure VITE_FACEBOOK_APP_ID e gere o build novamente.');
            return;
        }

        // Connect está em `/connect` e o callback está em `/callback` (mantendo o basename do Router).
        const callbackPath = window.location.pathname.replace(/\/connect\/?$/, '/callback');
        const redirectUri = `${window.location.origin}${callbackPath}`;

        // OAuth - Meta dialog/oauth, retorna `code` para `/callback`.
        const state = Math.random().toString(36).slice(2);
        const scopes = [
            'pages_show_list',
            'pages_read_engagement',
            'instagram_basic',
            'instagram_manage_insights',
        ].join(',');

        const url = new URL('https://www.facebook.com/v18.0/dialog/oauth');
        url.searchParams.set('client_id', facebookAppId);
        url.searchParams.set('redirect_uri', redirectUri);
        url.searchParams.set('response_type', 'code');
        url.searchParams.set('scope', scopes);
        url.searchParams.set('state', state);
        // Re-request ajuda em casos onde permissões antigas ainda não foram concedidas.
        url.searchParams.set('auth_type', 'rerequest');

        setIsConnecting(true);
        window.location.href = url.toString();
    };

    // Salva rascunho dos posts no mesmo storage do onboarding (persist) — não perde ao voltar ao /setup ou recarregar.
    useEffect(() => {
        const id = window.setTimeout(() => {
            useOnboardingStore.getState().setPosts(posts);
        }, 400);
        return () => window.clearTimeout(id);
    }, [posts]);

    const addPost = () => {
        if (posts.length < MAX_POSTS) {
            setLocalPosts([...posts, emptyPost()]);
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
                    plan,
                    email,
                    instagram,
                    whatsapp,
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
            <div className="flex min-h-screen flex-col items-center justify-center p-6 text-center antialiased">
                <div className="fixed top-0 left-1/2 z-0 h-[280px] w-full max-w-lg -translate-x-1/2 bg-emerald-500/[0.07] blur-[90px]" />

                <motion.div initial={{ scale: 0.96, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="card-premium relative z-10 w-full max-w-lg py-16 shadow-lg">
                    <div className="mx-auto mb-8 flex h-20 w-20 items-center justify-center rounded-full border border-emerald-200 bg-emerald-50">
                        <CheckCircle2 className="h-10 w-10 text-emerald-600" />
                    </div>
                    <h1 className="mb-4 font-display text-3xl font-bold text-slate-900">Tudo pronto!</h1>
                    <p className="mb-10 px-6 text-base leading-relaxed text-slate-600">
                        Seus dados foram recebidos. O <b>Conselho de IAs</b> iniciou o processamento da sua estratégia agora mesmo.
                        <br /><br />
                        Em instantes, você receberá o relatório no e-mail <b className="text-slate-800">{email}</b>.
                    </p>
                    <button
                        type="button"
                        onClick={() => navigate('/')}
                        className="text-[11px] font-bold uppercase tracking-widest text-emerald-700 transition hover:text-emerald-800"
                    >
                        Voltar para o início
                    </button>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="flex min-h-screen flex-col items-center overflow-x-hidden px-4 py-12 antialiased sm:px-6 sm:py-16 md:py-20">
            <div className="fixed top-0 left-1/2 z-0 h-[240px] w-full max-w-3xl -translate-x-1/2 bg-emerald-500/[0.05] blur-[100px]" />

            <div className="relative z-10 mb-10 w-full max-w-3xl text-center">
                <div className="mb-6 inline-flex items-center justify-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-[10px] font-bold uppercase tracking-widest text-slate-600 shadow-sm">
                    <BarChart2 className="h-3.5 w-3.5 text-emerald-600" /> Conexão com Instagram
                </div>
                <button
                    type="button"
                    onClick={handleFacebookAutoConnect}
                    disabled={isConnecting}
                    className="flex w-full items-center justify-center gap-3 rounded-2xl border border-slate-200 bg-white py-5 text-lg font-semibold text-slate-700 shadow-inner transition hover:bg-slate-50 disabled:opacity-60 disabled:hover:bg-white"
                >
                    {isConnecting ? 'Abrindo login do Facebook...' : 'Conectar Instagram (Facebook) — automático'}
                </button>
                <div className="mt-4 rounded-2xl border border-amber-200 bg-amber-50/90 px-4 py-3 text-left text-sm leading-relaxed text-amber-950">
                    Se a conexão automática falhar, use o <strong className="font-semibold">modo manual</strong> abaixo: envie os links dos posts e as métricas.
                </div>
                <button
                    type="button"
                    onClick={() => setShowManualMode((v) => !v)}
                    className="mt-5 text-[11px] font-bold uppercase tracking-widest text-slate-500 transition hover:text-slate-700"
                >
                    {showManualMode ? 'Ocultar modo manual' : 'Nao consigo conectar agora (modo manual)'}
                </button>
                <button
                    type="button"
                    onClick={() => navigate('/setup')}
                    className="mt-4 w-full text-center text-xs font-semibold text-emerald-700 underline-offset-2 hover:underline sm:text-sm"
                >
                    Voltar ao questionário (seus dados continuam salvos)
                </button>
            </div>

            {showManualMode && (
                <div className="relative z-10 mb-10 w-full max-w-3xl text-center sm:mb-14">
                    <p className="mx-auto mb-6 flex max-w-xl items-start gap-2 rounded-xl border border-emerald-100 bg-emerald-50/80 px-3 py-2.5 text-left text-xs leading-relaxed text-emerald-950 sm:text-sm">
                        <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" aria-hidden />
                        <span>
                            <strong className="font-semibold">Rascunho salvo automaticamente.</strong> Você pode voltar ao
                            passo anterior, fechar o navegador ou coletar métricas em outra aba — os links e números ficam
                            guardados neste aparelho.
                        </span>
                    </p>
                    <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-slate-600 shadow-sm">
                        <BarChart2 className="h-3.5 w-3.5 text-emerald-600" /> Passo final: performance
                    </div>
                    <h1 className="mb-4 font-display text-balance text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl md:text-4xl">
                        Dados reais
                    </h1>
                    <p className="text-pretty text-base leading-relaxed text-slate-600 sm:text-lg">
                        Adicione as metricas dos posts que melhor performaram para extrairmos os padroes de sucesso.
                    </p>
                </div>
            )}

            {showManualMode && (
            <div className="relative z-10 w-full max-w-3xl space-y-8">
                <AnimatePresence>
                    {posts.map((post, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="card-premium group relative overflow-hidden shadow-md"
                        >
                            <div className="mb-10 flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-500">
                                        {index + 1}
                                    </div>
                                    <span className="text-xs font-bold uppercase tracking-widest text-slate-500">Análise de conteúdo</span>
                                </div>
                                {posts.length > 1 && (
                                    <button
                                        type="button"
                                        onClick={() => removePost(index)}
                                        className="rounded-lg p-2 text-slate-400 transition-all hover:bg-slate-100 hover:text-slate-700"
                                    >
                                        <Minus className="h-4 w-4" />
                                    </button>
                                )}
                            </div>

                            <div className="space-y-8">
                                <div className="space-y-3">
                                    <label className="ml-1 block text-[11px] font-bold uppercase tracking-widest text-slate-500">Link do post (Reels ou carrossel)</label>
                                    <div className="group relative">
                                        <LinkIcon className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400 transition-colors group-focus-within:text-emerald-600" />
                                        <input
                                            placeholder="https://www.instagram.com/p/..."
                                            value={post.link}
                                            onChange={(e) => updatePost(index, 'link', e.target.value)}
                                            className="input-app pl-12"
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6 lg:grid-cols-3">
                                    <MetricInput label="Visualizações" placeholder="0" value={post.views} onChange={(val: string) => updatePost(index, 'views', val)} />
                                    <MetricInput label="Curtidas" placeholder="0" value={post.likes} onChange={(val: string) => updatePost(index, 'likes', val)} />
                                    <MetricInput label="Comentários" placeholder="0" value={post.comments} onChange={(val: string) => updatePost(index, 'comments', val)} />
                                    <MetricInput label="Compartilhamentos" placeholder="0" value={post.shares} onChange={(val: string) => updatePost(index, 'shares', val)} />
                                    <MetricInput label="Salvamentos" placeholder="0" value={post.saves} onChange={(val: string) => updatePost(index, 'saves', val)} />
                                    <MetricInput label="Vendas/Leads" placeholder="0" value={post.conversions} onChange={(val: string) => updatePost(index, 'conversions', val)} highlight />
                                </div>
                                <div className="space-y-3 border-t border-slate-100 pt-6">
                                    <label className="ml-1 block text-[11px] font-bold uppercase tracking-widest text-slate-500">
                                        Tema do criativo (opcional) — post {index + 1}
                                    </label>
                                    <p className="ml-1 text-left text-xs leading-relaxed text-slate-500">
                                        Descreva a cena ou estética que você quer para a imagem deste roteiro (ex.: &quot;cozinha minimalista ao amanhecer&quot;). Deixe em branco para a IA decidir pelo DNA da marca.
                                    </p>
                                    <input
                                        placeholder="Ex.: bastidores do estúdio, produto em superfície de madeira, lifestyle urbano..."
                                        value={post.creativeTheme ?? ''}
                                        onChange={(e) => updatePost(index, 'creativeTheme', e.target.value)}
                                        className="input-app"
                                    />
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                <button
                    type="button"
                    onClick={addPost}
                    className="group flex w-full items-center justify-center gap-2 rounded-2xl border-2 border-dashed border-slate-200 bg-white py-4 text-sm font-medium text-slate-500 transition-all hover:border-emerald-300 hover:text-emerald-700"
                >
                    <Plus className="h-4 w-4" /> Adicionar mais um post
                </button>

                <div className="pt-10">
                    <button
                        type="button"
                        onClick={handleFinalize}
                        disabled={isSaving || posts.some(p => !p.link)}
                        className="btn-primary flex w-full items-center justify-center gap-3 py-5 text-lg disabled:opacity-50"
                    >
                        {isSaving ? "Processando..." : (
                            <>
                                Gerar minha estratégia <Send className="h-5 w-5" />
                            </>
                        )}
                    </button>
                    <p className="mt-6 text-center text-xs text-slate-500">
                        Sua estratégia será enviada em até 5 minutos para o e-mail cadastrado.
                    </p>
                </div>
            </div>
            )}
        </div>
    );
}

function MetricInput({ label, placeholder, value, onChange, highlight = false }: {
    label: string
    placeholder: string
    value: string
    onChange: (val: string) => void
    highlight?: boolean
}) {
    return (
        <div className="space-y-2">
            <label className={`block text-center text-[10px] font-bold uppercase tracking-widest ${highlight ? 'text-emerald-700' : 'text-slate-500'}`}>{label}</label>
            <input
                type="number"
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className={`input-app text-center ${highlight ? 'border-emerald-200 focus:border-emerald-500' : ''}`}
            />
        </div>
    )
}
