
import { supabase } from '../lib/supabaseClient';

export interface PostData {
    link: string;
    views: number;
    likes: number;
    saves: number;
    shares: number;
    comments: number;
}

export interface BriefingData {
    mission: string;
    toneOfVoice: string; // Ex: Provocativo
    authority: string;
    bigPromise: string;
    enemy: string;
    pain: string;
    desire: string;
    method?: string;
    dreamClient: string;
}

export const LeadsRepository = {
    // 1. Cria o Cliente (Setup Inicial)
    async createSetup(instagram: string, email: string) {
        // Verifica se já existe, se sim atualiza, senão cria
        const { data, error } = await supabase
            .from('clients')
            .upsert({ instagram_handle: instagram, email: email }, { onConflict: 'instagram_handle' })
            .select()
            .single();

        if (error) throw new Error(`Erro ao criar cliente: ${error.message}`);
        return data; // Retorna o ID do cliente
    },

    // 2. Salva o Briefing Estratégico
    async saveBriefing(clientId: string, briefing: BriefingData) {
        const { error } = await supabase
            .from('briefings')
            .upsert({
                client_id: clientId,
                mission: briefing.mission,
                tone_voice: briefing.toneOfVoice,
                authority_proof: briefing.authority,
                big_promise: briefing.bigPromise,
                enemy: briefing.enemy,
                pain_point: briefing.pain,
                desire_point: briefing.desire,
                method_name: briefing.method,
                dream_client: briefing.dreamClient,
                updated_at: new Date()
            }, { onConflict: 'client_id' });

        if (error) throw new Error(`Erro ao salvar briefing: ${error.message}`);
    },

    // 3. Salva os Posts para Análise (Limpa anteriores e reinsere)
    async savePosts(clientId: string, posts: PostData[]) {
        // Primeiro remove posts antigos desse cliente para não duplicar
        await supabase.from('analyzed_posts').delete().eq('client_id', clientId);

        // Insere os novos
        const postsToInsert = posts.map(p => ({
            client_id: clientId,
            post_link: p.link,
            views: p.views || 0,
            likes: p.likes || 0,
            saves: p.saves || 0,
            shares: p.shares || 0,
            comments: p.comments || 0,
            status: 'pending_analysis' // Status inicial para o backend Python pegar
        }));

        const { error } = await supabase.from('analyzed_posts').insert(postsToInsert);

        if (error) throw new Error(`Erro ao salvar posts: ${error.message}`);
    }
};
