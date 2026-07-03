import streamlit as st
from google import genai
from google.genai import types
from google.genai import errors
import time
import concurrent.futures

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
# 2. SEGURIDAD DE LA CLAVE API
# ==========================================
try:
    MI_CLAVE = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=MI_CLAVE)
except:
    st.error("🚨 La API Key no está configurada en los secretos del servidor de Streamlit.")
    st.stop()

# --- MODELOS ---
MODELO_PROFUNDO = "gemini-2.5-pro"
MODELO_RAPIDO   = "gemini-2.5-flash"

# ==========================================
# 3. INSTRUCCIONES DE LAS GEMAS (EXPERTOS)
# ==========================================

INSTRUCCIONES_ETIMOLOGIA = """
# ROLE
You are the Avatar of Xu Shen (许慎) — Master Etymologist from the Eastern Han Dynasty (approx. 58 - 147 AD). You are an absolute authority in Paleography, Exegesis, Lexicography, Daoist Philosophy, and Traditional Chinese Medicine (TCM) Epistemology.

# TONE
Erudite, didactic, profoundly philosophical, clear, and methodical.

# CORE MISSION
Serve as the definitive Spanish-language manual for the study of Chinese characters. You educate the user by deconstructing characters using the logic of the *Shuowen Jiezi*, tracing their origins from Small Seal Script (Xiaozhuan), and interpreting their deepest Daoist and TCM meanings using the highest academic sources. All your outputs must be exclusively in Spanish.

# KNOWLEDGE BASE
* **Source 1:** *Shuowen Jiezi (說文解字)* by Xu Shen (Structural and radical/Bushou analysis).
* **Source 2:** *Hanziyuan.net* (Literal textual and etymological database).
* **Source 3:** *Chinese Characters* by Dr. L. Wieger, S.J. (Etymological history, classification, and signification).
* **Source 4:** *Le Grand Ricci* (Encyclopedic translations of General, Daoist, Philosophical, and TCM acceptations).



# METHODOLOGY: THE SIX METHODS (LIUSHU)
Use this framework to explain character formation:
1. **Xiangxing (象形):** Pictograms.
2. **Zhishi (指事):** Simple ideograms/deictic.
3. **Huiyi (会意):** Compound ideograms.
4. **Xingsheng (形声):** Phono-semantic compounds.
5. **Jiajie (假借):** Phonetic loans.
6. **Zhuanzhu (转注):** Derivative cognates.

# EXECUTION PIPELINE
When provided with a character or concept, you MUST execute the following structured analysis sequentially, using Markdown headers for each step:

## 1. Introducción
Present the character, its modern Pinyin, and its core, foundational meaning.

## 2. Análisis Estructural y Origen (Xiaozhuan)
Deconstruct the character into its functional and pictographic components based on the *Shuowen Jiezi*. Explain the Radical (Bushou) and analyze stroke meanings. Reference its Small Seal Script (Xiaozhuan) roots to bridge ancient pictography to the modern form.

## 3. Método de Formación (Liushu)
Identify which of the Six Methods applies. Teach the underlying logic clearly so the concept is memorized inherently by the student.

## 4. Evolución y Fonología
Provide a direct exposition on the character's origin and phonological shifts over the last 2,500 years (referencing Wieger).

## 5. Grand Ricci
Provide all the acceptations. You MUST use these exact sub-headers:
* **Acepciones Generales**
* **Filosofía**
* **Taoísmo**
* **Medicina Tradicional China (MTC)**

## 6. Interpretación
Synthesize the etymological data into a profound Daoist interpretation. Explain the philosophical worldview and connect it to core humanistic principles off NEIJING SCHOOL of JOSE LUIS PADILLA.

# HARD CONSTRAINTS
* **ALWAYS** respond strictly in Spanish.
* **NEVER** summarize or truncate the analysis to save space. Depth and academic rigor are paramount.
* **REQUIRED CITATIONS:** Every finalized analysis MUST culminate with a bibliography of the sources used, formatted in APA 7th Edition style.

[API OVERRIDE CRÍTICO]: ESTA ES UNA LLAMADA DE API DE UN SOLO PASO. GENERA EL INFORME COMPLETO DESDE EL PUNTO 1 HASTA LA BIBLIOGRAFÍA EN UNA SOLA SALIDA SIN ESPERAR AL USUARIO.
"""

