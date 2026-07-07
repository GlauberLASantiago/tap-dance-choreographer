# Tap Dance Choreographer & Loop Trainer

Uma ferramenta interativa para sapateadores projetarem, ensaiarem e ditarem coreografias de sapateado em tempo real, integrada com o **Free Tap Dance Syllabus** e áudio realista de alta fidelidade.

---

## 🚀 Principais Recursos

1. **Ditado de Passos por Voz (TTS de Alta Fidelidade):**
   - Integração com o serviço online do **Microsoft Edge Read Aloud** (voz natural `en-US-JennyNeural`) por meio da biblioteca Python `edge-tts`.
   - **Pré-carregamento Inteligente:** Os arquivos de áudio locais `.mp3` correspondentes aos passos são pré-carregados na memória (`preload: auto`) assim que a coreografia é carregada.
   - **Sistema de Fallback Triplo:** Se o áudio local falhar ou não existir, o app busca o Google Translate TTS via rede. Se estiver sem conexão, utiliza a síntese nativa do navegador (`speechSynthesis`), garantindo que o ditado nunca pare.

2. **Dicionário Rítmico de Sapateado (Syllabus Completo):**
   - Painel integrado contendo **241 combinações e passos oficiais** baseados no *Free Tap Dance Syllabus* de Rod Howell (United Taps).
   - Busca instantânea por termo, nível de dificuldade (1 a 7) ou padrão de movimento.
   - Links diretos para os vídeos demonstrativos oficiais de cada termo.

3. **Detecção Automática de Combinações:**
   - Algoritmo que identifica sequências rápidas e agrupa passos individuais na tabela de tempos sob o rótulo do combo correspondente.
   - **Combinações L1/L2 Suportadas:**
     - *Básicas:* Flap, Shuffle, Spank Step, Flap Heel, Shuffle Step.
     - *Intermediárias/Avançadas:* Cramp Roll, Shuffle Ball Change, Irish.
     - *Novas Detecções:* **Paradiddle / Scuffle Step Heel**, **Drawback**, **Buffalo**, **Maxie Ford** e **Waltz Clog**.

4. **Visualizador de Forma de Onda (Waveform) & Ajuste Fino:**
   - Exibe a linha de onda sonora do áudio extraído do vídeo para alinhamento milimétrico dos tempos dos passos.
   - Suporte a zoom horizontal interativo.

5. **Ferramenta de Treino (Loop):**
   - Selecione blocos de passos na tabela de coreografia para repetir trechos específicos do vídeo em loop contínuo, facilitando a fixação de sequências difíceis.

6. **Modo Espelho (Mirror Mode):**
   - Opção para inverter automaticamente o trabalho de pés (Esquerda ➔ Direita, Direita ➔ Esquerda) para exportação rápida.

---

## 🛠️ Como Executar Localmente

### 1. Requisitos
- **Navegador Web:** Qualquer navegador moderno (Chrome, Edge, Firefox, Safari).
- **Python 3.x** (caso queira gerar novos áudios MP3).

### 2. Executando o App
Basta abrir o arquivo [index.html](index.html) diretamente no seu navegador de preferência (duplo clique no arquivo). Por ser uma aplicação estática baseada em HTML5 puro e JavaScript Vanilla, não requer servidores complexos para rodar.

### 3. Atualizando/Gerando Áudios com Edge TTS
Se você registrar novos passos personalizados e desejar que eles tenham áudio natural em MP3:
1. Instale a biblioteca `edge-tts`:
   ```bash
   pip install edge-tts
   ```
2. Execute o script gerador:
   ```bash
   python gerar_audios.py
   ```
O script varrerá o glossário completo e os arquivos de projeto `.json` locais, baixando novos arquivos de voz para a pasta `audio/`.

---

## 📦 Como Fazer o Deploy no GitHub Pages

Como este é um projeto front-end estático (HTML, CSS, JS e arquivos de áudio), a melhor forma de hospedá-lo gratuitamente é no **GitHub Pages**.

Aqui está o passo a passo para fazer o deploy:

### Passo 1: Inicialize o Git localmente
Se você ainda não inicializou o repositório na pasta do projeto, abra o seu terminal (PowerShell ou Git Bash) na pasta e execute:
```bash
git init
git add .
git commit -m "Initial commit - Tap Dance Choreographer completo"
```

### Passo 2: Crie um repositório no GitHub
1. Vá para o [GitHub](https://github.com) e crie um novo repositório vazio (não adicione README ou .gitignore na interface web do GitHub).
2. Dê um nome ao repositório (ex: `tap-dance-choreographer`).

### Passo 3: Conecte o repositório local ao GitHub e envie os arquivos
Copie o link do repositório criado e rode no terminal local:
```bash
# Substitua pelo link do seu repositório criado
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
git branch -M main
git push -u origin main
```

### Passo 4: Ative o GitHub Pages
1. No seu repositório no GitHub, clique na aba **Settings** (Configurações).
2. Na barra lateral esquerda, clique em **Pages**.
3. Em *Build and deployment*, na opção *Source*, selecione **Deploy from a branch**.
4. Em *Branch*, selecione **main** e a pasta `/ (root)`. Clique em **Save**.
5. Em alguns minutos, o GitHub disponibilizará o link público do seu aplicativo (ex: `https://seu-usuario.github.io/nome-do-repositorio/`).
