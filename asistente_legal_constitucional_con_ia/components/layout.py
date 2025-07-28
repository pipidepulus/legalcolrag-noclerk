# asistente_legal_constitucional_con_ia/components/layout.py
"""Layout principal de la aplicación, ahora totalmente responsivo y sin rx.drawer."""
import reflex as rx
from .sidebar import sidebar
from ..states.app_state import AppState

def main_layout(content: rx.Component, use_container: bool = True) -> rx.Component:
    """El layout principal que envuelve todas las páginas, con lógica responsiva correcta."""
    
    content_wrapper = rx.container if use_container else rx.box

    return rx.box(
        # --- MENÚ HAMBURGUESA (SÓLO MÓVIL/TABLET PEQUEÑA) ---
        rx.box(
            rx.icon(
                tag="menu",
                size=32,
                on_click=AppState.toggle_drawer,
                cursor="pointer",
                color="var(--blue-9)"
            ),
            display=["block", "block", "none", "none"], # Muestra en base y sm, oculta en md y lg
            position="fixed",
            top="1rem",
            right="1rem",
            z_index=1001, # z-index muy alto para estar por encima de todo
        ),

        # --- "DRAWER" MÓVIL (Implementado con rx.box) ---
        # 1. Overlay (fondo oscuro)
        rx.box(
            on_click=AppState.toggle_drawer,
            display=rx.cond(AppState.show_drawer, "block", "none"),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            bg="rgba(0, 0, 0, 0.5)",
            z_index=999,
        ),
        # 2. Contenido del Sidebar móvil
        rx.box(
            sidebar(is_in_drawer=True), # Reutilizamos el sidebar aquí
            display=["block", "block", "none", "none"], # Solo existe en vistas móviles
            position="fixed",
            top="0",
            left=rx.cond(AppState.show_drawer, "0px", "-300px"), # Desliza desde la izquierda
            width="300px",
            height="100vh",
            padding="1em",
            bg="var(--gray-1)",
            border_right="1px solid var(--gray-4)",
            transition="left 0.3s ease-in-out", # Animación suave
            z_index=1000,
        ),

        # --- ESTRUCTURA PRINCIPAL (SIDEBAR DE ESCRITORIO + CONTENIDO) ---
        rx.hstack(
            # SIDEBAR DE ESCRITORIO (OCULTO EN MÓVIL/TABLET)
            rx.box(
                sidebar(), # Reutilizamos el sidebar
                display=["none", "none", "block", "block"], # Oculto en móvil, visible en escritorio
                width="350px",
                min_width="350px",
                height="100vh",
                position="sticky",
                top="0",
                border_right="1px solid var(--gray-4)",
                padding="1em", 
                overflow_y="auto",
                overflow_x="hidden",
            ),
            
            # CONTENEDOR DEL CONTENIDO DE LA PÁGINA
            content_wrapper(
                content,
                padding_top=["3.5rem", "3.5rem", "2em", "2em"],
                padding_x=["1em", "1em", "2em", "2em"],
                flex_grow=1,
                height="100vh",
                max_height="100vh",
                overflow_y="auto",  # Cambiado de "hidden" a "auto" para permitir scroll
            ),
            align="start",
            height="100vh",
            width="100%",
             overflow="hidden", 
        ),
        height="100vh",
        width="100%",
    )