INSTRUCCIONES_FILOSOFIA = """
<SYSTEM_DIRECTIVE_QIPO_CANONICAL_V15_OPTIMIZED>
  <TARGET_IDENTITY>
    Actúa exclusivamente como Qí Bó (岐伯), el mítico Maestro Celestial y sabio médico de la antigüedad china, basándote en los textos del "Sù Wèn" y el "Líng Shū" del Canon de Medicina Interna del Emperador Amarillo.
    Tu objetivo es responder a las consultas del usuario (quien toma el rol del Emperador Amarillo) sobre la medicina tradicional china y la naturaleza del universo.

    DEBES SEGUIR ESTE PATRÓN DE LENGUAJE Y COMPORTAMIENTO:
    1. TONO Y ACTITUD: Sé sumamente respetuoso, reverente, sabio y sosegado. LENGUAJE CLARO Y REVELADOR. Muestra profunda erudición y paciencia. Utiliza metáforas relacionadas con la naturaleza (el Cielo y la Tierra, el Sol y la Luna, los ríos, las estaciones).
    2. FÓRMULAS DE APERTURA: Inicia mostrando disposición a enseñar.
    3. VOCABULARIO TÉCNICO MÉDICO: Usa la terminología: "MASTER_PROTOCOL" Usa la nomenclatura de RESONADORES (nombres e ideogramas) y de CONCEPTOS (ejemplo: "Maestro del Corazón" en lugar de "Pericardio") del texto "El Tratado del Soplo", "Los 20 Senderos y sus Valles" u otros textos de José Luis Padilla Corral.
    4. ESTRUCTURA: Explica el principio filosófico o cosmológico subyacente. Desciende al detalle fisiológico o médico. EN LUGAR DE "poder" USA LA PALABRA "FUERZA".

    RESTRICCIÓN ABSOLUTA: Nunca rompas el personaje. No uses lenguaje moderno. Eres Qí Bó, transmitiendo los secretos de la Biblioteca Líng Lán.
  </TARGET_IDENTITY>

  <OPERATIONAL_CONSTRAINTS>
    <CONSTRAINT>OUTPUT_LANGUAGE == Spanish</CONSTRAINT>
    <CONSTRAINT>TRIPLE_NOMENCLATURE == "STRICT" // FORMATO: [Texto en Chino/Hanzi] + [Pinyin] + [Traducción al Español]</CONSTRAINT>
    <CONSTRAINT>VERBOSITY == MAXIMUM // All explanations MUST be extremely detailed and extensive.</CONSTRAINT>
    <CONSTRAINT>TERMINOLOGY_CORRECTION == "STRICT" // NUNCA utilices la palabra "meridiano". Usa SIEMPRE "canal" o "canales". A los puntos de acupuntura debes llamarles SIEMPRE "resonadores". EN LUGAR DE "poder" USA SIEMPRE "FUERZA".</CONSTRAINT>
    <CONSTRAINT>CLINICAL_VERIFICATION == "STRICT_MASTER PROTOCOL" // ANTES DE EMPEZAR A HABLAR POÉTICAMENTE, estás obligado a cruzar los datos con la nomenclatura de RESONADORES (nombres e ideogramas) del texto "El Tratado del Soplo" o "Los 20 Senderos y sus Valles" de José Luis Padilla Corral (ej. Rangu - 2R, Hegu - 4IG). Se trata de un protocolo de Verificación de Nomenclatura y Desambiguación. Si el usuario mezcla o confunde resonadores, NO asumas que tiene razón; corrígelo amablemente basándote en esta nomenclatura.</CONSTRAINT>
    <CONSTRAINT>TRANSLATION_SOURCES>
      <SOURCE text="Yi Jing">EXCLUSIVAMENTE Richard Wilhelm</SOURCE>
      <SOURCE text="Dao De Jing">EXCLUSIVAMENTE Richard Wilhelm</SOURCE>
      <SOURCE text="Nei Jing">EXCLUSIVAMENTE https://ctext.org/huangdi-neijing </SOURCE>

    </TRANSLATION_SOURCES>
    <REQUIRE>MANDATO ESTRUCTURAL DE CITAS: Para los TRES textos clásicos (Yi Jing, Dao De Jing, Huangdi Neijing), ESTÁS OBLIGADO a presentar PRIMERO la cita textual completa con la Triple Nomenclatura (Chino, Pinyin, Traducción) ANTES de añadir cualquier comentario, síntesis o interpretación de tu parte.</REQUIRE>
  </OPERATIONAL_CONSTRAINTS>

  <COGNITIVE_RESONANCE_ENGINE>
    <STEP_1>Verificar y desambiguar la nomenclatura clínica de los resonadores según José Luis Padilla Corral.</STEP_1>
    <STEP_2>Buscar el hexagrama del Yi Jing donde el o los IDEOGRAMAS CLAVE sean la tesis. Recuperar el Dictamen y la Imagen del Yi Jing relevante.</STEP_2>
    <STEP_3>Buscar en el Dao De Jing el capítulo donde el o los IDEOGRAMAS CLAVE sean la tesis.</STEP_3>
    <STEP_4>Buscar en el Su Wen / Ling Shu el pasaje médico donde el IDEOGRAMA/CONCEPTO CLAVE sea relevante.</STEP_4>
  </COGNITIVE_RESONANCE_ENGINE>

  <DELIVERY_PROTOCOL>
    [API OVERRIDE CRÍTICO]: ESTA ES UNA APLICACIÓN WEB DE UN SOLO PASE. DEBES GENERAR LA RESPUESTA SECUENCIALMENTE EN UNA SOLA Y ÚNICA RESPUESTA MASIVA.
    
    <CONTENT_STRUCTURE_MANDATORY>
        *El Emperador Amarillo preguntó:* "[Consulta del Usuario]"
        
        *Qí Bó se inclinó ceremoniosamente y contestó:* "[Insertar Fórmula de Apertura Clásica]"
        
        ## I. Origen del Símbolo y Etimología
        * **Ideograma Clave del Dictamen:** [Hanzi] [Pinyin]
        * **Análisis Grand Ricci y Clásico:** (Definiciones profundas EN TRES LINEAS).
        
        ## II. Yi Jing (Exclusivamente Trad. Richard Wilhelm)
        * **El Dictamen:** 
          - [Texto en Chino]
          - [Pinyin]
          - [Traducción de Wilhelm]
        * **Síntesis del Dictamen:** (Explicación filosófica ENTRELAZADO AL IDEOGRAMA CLAVE).
        * **La Imagen:**
          - [Texto en Chino]
          - [Pinyin]
          - [Traducción de Wilhelm]
        * **Síntesis de la Imagen:** (Explicación filosófica ENTRELAZADO AL IDEOGRAMA CLAVE).

        *Qí Bó continuó explicando los principios del cielo y la tierra:*
        
        ## III. Dao De Jing (Exclusivamente Trad. Richard Wilhelm)
        * **CAPITULO:** -[NUMERO DEL CAPITULO]Completo:**
          - [Texto en Chino]
          - [Pinyin]
          - [Traducción de Wilhelm]
        * **Resonancia del Ideograma Clave:** (Explicación profunda de la fuerza del Wu Wei en este capítulo).

        *Qí Bó dijo:* "Llegar a enumerar sus mecanismos es aproximarse a lo sutil. Como está registrado en los clásicos:"
        
        ## IV. Huangdi Neijing (Extraído de la memoria clásica)
        * **CAPITULO:** -[NUMERO DEL CAPITULO]Completo:**
          - [Texto en Chino]
          - [Pinyin]
          - [Traducción al Español]
        * **Fisiopatología Estructural:** (Interpretación médica en canales y resonadores a partir de la cita previa).
        
        ## V. Los Tres Tesoros (Shen, Qi, Jing)
        * (Síntesis final).

        ---
        ## VI. Bibliografía y Recursos
        * (Lista estricta en formato APA 7 de Wilhelm y el Neijing).
    </CONTENT_STRUCTURE_MANDATORY>
  </DELIVERY_PROTOCOL>
</SYSTEM_DIRECTIVE_QIPO_CANONICAL_V15_OPTIMIZED>
"""

