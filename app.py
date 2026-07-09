import streamlit as st
from google import genai
from google.genai import types
from google.genai import errors
import time

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

st.markdown("<p style='text-align: center; color: #333;'> 玄永 XuánYǒng Etimología y filosofía Oriental. ©Alfred Bristol</p>", unsafe_allow_html=True)

# ==========================================
# 2. SEGURIDAD Y CONFIGURACIÓN DE LA API
# ==========================================
try:
    MI_CLAVE = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=MI_CLAVE)
except Exception as e:
    st.error("🚨 La API Key no está configurada en los secretos del servidor de Streamlit.")
    st.stop()

# Único modelo ligero y rápido para todo el flujo
MODELO_UNICO = "gemini-2.5-flash"

# ==========================================
# 3. INSTRUCCIÓN MAESTRA (OPTIMIZADA EN INGLÉS)
# ==========================================
SUPER_INSTRUCCION = """
BE EXTREMELY DETAILED AND PROFOUND. FOLLOW EVERY SECTION DESCRIBED HERE STRICTLY.
CRITICAL RULE: Your final output MUST be entirely in Spanish (except for necessary Chinese characters or Pinyin). 
NEVER use the word "meridiano" (always use "canal" or "canales"). ALWAYS call acupuncture points "resonadores". Instead of "poder" (power), ALWAYS use the word "fuerza" (force).

You must structure the massive report in a single fluid text following exactly this order and formatting:

---

## PRESENTACIÓN
Write a brief and direct executive summary (maximum 3 paragraphs). Synthesize the graphic origin of the analyzed character and its subsequent connection and common threads with the Yi Jing, the Dao De Jing, and the Huangdi Neijing.
End this section with a single line containing 3 to 5 keywords formatted exactly as: "Palabras clave: [keyword 1], [keyword 2]...".

## ETIMOLOGÍA
Perform this rigorous analysis:
1. Introducción: The character, its modern Pinyin, and its root meaning.
2. Análisis (Xiaozhuan): Deconstruct the character into its pictographic components based on the 'Shuowen Jiezi'. Explain its Radical (Bushou) and infer the ancient meaning from pictograms on oracle bones/tortoise shells to the present.
3. Formación (Liushu): Identify which of the 6 classical formation methods applies (Xiangxing, Zhishi, Huiyi, Xingsheng, Jiajie, Zhuanzhu).
4. Evolución: Evolution of the character according to Léon Wieger in "Chinese Characters: Their Origin, Etymology, History, Classification And Signification".
5. Grand Ricci: Detail the General acceptations. Add IF AVAILABLE: acceptations in 'Filosofía', 'Taoísmo', and 'Medicina Tradicional China (MTC)'.
6. Nuestra visión: Profound synthesis connecting the character with Daoist worldviews. (ALWAYS specify sources in APA 7).

## FILOSOFÍA Y COSMOLOGÍA

I. ORIGEN
- Core Ideogram: [Hanzi] [Pinyin] [Spanish Translation]
- Briefly explain: Why this ideogram was selected, its conceptual or ideogrammatic connections.

II. YI JING (Richard Wilhelm Translation)
- El Dictamen: [Chinese Text] + [Pinyin] + [Wilhelm Translation in Spanish]
- Synthesis of the Judgement: Intertwined with the core ideogram.
- La Imagen: [Chinese Text] + [Pinyin] + [Wilhelm Translation in Spanish]
- Synthesis of the Image.

III. DAO DE JING (Richard Wilhelm Translation)
- Quote the complete relevant CHAPTER: [Chinese Text] + [Pinyin] + [Wilhelm Translation in Spanish]
- Resonance of the Core Ideogram: Explanation of the force of Wu Wei in that chapter.

IV. HUANGDI NEIJING (Su Wen / Ling Shu)
- Quote the complete medical passage: [Chinese Text] + [Pinyin] + [Spanish Translation] + [Source in APA 7 format]
- MODO TCM: Be brief, use CLEAR, SIMPLE, AND REVEALING language. DO NOT REPEAT ANYTHING SAID PREVIOUSLY. Profound synthesis connecting the three previous texts and their healing humanistic deductions in daily life.

V. LOS TRES TESOROS
- Synthesis of the concept's resonance or effect on Shen (Spirit), Qi (Breath/Energy), and Jing (Essence).

---
## BIBLIOGRAFÍA Y RECURSOS CLÁSICOS
Add a strict bibliography at the very end of the text using APA 7th Edition format to support all cited works (Wilhelm, Wieger, Padilla Corral, ctext Nei Jing).
"""

# ==========================================
# 4. FUNCIÓN ROBUSTA DE LLAMADA ÚNICA
# ==========================================
def llamar_api_unificada(contenido, max_intentos=3, espera_inicial=4):
    """
    Realiza una única consulta lineal a Gemini 2.5 Flash evitando
    concurrencias que rompan los hilos gRPC y maneja errores de cuota (429).
    """
    config = types.GenerateContentConfig(
        system_instruction=SUPER_INSTRUCCION,
        temperature=0.3, # Mayor precisión y fidelidad a los textos sagrados
    )

    for intento in range(max_intentos):
        try:
            respuesta = client.models.generate_content(
                model=MODELO_UNICO,
                contents=f"Analyze the following user query based on your unified instructions (Respond in Spanish): {contenido}",
                config=config,
            )
            return respuesta.text
        except errors.ClientError as e:
            es_cuota_excedida = getattr(e, "code", None) == 429
            if es_cuota_excedida and intento < max_intentos - 1:
                tiempo_espera = espera_inicial * (intento + 1)
                time.sleep(tiempo_espera)
            elif es_cuota_excedida:
                raise RuntimeError("El servidor de Google está experimentando alta demanda. Reintenta en unos instantes.")
            else:
                raise

# ==========================================
# 5. CACHÉ DE DATOS
# ==========================================
@st.cache_data(show_spinner=False)
def procesar_investigacion(concepto: str) -> str:
    """Invoca la consulta unificada sin romper el flujo de procesamiento."""
    return llamar_api_unificada(concepto)

# ==========================================
# 6. INTERFAZ DE USUARIO
# ==========================================
ideograma = st.text_input("Busca conceptos, ideogramas o hexagramas de Yi Jing (ej. 道, 觀-Guān, 42V-Pò Hù, Tao AND Ling OR Shen)")

if ideograma:
    try:
        with st.status("Buscando.", expanded=True) as estado:
            
            # Llamada limpia en un solo bloque de texto
            reporte_completo = procesar_investigacion(ideograma)
            
            estado.update(label="OK", state="complete", expanded=False)

        # ==========================================
        # 7. MOSTRAR RESULTADOS 
        # ==========================================
        caracter_limpio = ideograma[0] 
        
        # Creamos dos columnas
        col_img, col_texto = st.columns([1, 4])
        
        with col_img:
            # IDEOGRAMA renderizado en grande a la izquierda
            st.markdown(f"<div style='font-size: 40px; text-align:center; padding-top: 20px;'>{caracter_limpio}</div>", unsafe_allow_html=True)
            st.caption("<p style='text-align:center;'>Forma base</p>", unsafe_allow_html=True)
            
        with col_texto:
            # Texto principal a la derecha
            st.markdown(reporte_completo)
            
    except RuntimeError as e:
        st.error(f"⚠️ **Incidencia con la API:** {str(e)}")
    except Exception as e:
        st.error(f"🚨 Excepción inesperada del sistema: {str(e)}")
