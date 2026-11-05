"""Ejecutar: streamlit run app.py. Cada visitante tiene su propia simulación."""
import time
import streamlit as st
from physics import WaveSimulation
from svg_canvas import SVGCanvas
from visuals import Visuals

st.set_page_config(page_title='El Efecto Doppler', page_icon='🔭', layout='wide')
st.markdown('''<style>
h1 {font-size:2.2rem !important} label, button {font-size:1.1rem !important}
.block-container {padding-top:1.5rem; max-width:1450px}
</style>''', unsafe_allow_html=True)
st.title('El Efecto Doppler')
st.write('Escuchar y medir el universo')

SCENES = ['Ondas y movimiento', 'Medir una estrella', 'Descubrir un planeta']
DEFAULTS = {'wave':0.0, 'velocity':0, 'mass':1.0, 'distance':1.0, 'inclination':90}
KEYS = [('wave',), ('velocity',), ('mass','distance','inclination')]
QUESTIONS = ['¿Cómo cambia la separación entre ondas?',
             '¿Se acerca o se aleja? Compara las líneas con la referencia.',
             '¿Cómo cambia el movimiento de la estrella que podemos medir?']
CHALLENGES = ['Haz que las ondas delante de la fuente estén más juntas. ¿Y detrás?',
              'Duplica la velocidad. ¿Se duplica exactamente el desplazamiento?',
              'Lleva la inclinación a 0°. ¿La estrella se mueve hacia nosotros o solo de lado?']

if 'simulation' not in st.session_state:
    st.session_state.simulation = {'waves': WaveSimulation(), 'phase':0.0,
                                   'last':time.monotonic(), 'scene':0,
                                   'speed':0.0, 'paused':False}
for key, value in DEFAULTS.items():
    # Mantener los parámetros al ocultar los controles de otra escena.
    st.session_state[key] = st.session_state.get(key, value)


def advance_clock():
    model = st.session_state.simulation
    now = time.monotonic()
    # Evita saltos grandes tras suspender la pestaña o perder la conexión.
    dt = min(max(now-model['last'], 0), .25)
    if not model['paused']:
        if model['scene'] == 0:
            model['waves'].advance(dt, model['speed'])
        elif model['scene'] == 2:
            model['phase'] += dt
    model['last'] = now


def reset_scene():
    advance_clock()
    index = SCENES.index(st.session_state.scene)
    for key in KEYS[index]:
        st.session_state[key] = DEFAULTS[key]
    if index == 0:
        st.session_state.simulation['waves'].reset()
        st.session_state.simulation['speed'] = DEFAULTS['wave']
    elif index == 2:
        st.session_state.simulation['phase'] = 0.0
    st.session_state.show_challenge = False


scene = st.radio('Experiencia', SCENES, horizontal=True, key='scene', label_visibility='collapsed')
index = SCENES.index(scene)
st.subheader(QUESTIONS[index])
control, display = st.columns([1, 3])
with control:
    if index == 0:
        st.slider('Velocidad de la fuente / velocidad de onda', -.8, .8, step=.01, key='wave')
    elif index == 1:
        st.slider('Velocidad radial (km/s)', -3000, 3000, step=10, key='velocity')
        st.write('− Se acerca · + Se aleja')
    else:
        st.slider('Masa del planeta (masas de Júpiter)', .1, 10., step=.1, key='mass')
        st.slider('Separación orbital (UA)', .05, 3., step=.05, key='distance')
        st.slider('Inclinación (°)', 0, 90, key='inclination')
    st.checkbox('Pausar', key='paused')
    st.button('Restablecer escena', on_click=reset_scene)
    st.checkbox('Mostrar reto', key='show_challenge')
    if st.session_state.show_challenge:
        st.info(CHALLENGES[index])


class Value:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


@st.fragment(run_every=.1 if index != 1 and not st.session_state.paused else None)
def animation():
    # Primero integra con los controles anteriores; luego aplica los nuevos.
    # Así mover un control nunca modifica la historia de ondas ya emitidas.
    advance_clock()
    model = st.session_state.simulation
    model.update(scene=index, speed=st.session_state.wave, paused=st.session_state.paused)
    view = Visuals()
    view.values = {key:Value(st.session_state[key]) for key in DEFAULTS}
    view.waves = model['waves']
    view.phase = model['phase']
    canvas = SVGCanvas()
    [view.draw_waves, view.draw_star, view.draw_planet][index](canvas, canvas.width, canvas.height)
    st.image(canvas.svg(), width='stretch')


with display:
    animation()
