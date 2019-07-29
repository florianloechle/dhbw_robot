import unittest
from components.engine import Engine, Claw, Lift, Drive

class TestUtilsMethods(unittest.TestCase):

    def test_engine_initilizes_correctly(self):
        test_engine = Engine((1,2,3))
        self.assertEqual(test_engine.pin1, 1)
        self.assertEqual(test_engine.pin2, 2)
        self.assertEqual(test_engine.pinPWM, 3)

    def test_engine_has_correct_api(self):
        test_engine = Engine((1,2,3))
        self.assertIsNotNone(test_engine.forward)
        self.assertIsNotNone(test_engine.backward)
        self.assertIsNotNone(test_engine.stop)
        self.assertIsNotNone(test_engine.power)

    def test_engine_sets_states_correctly(self):
        test_engine = Engine((1,2,3))
        test_engine.forward(50)
        self.assertEquals(test_engine.power,50)

        test_engine.backward(25)
        self.assertEquals(test_engine.power,25)

        test_engine.stop()
        self.assertEquals(test_engine.power,0)