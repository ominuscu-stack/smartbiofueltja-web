import streamlit as st
import pandas as pd

NOMBRE_APP = "SmartBioFuel Power"
FACTOR_AGUA_PROTEGIDA = 1000
FACTOR_CO2_EVITADO = 2.5
PRECIO_LITRO_BIODIESEL = 0.85
RENDIMIENTO_BIODIESEL = 0.90

# Responsabilidad: Sebastian Espana (Energia)
def calcular_impacto_ambiental(litros):
    try:
        if litros <= 0:
            return 0.0, 0.0, 0.0
        
        agua_salvada = litros * FACTOR_AGUA_PROTEGIDA
        co2_reducido = round(litros * FACTOR_CO2_EVITADO, 2)
        biodiesel_producido = round(litros * RENDIMIENTO_BIODIESEL, 2)
        
        return agua_salvada, co2_reducido, biodiesel_producido
    except Exception:
        return 0.0, 0.0, 0.0

# Responsabilidad: Luciana Coca (Industrial)
def calcular_balance_economico(biodiesel_producido):
    try:
        if biodiesel_producido <= 0:
            return 0.0
        
        valor_economico = round(biodiesel_producido * PRECIO_LITRO_BIODIESEL, 2)
        return valor_economico
    except Exception:
        return 0.0

# Responsabilidad: Pamela Maldonado (Sistemas)
def validar_y_estructurar_lote(restaurante, litros, direccion, tipo_aceite):
    try:
        restaurante_limpio = restaurante.strip()
        direccion_limpia = direccion.strip()
        
        if not restaurante_limpio or not direccion_limpia or litros <= 0:
            return False, {}
        
        agua_salvada, co2_reducido, biodiesel_producido = calcular_impacto_ambiental(litros)
        valor_economico = calcular_balance_economico(biodiesel_producido)
        
        lote = {
            "Restaurante": restaurante_limpio,
            "Litros Aceite (L)": litros,
            "Direccion": direccion_limpia,
            "Tipo": tipo_aceite,
            "Biodiesel Est. (L)": biodiesel_producido,
            "Agua Protegida (L)": agua_salvada,
            "CO2 Mitigado (kg)": co2_reducido,
            "Valor Combustible ($)": valor_economico
        }
        return True, lote
    except Exception:
        return False, {}

st.set_page_config(page_title=NOMBRE_APP, layout="wide")

if "lotes_recolectados" not in st.session_state:
    st.session_state.lotes_recolectados = [
        {
            "Restaurante": "Pollos Tropical",
            "Litros Aceite (L)": 50.0,
            "Direccion": "Av. Las Americas #120",
            "Tipo": "Vegetal Mixto",
            "Biodiesel Est. (L)": 45.0,
            "Agua Protegida (L)": 50000.0,
            "CO2 Mitigado (kg)": 125.0,
            "Valor Combustible ($)": 38.25
        }
    ]

st.sidebar.title(NOMBRE_APP)
st.sidebar.caption("Plataforma Circular de Aceite a Biocombustible")

opcion_menu = st.sidebar.radio(
    "Modulos:",
    ["Dashboard de Impacto", "Registrar Recoleccion IoT", "Detalle de Lotes y Reporte"]
)

st.title(NOMBRE_APP)
st.caption("Ingenieria en Energia - Industrial - Sistemas | Triple Impacto")

if opcion_menu == "Dashboard de Impacto":
    st.header("Tablero de Control y Metricas ESG")
    
    total_lotes = len(st.session_state.lotes_recolectados)
    total_aceite = sum(item["Litros Aceite (L)"] for item in st.session_state.lotes_recolectados)
    total_biodiesel = sum(item["Biodiesel Est. (L)"] for item in st.session_state.lotes_recolectados)
    total_agua = sum(item["Agua Protegida (L)"] for item in st.session_state.lotes_recolectados)
    total_co2 = sum(item["CO2 Mitigado (kg)"] for item in st.session_state.lotes_recolectados)
    total_dinero = sum(item["Valor Combustible ($)"] for item in st.session_state.lotes_recolectados)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Aceite Recolectado (L)", value=f"{total_aceite:.1f} L", delta=f"{total_lotes} Lotes")
        st.metric(label="Valor Economico Generado", value=f"${total_dinero:.2f} USD")
    with col2:
        st.metric(label="Biodiesel Obtenido (L)", value=f"{total_biodiesel:.1f} L", delta="Rendimiento 90%")
        st.metric(label="Emisiones CO2 Mitigadas", value=f"{total_co2:.1f} kg")
    with col3:
        st.metric(label="Agua Dulce Salvaguardada", value=f"{total_agua:,.0f} L", delta="Cero vertido")
        st.metric(label="Puntos Limpios Asociados", value=f"{total_lotes}")

elif opcion_menu == "Registrar Recoleccion IoT":
    st.header("Registro de Retiro de Aceite Usado (ACU)")
    with st.form("form_registro", clear_on_submit=True):
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            restaurante_input = st.text_input("Nombre del Establecimiento / Restaurante:")
            direccion_input = st.text_input("Direccion / Ubicacion del Local:")
        with col_form2:
            litros_input = st.number_input("Litros de Aceite Medidos por Sensor/Balanza:", min_value=1.0, max_value=2000.0, value=25.0, step=1.0)
            tipo_input = st.selectbox("Tipo de Aceite:", ["Girasol / Soja", "Palma Industrial", "Grasa Animal / Mixto"])
            
        boton_enviar = st.form_submit_button("Confirmar y Procesar Lote")
        
        if boton_enviar:
            exito, nuevo_lote = validar_y_estructurar_lote(restaurante_input, litros_input, direccion_input, tipo_input)
            if exito:
                st.session_state.lotes_recolectados.append(nuevo_lote)
                st.success(f"Lote de {litros_input}L registrado exitosamente de '{restaurante_input}'")
            else:
                st.error("Error al registrar: Verifique que los campos no esten vacios y el volumen sea mayor a 0.")

elif opcion_menu == "Detalle de Lotes y Reporte":
    st.header("Trazabilidad y Descarga de Certificados")
    if len(st.session_state.lotes_recolectados) > 0:
        df_lotes = pd.DataFrame(st.session_state.lotes_recolectados)
        st.dataframe(df_lotes, use_container_width=True)
        
        csv_data = df_lotes.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar Reporte en Excel / CSV",
            data=csv_data,
            file_name="reporte_smartbiofuel.csv",
            mime="text/csv"
        )
    else:
        st.warning("No hay lotes registrados todavia en el sistema.")
