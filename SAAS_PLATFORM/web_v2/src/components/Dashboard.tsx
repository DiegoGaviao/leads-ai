import { useState } from 'react'
import { motion } from 'framer-motion'
import { Plus, Minus, Send } from 'lucide-react'

interface DashboardProps {
    onSubmit?: (data: any) => void
}

export function Dashboard({ onSubmit }: DashboardProps) {
    // const [step, setStep] = useState(1)
    const [formData, setFormData] = useState({
        instagram: '',
        email: '',
        missao: '',
        inimigo: '',
        dor_cliente: '',
        metodo_nome: '',
        posts: [{ tema: '', views: '', likes: '', saves: '', comments: '' }]
    })

    const addPost = () => {
        if (formData.posts.length < 10) {
            setFormData({ ...formData, posts: [...formData.posts, { tema: '', views: '', likes: '', saves: '', comments: '' }] })
        }
    }

    const removePost = (index: number) => {
        const newPosts = formData.posts.filter((_, i) => i !== index)
        setFormData({ ...formData, posts: newPosts })
    }

    const updatePost = (index: number, field: string, value: string) => {
        const newPosts = [...formData.posts]
        newPosts[index] = { ...newPosts[index], [field]: value }
        setFormData({ ...formData, posts: newPosts })
    }

    return (
        <div className="max-w-4xl mx-auto px-6 py-20">
            <div className="mb-12">
                <h2 className="text-4xl font-bold mb-4">Configuração da Estratégia</h2>
                <p className="text-muted-foreground text-lg">Preencha os dados para que o Conselho de IAs possa trabalhar.</p>
            </div>

            <div className="space-y-12">
                {/* Step 1: Identidade */}
                <section className="glass rounded-3xl p-8 md:p-12">
                    <h3 className="text-2xl font-bold mb-8 flex items-center gap-2">
                        <span className="w-8 h-8 rounded-full bg-primary/20 text-primary text-sm flex items-center justify-center">1</span>
                        Identidade da Marca
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-muted-foreground uppercase tracking-widest">Instagram</label>
                            <input
                                value={formData.instagram}
                                onChange={e => setFormData({ ...formData, instagram: e.target.value })}
                                placeholder="@seu_perfil"
                                className="w-full bg-white/5 border border-white/10 rounded-xl p-4 outline-none focus:ring-2 focus:ring-primary/50 transition-all font-medium"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-muted-foreground uppercase tracking-widest">E-mail</label>
                            <input
                                value={formData.email}
                                onChange={e => setFormData({ ...formData, email: e.target.value })}
                                placeholder="voce@exemplo.com"
                                className="w-full bg-white/5 border border-white/10 rounded-xl p-4 outline-none focus:ring-2 focus:ring-primary/50 transition-all font-medium"
                            />
                        </div>
                    </div>
                </section>

                {/* Step 2: Briefing Estratégico */}
                <section className="glass rounded-3xl p-8 md:p-12">
                    <h3 className="text-2xl font-bold mb-8 flex items-center gap-2">
                        <span className="w-8 h-8 rounded-full bg-secondary/20 text-secondary text-sm flex items-center justify-center">2</span>
                        Briefing com Alma
                    </h3>
                    <div className="space-y-8">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-muted-foreground uppercase tracking-widest">Sua Missão / O que você faz?</label>
                            <textarea
                                value={formData.missao}
                                onChange={e => setFormData({ ...formData, missao: e.target.value })}
                                rows={3}
                                placeholder="Ex: Ajudo psicólogas a lotarem a agenda sem surtar com o marketing."
                                className="w-full bg-white/5 border border-white/10 rounded-xl p-4 outline-none focus:ring-2 focus:ring-secondary/50 transition-all resize-none"
                            />
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-muted-foreground uppercase tracking-widest">O Inimigo (O que você NÃO quer ser)</label>
                                <input
                                    value={formData.inimigo}
                                    onChange={e => setFormData({ ...formData, inimigo: e.target.value })}
                                    placeholder="Ex: O marketing vazio de dancinhas."
                                    className="w-full bg-white/5 border border-white/10 rounded-xl p-4 outline-none focus:ring-2 focus:ring-secondary/50 transition-all"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-muted-foreground uppercase tracking-widest">Nome do seu Método (Opcional)</label>
                                <input
                                    value={formData.metodo_nome}
                                    onChange={e => setFormData({ ...formData, metodo_nome: e.target.value })}
                                    placeholder="Ex: Método Flow"
                                    className="w-full bg-white/5 border border-white/10 rounded-xl p-4 outline-none focus:ring-2 focus:ring-secondary/50 transition-all"
                                />
                            </div>
                        </div>
                    </div>
                </section>

                {/* Step 3: Dados de Performance */}
                <section className="glass rounded-3xl p-8 md:p-12">
                    <div className="flex items-center justify-between mb-8">
                        <h3 className="text-2xl font-bold flex items-center gap-2">
                            <span className="w-8 h-8 rounded-full bg-accent/20 text-accent text-sm flex items-center justify-center">3</span>
                            Dados de Performance
                        </h3>
                        <button onClick={addPost} className="btn-secondary py-2 flex items-center gap-2 text-sm">
                            <Plus className="w-4 h-4" /> Adicionar Post
                        </button>
                    </div>

                    <div className="space-y-6">
                        {formData.posts.map((post, index) => (
                            <motion.div
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                key={index}
                                className="p-6 bg-white/5 rounded-2xl border border-white/5 space-y-4 relative group"
                            >
                                <div className="flex justify-between items-center mb-2">
                                    <span className="text-xs font-bold uppercase tracking-widest text-muted-foreground">Post #{index + 1}</span>
                                    {index > 0 && (
                                        <button onClick={() => removePost(index)} className="text-red-400 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <Minus className="w-4 h-4" />
                                        </button>
                                    )}
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <input
                                        placeholder="Tema ou Gancho"
                                        value={post.tema}
                                        onChange={e => updatePost(index, 'tema', e.target.value)}
                                        className="col-span-1 md:col-span-2 bg-black/20 border border-white/5 rounded-lg p-3 text-sm"
                                    />
                                    <div className="grid grid-cols-2 md:grid-cols-4 col-span-1 md:col-span-2 gap-4">
                                        <input type="number" placeholder="Views" value={post.views} onChange={e => updatePost(index, 'views', e.target.value)} className="bg-black/20 border border-white/5 rounded-lg p-3 text-sm" />
                                        <input type="number" placeholder="Likes" value={post.likes} onChange={e => updatePost(index, 'likes', e.target.value)} className="bg-black/20 border border-white/5 rounded-lg p-3 text-sm" />
                                        <input type="number" placeholder="Saves" value={post.saves} onChange={e => updatePost(index, 'saves', e.target.value)} className="bg-black/20 border border-white/5 rounded-lg p-3 text-sm" />
                                        <input type="number" placeholder="Coment." value={post.comments} onChange={e => updatePost(index, 'comments', e.target.value)} className="bg-black/20 border border-white/5 rounded-lg p-3 text-sm" />
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </section>

                <button
                    onClick={() => {
                        if (onSubmit) {
                            onSubmit(formData);
                        }
                    }}
                    className="btn-primary w-full py-6 text-xl flex items-center justify-center gap-3 shadow-primary/30"
                >
                    Iniciar Reunião do Conselho <Send className="w-6 h-6" />
                </button>
            </div>
        </div>
    )
}
