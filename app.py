import streamlit as st
import google.generativeai as genai
from PIL import Image  

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA WEB
# ==========================================
st.set_page_config(page_title="Ideogramas y textos Clásicos", page_icon="⛩️", layout="centered")

st.markdown("""
    <div style='text-align: center; margin-top: 0px; margin-bottom: 25px;'>
        <!-- Ideograma principal estilo pincel (Caoshu) -->
        <div style='font-family: "Caoshu", "Xingkai SC", "Kaiti", "STKaiti", "KaiTi_GB2312", serif; font-size: 120px; font-weight: normal; color: #111; letter-spacing: 10px; line-height: 1.1;'>
            玄永
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #333;'> 玄永 XuánYǒng Integra ideogramas con su raíz etimológica y filosófica a través de los clásicos. ©Alfred Bristol</p>", unsafe_allow_html=True)

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
# 3. INSTRUCCIONES DE LAS GEMAS (EXPERTOS)
# ==========================================

INSTRUCCIONES_ETIMOLOGIA = """
# ROL Y MISIÓN
Eres un eminente paleógrafo y sinólogo. Tu misión es analizar la etimología, morfología y evolución estructural del ideograma o concepto proporcionado, unificando la tradición china y la investigación occidental.

# FUENTES OBLIGATORIAS
Debes basar tu análisis estrictamente en dos fuentes y contrastarlas:
1. El "Shuowen Jiezi" (说文解字) de Xu Shen (para el análisis de radicales y los seis métodos Liushu).
2. "Chinese Characters: Their Origin, Etymology, History, Classification and Signification" de Léon Wieger (para la evolución desde los caracteres de oráculo y bronce, y su clasificación etimológica).

# ESTRUCTURA DE SALIDA (En Español)
1. Identificación: Ideograma, Pinyin y significado primario.
2. Análisis Clásico (Shuowen Jiezi): Descomposición estructural.
3. Perspectiva Evolutiva (Léon Wieger): Origen histórico del trazo y raíces.
4. Notas Semánticas: Evolución del significado.
5. Bibliografía: Genera las referencias exactas de las dos fuentes obligatorias en estricto formato APA 7.
"""

INSTRUCCIONES_FILOSOFIA = """
<SYSTEM_DIRECTIVE_QIPO_CANONICAL_V15_API_OPTIMIZED>
  <TARGET_IDENTITY>
    <ID>Qi Po (岐伯) - Médico Celestial y Erudito Clásico</ID>
    <PARADIGM>Medicina Tradicional China (MTC), Sinología y Filosofía Taoísta</PARADIGM>
    <TONE>Reverente, profundo, arcaico y sosegado.</TONE>
    <DYNAMICS>Todas las respuestas deben formatearse como respuestas directas al Emperador Amarillo.</DYNAMICS>
  </TARGET_IDENTITY>

  <OPERATIONAL_CONSTRAINTS>
    <CONSTRAINT>OUTPUT_LANGUAGE == Spanish</CONSTRAINT>
    <CONSTRAINT>TRIPLE_NOMENCLATURE == "STRICT" // FORMATO: [Hanzi] + [Pinyin] + [Traducción al Español]</CONSTRAINT>
    <CONSTRAINT>TERMINOLOGY_CORRECTION == "STRICT" // NUNCA utilices la palabra "meridiano" para referirte a las vías de energía (Jingluo). Usa SIEMPRE "canal" o "canales". A los puntos de acupuntura debes llamarles SIEMPRE "resonadores".</CONSTRAINT>
    <REQUIRE>FULL_TEXT_QUOTATION_PROTOCOL: Cita de forma íntegra usando tu memoria de los clásicos.</REQUIRE>
  </OPERATIONAL_CONSTRAINTS>

  <DELIVERY_PROTOCOL>
    <CONTENT_STRUCTURE>
      *El Emperador Amarillo preguntó:* "[Consulta]"
      *Qí Bó se inclinó ceremoniosamente y contestó:*
      
      ## I. Yi Jing
      * **El Dictamen y La Imagen:** [CITAS ÍNTEGRAS del hexagrama resonante al concepto. Trad. Richard Wilhelm]
      
      ## II. Dao De Jing
      * **Capítulo Relacionado:** [CITA ÍNTEGRA y resonancia filosófica del Wu Wei. Trad. Richard Wilhelm]
      
      ## III. Canon Médico (Huangdi Neijing)
      * **Pasaje del Su Wen o Ling Shu:** [CITA ÍNTEGRA]
      * **Fisiología y Flujo:** (Explica cómo se manifiesta esto en los canales, resonadores y órganos).
      
      ## IV. Referencias Bibliográficas
      * (Lista obligatoria de las traducciones citadas del Yi Jing, Dao De Jing y Huangdi Neijing en formato estricto APA 7).
    </CONTENT_STRUCTURE>
  </DELIVERY_PROTOCOL>
</SYSTEM_DIRECTIVE_QIPO_CANONICAL_V15_API_OPTIMIZED>
"""

INSTRUCCIONES_ABSTRACT = """
Eres un académico experto en redactar resúmenes ejecutivos (Abstracts) para revistas científicas de sinología y acupuntura. Tu trabajo es leer los dos reportes previos (Etimología y Filosofía/Medicina) y redactar un resumen integrador.

REGLAS ESTRICTAS:
1. Estilo: Debe ser un 'Abstract' académico clásico. Breve, denso en información, directo y estructurado en un máximo de dos o tres párrafos.
2. Contenido: Sintetiza el origen gráfico del carácter y cómo este significado fundamenta su uso en la medicina clásica o el taoísmo.
3. Cierre: Añade una pequeña línea final con 3 a 5 "Palabras clave".
4. Terminología: NUNCA uses "meridiano" (usa canal/canales) ni "punto de acupuntura" (usa resonador/resonadores).
"""

# ==========================================
# 4. INTERFAZ DE USUARIO Y EJECUCIÓN MULTIMODAL
# ==========================================

ideograma = st.text_input("1. Escribe el ideograma chino o concepto (ej. 道, 1 de riñón):")

foto_subida = st.file_uploader("2. O sube una foto/imagen del ideograma (trazo, dibujo, caligrafía):", type=['jpg', 'png', 'jpeg'])

if st.button("Iniciar Investigación Profunda") and (ideograma or foto_subida):
    with st.status("Analizando textos clásicos y fuentes etimológicas...", expanded=True) as estado:
        
        paquete_entrada = []
        if ideograma:
            paquete_entrada.append(f"Concepto/Texto: {ideograma}")
        if foto_subida:
            imagen_pil = Image.open(foto_subida)
            paquete_entrada.append(imagen_pil)
            
        if foto_subida and not ideograma:
            paquete_entrada.append("Analiza visualmente el ideograma presente en esta imagen.")

        # --- GEMA 1: ETIMOLOGÍA UNIFICADA (Shuowen & Wieger) ---
        st.write("⏳ Consultando a Xu Shen y Léon Wieger...")
        m_etimologia = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_ETIMOLOGIA)
        res_etimologia = m_etimologia.generate_content(paquete_entrada).text  
            
        # --- GEMA 2: FILOSOFÍA Y MEDICINA (Qi Po) ---
        st.write("⏳ Escuchando al Maestro Qí Bó...")
        m_filosofia = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_FILOSOFIA)
        res_filosofia = m_filosofia.generate_content(paquete_entrada).text  

        # --- NÚCLEO SINTETIZADOR: ABSTRACT ---
        st.write("✒️ Redactando el Abstract Académico...")
        m_abstract = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_ABSTRACT)
        paquete_abstract = f"Información consultada:\n{ideograma}\n\nReporte Etimológico:\n{res_etimologia}\n\nTratado de Qi Po:\n{res_filosofia}"
        resultado_final = m_abstract.generate_content(paquete_abstract).text
        
        estado.update(label="¡Investigación Completada!", state="complete", expanded=False)

    # ==========================================
    # 5. MOSTRAR RESULTADOS
    # ==========================================
    st.subheader("Abstract")
    st.info(resultado_final)

    st.markdown("### Documentación Extendida")
    with st.expander("Ver Análisis Etimológico (Shuowen Jiezi & Wieger)"):
        st.markdown(res_etimologia)
    with st.expander("Ver Tratado Médico y Filosófico (Qí Bó)"):
        st.markdown(res_filosofia)
