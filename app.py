import streamlit as st
from google import genai
import os
from PIL import Image
from gtts import gTTS

# Importações do MoviePy (Novo padrão estável da versão 2.0+)
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ImobiScript & Video IA", page_icon="🏢", layout="centered")

st.title("🏢 ImobiScript & Video IA")
st.subheader("Gere Roteiros e Vídeos Automatizados para Redes Sociais")

# --- INICIALIZAÇÃO DE ESTADOS NA SESSÃO ---
if "contador_uso" not in st.session_state:
    st.session_state.contador_uso = 0

if "texto_gerado" not in st.session_state:
    st.session_state.texto_gerado = ""

LIMITE_GRATUITO = 3
usos_restantes = LIMITE_GRATUITO - st.session_state.contador_uso

# --- BARRA LATERAL COMERCIAL ---
with st.sidebar:
    st.header("👑 Estatuto da Conta")
    if usos_restantes > 0:
        st.warning(f"Versão de Teste: {usos_restantes} créditos restantes.")
    else:
        st.error("❌ Créditos esgotados!")
    st.markdown("---")
    st.markdown("### 🚀 Vantagens do Plano Premium")
    st.write("- Roteiros ilimitados no Gemini 3.8-Flash")
    st.write("- Renderização de vídeo em alta definição")
    st.write("- Suporte e atualizações")

# --- CRIAÇÃO DAS ABAS (TABS) ---
tab1, tab2 = st.tabs(["📝 1. Gerador de Roteiros (Texto)", "🎬 2. Criador de Vídeo Automático"])

# ==========================================
# ABA 1: GERADOR DE ROTEIROS
# ==========================================
with tab1:
    if usos_restantes <= 0:
        st.error("⚠️ **Limite de teste atingido!**")
        st.markdown("Ativa a tua **Conta Premium** por apenas 19€/mês para continuar a utilizar. Paga via MB WAY e envia o comprovativo ao desenvolvedor!")
    else:
        st.write("### 📝 Detalhes do Imóvel e Público")
        
        tipo_imovel = st.selectbox(
            "Qual o tipo do imóvel?",
            ["Apartamento Compacto/Studio (Foco em investidores/jovens)", 
             "Casa em Condomínio Fechado (Foco em famílias)", 
             "Cobertura/Imóvel de Alto Padrão (Foco em luxo)",
             "Imóvel na Planta / Lançamento"]
        )
        
        localizacao = st.text_input("Localização/Bairro (ex: Moema, SP ou Belas Clube de Campo, Portugal):", key="loc_input")
        preco = st.text_input("Preço médio ou diferencial (ex: A partir de 340.000 €):", key="price_input")
        diferenciais = st.text_area("Quais os 3 principais pontos fortes? (ex: Em frente ao Golfe, piscina privativa, 20 min de Lisboa):", key="diff_input")
        
        tipo_script = st.radio(
            "O que deseja gerar?",
            ["Roteiro de Vídeo (Reels/Instagram)", "Mensagem de Abordagem (WhatsApp)", "Texto para Anúncio Patrocinado (Meta Ads)"],
            horizontal=True,
            key="type_script_input"
        )
        
        if st.button("🚀 Gerar Script de Vendas Magnético", type="primary"):
            if not localizacao or not diferenciais:
                st.warning("Por favor, preencha a localização e os diferenciais do imóvel.")
            else:
                with st.spinner("A IA está analisando o mercado e criando seu script..."):
                    try:
                        api_key_segura = st.secrets["GEMINI_API_KEY"]
                        client = genai.Client(api_key=api_key_segura)
                        
                        prompt_base = f"""
                        Você é um Copywriter de elite especializado no mercado imobiliário e gatilhos mentais de escassez e exclusividade.
                        Gere um material focado no seguinte imóvel:
                        - Tipo: {tipo_imovel} - Localização: {localizacao} - Preço: {preco} - Diferenciais: {diferenciais}
                        """
                        
                        if tipo_script == "Roteiro de Vídeo (Reels/Instagram)":
                            prompt_final = prompt_base + "Crie um roteiro de vídeo dinâmico de até 60 segundos. Divida rigorosamente em colunas ou blocos de: [CENA] e [ÁUDIO/FALA DO CORRETOR]. Comece com um GANCHO FORTE de 3 segundos e termine com CTA para comentar."
                        elif tipo_script == "Mensagem de Abordagem (WhatsApp)":
                            prompt_final = prompt_base + "Crie uma mensagem direta, profissional, altamente persuasiva para WhatsApp com emojis. Termine com uma pergunta aberta."
                        else:
                            prompt_final = prompt_base + "Crie um texto de anúncio completo (Copy para legenda). Inclua Título, Corpo focado em estilo de vida e CTA 'Clique em Saiba Mais'."
                        
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=prompt_final,
                        )
                        
                        # Salva o resultado no estado da sessão para não sumir
                        st.session_state.texto_gerado = response.text
                        st.session_state.contador_uso += 1
                        st.toast("Roteiro criado com sucesso!", icon="🎉")
                        
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao gerar o script: {e}")
        
        # EXIBIÇÃO DO TEXTO FORA DO BOTÃO (Garante a persistência da informação)
        if st.session_state.texto_gerado:
            st.success("🎉 Script generated com sucesso!")
            st.markdown("---")
            st.markdown(st.session_state.texto_gerado)
            st.markdown("---")
            
            # Caixa com o botão nativo para cópia instantânea
            st.text_area("Texto pronto para cópia (Usa para alimentar a Aba de Vídeo):", value=st.session_state.texto_gerado, height=200)
            st.caption("💡 **Dica:** Clica no ícone da prancheta no canto superior direito da caixa acima para copiar tudo.")

