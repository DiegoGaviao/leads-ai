import { useOnboardingStore } from '../data/onboardingStore';
import { Instagram } from 'lucide-react';

const FB_APP_ID = "880409131510410";
// MUDAR NA PRODUÇÃO PARA A URL REAL
const REDIRECT_URI = "http://localhost:5173/callback";

export default function ConnectInstagramPage() {
    const { instagram } = useOnboardingStore();

    const handleConnect = () => {
        // URL OFICIAL DE LOGIN
        const authUrl = `https://www.facebook.com/v18.0/dialog/oauth?client_id=${FB_APP_ID}&redirect_uri=${REDIRECT_URI}&scope=public_profile,instagram_basic,pages_show_list,instagram_manage_insights,pages_read_engagement,business_management&response_type=code`;

        // Redireciona o usuário para o Facebook
        window.location.href = authUrl;
    };

    return (
        <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-6 font-['Inter']">
            <div className="w-full max-w-2xl mb-8 flex items-center justify-between px-4 opacity-50 pointer-events-none">
                {/* Visual Progress Bar (Completo) */}
                <div className="flex flex-col items-center text-green-500">
                    <div className="w-8 h-8 rounded-full bg-green-500/20 border-2 border-green-500 flex items-center justify-center text-xs font-bold mb-1">OK</div>
                </div>
                <div className="flex-1 h-0.5 mx-2 bg-green-500/50"></div>
                <div className="flex flex-col items-center text-green-500">
                    <div className="w-8 h-8 rounded-full bg-green-500/20 border-2 border-green-500 flex items-center justify-center text-xs font-bold mb-1">OK</div>
                </div>
                <div className="flex-1 h-0.5 mx-2 bg-blue-500"></div>
                <div className="flex flex-col items-center text-blue-500">
                    <div className="w-10 h-10 rounded-full border-2 border-blue-500 bg-blue-500/20 flex items-center justify-center font-bold mb-2 shadow-[0_0_15px_rgba(59,130,246,0.5)]">3</div>
                    <span className="text-xs font-bold uppercase tracking-wider text-blue-400">CONECTAR</span>
                </div>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-10 max-w-lg w-full text-center shadow-2xl relative overflow-hidden backdrop-blur-xl">
                {/* Glow Effect */}
                <div className="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-purple-500/20 rounded-full blur-[50px]"></div>
                <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-40 h-40 bg-blue-500/20 rounded-full blur-[50px]"></div>

                <div className="w-24 h-24 bg-gradient-to-br from-pink-500 to-orange-500 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-lg transform rotate-3 hover:rotate-6 transition-transform">
                    <Instagram className="w-12 h-12 text-white" />
                </div>

                <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 mb-4">
                    Conexão Segura
                </h1>

                <p className="text-slate-400 mb-8 leading-relaxed">
                    Para que nosso Robô possa ler seus posts e entender o que performa, precisamos de sua permissão oficial.
                </p>

                <div className="bg-slate-950 rounded-xl p-4 mb-8 text-left border border-slate-800">
                    <p className="text-xs text-slate-500 uppercase font-bold tracking-wider mb-2">Dados que vamos acessar:</p>
                    <ul className="space-y-2 text-sm text-slate-300">
                        <li className="flex items-center gap-2">✅ Insights dos seus Posts (Views, Likes, Saves)</li>
                        <li className="flex items-center gap-2">✅ Legendas e Datas das publicações</li>
                        <li className="flex items-center gap-2">🔒 <strong>NÃO</strong> postamos nada por você</li>
                        <li className="flex items-center gap-2">🔒 <strong>NÃO</strong> lemos suas DMs</li>
                    </ul>
                </div>

                <button
                    onClick={handleConnect}
                    className="w-full bg-[#1877F2] hover:bg-[#166fe5] text-white font-bold py-4 px-6 rounded-xl flex items-center justify-center gap-3 transition-all shadow-lg hover:shadow-blue-500/30 transform hover:scale-[1.02]"
                >
                    <svg className="w-6 h-6 fill-current" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" /></svg>
                    <span>Continuar com Facebook</span>
                </button>

                <p className="mt-4 text-[10px] text-slate-600">
                    Ao continuar, você concorda com nossos Termos de Uso. Usamos a API Oficial da Meta.
                </p>

            </div>
        </div>
    );
}
