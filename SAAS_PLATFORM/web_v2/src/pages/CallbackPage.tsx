import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { Loader2 } from 'lucide-react';

export default function CallbackPage() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const {
        setAuth,
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
        posts,
    } = useOnboardingStore();
    const [status, setStatus] = useState("Processando autorização...");

    const API_URL = import.meta.env.VITE_API_URL || "https://leads-ai-v2.onrender.com";

    useEffect(() => {
        const code = searchParams.get('code');

        if (code) {
            handleAuthExchange(code);
        } else {
            setStatus("Erro: Nenhum código recebido do Facebook.");
        }
    }, [searchParams]);

    const handleAuthExchange = async (code: string) => {
        try {
            const redirectUri = `${window.location.origin}${window.location.pathname}`;

            setStatus("Validando token...");

            const resExchange = await fetch(`${API_URL}/auth/facebook/exchange`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ access_token: code, redirect_uri: redirectUri })
            });

            const dataExchange = await resExchange.json();

            if (!dataExchange.success) throw new Error(dataExchange.message);

            const token = dataExchange.token;
            const accounts = dataExchange.accounts;
            const accountId = accounts[0]?.ig_id;

            if (!accountId) throw new Error("Nenhuma conta do Instagram encontrada.");

            setStatus("Salvando seu perfil...");

            const resOnboarding = await fetch(`${API_URL}/auth/onboarding/complete`, {
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
                    manual_posts: posts.length ? posts : undefined,
                    facebook_token: token,
                    instagram_id: accountId,
                }),
            });

            if (!resOnboarding.ok) throw new Error("Falha ao salvar perfil.");

            setStatus("Coletando posts automáticos...");

            setAuth(token, accountId);

            setStatus("Sucesso! Redirecionando...");
            setTimeout(() => navigate('/strategy'), 1500);

        } catch (error: any) {
            console.error(error);
            setStatus("Erro: " + error.message);
        }
    };

    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-[#F8FAFC] px-6 font-sans text-slate-900 antialiased">
            <Loader2 className="mb-6 h-14 w-14 animate-spin text-emerald-600" />
            <h2 className="animate-pulse text-center text-xl font-bold text-slate-900 md:text-2xl">{status}</h2>
            <p className="mt-4 text-center text-sm text-slate-500">Por favor, não feche esta janela.</p>
        </div>
    );
}
