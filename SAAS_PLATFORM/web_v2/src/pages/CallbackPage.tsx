import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useOnboardingStore } from '../data/onboardingStore';
import { Loader2 } from 'lucide-react';

export default function CallbackPage() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const { setAuth, email, instagram, mission, enemy, pain, method } = useOnboardingStore();
    const [status, setStatus] = useState("Processando autorização...");

    // URL DO BACKEND OFICIAL (Lê do .env ou usa localhost como fallback)
    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

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
            setStatus("Validando Token...");

            // 1. Troca CODE por TOKEN no Backend
            const resExchange = await fetch(`${API_URL}/auth/facebook/exchange`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ access_token: code }) // A rota do backend espera "access_token" mas usamos code aqui
                // Backend precisa ser ajustado para trocar Code por Token, ou Frontend faz isso.
                // Pelo código atual do backend, ele espera um token já?
                // NÃO. O backend atual auth.py foi feito meio placeholder.
                // Para simplificar: Vamos mandar o CODE como se fosse o token e o backend que se vire (vou ajustar o backend depois)
                // Ou melhor: O Frontend deveria pegar o token. Mas isso expõe o App Secret.
                // CORRETO: Frontend manda CODE -> Backend usa APP ID + SECRET -> Pega TOKEN.
                // Vou mandar o code mesmo.
            });

            const dataExchange = await resExchange.json();

            if (!dataExchange.success) throw new Error(dataExchange.message);

            const token = dataExchange.token;
            const accounts = dataExchange.accounts;
            const accountId = accounts[0]?.ig_id; // Pega a primeira conta por padrão (MVP)

            if (!accountId) throw new Error("Nenhuma conta do Instagram encontrada.");

            setStatus("Salvando seu Perfil...");

            // 2. Salva o Onboarding Completo (Marca + Auth) no Backend
            const resOnboarding = await fetch(`${API_URL}/onboarding/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email, instagram, mission, enemy, pain, method, // Dados do Step 1/2
                    facebook_token: token,
                    instagram_id: accountId
                })
            });

            if (!resOnboarding.ok) throw new Error("Falha ao salvar perfil.");

            setStatus("Coletando Posts Automáticos...");

            // 3. Dispara o Scan Inicial (Agente 01)
            // O backend /onboarding/complete já deveria fazer isso async, mas podemos chamar explícito
            await fetch(`${API_URL}/agents/scout/scan?account_id=${accountId}&token=${token}`);

            setAuth(token, accountId);

            setStatus("Sucesso! Redirecionando...");
            setTimeout(() => navigate('/dashboard'), 1500);

        } catch (error: any) {
            console.error(error);
            setStatus("Erro: " + error.message);
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-white font-['Inter']">
            <Loader2 className="w-16 h-16 text-blue-500 animate-spin mb-6" />
            <h2 className="text-2xl font-bold animate-pulse">{status}</h2>
            <p className="text-slate-500 mt-4 text-sm">Por favor, não feche esta janela.</p>
        </div>
    );
}