# ==========================================
# ABA 2: CRIADOR DE VÍDEO AUTOMÁTICO
# ==========================================
with tab2:
    st.write("### 🎬 Montagem Automática do Reels")
    st.write("Pega na fala gerada pela IA na aba anterior e junta as fotos do teu imóvel para gerar o vídeo final.")
    
    fotos_carregadas = st.file_uploader(
        "Faz o upload das fotos do imóvel (Formatos válidos: JPG, PNG):", 
        type=["jpg", "png", "jpeg"], 
        accept_multiple_files=True,
        key="uploader_global"
    )
    
    # Se já existir texto gerado na aba 1, ele pré-preenche aqui para poupar tempo
    texto_inicial = st.session_state.texto_gerado if st.session_state.texto_gerado else "Não compre nenhum imóvel para investimento antes de ver isto. Este apartamento fica a 3 minutos do metro e tem piscina infinita na cobertura. Condições únicas de pré-lançamento."
    
    texto_narracao = st.text_area(
        "Cola aqui apenas o texto das FALAS do corretor (Remova as marcações de [CENA]):",
        value=texto_inicial,
        height=150
    )
    
    if st.button("🎥 Renderizar e Baixar Vídeo", type="secondary"):
        if not fotos_carregadas:
            st.warning("Por favor, adiciona pelo menos 2 fotos do imóvel.")
        elif len(fotos_carregadas) < 2:
            st.warning("Adiciona mais imagens para fazer uma transição dinâmica.")
        else:
            with st.spinner("A processar a voz por IA e a estruturar os frames visuais..."):
                try:
                    # Gerar a narração com gTTS
                    arquivo_audio = "narracao.mp3"
                    tts = gTTS(text=texto_narracao, lang='pt', tld='com.br')
                    tts.save(arquivo_audio)
                    
                    audio_clip = AudioFileClip(arquivo_audio)
                    duracao_total = audio_clip.duration
                    duracao_por_foto = duracao_total / len(fotos_carregadas)
                    
                    clips_de_imagem = []
                    if not os.path.exists("temp_img"):
                        os.makedirs("temp_img")
                    
                    for i, ficheiro in enumerate(fotos_carregadas):
                        img = Image.open(ficheiro)
                        img_redimensionada = img.resize((1080, 1920)) # Formato vertical do Instagram Reels
                        caminho_temp = f"temp_img/foto_{i}.jpg"
                        img_redimensionada.save(caminho_temp)
                        
                        # CORREÇÃO EFETUADA AQUI: Mudança de set_duration para with_duration (MoviePy v2+)
                        clip = ImageClip(caminho_temp).with_duration(duracao_por_foto)
                        clips_de_imagem.append(clip)
                    
                    video_final = concatenate_videoclips(clips_de_imagem, method="compose")
                    video_final = video_final.with_audio(audio_clip)

                    
                    nome_video_saida = "reels_final_imovel.mp4"
                    video_final.write_videofile(nome_video_saida, fps=24, codec="libx264", audio_codec="aac")
                    
                    st.success("🎉 O teu Reels com narração foi construído com sucesso!")
                    
                    with open(nome_video_saida, "rb") as file:
                        st.download_button(
                            label="⬇️ Descarregar Vídeo Pronto (.mp4)",
                            data=file,
                            file_name="reels_imovel_ia.mp4",
                            mime="video/mp4"
                        )
                    
                    audio_clip.close()
                    video_final.close()
                    
                except Exception as e:
                    st.error(f"Erro ao processar a renderização do vídeo: {e}")
