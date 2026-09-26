import unittest

from app import CalculatorError, app, evaluate


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.client = app.test_client()

    def test_arithmetic_precedence_parentheses_and_exponents(self):
        self.assertEqual(evaluate("2 + 3 * (4 - 1)"), "11")
        self.assertEqual(evaluate("2**3"), "8")
        self.assertEqual(evaluate("5 % 2"), "1")
        self.assertEqual(evaluate("-2**2"), "-4")
        self.assertEqual(evaluate("sqrt(81)"), "9")
        self.assertEqual(evaluate("sin(pi / 2)"), "1")
        self.assertEqual(evaluate("log(100)"), "2")
        self.assertEqual(evaluate("ln(e)"), "1")
        self.assertEqual(evaluate("root(3, -8)"), "-2")

    def test_rejects_unsupported_python_and_unsafe_values(self):
        for expression in (
            "__import__('os')",
            "open(1)",
            "True + 1",
            "2 ** 1001",
            "sqrt(-1)",
            "1 / 0",
        ):
            with self.subTest(expression=expression), self.assertRaises(CalculatorError):
                evaluate(expression)

    def test_home_page_has_visual_keys_and_no_javascript(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Fieldnote Calculator", response.data)
        self.assertIn(b'name="key" value="equals"', response.data)
        self.assertIn(b'target="calculator-display"', response.data)
        self.assertNotIn(b"<script", response.data)

    def test_keypad_submission_and_calculation(self):
        response = self.client.post("/display", data={"expression": "2+3*4", "key": "equals"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"=</span> 14", response.data)
        self.assertIn(b'data-theme="cobalt"', response.data)

    def test_keypad_updates_session_between_display_posts(self):
        for expression, key in (("", "seven"), ("7", "multiply"), ("7*", "six")):
            self.client.post("/display", data={"expression": expression, "key": key})
        response = self.client.post("/display", data={"key": "equals"})
        self.assertIn(b"=</span> 42", response.data)


if __name__ == "__main__":
    unittest.main()