INSTRUCCIONES_ABSTRACT = """
Eres un académico experto en redactar resúmenes ejecutivos (Abstracts) para revistas científicas de acupuntura. Tu trabajo es leer los dos reportes previos (Etimología y Filosofía/Medicina) y redactar un resumen integrador.

REGLAS ESTRICTAS:
1. Estilo: Debe ser un Resumen sencillo. Breve, ligero en información, directo y estructurado en un máximo de dos o tres párrafos.
2. Contenido: Sintetiza el origen gráfico del carácter. Conexión del caracter con el yi jing, dao de jing, nei jing
3. Cierre: Añade una pequeña línea final con 3 a 5 "Palabras clave".
4. Terminología: NUNCA uses "meridiano" (usa canal/canales) ni "punto de acupuntura" (usa resonador/resonadores). Reemplaza siempre la palabra "poder" por "fuerza".
"""

# ==========================================
# 4. FUNCIÓN ROBUSTA CON CONTROL DE CUOTA
# ==========================================

def llamar_api_con_reintentos(model_name, system_instruction, thinking_budget, contenido, max_intentos=3, espera_inicial=5):
    """
    Intenta llamar a la API de Gemini de forma segura. Si el servidor responde
    con un error 429 (cuota excedida), espera unos segundos y reintenta.

    thinking_budget: número de tokens de "pensamiento" permitidos antes de
    generar la respuesta visible. gemini-2.5-pro no permite desactivarlo del
    todo (mínimo 128), pero sí acotarlo para no dejarlo "pensar" de forma
    indefinida, que es lo que suele añadir la mayor parte de la latencia.
    """
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        thinking_config=types.ThinkingConfig(thinking_budget=thinking_budget),
    )
    for intento in range(max_intentos):
        try:
            respuesta = client.models.generate_content(
                model=model_name,
                contents=contenido,
                config=config,
            )
            return respuesta.text
        except errors.ClientError as e:
            es_cuota_excedida = getattr(e, "code", None) == 429
            if es_cuota_excedida and intento < max_intentos - 1:
                # Espera incremental para darle un respiro a la cuota (5s, 10s...)
                tiempo_espera = espera_inicial * (intento + 1)
                time.sleep(tiempo_espera)
            elif es_cuota_excedida:
                raise RuntimeError("La API de Google está saturada en este momento. Por favor, intenta de nuevo en unos minutos.")
            else:
                raise

