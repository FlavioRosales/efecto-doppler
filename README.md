# El Efecto Doppler: escuchar y medir el universo

Laboratorio visual interactivo en Python, sin audio ni conexión a internet.

## Ejecutar

Desde esta carpeta:

```sh
python3 main.py
```

Requiere Python 3.10 o posterior con Tkinter. No requiere paquetes de pip.
En distribuciones que no incluyen Tkinter, instalar el paquete del sistema `python3-tk`.

Tres pestañas: ondas en un medio, espectros estelares y detección de planetas
mediante velocidad radial. Cambiar los controles actualiza las observaciones.
F11 activa pantalla completa; Esc la desactiva. Pausar congela el tiempo,
pero permite seguir explorando los parámetros. Restablecer afecta la escena actual.

## Física y alcance de esta primera versión

- Ondas: emisión cada 0.45 s, propagación constante en un medio en reposo;
  cada frente permanece centrado en la posición donde fue emitido. La fuente
  tiene velocidad subsónica ajustable. Su trayectoria se integra en el tiempo;
  cambiar el control solo modifica el movimiento futuro. Cada frente almacena
  su instante, posición y velocidad de la fuente al emitirse. Los puntos blancos
  señalan esos centros de emisión, que no se desplazan después. La secuencia se reinicia cada 15 s.
- Estrella: Doppler longitudinal relativista, λ observada / λ emitida =
  sqrt((1+v/c)/(1-v/c)). Velocidad positiva indica alejamiento. Líneas de
  Balmer aproximadas en nm. El eje espectral representa longitudes de onda,
  sin exageración del desplazamiento. No incluye ensanchamiento instrumental.
- Planeta: órbita circular newtoniana de dos cuerpos con estrella de una masa
  solar. El período depende de la separación y de la masa total. La señal es
  la velocidad radial estelar clásica, apropiada para estas velocidades.
  Inclinación 0° de frente y 90° de canto. La cruz indica el centro de masa.
  El desplazamiento estelar se amplía 30 veces; los tamaños son ilustrativos.
  Cada órbita tarda el mismo tiempo en animarse para facilitar la exploración;
  el período físico se muestra en días. El eje de velocidad parte de ±40 m/s y se amplía si es necesario;
  sus límites numéricos se muestran en la gráfica.

La primera versión incluye preguntas exploratorias; todavía no incluye
evaluación automática de retos, alineación manual de espectros ni ruido de medición.

## Verificar los modelos

```sh
python3 -m unittest discover -s tests -v
```

## Mejoras para proyección

Tipografía ampliada, trazos de alto contraste y ciclos visuales de 15 s.
El espectro muestra una porción del visible con colores esquemáticos y líneas
oscuras de absorción del hidrógeno identificadas.
El sistema planetario se muestra de lado: el observador está arriba del dibujo
y mira hacia abajo; la gráfica usa velocidad positiva para alejamiento.
La señal más grande facilita medir el movimiento, sin modelar ruido instrumental.

La pestaña de ondas es un modelo clásico en un medio, no una simulación
relativista de luz estelar. La pestaña espectral usa el Doppler relativista.

## Presentación simplificada

La aplicación abre en Ondas y movimiento. Se eliminaron las notas técnicas
de las escenas; las convenciones y ampliaciones siguen documentadas aquí.
En la vista lateral del sistema el observador está centrado arriba y mira
verticalmente hacia abajo. A 0° la estrella se mueve lateralmente, sin variar
su coordenada de profundidad ni su velocidad radial. La posición dibujada y
la velocidad de la gráfica se calculan con el mismo modelo orbital.


## Versión web con Streamlit

La interfaz web usa el mismo modelo físico y los mismos dibujos que la versión
Tkinter. No necesita pantalla gráfica en el servidor ni Tkinter instalado.
Cada visitante tiene parámetros e historial independientes. La animación se
actualiza aproximadamente diez veces por segundo mientras la sesión está activa;
puede ser menos fluida que en escritorio según la conexión y la carga del servidor.
Al suspender la pestaña se evitan saltos grandes de tiempo.

### Probar en tu computadora

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abre la dirección local que aparece en la terminal. La aplicación permite cambiar
parámetros, pausar, restablecer cada escena y mostrar retos.

### GitHub y publicación

1. Crea un repositorio en GitHub, por ejemplo `efecto-doppler`.
2. Sube `app.py`, `physics.py`, `visuals.py`, `svg_canvas.py`, `requirements.txt`,
   `.streamlit/config.toml`, `README.md` y `tests/`. Puedes incluir `main.py` para
   conservar la aplicación de escritorio. No subas `.venv/` ni archivos de secretos.
3. En https://share.streamlit.io inicia sesión con GitHub y elige **Create app**.
4. Selecciona el repositorio y la rama donde subiste los archivos. Como archivo
   principal indica **app.py**; selecciona Python 3.12 en las opciones avanzadas.
5. Pulsa **Deploy**. Comparte la dirección `https://...streamlit.app` generada.

GitHub almacena el código. Streamlit Community Cloud ejecuta Python y sirve la
aplicación interactiva; GitHub Pages por sí solo no ejecuta este programa.

Documentación oficial:
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies

### Verificación de la versión web

Con las dependencias instaladas:

```sh
python -m unittest discover -s tests -v
```

Las pruebas web comprueban navegación, parámetros, pausa, restablecimiento y
separación de las sesiones de distintos visitantes.
# efecto-doppler
