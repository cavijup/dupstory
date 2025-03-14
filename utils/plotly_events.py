import streamlit as st
from streamlit.components.v1 import html
import json
import uuid

def plotly_events(fig, click_event=True, select_event=False, hover_event=False, override_height=None):
    """
    Función personalizada para capturar eventos de Plotly.
    Basada en el paquete streamlit-plotly-events, pero implementada directamente.
    
    Parámetros:
    - fig: figura de Plotly
    - click_event: capturar eventos de clic
    - select_event: capturar eventos de selección
    - hover_event: capturar eventos de hover
    - override_height: altura personalizada
    
    Retorna:
    - Lista de puntos seleccionados
    """
    # Generar un ID único para este componente
    div_id = f"plotly-{uuid.uuid4()}"
    
    # Configurar qué eventos capturar
    event_names = []
    if click_event:
        event_names.append("click")
    if select_event:
        event_names.append("select")
    if hover_event:
        event_names.append("hover")
    
    # Variable para almacenar los puntos seleccionados
    selected_points_key = f"{div_id}-selected-points"
    if selected_points_key not in st.session_state:
        st.session_state[selected_points_key] = []
    
    # Convertir la figura a JSON
    fig_json = fig.to_json()
    
    # Crear el HTML personalizado con el gráfico y los manejadores de eventos
    component_html = f"""
    <div id="{div_id}"></div>
    <script>
        // Asegurarse de que Plotly esté disponible
        if (window.Plotly) {{
            var fig = {fig_json};
            Plotly.newPlot("{div_id}", fig.data, fig.layout, {{responsive: true}});
            
            var selected_points = [];
            
            // Manejar eventos
            {div_id}.on("plotly_click", function(data) {{
                selected_points = [];
                var point = data.points[0];
                selected_points.push({{
                    curveNumber: point.curveNumber,
                    pointNumber: point.pointNumber,
                    pointIndex: point.pointIndex,
                    x: point.x,
                    y: point.y
                }});
                console.log("Punto seleccionado:", selected_points);
                
                // Enviar los datos al backend de Streamlit
                const json_data = JSON.stringify(selected_points);
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: json_data
                }}, "*");
            }});
        }}
    </script>
    """
    
    # Crear componente HTML
    selected_points_json = html(
        component_html,
        height=override_height if override_height else fig.layout.height or 400,
        key=div_id
    )
    
    # Procesar respuesta
    if selected_points_json:
        try:
            selected_points = json.loads(selected_points_json)
            st.session_state[selected_points_key] = selected_points
            return selected_points
        except:
            return []
    
    return st.session_state[selected_points_key]