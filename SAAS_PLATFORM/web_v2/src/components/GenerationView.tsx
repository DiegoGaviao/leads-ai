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
]

export function GenerationView({ data, onComplete }: GenerationViewProps) {
    const [currentStep, setCurrentStep] = useState(0)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        // 1. Simulação visual dos passos
        const stepInterval = setInterval(() => {
            setCurrentStep(prev => {
                if (prev < steps.length - 1) return prev + 1
                return prev
            })
        }, 4000)

        // 2. Chamada Real para o Backend
        const startAnalysis = async () => {
            try {
                const response = await fetch('http://localhost:8000/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                })

                if (!response.ok) throw new Error('Falha na comunicação com o Conselho de IAs')

                const result = await response.json()
                if (result.success) {
                    // Pequeno delay para garantir que o usuário viu o passo final
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
            <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center">
                <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center text-red-500 mb-6">
                    <AlertCircle className="w-10 h-10" />
                </div>
                <h3 className="text-2xl font-bold mb-2">Ops! Houve um problema</h3>
                <p className="text-muted-foreground mb-8">{error}</p>
                <button onClick={() => window.location.reload()} className="btn-secondary">Tentar novamente</button>
            </div>
        )
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center">
            <div className="relative mb-20">
                <div className="absolute inset-0 bg-primary/20 blur-[100px] animate-pulse-slow rounded-full" />
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                    className="relative w-32 h-32 border-2 border-white/10 rounded-full flex items-center justify-center"
                >
                    <Brain className="w-12 h-12 text-primary" />
                </motion.div>
            </div>

            <div className="max-w-md w-full space-y-4">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentStep}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="flex items-center gap-4 p-6 glass rounded-2xl text-left border-primary/20"
                    >
                        <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary shrink-0">
                            {steps[currentStep].icon}
                        </div>
                        <p className="text-lg font-medium">{steps[currentStep].text}</p>
                    </motion.div>
                </AnimatePresence>

                <div className="flex gap-1 justify-center pt-8">
                    {steps.map((_, i) => (
                        <div
                            key={i}
                            className={`h-1.5 rounded-full transition-all duration-500 ${i <= currentStep ? 'w-8 bg-primary' : 'w-2 bg-white/10'}`}
                        />
                    ))}
                </div>
            </div>

            <p className="fixed bottom-12 text-muted-foreground text-sm flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-accent" />
                A IA está cruzando seus dados de retenção agora...
            </p>
        </div>
    )
}