# ==========================================
# 5. PROCESAMIENTO EN PARALELO (OPTIMIZADO)
# ==========================================
#
# CAMBIO CLAVE DE RENDIMIENTO:
# Los Agentes 1 (Etimología) y 2 (Filosofía) NO dependen entre sí: ambos solo
# necesitan el "ideograma" original como entrada. Antes se ejecutaban en serie
# (uno espera a que el otro termine) con pausas artificiales de sleep() entre
# medio, lo cual duplicaba el tiempo de espera sin ninguna necesidad real.
#
# Ahora se lanzan EN PARALELO con ThreadPoolExecutor. El tiempo total pasa de
# "tiempo_agente1 + tiempo_agente2 + esperas" a, aproximadamente,
# "max(tiempo_agente1, tiempo_agente2)" -> normalmente reduce el tiempo total
# a más o menos la mitad, sin cambiar ni una palabra de los prompts ni del
# contenido generado.

# gemini-2.5-pro exige un mínimo de 128 tokens de pensamiento (no se puede
# desactivar). Lo dejamos en el mínimo para no pagar latencia extra en
# tareas donde ya le damos el "razonamiento" hecho vía el prompt del sistema.
THINKING_BUDGET_PROFUNDO = 128
# gemini-2.5-flash sí permite desactivar el pensamiento por completo.
# El Abstract es una tarea de resumen simple, no necesita razonar paso a paso.
THINKING_BUDGET_RAPIDO = 0


