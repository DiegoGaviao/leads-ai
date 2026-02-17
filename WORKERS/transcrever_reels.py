
import os
import sys
import warnings

# Tenta importar whisper, se não der, avisa
try:
    import whisper
except ImportError:
    print("❌ Biblioteca 'openai-whisper' não encontrada.")
    print("👉 Rode: pip install openai-whisper ffmpeg-python")
    print("👉 E instale o FFmpeg no sistema (ex: brew install ffmpeg)")
    sys.exit(1)

BENCHMARK_DIR = "BENCHMARKS"

def transcrever_videos():
    print("🎧 Carregando modelo Whisper (pode demorar um pouco na 1ª vez)...")
    # Modelo 'base' é um bom equilíbrio entre velocidade e precisão para PT-BR
    model = whisper.load_model("base") 
    
    files = [f for f in os.listdir(BENCHMARK_DIR) if f.lower().endswith(('.mp4', '.mov', '.m4a', '.mp3'))]
    
    if not files:
        print(f"⚠️ Nenhum arquivo de vídeo encontrado na pasta '{BENCHMARK_DIR}'.")
        print("📥 Baixe algum Reel (ex: SaveInsta) e jogue o .mp4 lá.")
        return

    print(f"🎞️ Encontrados {len(files)} vídeos. Processando...")

    for filename in files:
        filepath = os.path.join(BENCHMARK_DIR, filename)
        txt_path = os.path.join(BENCHMARK_DIR, f"{filename}.txt")
        
        # Se já existe txt, pula (cache)
        if os.path.exists(txt_path):
            print(f"⏩ Já processado: {filename}")
            continue
            
        print(f"▶️ Transcrevendo: {filename} ...")
        
        try:
            # O Whisper faz a mágica (extrai áudio e transcreve)
            result = model.transcribe(filepath, fp16=False) # fp16=False evita erro de CPU
            texto = result["text"]
            
            # Salva no .txt
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"ARQUIVO: {filename}\n")
                f.write("="*40 + "\n")
                f.write(texto.strip())
                
            print(f"✅ Transcrição salva: {filename}.txt")
            
        except Exception as e:
            print(f"❌ Erro ao converter {filename}: {e}")

    print("\n🏁 Processo concluído! Os textos estão na pasta. Agora o Antigravity pode ler.")

if __name__ == "__main__":
    # Suprimir warnings chatos do Torch/Whisper
    warnings.filterwarnings("ignore")
    transcrever_videos()
