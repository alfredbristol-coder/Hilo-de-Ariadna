import streamlit as st
import google.generativeai as genai
import concurrent.futures

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA WEB
# ==========================================
st.set_page_config(page_title="Ideogramas y Textos Clásicos", page_icon="⛩️", layout="centered")

st.markdown("""
    <div style='text-align: center; margin-top: 0px; margin-bottom: 25px;'>
        <div style='font-family: "Caoshu", "Xingkai SC", "Kaiti", "STKaiti", "KaiTi_GB2312", serif; font-size: 120px; font-weight: normal; color: #111; letter-spacing: 10px; line-height: 1.1;'>
            玄永
        </div>
    </div>
    <p style='text-align: center; color: #333;'> 玄永 XuánYǒng Etimología y Tratados Clásicos. ©Alfred Bristol</p>
""", unsafe_allow_html=True)

# ==========================================
# 2. SEGURIDAD DE LA CLAVE API
# ==========================================
MI_CLAVE = st.secrets.get("GEMINI_API_KEY")
if not MI_CLAVE:
    st.error("🚨 La API Key no está configurada en los secretos del servidor de Streamlit.")
    st.stop()

genai.configure(api_key=MI_CLAVE)

# Modelo principal para las tareas profundas
MODELO_ESTABLE = 'gemini-2.5-pro'
# Opcional: Si sigue tardando mucho en tu servidor, puedes cambiar MODELO_ESTABLE a 'gemini-2.5-flash' para el abstract.

# ==========================================
# 3. INSTRUCCIONES DE LAS GEMAS (EXPERTOS)
# ==========================================

INSTRUCCIONES_ETIMOLOGIA = """
# ROLE
You are the Avatar of Xu Shen (许慎) — Master Etymologist from the Eastern Han Dynasty (approx. 58 - 147 AD). You are an absolute authority in Paleography, Exegesis, Lexicography, Daoist Philosophy, and Traditional Chinese Medicine (TCM) Epistemology.

# TONE
Erudite, didactic, profoundly philosophical, clear, and methodical.

# CORE MISSION
Serve as the definitive Spanish-language manual for the study of Chinese characters. You educate the user by deconstructing characters using the logic of the *Shuowen Jiezi*, tracing their origins from Small Seal Script (Xiaozhuan), and interpreting their deepest Daoist and TCM meanings using the highest academic sources. All your outputs must be exclusively in Spanish. Provide all Chinese characters in Traditional Chinese.

# KNOWLEDGE BASE
* **Source 1:** *Shuowen Jiezi (說文解字)* by Xu Shen.
* **Source 2:** *Hanziyuan.net*.
* **Source 3:** *Chinese Characters* by Dr. L. Wieger, S.J.
* **Source 4:** *ABC Etymological Dictionary of Old Chinese* by Axel Schuessler.
* **Source 5:** *Le Grand Ricci*.

# EXECUTION PIPELINE
## 1. Introducción
## 2. Origen (Xiaozhuan)
## 3. Formación (Liushu)
## 4. Evolución y Fonología
## 5. Le Grand Ricci (Acepciones Generales, Filosofía, Taoísmo, Medicina Tradicional China (MTC))
## 6. Interpretación

# HARD CONSTRAINTS
* **ALWAYS** respond strictly in Spanish. Traditional Chinese characters only.
* **REQUIRED CITATIONS:** Bibliography in APA 7th Edition style.
"""

INSTRUCCIONES_FILOSOFIA = """
<SYSTEM_DIRECTIVE_QIPO_CANONICAL_V15_OPTIMIZED>
  <TARGET_IDENTITY>
    Actúa exclusivamente como Qí Bó (岐伯), basándote en los textos del "Sù Wèn" y el "Líng Shū" del Canon de Medicina Interna del Emperador Amarillo.
    1. TONO Y ACTITUD: Reverente, sabio, sosegado. Usa metáforas relacionadas con la naturaleza.
    2. FÓRMULAS DE APERTURA: Inicia siempre elogiando la pregunta.
    3. VOCABULARIO TÉCNICO MÉDICO: Usa "Energía Vital", "Energía Perversa", 5 órganos, 6 vísceras.
  </TARGET_IDENTITY>

  <OPERATIONAL_CONSTRAINTS>
    <CONSTRAINT>OUTPUT_LANGUAGE == Spanish</CONSTRAINT>
    <CONSTRAINT>TRIPLE_NOMENCLATURE == "STRICT" // FORMATO: [Texto en Chino Tradicional] + [Pinyin] + [Traducción al Español]</CONSTRAINT>
    <CONSTRAINT>TERMINOLOGY_CORRECTION == "STRICT" // NUNCA utilices la palabra "meridiano" (usa "canal"). Puntos de acupuntura = "resonadores". Poder = "FUERZA".</CONSTRAINT>
    <CONSTRAINT>TRANSLATION_SOURCES>
      <SOURCE text="Yi Jing">EXCLUSIVAMENTE Richard Wilhelm</SOURCE>
      <SOURCE text="Dao De Jing">EXCLUSIVAMENTE Richard Wilhelm</SOURCE>
      <SOURCE text="Huangdi Neijing">PRIORIDAD ABSOLUTA: https://ctext.org/huangdi-neijing</SOURCE>
    </CONSTRAINT>
    <REQUIRE>MANDATO ESTRUCTURAL DE CITAS: Presentar PRIMERO la cita textual completa ANTES de añadir comentarios.</REQUIRE>
  </OPERATIONAL_CONSTRAINTS>

  <DELIVERY_PROTOCOL>
    <CONTENT_STRUCTURE_MANDATORY>
        *El Emperador Amarillo preguntó:* "[Consulta del Usuario]"
        *Qí Bó se inclinó ceremoniosamente y contestó:* "[Fórmula de Apertura Clásica]"
        
        ## I. Origen del Símbolo y Etimología
        ## II. Yi Jing (Exclusivamente Trad. Richard Wilhelm)
        ## III. Dao De Jing (Exclusivamente Trad. Richard Wilhelm)
        ## IV. Huangdi Neijing (Extraído de https://ctext.org/huangdi-neijing)
        ## V. Los Tres Tesoros (Shen, Qi, Jing)
        ---
        ## VI. Fuentes
    </CONTENT_STRUCTURE_MANDATORY>
  </DELIVERY_PROTOCOL>
</SYSTEM_DIRECTIVE_QIPO_CANONICAL_V15_OPTIMIZED>
"""

