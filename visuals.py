"""Dibujo compartido por Tkinter y la versión web, sin dependencias gráficas."""
import math
from physics import doppler_factor, circular_orbit, orbital_projection

BG = '#0b1224'
FG = '#ffffff'
MUTED = '#dce8ff'
CYAN = '#5cffff'
GOLD = '#ffe16b'

class Visuals:
    def text(self, c, x, y, text, color=FG, size=16, anchor='center'):
        c.create_text(x, y, text=text, fill=color, font=('Sans', size), anchor=anchor)

    def spectrum(self, c, y, velocity, width):
        left, right = 90, width - 90
        factor = doppler_factor(velocity)
        # Banda visible parcial, con colores esquemáticos, no fotométricos.
        stops = [(116, 60, 255), (42, 100, 255), (30, 220, 230),
                 (80, 235, 90), (250, 240, 65), (255, 140, 40), (245, 55, 55)]
        lines = [(410.17, 'Hδ'), (434.05, 'Hγ'), (486.13, 'Hβ'), (656.28, 'Hα')]
        for row, label in enumerate(['Referencia: hidrógeno en reposo', 'Observado: las mismas líneas desplazadas']):
            center = y + row * 115
            self.text(c, left, center - 28, label, FG, 17, 'w')
            for j in range(180):
                position = j / 179 * (len(stops)-1)
                k = min(int(position), len(stops)-2)
                t = position-k
                rgb = tuple(round(stops[k][n]*(1-t)+stops[k+1][n]*t) for n in range(3))
                color = '#%02x%02x%02x' % rgb
                c.create_rectangle(left+(right-left)*j/180, center,
                                   left+(right-left)*(j+1)/180+1, center+34,
                                   fill=color, outline='')
            for wavelength, name in lines:
                actual = wavelength * (factor if row else 1)
                x = left + (actual-390)/300*(right-left)
                c.create_line(x, center, x, center+34, fill='#000000', width=5)
                self.text(c, x, center+53, name, FG, 15)
        self.text(c, left, y+207, '390 nm · violeta', FG, 14, 'w')
        self.text(c, right, y+207, 'rojo · 690 nm', FG, 14, 'e')
        self.text(c, width/2, y+242, 'Espectro visible', FG, 17)
        self.text(c, width/2, y+271, 'Rayas oscuras = luz absorbida por el hidrógeno de la atmósfera estelar.', FG, 15)

    def draw_waves(self, c, w, h):
        speed = self.values['wave'].get()
        scale = min(w / 28, (h - 160) / 15)
        source_x = w/2 + self.waves.position * scale
        cy = h/2
        for front in self.waves.fronts:
            radius = self.waves.radius(front) * scale
            x = w/2 + front.position * scale
            c.create_oval(x-radius, cy-radius, x+radius, cy+radius, outline=CYAN, width=3)
            c.create_oval(x-3, cy-3, x+3, cy+3, fill=FG, outline='')
        c.create_oval(source_x-10, cy-10, source_x+10, cy+10, fill=GOLD, outline='')
        self.text(c, w/2, 24, f'Fuente: {speed:+.2f} veces la velocidad de propagación', GOLD)
        self.text(c, w/2, h-62, 'Puntos blancos: lugares de emisión. Cada onda se expande desde su propio punto.', FG, 15)

    def draw_star(self, c, w, h):
        v = self.values['velocity'].get()
        state = 'Se aleja → hacia el rojo' if v > 0.01 else 'Se acerca → hacia el azul' if v < -0.01 else 'En reposo respecto al observador'
        self.text(c, w/2, 25, state, CYAN, 21)
        self.spectrum(c, 85, v, w)
        shift = 656.28 * (doppler_factor(v) - 1)
        self.text(c, w/2, h-53, f'Velocidad radial: {v:+.1f} km/s     Cambio en Hα: {shift:+.3f} nm', GOLD, 18)

    def draw_planet(self, c, w, h):
        mass, distance, inc = (self.values[k].get() for k in ['mass', 'distance', 'inclination'])
        period, radius, amplitude = circular_orbit(mass, distance, inc)
        angle = self.phase * 2 * math.pi / 15
        star_x, star_z, radial = orbital_projection(mass, distance, inc, angle)
        cx, cy = w * .25, h * .40
        orbit = min(w*.16, h*.16)
        sini = math.sin(math.radians(inc))
        # Vista lateral x-z: observador distante en z negativo (arriba).
        # Su dirección de observación es vertical y común a todo el sistema.
        eye_y = 38
        c.create_oval(cx-18, eye_y-10, cx+18, eye_y+10, outline=FG, width=3)
        c.create_oval(cx-5, eye_y-5, cx+5, eye_y+5, fill=CYAN)
        self.text(c, cx+32, eye_y, 'Observador', FG, 16, 'w')
        c.create_line(cx, eye_y+18, cx, cy-orbit-18, fill=FG, width=3, arrow='last')
        c.create_oval(cx-orbit, cy-orbit*sini, cx+orbit, cy+orbit*sini,
                      outline=MUTED, width=3)
        px, py = cx+orbit*math.cos(angle), cy+orbit*sini*math.sin(angle)
        # La misma posición física que produce la curva, ampliada para dibujarla.
        display_scale = orbit / (distance * 149597870700.0) * 30
        sx, sy = cx+star_x*display_scale, cy+star_z*display_scale
        c.create_oval(sx-16, sy-16, sx+16, sy+16, fill=GOLD, outline=FG, width=2)
        c.create_oval(px-8, py-8, px+8, py+8, fill=CYAN, outline=FG, width=2)
        if abs(radial) > 1e-8:
            c.create_line(sx+24, sy, sx+24, sy+38*radial/max(amplitude, 1e-9),
                          fill=GOLD, width=4, arrow='last')
        state = ('Solo movimiento lateral' if amplitude < 1e-8 else
                 'La estrella se aleja ↓' if radial > 1e-8 else
                 'La estrella se acerca ↑' if radial < -1e-8 else
                 'Ahora se mueve de lado')
        self.text(c, cx, h*.68, state, GOLD, 18)
        x0, x1, mid, amp = w*.58, w*.95, h*.38, h*.19
        # Antes ±1300 m/s ocultaba casi por completo la señal inicial de 28 m/s.
        limit = max(40, math.ceil(amplitude/100)*100)
        c.create_line(x0, mid, x1, mid, fill=FG, width=2)
        for value in (-limit, limit):
            gy = mid - amp*value/limit
            c.create_line(x0, gy, x1, gy, fill='#52617c', dash=(5, 5))
            self.text(c, x0-10, gy, f'{value:+.0f}', FG, 14, 'e')
        self.text(c, x0-10, mid, '0', FG, 14, 'e')
        points = []
        for j in range(241):
            _, _, velocity = orbital_projection(mass, distance, inc, j/240*2*math.pi)
            points.extend([x0+(x1-x0)*j/240, mid-amp*velocity/limit])
        c.create_line(*points, fill=CYAN, width=4)
        x = x0+(x1-x0)*(angle%(2*math.pi))/(2*math.pi)
        y = mid-amp*radial/limit
        c.create_oval(x-7, y-7, x+7, y+7, fill=GOLD, outline=FG)
        self.text(c, (x0+x1)/2, 28, 'Velocidad hacia / desde nosotros (m/s)', CYAN, 17)
        self.text(c, (x0+x1)/2, 62, '+ se aleja     ·     − se acerca', FG, 15)
        self.text(c, (x0+x1)/2, h*.68, 'Tiempo → una vuelta completa', FG, 15)
        self.text(c, w/2, h-45, f'Período: {period/86400:.2f} días   ·   Velocidad medida ahora: {radial:+.2f} m/s', GOLD, 18)
