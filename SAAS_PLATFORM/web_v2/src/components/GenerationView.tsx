import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Search, Code, CheckCircle2, Sparkles, AlertCircle } from 'lucide-react'

interface GenerationViewProps {
    data: any
    onComplete: (result: any) => void
}

const steps = [
    { id: 1, text: "Convocando o Cientista de Dados (DeepSeek)...", icon: <Search className="w-5 h-5" /> },
    { id: 2, text: "Analisando padrões nos seus posts mais salvos...", icon: <Sparkles className="w-5 h-5" /> },
    { id: 3, text: "Consultando o Crítico Criativo (Mistral)...", icon: <Brain className="w-5 h-5" /> },
    { id: 4, text: "Lapidando a persona para evitar clichês...", icon: <CheckCircle2 className="w-5 h-5" /> },
    { id: 5, text: "Roteirizando 5 novas ideias com alma...", icon: <Code className="w-5 h-5" /> },
    { id: 6, text: "Gerando criativos de imagem (um por roteiro)...", icon: <Sparkles className="w-5 h-5" /> },
]

export function GenerationView({ data, onComplete }: GenerationViewProps) {
    const [currentStep, setCurrentStep] = useState(0)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const stepInterval = setInterval(() => {
            setCurrentStep(prev => {
                if (prev < steps.length - 1) return prev + 1
                return prev
            })
        }, 4000)

        const startAnalysis = async () => {
            const API_URL = import.meta.env.VITE_API_URL || "https://leads-ai-v2.onrender.com";
            try {
                const response = await fetch(`${API_URL}/analyze`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                })

                if (!response.ok) throw new Error('Falha na comunicação com o Conselho de IAs')

                const result = await response.json()
                if (result.success) {
                    setTimeout(() => onComplete(result.data), 1500)
                } else {
                    throw new Error('Erro no processamento da estratégia')
                }
            } catch (err: any) {
                setError(err.message)
            }
        }

        startAnalysis()

        return () => clearInterval(stepInterval)
    }, [data, onComplete])

    if (error) {
        return (
            <div className="flex min-h-screen flex-col items-center justify-center p-6 text-center antialiased">
                <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-red-50 text-red-600">
                    <AlertCircle className="h-10 w-10" />
                </div>
                <h3 className="mb-2 text-2xl font-bold text-slate-900">Ops! Houve um problema</h3>
                <p className="mb-8 text-slate-600">{error}</p>
                <button type="button" onClick={() => window.location.reload()} className="btn-secondary">Tentar novamente</button>
            </div>
        )
    }

    return (
        <div className="flex min-h-screen flex-col items-center justify-center p-6 text-center antialiased">
            <div className="relative mb-16">
                <div className="absolute inset-0 animate-pulse rounded-full bg-emerald-500/10 blur-[80px]" />
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                    className="relative flex h-32 w-32 items-center justify-center rounded-full border-2 border-slate-200 bg-white shadow-sm"
                >
                    <Brain className="h-12 w-12 text-emerald-600" />
                </motion.div>
            </div>

            <div className="w-full max-w-md space-y-4">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentStep}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="glass flex items-center gap-4 rounded-2xl border border-emerald-100 p-6 text-left shadow-md"
                    >
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-50 text-emerald-700">
                            {steps[currentStep].icon}
                        </div>
                        <p className="text-lg font-medium text-slate-800">{steps[currentStep].text}</p>
                    </motion.div>
                </AnimatePresence>

                <div className="flex justify-center gap-1 pt-8">
                    {steps.map((_, i) => (
                        <div
                            key={i}
                            className={`h-1.5 rounded-full transition-all duration-500 ${i <= currentStep ? 'w-8 bg-emerald-600' : 'w-2 bg-slate-200'}`}
                        />
                    ))}
                </div>
            </div>

            <p className="fixed bottom-12 flex items-center gap-2 text-sm text-slate-500">
                <Sparkles className="h-4 w-4 text-emerald-600" />
                A IA está cruzando seus dados de retenção agora...
            </p>
        </div>
    )
}
