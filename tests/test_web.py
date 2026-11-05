import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / 'app.py')

class WebTests(unittest.TestCase):
    def test_navigation_controls_pause_and_reset(self):
        app = AppTest.from_file(APP).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.radio[0].value, 'Ondas y movimiento')
        app.slider(key='wave').set_value(.8).run()
        app.checkbox(key='paused').check().run()
        self.assertTrue(app.session_state['simulation']['paused'])
        app.button[0].click().run()
        self.assertEqual(app.slider(key='wave').value, 0)
        app.radio[0].set_value('Medir una estrella').run()
        app.slider(key='velocity').set_value(-3000).run()
        self.assertFalse(app.exception)
        app.radio[0].set_value('Descubrir un planeta').run()
        app.slider(key='inclination').set_value(0).run()
        self.assertFalse(app.exception)
        app.radio[0].set_value('Medir una estrella').run()
        self.assertEqual(app.slider(key='velocity').value, -3000)

    def test_visitors_have_independent_state(self):
        first = AppTest.from_file(APP).run()
        first.slider(key='wave').set_value(.8).run()
        second = AppTest.from_file(APP).run()
        self.assertEqual(second.slider(key='wave').value, 0)
        self.assertIsNot(first.session_state['simulation'], second.session_state['simulation'])
