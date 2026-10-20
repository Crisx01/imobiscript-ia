import streamlit as st
from google import genai
import os

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ImobiScript IA", page_icon="🏢", layout="centered")

st.title("🏢 ImobiScript IA")
st.subheader("Gerador de Scripts de Venda de Alta Conversão para Corretores")
st.write("Crie copys perfeitas para seus imóveis sem precisar pensar em prompts complexos.")

# --- BARRA LATERAL COMERCIAL ---
with st.sidebar:
    st.header("👑 Conta Premium")
    st.success("Acesso Vitalício Ativado")
    st.markdown("---")
    st.markdown("""
    ### 🚀 Como funciona?
    A nossa IA está conectada diretamente ao banco de dados do mercado imobiliário para gerar as melhores copys do mercado.
    """)

# --- FORMULÁRIO DE ENTRADA DO CORRETOR ---
st.write("### 📝 Detalhes do Imóvel e Público")

tipo_imovel = st.selectbox(
    "Qual o tipo do imóvel?",
    ["Apartamento Compacto/Studio (Foco em investidores/jovens)", 
     "Casa em Condomínio Fechado (Foco em famílias)", 
     "Cobertura/Imóvel de Alto Padrão (Foco em luxo)",
     "Imóvel na Planta / Lançamento"]
)

localizacao = st.text_input("Localização/Bairro (ex: Moema, SP ou Barra da Tijuca, RJ):")
preco = st.text_input("Preço médio ou diferencial de preço (ex: A partir de R$ 450 mil ou 'Excelente custo-benefício'):")
diferenciais = st.text_area("Quais os 3 principais pontos fortes? (ex: Varanda gourmet, 2 vagas cobertas, metrô próximo):")

tipo_script = st.radio(
    "O que você deseja gerar?",
    ["Roteiro de Vídeo (Reels/Instagram)", "Mensagem de Abordagem (WhatsApp)", "Texto para Anúncio Patrocinado (Meta Ads)"],
    horizontal=True
)

# --- LÓGICA DE GERAÇÃO ---
if st.button("🚀 Gerar Script de Vendas Magnético", type="primary"):
    if not localizacao or not diferenciais:
        st.warning("Por favor, preencha a localização e os diferenciais do imóvel.")
    else:
        with st.spinner("A IA está analisando o mercado e criando seu script..."):
            try:
                # BUSCA A CHAVE AUTOMATICAMENTE DOS SECRETS DE FORMA OCULTA E SEGURA
                api_key_segura = st.secrets["GEMINI_API_KEY"]
                
                # Inicializa o cliente oficial
                client = genai.Client(api_key=api_key_segura)
                
                # Engenharia de Prompt especializada
                prompt_base = f"""
                Você é um Copywriter de elite especializado no mercado imobiliário e gatilhos mentais de escassez e exclusividade.
                Gere um material focado no seguinte imóvel:
                - Tipo: {tipo_imovel}
                - Localização: {localizacao}
                - Preço/Condição: {preco}
                - Diferenciais: {diferenciais}
                
                Instruções específicas para o formato:
                """
                
                if tipo_script == "Roteiro de Vídeo (Reels/Instagram)":
                    prompt_final = prompt_base + "Crie um roteiro de vídeo dinâmico de até 60 segundos. Divida rigorosamente em colunas ou blocos de: [CENA/O QUE MOSTRAR] e [ÁUDIO/FALA DO CORRETOR]. Comece com um GANCHO FORTE de 3 segundos e termine com CTA para comentar."
                elif tipo_script == "Mensagem de Abordagem (WhatsApp)":
                    prompt_final = prompt_base + "Crie uma mensagem direta, profissional, altamente persuasiva para WhatsApp com emojis. Termine com uma pergunta aberta."
                else:
                    prompt_final = prompt_base + "Crie um texto de anúncio completo (Copy para legenda). Inclua Título, Corpo focado em estilo de vida e CTA 'Clique em Saiba Mais'."
                
                # Executa a chamada usando a geração estável atual
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt_final,
                )
                
                # Exibe o resultado de forma elegante
                st.success("🎉 Script gerado com sucesso!")
                st.markdown("---")
                
                texto_gerado = response.text
                st.markdown(texto_gerado)
                st.markdown("---")
                
                # Componente de cópia com um clique
                st.text_area("Texto pronto para cópia:", value=texto_gerado, height=150)
                st.toast("Script pronto para uso!", icon="📝")
                
            except Exception as e:
                st.error(f"Ocorreu um erro ao gerar o script: {e}")
