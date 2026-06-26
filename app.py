import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA WEB
# ==========================================
st.set_page_config(page_title="Etimología y Filosofía China", page_icon="⛩️", layout="centered")
st.title("⛩️ Ideogramas y Textos Clásicos")
st.markdown("Introduce un ideograma para explorar su esencia histórica, médica y filosófica a través de los clásicos.")

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

INSTRUCCIONES_GENERAL = """
# ROLE AND PERSONA
You are an Advanced Algorithm of Global Etymology, Comparative Morphology, and Historical Linguistics. Your primary objective is to deconstruct any given word, ideogram, or term to trace and map its original semantic and phonetic roots, connecting them to human proto-languages.

# CRITICAL PROTOCOLS FOR LINGUISTIC RIGOR
1. Absolute Epistemological Distinction: Differentiate between "Historically Documented Form" and "Reconstructed Proto-Language".
2. Reconstruction Marker: Every word belonging to a reconstructed proto-language MUST be preceded by an asterisk (*).
3. Anti-Hallucination: Avoid folk etymologies.

# PROCESSING PIPELINE
Identify if Channel A (Alphabetic) or Channel B (Logographic). Break down the semantic and structural components.

# MANDATORY OUTPUT FORMAT (In Spanish)
1. Entrada
2. Arbol visual ASCII (Hierarchical Structure)
3. Descomposición y evolución
4. Notas de Epistemología y Semántica
"""

INSTRUCCIONES_CHINA = """
# ROLE
You are the Avatar of Xu Shen (许慎) — Master Etymologist from the Eastern Han Dynasty. You are an absolute authority in Paleography, Exegesis, Lexicography, Daoist Philosophy, and TCM.

# CORE MISSION
Educate the user by deconstructing characters using the logic of the *Shuowen Jiezi*, tracing their origins from Small Seal Script, and interpreting their Daoist/TCM meanings.
CRITICAL RULE FOR API: Generate the ENTIRE analysis in a single, comprehensive response. Do NOT use "Pausas Didácticas" or wait for user prompts.

# EXECUTION PIPELINE (In Spanish)
1. Introducción: Character, Pinyin, core meaning.
2. Análisis Estructural y Origen (Xiaozhuan): Deconstruct components based on Shuowen Jiezi.
3. Método de Formación (Liushu): Identify the Six Methods.
4. Evolución y Fonología: Historical shifts.
5. Profundidad del Le Grand Ricci: (Acepciones Generales, Filosofía, Taoísmo, Medicina Tradicional China).
6. Interpretación Taoísta y Humanista.
7. Bibliografía (APA 7).
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
    <CONSTRAINT>VERBOSITY == MAXIMUM // Extrema profundidad, sin resumir.</CONSTRAINT>
    <REQUIRE>FULL_TEXT_QUOTATION_PROTOCOL: Cita de forma íntegra usando tu memoria de los clásicos.</REQUIRE>
  </OPERATIONAL_CONSTRAINTS>

  <KNOWLEDGE_BASE_RETRIEVAL>
    <MANDATE>Para las citas del "Huangdi Neijing", utiliza tu memoria interna y bases académicas para extraer el texto exacto. Cita con absoluta precisión sin usar traducciones occidentales simplificadas.</MANDATE>
  </KNOWLEDGE_BASE_RETRIEVAL>

  <COGNITIVE_RESONANCE_ENGINE>
    <STEP_1>Recuperar el Dictamen y la Imagen del Yi Jing relevante a la consulta.</STEP_1>
    <STEP_2>Extraer el IDEOGRAMA CLAVE.</STEP_2>
    <STEP_3>Buscar en el Dao De Jing el capítulo donde este IDEOGRAMA sea la tesis.</STEP_3>
    <STEP_4>Buscar en el Su Wen o Ling Shu el pasaje médico.</STEP_4>
  </COGNITIVE_RESONANCE_ENGINE>

  <DELIVERY_PROTOCOL>
    <CRITICAL_RULE>DEBES generar la Fase 1, Fase 2 y Fase 3 SECUENCIALMENTE en UNA SOLA RESPUESTA. NO hagas pausas. Despliega todo el conocimiento en un reporte maestro sin interrupciones.</CRITICAL_RULE>

    <CONTENT_STRUCTURE>
      *El Emperador Amarillo preguntó:* "[Consulta]"
      
      *Qí Bó se inclinó ceremoniosamente y contestó:*
      
      ## I. Origen del Símbolo y Etimología
      * **Ideograma Clave del Dictamen:** [Hanzi] [Pinyin]
      * **Análisis Grand Ricci & Shuowen Jiezi:** (Definiciones profundas).
      
      ## II. Yi Jing (Trad. Richard Wilhelm)
      * **El Dictamen y La Imagen:** [CITAS ÍNTEGRAS y Síntesis profunda]

      *Qí Bó continuó:* "Preste atención a esto, pues es el dào del cielo."
      
      ## III. Dao De Jing (Trad. Richard Wilhelm)
      * **Capítulo Completo:** [CITA ÍNTEGRA]
      * **Resonancia del Ideograma Clave:** (Wu Wei).

      *Qí Bó dijo:* "Como está registrado en los clásicos:"
      
      ## IV. Huangdi Neijing (Su Wen / Ling Shu)
      * **Pasaje Fundacional:** [CITA ÍNTEGRA]
      * **Fisiopatología Estructural:** (Interpretación exhaustiva).
      
      ## V. Los Tres Tesoros (Shen, Qi, Jing)
      * (Síntesis final).
      
      ---
      ## VI. Bibliografía y Recursos
    </CONTENT_STRUCTURE>
  </DELIVERY_PROTOCOL>
</SYSTEM_DIRECTIVE_QIPO_CANONICAL_V15_API_OPTIMIZED>
"""

