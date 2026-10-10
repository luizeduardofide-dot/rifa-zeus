import streamlit as st
import urllib.parse
import json
import os
import time
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Rifa Equipe Zeus - Fórmula SAE",
    page_icon="🏎️",
    layout="centered"
)

# --- DESIGN CUSTOMIZADO (IDENTIDADE ZEUS & AJUSTE MOBILE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0c10; color: #ffffff; }
    
    /* Arredondar cantos das imagens para um look premium */
    img { border-radius: 15px; }
    
    /* --- CORREÇÃO DO LOGÓTIPO NO CELULAR --- */
    @media (max-width: 768px) {
        div[data-testid="column"]:first-child img {
            max-width: 90px !important;
            margin: 0 auto;
            display: block;
        }
    }
    
    /* --- ESTILOS PARA AS PROMOÇÕES --- */
    .promo-container { display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 25px; justify-content: center; }
    .promo-card { background: linear-gradient(145deg, #1f2833, #0b0c10); border: 1px solid #3b42f5; border-radius: 10px; padding: 15px; text-align: center; flex: 1 1 120px; box-shadow: 0 4px 8px rgba(59, 66, 245, 0.15); }
    .promo-card.destaque { border: 2px solid #ffcc00; box-shadow: 0 0 15px rgba(255, 204, 0, 0.4); transform: scale(1.05); }
    .promo-qtd { font-size: 1.1em; font-weight: bold; color: #ffffff; margin-bottom: 8px;}
    .promo-valor { font-size: 1.4em; font-weight: 900; color: #28a745; }
    .promo-tag { font-size: 0.75em; color: #0b0c10; background-color:#ffcc00; padding: 3px 8px; border-radius: 15px; font-weight: bold; margin-top: 10px; display: inline-block;}
    
    /* Customizar a barra de progresso */
    .stProgress > div > div > div { background-color: #28a745; }
    </style>
""", unsafe_allow_html=True)

# --- DADOS E CONFIGURAÇÕES DA RIFA ---
TOTAL_NUMEROS = 350
CHAVE_PIX = "rifaequipezeus@gmail.com"  
NOME_PIX = "Equipe Zeus"
WHATSAPP_CONTATO = "5535997699577"  
ARQUIVO_BANCO = "banco_rifa.json" 

# --- SISTEMA DE SALVAMENTO ---
def carregar_dados():
    if os.path.exists(ARQUIVO_BANCO):
        with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            numeros = {int(k): v for k, v in dados.get("numeros_status", {}).items()}
            compradores = {int(k): v for k, v in dados.get("compradores", {}).items()}
            return numeros, compradores
    else:
        return {i: "Disponível" for i in range(1, TOTAL_NUMEROS + 1)}, {}

def salvar_dados():
    dados = {
        "numeros_status": st.session_state.numeros_status,
        "compradores": st.session_state.compradores
    }
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# --- INICIALIZAÇÃO DE VARIÁVEIS ---
numeros_salvos, compradores_salvos = carregar_dados()

if "numeros_status" not in st.session_state:
    st.session_state.numeros_status = numeros_salvos
if "compradores" not in st.session_state:
    st.session_state.compradores = compradores_salvos
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []
if "reserva_concluida" not in st.session_state:
    st.session_state.reserva_concluida = False
if "dados_reserva" not in st.session_state:
    st.session_state.dados_reserva = {}

def calcular_total(qtd):
    total = 0
    while qtd >= 10:
        total += 25.0
        qtd -= 10
    while qtd >= 8:
        total += 22.0
        qtd -= 8
    while qtd >= 4:
        total += 10.0
        qtd -= 4
    total += qtd * 3.0
    return total

# --- CABEÇALHO: LOGO E TÍTULO ALINHADOS ---
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    if os.path.exists("fotologo.jpeg"):
        st.image("fotologo.jpeg", use_container_width=True)

with col_titulo:
    st.markdown("<h1 style='margin-top: -15px;'>Rifa - Equipe Zeus</h1>", unsafe_allow_html=True)
    st.markdown("Acelerando sonhos com o Fórmula SAE UFLA!")

st.markdown("---")

# --- BANNER CENTRAL: CORTE AUTOMÁTICO DO CARRO ---
if os.path.exists("fotocarro.jpeg"):
    img_original = Image.open("fotocarro.jpeg")
    w, h = img_original.size
    nova_altura = int(w * 0.45)
    topo = (h - nova_altura) // 2
    fundo = topo + nova_altura
    img_cortada = img_original.crop((0, topo, w, fundo))
    st.image(img_cortada, use_container_width=True)

# --- BARRA DE PROGRESSO DE VENDAS ---
numeros_indisponiveis = sum(1 for status in st.session_state.numeros_status.values() if status != "Disponível")
porcentagem_vendida = numeros_indisponiveis / TOTAL_NUMEROS

st.write("")
st.markdown(f"### 🔥 Já vendemos **{numeros_indisponiveis}** de **{TOTAL_NUMEROS}** números!")
st.progress(porcentagem_vendida)
st.markdown("---")

# --- PROJETO E PRÉMIOS (RESUMO) ---
col_proj, col_premio = st.columns(2)

with col_proj:
    st.subheader("🏁 O Projeto")
    st.write("Nós projetamos e construímos um carro de corrida do zero para competir! Sua contribuição é o combustível para cobrir os custos de manufatura e colocar o nosso projeto na pista.")

with col_premio:
    st.subheader("🏆 Sorteio: 18/12")
    st.write("Confira as fotos detalhadas dos prêmios na aba **'Ver Prêmios'** logo abaixo!")

st.write("") 

# --- SISTEMA DE ABAS (TABS) ---
aba_comprar, aba_premios = st.tabs(["🎟️ Comprar Números", "🏆 Ver Prêmios"])

# --- CONTEÚDO DA ABA 1: COMPRAR NÚMEROS ---
with aba_comprar:
    st.header("💰 Combos Promocionais")
    st.write("Escolha seus números na grade abaixo. O sistema calcula o **melhor desconto automaticamente**!")

    st.markdown("""
    <div class="promo-container">
        <div class="promo-card">
            <div class="promo-qtd">🎟️ 1 Número</div>
            <div class="promo-valor">R$ 3,00</div>
        </div>
        <div class="promo-card">
            <div class="promo-qtd">🎟️ 3 Números</div>
            <div class="promo-valor">R$ 9,00</div>
        </div>
        <div class="promo-card destaque">
            <div class="promo-qtd">🔥 4 Números</div>
            <div class="promo-valor">R$ 10,00</div>
            <div class="promo-tag">MAIS VENDIDO</div>
        </div>
        <div class="promo-card">
            <div class="promo-qtd">⚡ 8 Números</div>
            <div class="promo-valor">R$ 22,00</div>
        </div>
        <div class="promo-card destaque">
            <div class="promo-qtd">🚀 10 Números</div>
            <div class="promo-valor">R$ 25,00</div>
            <div class="promo-tag">PACOTÃO ZEUS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- SELEÇÃO DE NÚMEROS OTIMIZADA COM CHECKBOXES ---
    st.subheader("👇 Selecione os números que deseja comprar:")
    st.markdown("* 🟦 **Disponíveis** | 🟩 **No Carrinho** | 🟡 **Reservados** | 🔴 **Pagos**")

    with st.form(key="form_selecao_rifa"):
        # Criação da grade adaptável em colunas nativas sem lentidão excessiva
        cols_por_linha = 5 # 5 colunas funciona perfeitamente bem tanto em PC quanto em Telemóvel
        for i in range(0, TOTAL_NUMEROS, cols_por_linha):
            cols = st.columns(cols_por_linha)
            for j in range(cols_por_linha):
                num = i + j + 1
                if num <= TOTAL_NUMEROS:
                    status = st.session_state.numeros_status[num]
                    
                    if status == "Disponível":
                        # Mantém estado no carrinho
                        ja_selecionado = num in st.session_state.carrinho
                        selecionado = cols[j].checkbox(f"Nº {num}", value=ja_selecionado, key=f"chk_{num}")
                        
                        if selecionado and num not in st.session_state.carrinho:
                            st.session_state.carrinho.append(num)
                        elif not selecionado and num in st.session_state.carrinho:
                            st.session_state.carrinho.remove(num)
                            
                    elif status == "Reservado":
                        cols[j].markdown(f"<div style='text-align:center; padding:8px; background-color:#856404; color:white; border-radius:5px; font-size:0.85em;'>Nº {num}<br><b>Reservado</b></div>", unsafe_allow_html=True)
                    else:
                        cols[j].markdown(f"<div style='text-align:center; padding:8px; background-color:#721c24; color:white; border-radius:5px; font-size:0.85em;'>Nº {num}<br><b>Pago</b></div>", unsafe_allow_html=True)

        st.write("")
        botao_atualizar = st.form_submit_button("🛒 Avançar com os Números Selecionados", use_container_width=True)

    st.markdown("---")

    # --- CHECKOUT E PAGAMENTO ---
    if st.session_state.reserva_concluida:
        dados = st.session_state.dados_reserva
        st.success(f"🎉 Reserva confirmada para {dados['nome']}!")
        st.subheader("💳 Falta pouco! Faça o PIX para garantir os números.")
        st.info(f"**Total a pagar: R$ {dados['valor_total']:.2f}** pelos números: {dados['numeros_str']}")
        
        st.write(f"**Favorecido:** {NOME_PIX}")
        st.write("**Copie a Chave PIX (E-mail) abaixo:**")
        st.code(CHAVE_PIX, language="text")
        
        msg = f"Olá! Me chamo {dados['nome']}. Reservei os números [{dados['numeros_str']}] na Rifa da Equipe Zeus. Segue o comprovante do PIX no valor de R$ {dados['valor_total']:.2f}:"
        msg_encoded = urllib.parse.quote(msg)
        link_wpp = f"https://wa.me/{WHATSAPP_CONTATO}?text={msg_encoded}"
        
        st.markdown(f"### 👉 **[CLIQUE AQUI PARA ENVIAR O COMPROVANTE NO WHATSAPP]({link_wpp})**", unsafe_allow_html=True)
        if st.button("Fazer nova compra"):
            st.session_state.reserva_concluida = False
            st.session_state.dados_reserva = {}
            st.rerun()

    elif len(st.session_state.carrinho) > 0:
        qtd_selecionada = len(st.session_state.carrinho)
        valor_final = calcular_total(qtd_selecionada)
        
        st.header("🛒 Fechar Pedido")
        st.write(f"Você selecionou **{qtd_selecionada}** número(s): {sorted(st.session_state.carrinho)}")
        st.info(f"💰 **Valor Total com Desconto: R$ {valor_final:.2f}**")
        
        col_nome, col_tel = st.columns(2)
        nome_comprador = col_nome.text_input("Seu Nome e Sobrenome:")
        tel_comprador = col_tel.text_input("Seu WhatsApp (com DDD):")
        
        if st.button("Confirmar Reserva e Gerar PIX", type="primary", use_container_width=True):
            if not nome_comprador or not tel_comprador:
                st.error("Por favor, preencha seu nome e WhatsApp para continuar.")
            else:
                numeros_atualizados, _ = carregar_dados()
                conflito = [n for n in st.session_state.carrinho if numeros_atualizados[n] != "Disponível"]
                
                if conflito:
                    st.error(f"⚠️ Eita! Alguém foi mais rápido e acabou de reservar os números: {conflito}. Por favor, desmarque eles e escolha outros!")
                    st.session_state.numeros_status = numeros_atualizados
                else:
                    for n in st.session_state.carrinho:
                        st.session_state.numeros_status[n] = "Reservado"
                        st.session_state.compradores[n] = nome_comprador
                    
                    salvar_dados()
                    
                    st.session_state.dados_reserva = {
                        "nome": nome_comprador, "telefone": tel_comprador,
                        "valor_total": valor_final, "numeros_str": ", ".join(map(str, sorted(st.session_state.carrinho)))
                    }
                    st.session_state.carrinho = []
                    st.session_state.reserva_concluida = True
                    st.rerun()

# --- CONTEÚDO DA ABA 2: VER PRÊMIOS ---
with aba_premios:
    st.header("🎁 Conheça os nossos Prêmios!")
    st.write("Ao participar na nossa rifa, além de ajudares o projeto, concorres a estes super prêmios:")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.subheader("🥇 1º LUGAR")
        st.markdown("**Televisão 43\"**")
        if os.path.exists("premio1.jpeg"):
            st.image("premio1.jpeg", use_container_width=True)
        else:
            st.info("Imagem da TV em breve!")
            
    with col_p2:
        st.subheader("🥈 2º LUGAR")
        st.markdown("**Airfryer + Kit Parafusadeira**")
        if os.path.exists("premio2.jpeg"):
            st.image("premio2.jpeg", use_container_width=True)
        else:
            st.info("Imagem da Airfryer em breve!")
            
    with col_p3:
        st.subheader("🥉 3º LUGAR")
        st.markdown("**Cesta de Queijos**")
        if os.path.exists("premio3.jpeg"):
            st.image("premio3.jpeg", use_container_width=True)
        else:
            st.info("Imagem da Cesta em breve!")


# --- PAINEL DO ADMINISTRADOR ---
st.markdown("---")
with st.expander("🔐 Área do Administrador"):
    senha_admin = st.text_input("Senha Admin", type="password")
    if senha_admin == "zeus0709":
        st.write("Gerenciar status dos números:")
        num_admin = st.number_input("Digite o Número que deseja gerenciar:", min_value=1, max_value=TOTAL_NUMEROS, step=1)
        
        col_pago, col_cancela = st.columns(2)
        with col_pago:
            if st.button("✅ Marcar como Pago", type="primary", use_container_width=True):
                st.session_state.numeros_status[num_admin] = "Pago"
                salvar_dados()
                st.success(f"Sucesso! Número {num_admin} confirmado como PAGO.")
                time.sleep(1.5)
                st.rerun()
                
        with col_cancela:
            if st.button("❌ Cancelar Reserva", use_container_width=True):
                st.session_state.numeros_status[num_admin] = "Disponível"
                if num_admin in st.session_state.compradores:
                    del st.session_state.compradores[num_admin]
                salvar_dados()
                st.success(f"Reserva cancelada! Número {num_admin} liberado para venda novamente.")
                time.sleep(1.5)
                st.rerun()