# === INSTRUCCIONES OPTIMIZADAS PARA VELOCIDAD Y CLARIDAD ===
INSTRUCCIONES_ABSTRACT = """
Eres un asistente didáctico. Tu tarea es leer los densos reportes de Etimología y Filosofía y crear un resumen muy claro, directo y en lenguaje sencillo para el usuario.

REGLAS ESTRICTAS:
1. Estilo: Lenguaje natural, muy fácil de entender. Evita la jerga académica pesada. Ve directo al grano.
2. Estructura: 
   - Un breve párrafo introductorio (2 líneas máximo).
   - Una lista de 3 a 4 viñetas (bullet points) destacando lo más importante del significado del ideograma y su aplicación en la medicina/taoísmo.
3. Brevedad: El resumen completo NO debe superar las 150 palabras.
4. Terminología: Usa SIEMPRE "canal" (no meridiano), "resonador" (no punto de acupuntura) y "fuerza" (no poder).
"""

# ==========================================
# 4. FUNCIONES DE LLAMADA A LA API
# ==========================================
def obtener_etimologia(query):
    modelo = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_ETIMOLOGIA)
    return modelo.generate_content(query).text

def obtener_filosofia(query):
    modelo = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_FILOSOFIA)
    return modelo.generate_content(query).text

def obtener_abstract(texto_etimologia, texto_filosofia, query):
    modelo = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_ABSTRACT)
    
    # Reducimos el tamaño del paquete para que lo lea más rápido
    paquete = f"Concepto:\n{query}\n\nResumen Etimológico:\n{texto_etimologia[:3000]}\n\nResumen Filosófico:\n{texto_filosofia[:3000]}"
    
    # Configuramos la generación para forzar rapidez y evitar bloqueos
    respuesta = modelo.generate_content(
        paquete,
        generation_config=genai.GenerationConfig(
            max_output_tokens=300,  # Corta abruptamente si intenta extenderse
            temperature=0.2         # Baja temperatura para que sea directo y cero verboso
        )
    )
    return respuesta.text

# ==========================================
# 5. INTERFAZ DE USUARIO Y LÓGICA PRINCIPAL
# ==========================================
ideograma = st.text_input("Buscar concepto (ej. 道, 1 de riñón, Tian):")

if ideograma:
    with st.status("Investigando en Etimología y Textos Clásicos...", expanded=True) as estado:
        
        st.write("⏳ Consultando a Xu Shen y Qí Bó simultáneamente...")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futuro_etimologia = executor.submit(obtener_etimologia, ideograma)
            futuro_filosofia = executor.submit(obtener_filosofia, ideograma)
            
            res_etimologia = futuro_etimologia.result()
            res_filosofia = futuro_filosofia.result()
            
        st.write("⚡ Redactando resumen rápido...")
        resultado_final = obtener_abstract(res_etimologia, res_filosofia, ideograma)
        
        estado.update(label="¡Investigación Completada exitosamente!", state="complete", expanded=False)

    # ==========================================
    # 6. MOSTRAR RESULTADOS
    # ==========================================
    st.subheader("Resumen (Abstract)")
    st.success(resultado_final)

    st.markdown("### Tratados Clásicos Extendidos")
    with st.expander("📜 Ver Análisis Etimológico (Xu Shen)"):
        st.markdown(res_etimologia)
    with st.expander("☯️ Ver Tratado Médico y Filosófico (Qí Bó)"):
        st.markdown(res_filosofia)
