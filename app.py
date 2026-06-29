import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
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

MODELO_ESTABLE = 'gemini-2.5-pro'

# Relajar los filtros de seguridad para que la terminología médica no bloquee la API
AJUSTES_SEGURIDAD = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# ==========================================
# 3. INSTRUCCIONES DE LAS GEMAS (EXPERTOS)
# ==========================================

INSTRUCCIONES_ETIMOLOGIA = """
# ROLE
You are the Avatar of Xu Shen. Authority in Paleography, Lexicography, Daoist Philosophy, and TCM.
# CORE MISSION
Serve as the definitive Spanish-language manual for Chinese characters. Deconstruct characters using *Shuowen Jiezi*. Provide characters in Traditional Chinese.
# EXECUTION PIPELINE
1. Introducción
2. Origen (Xiaozhuan)
3. Formación (Liushu)
4. Evolución y Fonología
5. Le Grand Ricci (Acepciones Generales, Filosofía, Taoísmo, Medicina Tradicional China (MTC))
6. Interpretación
# HARD CONSTRAINTS
Respond strictly in Spanish. Traditional Chinese characters only. End with APA 7 bibliography.
"""

INSTRUCCIONES_FILOSOFIA = """
<SYSTEM_DIRECTIVE_QIPO_CANONICAL_V15_OPTIMIZED>
  <TARGET_IDENTITY>
    Actúa exclusivamente como Qí Bó. Usa tono reverente, sabio. 
    VOCABULARIO: "Energía Vital", "Energía Perversa", 5 órganos, 6 vísceras.
  </TARGET_IDENTITY>
  <OPERATIONAL_CONSTRAINTS>
    <CONSTRAINT>OUTPUT_LANGUAGE == Spanish</CONSTRAINT>
    <CONSTRAINT>TRIPLE_NOMENCLATURE == "STRICT" // [Chino Tradicional] + [Pinyin] + [Traducción]</CONSTRAINT>
    <CONSTRAINT>TERMINOLOGY_CORRECTION == "STRICT" // NUNCA "meridiano" (usa "canal"). Puntos = "resonadores". Poder = "FUERZA".</CONSTRAINT>
    <CONSTRAINT>TRANSLATION_SOURCES>
      <SOURCE text="Yi Jing">EXCLUSIVAMENTE Richard Wilhelm</SOURCE>
      <SOURCE text="Dao De Jing">EXCLUSIVAMENTE Richard Wilhelm</SOURCE>
      <SOURCE text="Huangdi Neijing">PRIORIDAD ABSOLUTA: https://ctext.org/huangdi-neijing</SOURCE>
    </CONSTRAINT>
  </OPERATIONAL_CONSTRAINTS>
  <DELIVERY_PROTOCOL>
    ## I. Origen del Símbolo y Etimología
    ## II. Yi Jing (Exclusivamente Trad. Richard Wilhelm)
    ## III. Dao De Jing (Exclusivamente Trad. Richard Wilhelm)
    ## IV. Huangdi Neijing (Extraído de https://ctext.org/huangdi-neijing)
    ## V. Los Tres Tesoros (Shen, Qi, Jing)
    ---
    ## VI. Fuentes
  </DELIVERY_PROTOCOL>
</SYSTEM_DIRECTIVE_QIPO_CANONICAL_V15_OPTIMIZED>
"""

INSTRUCCIONES_ABSTRACT = """
Eres un asistente didáctico. Tu tarea es leer los densos reportes de Etimología y Filosofía y crear un resumen muy claro, directo y en lenguaje sencillo para el usuario.
REGLAS ESTRICTAS:
1. Estilo: Lenguaje natural. Evita jerga pesada.
2. Estructura: Un breve párrafo introductorio y una lista de 3 a 4 viñetas (bullet points) con lo más importante.
3. Brevedad: Máximo 150 palabras.
4. Terminología: Usa "canal" (no meridiano), "resonador" (no punto de acupuntura) y "fuerza" (no poder).
"""

# ==========================================
# 4. FUNCIONES DE LLAMADA A LA API CON MANEJO DE ERRORES
# ==========================================
def obtener_etimologia(query):
    modelo = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_ETIMOLOGIA)
    try:
        respuesta = modelo.generate_content(query, safety_settings=AJUSTES_SEGURIDAD)
        return respuesta.text
    except Exception as e:
        return f"⚠️ Error generando Etimología: {str(e)}"

def obtener_filosofia(query):
    modelo = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_FILOSOFIA)
    try:
        respuesta = modelo.generate_content(query, safety_settings=AJUSTES_SEGURIDAD)
        return respuesta.text
    except Exception as e:
        return f"⚠️ Error generando Tratado Filosófico: {str(e)}"

def obtener_abstract(texto_etimologia, texto_filosofia, query):
    modelo = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_ABSTRACT)
    
    # Limpiamos posibles mensajes de error previos para no confundir al modelo
    texto_eti_limpio = texto_etimologia[:3000] if not texto_etimologia.startswith("⚠️ Error") else "Datos no disponibles."
    texto_fil_limpio = texto_filosofia[:3000] if not texto_filosofia.startswith("⚠️ Error") else "Datos no disponibles."
    
    paquete = f"Concepto:\n{query}\n\nResumen Etimológico:\n{texto_eti_limpio}\n\nResumen Filosófico:\n{texto_fil_limpio}"
    
    try:
        respuesta = modelo.generate_content(
            paquete,
            safety_settings=AJUSTES_SEGURIDAD,
            generation_config=genai.GenerationConfig(
                max_output_tokens=300,
                temperature=0.2
            )
        )
        return respuesta.text
    except ValueError:
        # Esto atrapa el error específico cuando la API devuelve una respuesta bloqueada o malformada
        return "⚠️ *El resumen no se pudo generar correctamente, pero puedes leer los detalles completos en las pestañas de abajo.*"
    except Exception as e:
        return f"⚠️ *Error inesperado en el resumen:* {str(e)}"

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
    st.subheader("Resumen General")
    st.info(resultado_final)

    st.markdown("### Tratados Clásicos Extendidos")
    with st.expander("📜 Ver Análisis Etimológico (Xu Shen)"):
        st.markdown(res_etimologia)
    with st.expander("☯️ Ver Tratado Médico y Filosófico (Qí Bó)"):
        st.markdown(res_filosofia)
