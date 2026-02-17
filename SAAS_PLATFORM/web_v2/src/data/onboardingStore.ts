import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface OnboardingState {
    // Step 1: Identidade Básica
    email: string;
    instagram: string;
    whatsapp: string;

    // Step 2: Alma da Marca (Estratégia)
    mission: string; // Qual sua missão?
    enemy: string;   // Quem é o "inimigo" do seu cliente?
    pain: string;    // Qual a dor principal?
    method: string;  // Nome do seu método/produto

    // Step 3: Auth (Token do Facebook)
    accessToken: string | null;
    accountId: string | null;

    // Actions
    setBasicInfo: (data: Partial<OnboardingState>) => void;
    setStrategy: (data: Partial<OnboardingState>) => void;
    setAuth: (token: string, accountId: string) => void;
    reset: () => void;
}

export const useOnboardingStore = create<OnboardingState>()(
    persist(
        (set) => ({
            email: '',
            instagram: '',
            whatsapp: '',
            mission: '',
            enemy: '',
            pain: '',
            method: '',
            accessToken: null,
            accountId: null,

            setBasicInfo: (data) => set((state) => ({ ...state, ...data })),
            setStrategy: (data) => set((state) => ({ ...state, ...data })),
            setAuth: (token, accountId) => set({ accessToken: token, accountId }),
            reset: () => set({
                email: '', instagram: '', whatsapp: '',
                mission: '', enemy: '', pain: '', method: '',
                accessToken: null, accountId: null
            }),
        }),
        {
            name: 'leads-ai-onboarding-storage',
        }
    )
);
