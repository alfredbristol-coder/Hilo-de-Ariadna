import streamlit as st
import google.generativeai as genai
import time

# 1. CONFIGURACIÓN DE LA PÁGINA WEB
st.set_page_config(page_title="Agente de Filosofía China", page_icon="⛩️", layout="centered")
st.title("⛩️ Núcleo de Síntesis Sinológica")
st.markdown("Introduce un ideograma para que nuestros tres expertos lo analicen y sinteticen su esencia histórica, médica y filosófica.")

# 2. SEGURIDAD DE LA CLAVE API (¡Ya no está a la vista!)
# Streamlit leerá la clave desde la configuración privada del servidor
try:
    MI_CLAVE = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=MI_CLAVE)
except:
    st.error("🚨 La API Key no está configurada en los secretos del servidor.")
    st.stop()

# 3. INSTRUCCIONES DE LOS EXPERTOS (Pega aquí tus textos largos)
INSTRUCCIONES_GENERAL = """[Pega aquí tus instrucciones de Etimología General]"""
INSTRUCCIONES_CHINA = """[Pega aquí tus instrucciones de Xu Shen]"""
INSTRUCCIONES_FILOSOFIA = """[Pega aquí tus instrucciones de Qi Po]"""
INSTRUCCIONES_SINTESIS = """[Pega aquí tus instrucciones del Núcleo Sintetizador]"""

MODELO_ESTABLE = 'gemini-2.5-pro'

# 4. INTERFAZ DE USUARIO: CAJA DE TEXTO Y BOTÓN
ideograma = st.text_input("Escribe el ideograma chino (ej. 道, 本神):")

if st.button("Iniciar Investigación Profunda"):
    
    # 5. BARRA DE ESTADO VISUAL
    with st.status(f"Analizando '{ideograma}'...", expanded=True) as estado:
        
        # --- EXPERTO 1 ---
        st.write("⏳ Consultando Etimología General...")
        m_general = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_GENERAL)
        res_general = m_general.generate_content(ideograma).text
        
        # --- EXPERTO 2 (XU SHEN) ---
        st.write("⏳ Consultando a Xu Shen (Etimología Antigua)...")
        m_china = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_CHINA)
        chat_china = m_china.start_chat()
        res_china = chat_china.send_message(ideograma).text
        # (Aquí mantienes el bucle while que hicimos antes para la paginación)
        
        # --- EXPERTO 3 (QI PO) ---
        st.write("⏳ Consultando a Qi Po (Filosofía y Neijing)...")
        m_filosofia = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_FILOSOFIA)
        chat_filosofia = m_filosofia.start_chat()
        res_filosofia = chat_filosofia.send_message(ideograma).text
        # (Aquí mantienes el bucle while de Qi Po)

        # --- SÍNTESIS ---
        st.write("🧠 Fusionando datos en el Núcleo Sintetizador...")
        m_sintesis = genai.GenerativeModel(MODELO_ESTABLE, system_instruction=INSTRUCCIONES_SINTESIS)
        paquete = f"Analiza: {ideograma}\nGeneral: {res_general}\nXu Shen: {res_china}\nQi Po: {res_filosofia}"
        resultado_final = m_sintesis.generate_content(paquete).text
        
        estado.update(label="¡Investigación Completada!", state="complete", expanded=False)

    # 6. MOSTRAR RESULTADOS EN LA WEB
    st.subheader("SÍNTESIS GLOBAL UNIFICADA")
    st.success(resultado_final) # Se muestra en un recuadro verde destacado

    # 7. MENÚS DESPLEGABLES PARA VER LOS DATOS CRUDOS
    # Esto mantiene la pantalla limpia, pero permite al usuario leer los textos largos si quiere
    st.markdown("### Reportes de los Maestros")
    with st.expander("Ver reporte completo de Etimología General"):
        st.markdown(res_general)
    with st.expander("Ver transcripción de Xu Shen"):
        st.markdown(res_china)
    with st.expander("Ver diálogo completo con Qi Po"):
        st.markdown(res_filosofia)
