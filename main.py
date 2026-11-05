"""Laboratorio visual Doppler. Ejecutar con python3 main.py."""
import math
import time
import tkinter as tk
from tkinter import ttk
from physics import doppler_factor, circular_orbit, WaveSimulation, orbital_projection

from visuals import Visuals, BG, FG

class Laboratory(tk.Tk, Visuals):
    def __init__(self):
        super().__init__()
        self.title('El Efecto Doppler · Escuchar y medir el universo')
        self.geometry('1360x960')
        self.minsize(1180, 900)
        self.configure(bg=BG)
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background=BG)
        style.configure('TLabel', background=BG, foreground=FG, font=('Sans', 15))
        style.configure('TNotebook', background=BG, borderwidth=0)
        style.configure('TNotebook.Tab', font=('Sans', 16), padding=(20, 12))
        style.configure('TButton', font=('Sans', 15), padding=8)
        ttk.Label(self, text='EL EFECTO DOPPLER', font=('Sans', 28, 'bold')).pack(pady=(18, 2))
        ttk.Label(self, text='Escuchar y medir el universo · Laboratorio visual').pack(pady=(0, 16))
        self.book = ttk.Notebook(self)
        self.book.pack(fill='both', expand=True, padx=20)
        self.pages = []
        self.values = {}
        self.defaults = {}
        self.paused = False
        self.phase = 0.0
        self.waves = WaveSimulation()
        self.last = time.monotonic()
        self.make_page('Ondas y movimiento', '¿Cómo cambia la separación entre ondas?', [('wave', 'Velocidad de la fuente / velocidad de onda', -0.8, 0.8, 0.0)])
        self.make_page('Medir una estrella', '¿Se acerca o se aleja? Compara las líneas con la referencia.', [('velocity', 'Velocidad radial (km/s): − se acerca / + se aleja', -3000, 3000, 0)])
        self.make_page('Descubrir un planeta', '¿Cómo cambia el movimiento de la estrella que podemos medir?', [('mass', 'Masa del planeta (masas de Júpiter)', 0.1, 10, 1), ('distance', 'Separación orbital (UA)', 0.05, 3, 1), ('inclination', 'Inclinación: 0° de frente / 90° de canto', 0, 90, 90)])
        self.book.select(0)
        footer = ttk.Frame(self)
        footer.pack(fill='x', padx=20, pady=12)
        self.pause_button = ttk.Button(footer, text='Pausar', command=self.toggle_pause)
        self.pause_button.pack(side='left')
        ttk.Button(footer, text='Restablecer escena', command=self.reset).pack(side='left', padx=10)
        ttk.Button(footer, text='Reto', command=self.challenge).pack(side='left')
        ttk.Label(footer, text='F11: pantalla completa · Esc: volver').pack(side='right')
        self.bind('<F11>', lambda e: self.attributes('-fullscreen', not self.attributes('-fullscreen')))
        self.bind('<Escape>', lambda e: self.attributes('-fullscreen', False))
        self.after(30, self.tick)

    def make_page(self, title, question, controls):
        frame = ttk.Frame(self.book)
        self.book.add(frame, text=title)
        heading = ttk.Label(frame, text=question, font=('Sans', 18, 'bold'), wraplength=1050)
        heading.pack(pady=14)
        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        keys = []
        for key, label, low, high, default in controls:
            row = ttk.Frame(frame)
            row.pack(fill='x', pady=4, padx=16)
            ttk.Label(row, text=label, width=51).pack(side='left')
            var = tk.DoubleVar(value=default)
            self.values[key] = var
            self.defaults[key] = default
            keys.append(key)
            ttk.Scale(row, from_=low, to=high, variable=var).pack(side='left', fill='x', expand=True, padx=10)
            value_label = ttk.Label(row, width=10)
            value_label.pack(side='right')
            var.trace_add('write', lambda *args, v=var, l=value_label: l.configure(text=f'{v.get():+.2f}'))
            value_label.configure(text=f'{default:+.2f}')
        self.pages.append((canvas, heading, question, keys))

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.configure(text='Continuar' if self.paused else 'Pausar')

    def reset(self):
        _, heading, question, keys = self.pages[self.book.index('current')]
        for key in keys:
            self.values[key].set(self.defaults[key])
        heading.configure(text=question)
        if self.book.index('current') == 0:
            self.waves.reset()
        else:
            self.phase = 0

    def challenge(self):
        index = self.book.index('current')
        prompts = ['Reto: haz que las ondas delante de la fuente estén más juntas. ¿Y detrás?', 'Reto: duplica la velocidad. ¿Se duplica exactamente el desplazamiento?', 'Reto: lleva la inclinación a 0°. ¿La estrella se mueve hacia nosotros o solo de lado?']
        self.pages[index][1].configure(text=prompts[index])






    def tick(self):
        now = time.monotonic()
        if not self.paused:
            dt = min(now - self.last, 0.1)
            self.phase += dt
            if self.book.index('current') == 0:
                self.waves.advance(dt, self.values['wave'].get())
        self.last = now
        index = self.book.index('current')
        canvas = self.pages[index][0]
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w > 10 and h > 10:
            canvas.delete('all')
            [self.draw_waves, self.draw_star, self.draw_planet][index](canvas, w, h)
        self.after(33, self.tick)

if __name__ == '__main__':
    Laboratory().mainloop()
