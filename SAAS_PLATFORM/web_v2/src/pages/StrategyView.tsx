import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { supabase } from '../lib/supabaseClient';
import { ResultsView } from '../components/ResultsView';
import { Loader2, AlertCircle, Mail } from 'lucide-react';

export default function StrategyView() {
    const { email } = useOnboardingStore();
    const location = useLocation();
    const params = new URLSearchParams(location.search);
    const strategyIdParam = params.get('strategy_id');
    const [strategy, setStrategy] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchStrategy = async () => {
            // se strategy_id foi passado na URL, buscamos diretamente pela leads_ai_strategies.id
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
                // 1. Buscar a marca pelo e-mail
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

                // 2. Buscar a estratégia gerada para essa marca
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

        // Setup Realtime Subscription
        const channel = supabase
            .channel('leads_strategy_updates')
            .on('postgres_changes', {
                event: 'INSERT',
                schema: 'public',
                table: 'leads_ai_strategies'
            }, () => {
                console.log("🚀 Nova estratégia detectada no banco novo!");
                fetchStrategy();
            })
            .subscribe();

        return () => {
            supabase.removeChannel(channel);
        };
    }, [email]);

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-white">
                <Loader2 className="w-12 h-12 text-blue-500 animate-spin mb-4" />
                <p className="animate-pulse">Consultando o Conselho de IAs...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-white p-6 text-center">
                <AlertCircle className="w-16 h-16 text-red-500 mb-4" />
                <h1 className="text-2xl font-bold mb-2">Ops! Algo deu errado</h1>
                <p className="text-slate-400 mb-8 max-w-md">{error}</p>
                <a href="/" className="btn-primary">Voltar para Home</a>
            </div>
        );
    }

    if (!strategy) {
        return (
            <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-white p-6 text-center">
                <div className="w-20 h-20 bg-blue-500/10 rounded-full flex items-center justify-center mb-6">
                    <Mail className="w-10 h-10 text-blue-400 animate-bounce" />
                </div>
                <h1 className="text-3xl font-bold mb-4">Estamos Criando Sua Estratégia</h1>
                <p className="text-slate-400 mb-8 max-w-lg leading-relaxed">
                    O <b>Robô Analista</b> e o <b>Conselho Criativo</b> estão processando seus dados agora.
                    <br /><br />
                    Isso geralmente leva de 1 a 2 minutos. Você receberá um e-mail em <b>{email}</b> assim que estiver pronta, ou pode aguardar nesta página que ela atualizará automaticamente!
                </p>
                <div className="w-full max-w-xs h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-blue-500 w-1/2 animate-[loading_2s_infinite_linear]"></div>
                </div>
                <style>{`
                    @keyframes loading {
                        from { transform: translateX(-100%); }
                        to { transform: translateX(200%); }
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
