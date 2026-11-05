"""Modelos físicos en unidades SI, salvo velocidades espectrales en km/s."""
import math
from dataclasses import dataclass

C_KMS = 299792.458
G = 6.67430e-11
MSUN = 1.98847e30
MJUP = 1.89813e27
AU = 149597870700.0

def doppler_factor(velocity_kms):
    """Doppler longitudinal relativista; positivo = alejamiento."""
    beta = velocity_kms / C_KMS
    if abs(beta) >= 1:
        raise ValueError('La velocidad debe ser menor que la de la luz.')
    return math.sqrt((1 + beta) / (1 - beta))

def circular_orbit(mass_jupiter, separation_au, inclination_deg):
    """Estrella de una masa solar; separación entre cuerpos y órbita circular.

    Inclinación: 0° de frente (sin velocidad radial), 90° de canto.
    Retorna período en segundos, radio estelar en m y semiamplitud en m/s.
    """
    planet = mass_jupiter * MJUP
    separation = separation_au * AU
    total = MSUN + planet
    period = 2 * math.pi * math.sqrt(separation**3 / (G * total))
    radius = separation * planet / total
    amplitude = 2 * math.pi * radius / period * math.sin(math.radians(inclination_deg))
    return period, radius, amplitude


@dataclass(frozen=True)
class Wavefront:
    emitted_at: float
    position: float
    source_velocity: float


class WaveSimulation:
    """Onda clásica: velocidad de propagación = 1, medio en reposo.

    Las velocidades de la fuente son relativas a la propagación. Los centros
    de emisión son inmutables; cambiar la velocidad no reescribe el pasado.
    """
    def __init__(self, emission_period=0.45, duration=15.0):
        if emission_period <= 0 or duration <= 0:
            raise ValueError('El período y la duración deben ser positivos.')
        self.emission_period = emission_period
        self.duration = duration
        self.reset()

    def reset(self):
        self.time = 0.0
        self.position = 0.0
        self.fronts = []
        self._next_emission = 0

    def advance(self, dt, velocity):
        if dt < 0 or not math.isfinite(dt) or not math.isfinite(velocity):
            raise ValueError('Tiempo y velocidad deben ser finitos; tiempo no negativo.')
        while dt > 0:
            step = min(dt, self.duration - self.time)
            end = self.time + step
            while self._next_emission * self.emission_period <= end:
                emitted = self._next_emission * self.emission_period
                if emitted >= self.duration:
                    break
                x = self.position + velocity * (emitted - self.time)
                self.fronts.append(Wavefront(emitted, x, velocity))
                self._next_emission += 1
            self.position += velocity * step
            self.time = end
            dt = max(0.0, dt - step)
            if self.time >= self.duration:
                self.reset()

    def radius(self, front):
        return self.time - front.emitted_at


def orbital_projection(mass_jupiter, separation_au, inclination_deg, phase):
    """Posición estelar x,z (m) y velocidad radial (m/s) coherentes.

    Observador distante en z negativo; z positivo = alejamiento.
    Proyección lateral: a inclinación cero todo el movimiento queda sobre x.
    """
    period, radius, amplitude = circular_orbit(mass_jupiter, separation_au, inclination_deg)
    x = -radius * math.cos(phase)
    z = -radius * math.sin(math.radians(inclination_deg)) * math.sin(phase)
    radial_velocity = -amplitude * math.cos(phase)
    return x, z, radial_velocity
