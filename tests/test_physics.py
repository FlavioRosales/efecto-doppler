import math
import unittest
from physics import doppler_factor, circular_orbit, WaveSimulation, orbital_projection

class PhysicsTests(unittest.TestCase):
    def test_rest_and_reciprocity(self):
        self.assertEqual(doppler_factor(0), 1)
        self.assertAlmostEqual(doppler_factor(3000)*doppler_factor(-3000), 1)

    def test_relativistic_limit(self):
        self.assertAlmostEqual(doppler_factor(299792.458*0.6), 2)
        with self.assertRaises(ValueError):
            doppler_factor(299792.458)

    def test_earthlike_period_and_jupiter_signal(self):
        period, _, amplitude = circular_orbit(1, 1, 90)
        self.assertAlmostEqual(period/86400, 365.1, delta=0.3)
        self.assertAlmostEqual(amplitude, 28.4, delta=0.2)
        self.assertEqual(circular_orbit(1, 1, 0)[2], 0)
        self.assertAlmostEqual(circular_orbit(1, 4, 90)[0]/period, 8)

class WaveHistoryTests(unittest.TestCase):
    def test_velocity_reversal_preserves_emission_history(self):
        sim = WaveSimulation()
        sim.advance(1, 0.8)
        old = tuple(sim.fronts)
        radii = [sim.radius(f) for f in old]
        sim.advance(1, -0.8)
        self.assertEqual(tuple(sim.fronts[:len(old)]), old)
        self.assertAlmostEqual(sim.position, 0)
        for front, radius in zip(old, radii):
            self.assertAlmostEqual(sim.radius(front), radius + 1)
        self.assertAlmostEqual(sim.fronts[3].position, .8 - .8*(1.35-1))

    def test_stopping_does_not_move_existing_centers(self):
        sim = WaveSimulation()
        sim.advance(1, .5)
        sim.advance(1, 0)
        self.assertAlmostEqual(sim.position, .5)
        self.assertAlmostEqual(sim.fronts[1].position, .225)
        self.assertAlmostEqual(sim.fronts[-1].position, .5)

    def test_frame_rate_does_not_change_constant_speed_solution(self):
        a, b = WaveSimulation(), WaveSimulation()
        a.advance(4, .8)
        for _ in range(400):
            b.advance(.01, .8)
        self.assertEqual(len(a.fronts), len(b.fronts))
        for fa, fb in zip(a.fronts, b.fronts):
            self.assertAlmostEqual(fa.position, fb.position)
        self.assertAlmostEqual(a.position, b.position)

    def test_cycle_resets_at_fifteen_seconds_with_remainder(self):
        sim = WaveSimulation()
        sim.advance(14.9, .8)
        self.assertGreater(sim.position, 11)
        sim.advance(.2, -.8)
        self.assertAlmostEqual(sim.time, .1)
        self.assertAlmostEqual(sim.position, -.08)
        self.assertEqual(len(sim.fronts), 1)

class OrbitProjectionTests(unittest.TestCase):
    def test_face_on_has_only_lateral_motion(self):
        positions = [orbital_projection(1, 1, 0, a) for a in (0, .5, 1, 2)]
        self.assertGreater(len({x for x, _, _ in positions}), 1)
        for _, z, radial in positions:
            self.assertEqual(z, 0)
            self.assertEqual(radial, 0)

    def test_graphed_velocity_matches_position_derivative(self):
        for inc in (0, 30, 90):
            period, _, _ = circular_orbit(1, 1, inc)
            omega = 2*math.pi/period
            for angle in (0, .4, 2, 4):
                delta = 1e-5
                _, z1, _ = orbital_projection(1, 1, inc, angle-delta)
                _, z2, _ = orbital_projection(1, 1, inc, angle+delta)
                _, _, radial = orbital_projection(1, 1, inc, angle)
                derivative = (z2-z1)/(2*delta)*omega
                self.assertAlmostEqual(radial, derivative, places=7)

if __name__ == '__main__':
    unittest.main()
