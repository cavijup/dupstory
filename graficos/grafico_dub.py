import streamlit as st
import plotly.graph_objects as go
import time

def crear_grafico_dub(df):
    """
    Crea y muestra una barra horizontal de progreso para ID DUB.
    
    Args:
        df: DataFrame con los datos
    """
    if 'ID DUB' in df.columns:
        st.subheader("Progreso de ID DUB")
        dub_count = df['ID DUB'].nunique()
        meta = 24000
        porcentaje = (dub_count / meta) * 100
        
        # Crear contenedor para la animación
        progress_container = st.empty()
        
        # Valor inicial para animación
        step = max(1, dub_count // 20)  # 20 pasos para la animación
        
        # Animación del contador
        for count in range(0, dub_count + step, step):
            current_count = min(count, dub_count)
            current_percentage = (current_count / meta) * 100
            
            # Crear barra horizontal con Plotly para cada paso de la animación
            fig = go.Figure()
            
            # Barra de progreso (valor actual)
            fig.add_trace(go.Bar(
                x=[current_count],
                y=[''],
                orientation='h',
                marker=dict(color='darkblue'),
                text=f"{current_count:,} ({current_percentage:.1f}%)",
                textposition='inside',
                insidetextanchor='middle',
                hoverinfo='none',
                width=0.6
            ))
            
            # Barra de fondo (valor restante hasta meta)
            fig.add_trace(go.Bar(
                x=[meta - current_count],
                y=[''],
                orientation='h',
                marker=dict(color='lightgray'),
                hoverinfo='none',
                width=0.6
            ))
            
            # Configurar el diseño
            fig.update_layout(
                barmode='stack',
                title={
                    'text': f"Progreso hacia meta de 24,000 ID DUB únicos",
                    'font': {'size': 16},
                    'y': 0.9
                },
                xaxis=dict(
                    range=[0, meta * 1.05],
                    tickvals=[0, meta/4, meta/2, 3*meta/4, meta],
                    ticktext=[f"{0:,}", f"{int(meta/4):,}", f"{int(meta/2):,}", f"{int(3*meta/4):,}", f"{meta:,}"]
                ),
                yaxis=dict(showticklabels=False),
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=150,
                margin=dict(l=20, r=20, t=60, b=20),
                showlegend=False
            )
            
            # Añadir línea meta
            fig.add_shape(
                type="line",
                x0=meta, y0=-0.5,
                x1=meta, y1=0.5,
                line=dict(color="red", width=2, dash="dash")
            )
            
            # Añadir etiqueta para la meta
            fig.add_annotation(
                x=meta,
                y=0,
                text="Meta: 24,000",
                showarrow=False,
                yshift=20,
                font=dict(color="red")
            )
            
            # Actualizar el gráfico en el contenedor
            with progress_container:
                st.plotly_chart(fig, use_container_width=True)
            
            # Pequeña pausa para la animación
            time.sleep(0.05)
        
        # Mostrar información adicional del progreso
        cols = st.columns(2)
        with cols[0]:
            st.metric(
                label="Total ID DUB registrados", 
                value=f"{dub_count:,}"
            )
        with cols[1]:
            st.metric(
                label="Avance", 
                value=f"{porcentaje:.2f}%",
                delta=f"{meta-dub_count:,} restantes"
            )
    else:
        st.warning("No se encontró la columna 'ID DUB' en los datos")