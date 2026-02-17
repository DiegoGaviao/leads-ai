
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def generate_screenshots(root_dir):
    # Setup Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1200,1200") # Bigger than 1080 to ensure no bars
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--force-device-scale-factor=1")
    
    # Initialize Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print(f"📷 Iniciando geração de prints em: {root_dir}")
    
    image_count = 0

    try:
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(subdir, file)
                    abs_path = os.path.abspath(file_path)
                    
                    # Nome do arquivo de saída
                    output_name = file.replace(".html", ".png")
                    output_path = os.path.join(subdir, output_name)
                    
                    print(f"Processando: {file}...")
                    
                    # Carregar arquivo
                    driver.get(f"file://{abs_path}")
                    time.sleep(1) # Aguardar renderização/animações
                    
                    # Ajustar CSS para remover o scale(0.6) que coloquei para visualização manual
                    # E forçar tamanho 1080x1080
                    try:
                        driver.execute_script("""
                            document.body.style.transform = 'none';
                            document.body.style.zoom = '1';
                            document.body.style.overflow = 'hidden';
                            
                            var container = document.querySelector('.post-container');
                            if (container) {
                                container.style.transform = 'none'; // Remove scale(0.6)
                                container.style.margin = '0';
                                container.style.boxShadow = 'none'; // Remove sombra externa
                            }
                        """)
                        time.sleep(0.5)
                        
                        # Capturar o elemento exato
                        element = driver.find_element(By.CLASS_NAME, "post-container")
                        element.screenshot(output_path)
                        
                        print(f"✅ Salvo: {output_name}")
                        image_count += 1
                        
                    except Exception as e:
                        print(f"❌ Erro ao capturar {file}: {e}")

    finally:
        driver.quit()
        print(f"\n✨ Concluído! {image_count} imagens geradas.")

if __name__ == "__main__":
    target_dir = "CLIENTES/DHAWK/INSTAGRAM_CONTENT"
    generate_screenshots(target_dir)
