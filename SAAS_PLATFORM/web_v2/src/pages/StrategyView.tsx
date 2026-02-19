import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { supabase } from '../lib/supabaseClient';
import { ResultsView } from '../components/ResultsView';
import { AlertCircle, Mail, Sparkles } from 'lucide-react';

export default function StrategyView() {
    const { email } = useOnboardingStore();
    const navigate = useNavigate();
    const location = useLocation();
    const params = new URLSearchParams(location.search);
    const strategyIdParam = params.get('strategy_id');
    const [strategy, setStrategy] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchStrategy = async () => {
            if (strategyIdParam) {
                try {
                    const { data: strat, error: stratErr } = await supabase
                        .from('leads_ai_strategies')
                        .select('*')
                        .eq('id', strategyIdParam)
                        .maybeSingle();

                    if (stratErr) throw stratErr;
                    if (strat) {
                        setStrategy({
                            persona: strat.persona_markdown,
                            estrategia: strat.strategy_markdown,
                            roteiros: strat.scripts_json
                        });
                    } else {
                        setStrategy(null);
                    }
                } catch (err: any) {
                    console.error(err);
                    setError(err.message);
                } finally {
                    setLoading(false);
                }
                return;
            }

            if (!email) {
                setLoading(false);
                setError("E-mail não identificado. Por favor, faça o onboarding novamente.");
                return;
            }

            try {
                const { data: brand, error: brandErr } = await supabase
                    .from('leads_ai_brands')
                    .select('id')
                    .eq('email', email)
                    .order('created_at', { ascending: false })
                    .limit(1)
                    .maybeSingle();

                if (brandErr || !brand) {
                    setStrategy(null);
                    return;
                }

                const { data: stratData, error: stratErr } = await supabase
                    .from('leads_ai_strategies')
                    .select('*')
                    .eq('brand_id', brand.id)
                    .order('created_at', { ascending: false })
                    .limit(1)
                    .maybeSingle();

                if (stratErr) throw stratErr;

                if (stratData) {
                    setStrategy({
                        persona: stratData.persona_markdown,
                        estrategia: stratData.strategy_markdown,
                        roteiros: stratData.scripts_json
                    });
                } else {
                    setStrategy(null);
                }
            } catch (err: any) {
                console.error(err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchStrategy();

        const channel = supabase
            .channel('leads_strategy_updates')
            .on('postgres_changes', {
                event: 'INSERT',
                schema: 'public',
                table: 'leads_ai_strategies'
            }, () => {
                fetchStrategy();
            })
            .subscribe();

        return () => {
            supabase.removeChannel(channel);
        };
    }, [email, strategyIdParam]);

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-slate-50 antialiased">
                <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 animate-pulse border border-primary/20">
                    <Sparkles className="w-6 h-6 text-primary" />
                </div>
                <p className="text-sm font-medium tracking-widest uppercase text-slate-500 animate-pulse">Consultando Conselho de IAs</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 text-center antialiased">
                <div className="card-premium max-w-md w-full py-12">
                    <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-6" />
                    <h1 className="text-2xl font-bold mb-3 font-display">Algo deu errado</h1>
                    <p className="text-slate-400 mb-8 text-sm leading-relaxed">{error}</p>
                    <button onClick={() => navigate('/')} className="btn-primary py-3 px-8 text-sm">Voltar para Home</button>
                </div>
            </div>
        );
    }

    if (!strategy) {
        return (
            <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-slate-50 p-6 text-center antialiased">
                <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-[400px] bg-primary/5 blur-[120px] -z-10" />

                <div className="card-premium max-w-xl w-full py-16">
                    <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-8 border border-primary/20">
                        <Mail className="w-10 h-10 text-primary animate-bounce" />
                    </div>
                    <h1 className="text-3xl font-bold mb-4 font-display">Criando Sua Estratégia</h1>
                    <p className="text-slate-400 mb-10 text-base leading-relaxed px-8">
                        Nosso <b>Conselho Criativo</b> está analisando seu DNA de marca agora mesmo. Isso levará cerca de 2 minutos.
                        <br /><br />
                        Você pode aguardar aqui ou conferir seu e-mail em instantes.
                    </p>

                    <div className="w-full max-w-xs mx-auto h-1 bg-slate-900 rounded-full overflow-hidden">
                        <div className="h-full bg-primary w-1/3 animate-[loading_3s_infinite_ease-in-out]" />
                    </div>
                </div>

                <style>{`
                    @keyframes loading {
                        0% { transform: translateX(-100%); width: 10%; }
                        50% { transform: translateX(100%); width: 40%; }
                        100% { transform: translateX(300%); width: 10%; }
                    }
                `}</style>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950">
            <ResultsView data={strategy} />
        </div>
    );
}
