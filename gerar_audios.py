import os
import re
import json
import asyncio
import edge_tts

DEFAULT_TEXTS = [
    # Basic steps
    "step", "stamp", "stomp", "heel", "toe", "toe (tip)", "dig", "brush", "spank", "hop", "scuff", "chug", "click",
    # Combinations
    "cramp roll", "shuffle ball change", "irish", "flap heel", "shuffle step", "flap", "shuffle", "spank step",
    "paradiddle", "drawback", "buffalo", "maxie ford", "waltz clog"
]

VOICE = "en-US-JennyNeural"
OUTPUT_DIR = "audio"
INDEX_HTML_PATH = "index.html"

def get_speakable_text(text):
    clean = text.strip().lower()
    if clean in ['toe (tip)', 'toe tip', 'toe(tip)']:
        return 'tip'
    return clean

def get_audio_filename(text):
    clean = get_speakable_text(text)
    return re.sub(r'[^a-z0-9]', '_', clean) + '.mp3'

def extract_phrases(text):
    if not text:
        return set()
    
    phrases = {text.strip()}
    
    # 1. Strip parentheses completely to get a clean read-through phrase
    cleaned_parentheses = re.sub(r'[\(\)]', ' ', text).strip()
    cleaned_parentheses = re.sub(r'\s+', ' ', cleaned_parentheses)
    phrases.add(cleaned_parentheses)
    
    # 2. Extract parts inside parentheses
    matches = re.findall(r'\((.*?)\)', text)
    for m in matches:
        for sub in re.split(r'[/,]', m):
            phrases.add(sub.strip())
            
    # 3. Get the part before the parentheses
    before_parentheses = re.sub(r'\(.*?\)', '', text).strip()
    before_parentheses = re.sub(r'\s+', ' ', before_parentheses)
    if before_parentheses:
        phrases.add(before_parentheses)
        
    # 4. Split the whole text by slashes or commas
    for part in re.split(r'[/,]', text):
        clean_part = re.sub(r'[\(\)]', '', part).strip()
        clean_part = re.sub(r'\s+', ' ', clean_part)
        if clean_part:
            phrases.add(clean_part)
            
    # Clean up empty or single character strings
    return {p.lower().strip() for p in phrases if len(p.strip()) > 1}

def scan_glossary_combinations():
    glossary_texts = set()
    if not os.path.exists(INDEX_HTML_PATH):
        print("Aviso: index.html não encontrado no caminho padrão.")
        return glossary_texts
        
    try:
        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            
        match = re.search(r'const\s+SYLLABUS_COMBINATIONS\s*=\s*(\[.*?\]);', content, re.DOTALL)
        if match:
            json_str = match.group(1)
            combinations = json.loads(json_str)
            print(f"Lidas {len(combinations)} combinações do glossário em index.html.")
            for c in combinations:
                e_name = c.get('e', '')
                n_name = c.get('n', '')
                
                # Extrai variações para o termo em Inglês (utilizado para ditado por voz)
                glossary_texts.update(extract_phrases(e_name))
                # Também para o Português (caso seja adicionado como passo customizado)
                glossary_texts.update(extract_phrases(n_name))
        else:
            print("Aviso: SYLLABUS_COMBINATIONS não encontrado em index.html.")
    except Exception as e:
        print(f"Erro ao escanear o glossário: {e}")
        
    return glossary_texts

def scan_json_files():
    scanned_texts = set()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(current_dir):
        if file.endswith('.json'):
            file_path = os.path.join(current_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                def extract_steps(obj):
                    if isinstance(obj, dict):
                        if 'steps' in obj and isinstance(obj['steps'], list):
                            for step in obj['steps']:
                                if isinstance(step, dict) and 'step' in step:
                                    scanned_texts.update(extract_phrases(step['step']))
                        for val in obj.values():
                            extract_steps(val)
                    elif isinstance(obj, list):
                        for item in obj:
                            extract_steps(item)
                            
                extract_steps(data)
            except Exception as e:
                print(f"Erro ao ler JSON {file}: {e}")
    return scanned_texts

async def generate_file(text, sem):
    async with sem:
        clean_text = get_speakable_text(text)
        if not clean_text or clean_text in ['a definir', 'a_definir']:
            return
        
        filename = get_audio_filename(text)
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(filepath):
            return
        
        try:
            communicate = edge_tts.Communicate(clean_text, VOICE)
            await communicate.save(filepath)
            print(f"Gerado: {filename} ('{clean_text}')")
        except Exception as e:
            print(f"Erro ao gerar {filename} ('{clean_text}'): {e}")

async def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Diretório '{OUTPUT_DIR}' criado.")
        
    texts_to_generate = set()
    
    # 1. Adiciona passos padrão
    for t in DEFAULT_TEXTS:
        texts_to_generate.update(extract_phrases(t))
        
    # 2. Adiciona termos do glossário
    glossary_terms = scan_glossary_combinations()
    print(f"Total de termos extraídos do glossário: {len(glossary_terms)}")
    texts_to_generate.update(glossary_terms)
    
    # 3. Adiciona passos detectados em projetos JSON
    scanned_json = scan_json_files()
    print(f"Total de termos extraídos dos arquivos JSON: {len(scanned_json)}")
    texts_to_generate.update(scanned_json)
        
    print(f"Total de {len(texts_to_generate)} áudios únicos para processar.")
    
    sem = asyncio.Semaphore(5)  # limite de concorrência para evitar bloqueios
    tasks = [generate_file(text, sem) for text in texts_to_generate]
    await asyncio.gather(*tasks)
    print("Processamento concluído com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
