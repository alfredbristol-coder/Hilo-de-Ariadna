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
# 3. INSTRUCCIÓN MAESTRA
# ==========================================
SUPER_INSTRUCCION = """
SÉ EXTREMADAMENTE EXTENSO Y PROFUNDO. OBEDECE CADA SECCIÓN AQUÍ DESCRITA AL PIE DE LA LETRA. 
Tus respuestas deben ser completamente en español (salvo los términos requeridos en caracteres chinos o pinyin). 
NUNCA utilices la palabra "meridiano" (usa siempre "canal" o "canales"). A los puntos de acupuntura llámalos SIEMPRE "resonadores". En lugar de "poder" usa siempre la palabra "fuerza".

Debes estructurar el informe masivo en un solo texto fluido siguiendo exactamente este orden:

---

## PRESENTACIÓN
Escribe un resumen ejecutivo breve y directo (máximo 3 párrafos). Sintetiza el origen gráfico del carácter analizado y su posterior conexión e hilos conductores con el Yi Jing, el Dao De Jing y el Huangdi Neijing.
Finaliza esta sección con una línea que contenga entre 3 y 5 "Palabras clave: ...".

## ETIMOLOGÍA
Realiza este análisis riguroso:
1. Introducción: Carácter, su Pinyin moderno y su significado raíz.
2. Análisis (Xiaozhuan): Deconstruye el carácter en sus componentes pictográficos basados en el 'Shuowen Jiezi'. Explica su Radical (Bushou) e infiere el significado antiguo desde los pictogramas en el caparazon de la tortuga hasta la actualidad.
3. Formación (Liushu): Identifica cuál de los 6 métodos de formación clásica aplica (Xiangxing, Zhishi, Huiyi, Xingsheng, Jiajie, Zhuanzhu).
4. Evolución: Evolución del caracter según Wieger, Léon en "Chinese Characters: Their Origin, Etymology, History, Classification And Signification" 
5. Grand Ricci: Desglosa detalladamente las acepciones Generales. Añade SI LAS HAY: las acepciones en 'Filosofía', 'Taoísmo' y 'Medicina Tradicional China (MTC)'.
6. Nuestra visión: Síntesis profunda conectando el carácter con visiones taoístas del mundo. (especifica SIEMPRE las fuentes).

## (FILOSOFÍA Y COSMOLOGÍA)

I. ORIGEN
- Ideograma Clave del Dictamen: [Hanzi] [Pinyin] [Traducción al Español]
- Explica brevemente: Porqué hemos seleccionado este idiograma, sus conexiones conceptuales o ideogramaticas.

II. YI JING (Traducción Richard Wilhelm)
- El Dictamen: [Texto en Chino] + [Pinyin] + [Traducción de Wilhelm]
- Síntesis del Dictamen (entrelazado al ideograma clave).
- La Imagen: [Texto en Chino] + [Pinyin] + [Traducción de Wilhelm]
- Síntesis de la Imagen.

III. DAO DE JING (Traducción Richard Wilhelm)
- Cita el CAPÍTULO completo relevante: [Texto en Chino] + [Pinyin] + [Traducción de Wilhelm]
- Resonancia del Ideograma Clave: Explicación de la fuerza del Wu Wei en dicho capítulo.

IV. HUANGDI NEIJING (Su Wen / Ling Shu)
- Cita el pasaje médico completo: [Texto en Chino] + [Pinyin] + [Traducción al Español] + [Fuente en APA 7]
- MODO TCM: Se breve, con un lenguaje CLARO, SENCILLO Y REVELADOR. NO REPITAS NADA DE LO DICHO ANTERIORMENTE. Síntesis profunda conectando los tres textos anteriores y sus deducciones humanistas sanadoras en la vida cotidiana.

V. LOS TRES TESOROS
- Síntesis de la afectación o resonancia del concepto sobre el Shen (Espíritu), el Qi (Soplo/Energía) y el Jing (Esencia).

---
## BIBLIOGRAFÍA Y RECURSOS CLÁSICOS
Añade una bibliografía estricta al final de todo el texto usando formato APA 7ma Edición que fundamente las obras citadas (Wilhelm, Wieger, Padilla Corral, ctext Nei Jing).
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
                contents=f"Por favor analiza el siguiente concepto o consulta del usuario bajo tus instrucciones unificadas: {contenido}",
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
        with st.status("Accediendo a la biblioteca clásica del XuánYǒng...", expanded=True) as estado:
            st.write("📜 Extrayendo conocimientos de los textos sagrados y diccionarios etimológicos...")
            
            # Llamada limpia en un solo bloque de texto
            reporte_completo = procesar_investigacion(ideograma)
            
            estado.update(label="¡Consulta Finalizada Exitosamente!", state="complete", expanded=False)

        # ==========================================
        # 7. MOSTRAR RESULTADO EN UN SOLO TEXTO
        # ==========================================
        # Mostramos la respuesta completa directamente en pantalla sin cortarla ni meterla en pestañas complejas
        st.markdown(reporte_completo)
            
    except RuntimeError as e:
        st.error(f"⚠️ **Incidencia con la API:** {str(e)}")
    except Exception as e:
        st.error(f"🚨 Excepción inesperada del sistema: {str(e)}")