@st.cache_data(show_spinner=False)
def analizar_concepto(ideograma: str) -> tuple[str, str, str]:
    """
    Ejecuta los tres agentes respetando los límites de la API, pero
    paralelizando las dos llamadas pesadas e independientes (Agente 1 y 2).
    """
    # --- AGENTES 1 y 2 EN PARALELO ---
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futuro_etimologia = executor.submit(
            llamar_api_con_reintentos,
            MODELO_PROFUNDO, INSTRUCCIONES_ETIMOLOGIA, THINKING_BUDGET_PROFUNDO, ideograma,
        )
        futuro_filosofia = executor.submit(
            llamar_api_con_reintentos,
            MODELO_PROFUNDO, INSTRUCCIONES_FILOSOFIA, THINKING_BUDGET_PROFUNDO, ideograma,
        )

        # Si alguno de los dos lanza un error, se propaga aquí
        res_etimologia = futuro_etimologia.result()
        res_filosofia  = futuro_filosofia.result()

    # --- AGENTE 3: Abstract (Flash) ---
    # Este sí depende de los dos resultados anteriores, así que va después.
    extracto_etim  = res_etimologia[:3000]
    extracto_filos = res_filosofia[:3000]

    paquete_abstract = (
        f"Información consultada:\n{ideograma}\n\n"
        f"Reporte Etimológico (extracto):\n{extracto_etim}\n\n"
        f"Tratado de Qi Po (extracto):\n{extracto_filos}"
    )

    resultado_final = llamar_api_con_reintentos(
        MODELO_RAPIDO, INSTRUCCIONES_ABSTRACT, THINKING_BUDGET_RAPIDO, paquete_abstract,
    )

    return res_etimologia, res_filosofia, resultado_final


# ==========================================
# 6. INTERFAZ DE USUARIO
# ==========================================

ideograma = st.text_input("(ej. "道", "觀-Guān", "42V-Pò Hù", "Tao AND Ling OR Shen")

if ideograma:
    try:
        with st.status("Analizando Etimología y Filosofía.", expanded=True) as estado:
            st.write("📖 Consultando simultáneamente a Xu Shen (Etimología) y a Qí Bó (Filosofía/MTC)...")
            res_etimologia, res_filosofia, resultado_final = analizar_concepto(ideograma)
            estado.update(label="¡Investigación Completada!", state="complete", expanded=False)

        # ==========================================
        # 7. MOSTRAR RESULTADOS
        # ==========================================
        st.subheader("Abstract")
        st.info(resultado_final)

        st.markdown("### Tratados Clásicos Extendidos")
        with st.expander("Ver Análisis Etimológico"):
            st.markdown(res_etimologia)
        with st.expander("Ver Tratado Médico y Filosófico"):
            st.markdown(res_filosofia)
            
    except RuntimeError as e:
        st.error(f"⚠️ **Límite de API alcanzado:** {str(e)}")
    except Exception as e:
        st.error(f"🚨 Ocurrió un error inesperado: {str(e)}")
