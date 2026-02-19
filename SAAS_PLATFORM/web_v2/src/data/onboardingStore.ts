import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface OnboardingState {
    plan: 'free' | 'pro' | 'master' | null;
    // Step 1: Identidade Básica
    email: string;
    instagram: string;
    whatsapp: string;

    // Step 2: Alma da Marca (DNA Profundo)
    mission: string;
    enemy: string;
    pain: string;
    dream: string;
    dreamClient: string;
    method: string;
    toneVoice: string;     // Novo: Autoridade, Amigável, etc.
    brandValues: string;   // Novo: Valores pilares
    offerDetails: string;  // Novo: O que exatamente vende?
    differentiation: string; // Novo: Por que você e não o outro?

    // Step 3: Posts Manuais (Conforme PDF)
    posts: Array<{
        link: string;
        views: string;
        likes: string;
        comments: string;
        shares: string;
        saves: string;
        conversions: string;
    }>;

    // Step 4: Auth (Opcional por enquanto)
    accessToken: string | null;
    accountId: string | null;

    // Actions
    setBasicInfo: (data: Partial<OnboardingState>) => void;
    setStrategy: (data: Partial<OnboardingState>) => void;
    setPosts: (posts: OnboardingState['posts']) => void;
    setAuth: (token: string, accountId: string) => void;
    reset: () => void;
}

export const useOnboardingStore = create<OnboardingState>()(
    persist(
        (set) => ({
            plan: null,
            email: '',
            instagram: '',
            whatsapp: '',
            mission: '',
            enemy: '',
            pain: '',
            dream: '',
            dreamClient: '',
            method: '',
            toneVoice: '',
            brandValues: '',
            offerDetails: '',
            differentiation: '',
            posts: [],
            accessToken: null,
            accountId: null,

            setBasicInfo: (data) => set((state) => ({ ...state, ...data })),
            setStrategy: (data) => set((state) => ({ ...state, ...data })),
            setPosts: (posts) => set({ posts }),
            setAuth: (token, accountId) => set({ accessToken: token, accountId }),
            reset: () => set({
                plan: null,
                email: '', instagram: '', whatsapp: '',
                mission: '', enemy: '', pain: '', dream: '', dreamClient: '', method: '',
                toneVoice: '', brandValues: '', offerDetails: '', differentiation: '',
                posts: [],
                accessToken: null, accountId: null
            }),
        }),
        {
            name: 'leads-ai-onboarding-storage',
        }
    )
);