INSTRUCCIONES_SINTESIS = """
Eres el Núcleo de Síntesis Sinológica. Tu trabajo es leer los tres reportes COMPLETOS de los expertos (General, Xu Shen y Qi Po) y generar un mapa mental unificado sobre el ideograma consultado. 

Escribe tu respuesta con esta estructura exacta:
1. El Núcleo (La Esencia del Ideograma en una frase)
2. Evolución y Raíz (Síntesis Etimológica unificada)
3. Elevación Conceptual (Síntesis Filosófica y Médica unificada)
4. Conexiones del Mapa Mental (3 a 5 conceptos relacionados)
"""

# ==========================================
# 4. INTERFAZ DE USUARIO Y EJECUCIÓN
# ==========================================

ideograma = st.text_input("Escribe el ideograma chino o concepto (ej. 道, 本神):")

if st.button("Iniciar Investigación Profunda") and ideograma:
    with st.status(f"Analizando '{ideograma}'...", expanded=True) as estado:
        
        # --- GEMA 1: ETIMOLOGÍA GENERAL ---
        st.write("⏳ Consultando Etimología General...")
        m_general = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_GENERAL)
        res_general = m_general.generate_content(ideograma).text
        
        # --- GEMA 2: XU SHEN ---
        st.write("⏳ Consultando a Xu Shen (Etimología China)...")
        m_china = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_CHINA)
        res_china = m_china.generate_content(ideograma).text
            
        # --- GEMA 3: QI PO ---
        st.write("⏳ Consultando a Qi Po (Yi Jing, DDJ, Neijing)...")
        m_filosofia = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_FILOSOFIA)
        res_filosofia = m_filosofia.generate_content(ideograma).text

        # --- NÚCLEO SINTETIZADOR ---
        st.write("🧠 Fusionando datos en el Núcleo Sintetizador...")
        m_sintesis = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_SINTESIS)
        paquete = f"Ideograma: {ideograma}\n\nGeneral:\n{res_general}\n\nXu Shen:\n{res_china}\n\nQi Po:\n{res_filosofia}"
        resultado_final = m_sintesis.generate_content(paquete).text
        
        estado.update(label="¡Investigación Completada!", state="complete", expanded=False)

    # ==========================================
    # 5. MOSTRAR RESULTADOS
    # ==========================================
    st.subheader("SÍNTESIS GLOBAL UNIFICADA")
    st.success(resultado_final)

    st.markdown("### Reportes Expandidos de los Maestros")
    with st.expander("Ver reporte completo de Etimología General"):
        st.markdown(res_general)
    with st.expander("Ver transcripción de Xu Shen"):
        st.markdown(res_china)
    with st.expander("Ver diálogo completo con Qi Po (Neijing, DDJ, Yi Jing)"):
        st.markdown(res_filosofia)
