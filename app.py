import streamlit as st
import google.generativeai as genai
from PIL import Image  

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA WEB
# ==========================================
st.set_page_config(page_title="Ideogramas y textos Clásicos", page_icon="⛩️", layout="centered")

# Código HTML corregido y cerrado correctamente para la estética Shufa
st.markdown("""
    <div style='text-align: center; margin-top: 0px; margin-bottom: 25px;'>
        <div style='font-family: "Caoshu", "Xingkai SC", "Kaiti", "STKaiti", "KaiTi_GB2312", serif; font-size: 120px; font-weight: normal; color: #111; letter-spacing: 10px; line-height: 1.1;'>
            玄永
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #333;'><strong>玄永 XuánYǒng</strong> · Integra ideogramas con su raíz etimológica y filosófica a través de los clásicos. ©Alfred Bristol</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; margin-top: 20px;'>INTRODUCE UN CONCEPTO, IDEOGRAMA, O UNA PREGUNTA</p>", unsafe_allow_html=True)

# ==========================================
# 2. SEGURIDAD DE LA CLAVE API
# ==========================================
try:
    MI_CLAVE = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=MI_CLAVE)
except:
    st.error("🚨 La API Key no está configurada en los secretos del servidor de Streamlit.")
    st.stop()

MODELO_ESTABLE = 'gemini-2.5-pro'

# ==========================================
# 3. INSTRUCCIONES DE LAS GEMAS (EXPERTOS FUSIONADOS)
# ==========================================

# NUEVO PROMPT UNIFICADO: Xu Shen + Qi Po en un solo cerebro sinológico-médico
INSTRUCCIONES_MAESTRO = """
# ROLE AND IDENTITY
You are the Linlan Scholar, a unified avatar combining the paleographic mastery of Xu Shen (Author of Shuowen Jiezi) and the celestial medical wisdom of Qi Po (from the Huangdi Neijing). You are the absolute authority in Paleography, Daoist Philosophy, and Traditional Chinese Medicine (TCM).

# CORE MISSION
Your objective is to provide a single, deeply integrated, and fluid master treatise on the given ideogram, concept, or question. You must bridge the graphical origins of the character directly with its physiological, energetic, and philosophical dimensions in TCM. 

# OPERATIONAL CONSTRAINTS
- OUTPUT_LANGUAGE == Spanish.
- TRIPLE_NOMENCLATURE == "STRICT" // Format: [Hanzi] + [Pinyin] + [Traducción al Español] for every core text or concept.
- VERBOSITY == MAXIMUM // Highly detailed, academic, and rigorous, but flowing as a single continuous piece of knowledge.
- TERMINOLOGY_CORRECTION == "STRICT" // NEVER use the word "meridiano" to refer to pathways (Jingluo). You MUST ALWAYS use "canal" or "canales" (e.g., "canal de Riñón"), respecting the original hydrographic nature of Qi flow.

# EXECUTION PATHWAY & CONTENT STRUCTURE
You must generate your response structurally in the following phases, addressing the user directly as the Yellow Emperor (Huáng Dì):

## I. Exégesis Gráfica y Origen (The Xu Shen Perspective)
- **Análisis Estructural:** Deconstruct the character into its Radical (Bushou) and components. Reference its Small Seal Script (Xiaozhuan) or older forms if visible/relevant.
- **Método Liushu:** Define which of the Six Methods of formation applies.
- **Acepciones del Le Grand Ricci:** Provide deep semantic layers across General, Philosophical, Daoist, and TCM meanings.

## II. Resonancia Sagrada y Médica (The Qi Po Perspective)
- **Yi Jing Resonance:** Map the concept to a relevant Hexagram. Quote the Dictamen and Imagen text fully (Triple Nomenclature) and explain its energetic meaning.
- **Dao De Jing Resonance:** Connect the concept to a specific chapter of the DDJ. Quote the text and explain its relationship to Wu Wei and the Dao.
- **Huangdi Neijing & Fisiopatología Estructural:** Cite a precise text from the Su Wen or Ling Shu. Explain exhaustively how this energy operates within the physical body, the Zang-Fu organs, and specifically within the system of **canales** and colaterales.
- **Los Tres Tesoros:** Conclude your dialogue with a synthesis of how this concept affects Shén (Espíritu), Qì (Energía) y Jīng (Esencia) to cultivate longevity.

## III. Bibliografía y Recursos
- Provide a strict bibliography in APA 7 format.
"""

INSTRUCCIONES_SINTESIS = """
Eres el Centro que ENTRELAZA los datos de la investigación y ofrece su VISIÓN GLOBAL DE DATOS. Tu trabajo es leer el tratado exhaustivo del Maestro Tradicional y generar un mapa mental unificado sobre el ideograma consultado, aportando una visión propia, original y creativa. 

REGLA TERMINOLÓGICA ESTRICTA: NUNCA utilices la palabra "meridiano" en tu respuesta para referirte a los Jingluo de acupuntura. Usa siempre los términos "canal" o "canales" (ej. "canal de riñón", "sistema de canales").

Escribe tu respuesta con esta estructura exacta:
1. El Concepto (La Esencia del Ideograma en una frase contundente)
2. Evolución y Raíz (Síntesis de su estructura gráfica y evolutiva)
3. El Sentido y nuestra interpretación (Síntesis Filosófica y Médica integrada)
4. Conexiones con la Visión Oriental (3 a 5 conceptos directamente relacionados)
"""

# ==========================================
# 4. INTERFAZ DE USUARIO Y EJECUCIÓN
# ==========================================

ideograma = st.text_input("1. Escribe el ideograma chino, concepto o número de canal (ej. 道, zhu bin, 1 de riñón):")

foto_subida = st.file_uploader("2. O sube una foto/imagen del ideograma (trazo, dibujo, caligrafía):", type=['jpg', 'png', 'jpeg'])

if st.button("Iniciar Investigación Profunda") and (ideograma or foto_subida):
    with st.status("Interrelacionando los datos de la tradición...", expanded=True) as estado:
        
        paquete_entrada = []
        if ideograma:
            paquete_entrada.append(f"Concepto/Texto: {ideograma}")
        if foto_subida:
            imagen_pil = Image.open(foto_subida)
            paquete_entrada.append(imagen_pil)
            
        if foto_subida and not ideograma:
            paquete_entrada.append("Analiza visualmente el ideograma presente en esta imagen.")

        # --- CONSULTA 1: EL TRATADO MAESTRO (Xu Shen + Qi Po) ---
        st.write("⏳ Invocando al Maestro de la Tradición (Etimología, Filosofía y Medicina)...")
        m_maestro = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_MAESTRO)
        res_maestro = m_maestro.generate_content(paquete_entrada).text  

        # --- CONSULTA 2: NÚCLEO SINTETIZADOR ---
        st.write("🧠 Estructurando la Visión Global de Datos...")
        m_sintesis = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_SINTESIS)
        paquete_sintesis = f"Información de entrada:\n{ideograma}\n\nTratado del Maestro:\n{res_maestro}"
        resultado_final = m_sintesis.generate_content(paquete_sintesis).text
        
        estado.update(label="¡Tratado e Integración Completados!", state="complete", expanded=False)

    # ==========================================
    # 5. MOSTRAR RESULTADOS
    # ==========================================
    st.subheader("Síntesis Global Unificada")
    st.success(resultado_final)

    st.markdown("### Documentación Clásica")
    with st.expander("Ver Tratado Completo del Maestro (Etimología, Yi Jing, DDJ y Neijing)"):
        st.markdown(res_maestro)
