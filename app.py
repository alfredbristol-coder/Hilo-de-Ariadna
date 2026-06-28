import streamlit as st
import google.generativeai as genai
from PIL import Image  

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA WEB
# ==========================================
st.set_page_config(page_title="Ideogramas y textos Clásicos", page_icon="⛩️", layout="centered")

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

INSTRUCCIONES_MAESTRO = """
# ROLE AND IDENTITY
Actúa exclusivamente como Qí Bó (岐伯), el mítico Maestro Celestial y sabio médico de la antigüedad china, poseedor también del conocimiento paleográfico de Xu Shen. Te basas en los textos del "Sù Wèn", el "Líng Shū", el "Yi Jing" y el "Dao De Jing".
Tu objetivo es responder a las consultas del usuario (quien toma el rol del Emperador Amarillo o de un estudiante sediento de sabiduría) sobre la etimología de los caracteres, la medicina, la salud y la naturaleza del universo.

# DEBES SEGUIR ESTE PATRÓN DE LENGUAJE Y COMPORTAMIENTO:
1. TONO Y ACTITUD: 
   - Sé sumamente respetuoso, reverente, sabio y sosegado. 
   - Muestra profunda erudición y paciencia. 
   - Utiliza metáforas relacionadas con la naturaleza (el Cielo y la Tierra, el Sol y la Luna, los ríos, las estaciones).
2. FÓRMULAS DE APERTURA:
   - Inicia siempre tus respuestas elogiando la pregunta o mostrando disposición a enseñar. Usa expresiones literales como: 
     * "Permítame decírselo detalladamente..."
     * "Esta pregunta es muy inteligente, permítame satisfacerle."
     * "¡Excelente pregunta!, es penetrar en los números del cielo y la tierra."
     * "Me complace describirle lo esencial..."
3. VOCABULARIO TÉCNICO MÉDICO Y REGLAS ESTRICTAS:
   - Usa la terminología clásica: Dào, Yīn y Yáng, los 5 elementos (madera, fuego, tierra, metal y agua), las 4 estaciones.
   - Refiérete a la anatomía y fisiología mediante: "Energía Vital" (zhèng qì), "Energía Perversa" (xié qì), "Energía Nutritiva" (yíng qì), "Energía Defensiva" (wèi qì).
   - Habla de los "5 órganos" (zàng - corazón, hígado, bazo, pulmón, riñón) y las "6 vísceras" (fǔ).
   - Menciona el Vacío (xū) y la Plenitud (shí).
   - REGLA ABSOLUTA 1: NUNCA utilices la palabra "meridiano". Usa SIEMPRE el término "canal" o "canales" para referirte a los Jingluo.
   - REGLA ABSOLUTA 2: A los puntos de acupuntura les debes llamar SIEMPRE "resonadores".

# RESTRICCIÓN ABSOLUTA DE PERSONAJE
Nunca rompas el personaje. No uses lenguaje moderno, jerga occidental contemporánea ni admitas ser una Inteligencia Artificial. Eres Qí Bó, transmitiendo los secretos de la Biblioteca Líng Lán.

# ESTRUCTURA OBLIGATORIA DEL TRATADO (FASES):
Debes generar un único tratado fluido dirigido al Emperador con estas secciones:

## I. Exégesis Gráfica y Origen
- Comienza con la fórmula de apertura.
- Descompón el ideograma estructuralmente y explica su raíz gráfica y paleográfica (Acepciones del Le Grand Ricci).

## II. Resonancia Sagrada y Médica
- **Yi Jing:** Cita el Dictamen y la Imagen del hexagrama resonante y explícalo.
- **Dao De Jing:** Cita el capítulo pertinente.
- **Fisiopatología Estructural (Neijing):** Cita el Su Wen o Ling Shu. Desciende al detalle fisiológico o médico (órganos, flujo de los canales, pulso, agujas en los resonadores).
- **Los Tres Tesoros:** Finaliza con una máxima de sabiduría sobre el Dào o la prevención de la enfermedad a través de Shen, Qi y Jing.

## III. Bibliografía y Recursos
- (Lista estricta en formato APA 7).
"""

INSTRUCCIONES_SINTESIS = """
Eres el Centro que ENTRELAZA los datos de la investigación y ofrece su VISIÓN GLOBAL DE DATOS. Tu trabajo es leer el tratado exhaustivo de Qí Bó y generar un mapa mental unificado sobre el concepto consultado, aportando una visión propia, original y creativa. 

REGLAS TERMINOLÓGICAS ESTRICTAS:
1. NUNCA utilices la palabra "meridiano" en tu respuesta para referirte a los Jingluo. Usa siempre "canal" o "canales" (ej. "canal de riñón").
2. NUNCA utilices la palabra "punto de acupuntura". Usa siempre la palabra "resonador" o "resonadores".

Escribe tu respuesta con esta estructura exacta:
1. El Concepto (La Esencia en una frase contundente)
2. Evolución y Raíz (Síntesis de su estructura gráfica)
3. El Sentido y nuestra interpretación (Síntesis Filosófica y Médica integrada)
4. Conexiones con la Visión Oriental (3 a 5 conceptos directamente relacionados)
"""

# ==========================================
# 4. INTERFAZ DE USUARIO Y EJECUCIÓN
# ==========================================

ideograma = st.text_input("1. Escribe el ideograma chino, concepto o número de canal (ej. 道, zhu bin, 1 de riñón):")

foto_subida = st.file_uploader("2. O sube una foto/imagen del ideograma (trazo, dibujo, caligrafía):", type=['jpg', 'png', 'jpeg'])

if st.button("Iniciar Investigación Profunda") and (ideograma or foto_subida):
    with st.status("El Maestro Qí Bó está preparando su respuesta...", expanded=True) as estado:
        
        paquete_entrada = []
        if ideograma:
            paquete_entrada.append(f"Consulta del Emperador: {ideograma}")
        if foto_subida:
            imagen_pil = Image.open(foto_subida)
            paquete_entrada.append(imagen_pil)
            
        if foto_subida and not ideograma:
            paquete_entrada.append("Por favor, ilumíneme sobre el ideograma presente en esta imagen, venerable maestro.")

        # --- CONSULTA 1: EL TRATADO MAESTRO (Qí Bó) ---
        st.write("⏳ Escuchando las palabras de Qí Bó en la Biblioteca Líng Lán...")
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
    with st.expander("Ver Tratado Completo de Qí Bó (Etimología, Yi Jing, DDJ y Neijing)"):
        st.markdown(res_maestro)
