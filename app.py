"""A small, server-rendered scientific calculator."""

import ast
import math
import operator
import os

from flask import Flask, render_template, request, session


class CalculatorError(ValueError):
    """An expression is invalid or outside the calculator's supported range."""


class SafeEvaluator(ast.NodeVisitor):
    """Evaluate arithmetic syntax without exposing Python execution."""

    binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    unary_operators = {ast.UAdd: operator.pos, ast.USub: operator.neg}
    constants = {"pi": math.pi, "e": math.e}
    functions = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sqrt": math.sqrt,
        "root": None,
        "log": math.log10,
        "ln": math.log,
    }

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculatorError("Only numbers are allowed.")
        return self.checked(node.value)

    def visit_Name(self, node):
        if node.id not in self.constants:
            raise CalculatorError("Unknown constant.")
        return self.constants[node.id]

    def visit_UnaryOp(self, node):
        operation = self.unary_operators.get(type(node.op))
        if operation is None:
            raise CalculatorError("That operator is not supported.")
        return self.checked(operation(self.visit(node.operand)))

    def visit_BinOp(self, node):
        operation = self.binary_operators.get(type(node.op))
        if operation is None:
            raise CalculatorError("That operator is not supported.")
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise CalculatorError("That power is too large.")
        return self.checked(operation(left, right))

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name) or node.func.id not in self.functions:
            raise CalculatorError("Unknown function.")
        if node.keywords:
            raise CalculatorError("Functions take positional values only.")

        arguments = [self.visit(argument) for argument in node.args]
        if node.func.id == "root":
            if len(arguments) != 2 or arguments[0] == 0:
                raise CalculatorError("Use root(degree, value) with a nonzero degree.")
            degree, value = arguments
            if value < 0 and float(degree).is_integer() and int(degree) % 2:
                return self.checked(-((-value) ** (1 / degree)))
            return self.checked(value ** (1 / degree))
        if len(arguments) != 1:
            raise CalculatorError("Functions take one value.")
        return self.checked(self.functions[node.func.id](*arguments))

    def generic_visit(self, node):
        raise CalculatorError("That expression is not supported.")

    @staticmethod
    def checked(value):
        if isinstance(value, complex) or not math.isfinite(value):
            raise CalculatorError("The result is outside the supported range.")
        return value


def evaluate(expression):
    """Return a compact result for a supported arithmetic expression."""
    if not expression or len(expression) > 120:
        raise CalculatorError("Enter an expression up to 120 characters.")

    normalized = expression.replace("^", "**")
    try:
        tree = ast.parse(normalized, mode="eval")
        if sum(1 for _ in ast.walk(tree)) > 80:
            raise CalculatorError("That expression is too complex.")
        result = SafeEvaluator().visit(tree)
        return format(result, ".12g")
    except CalculatorError:
        raise
    except (ArithmeticError, SyntaxError, TypeError, ValueError, OverflowError, RecursionError) as error:
        raise CalculatorError("Check the expression and try again.") from error


THEME = "cobalt"
KEYS = {
    "sin": "sin(", "cos": "cos(", "tan": "tan(",
    "asin": "asin(", "acos": "acos(", "atan": "atan(",
    "sqrt": "sqrt(", "root": "root(", "log": "log(", "ln": "ln(",
    "square": "^2", "cube": "^3", "pi": "pi", "e": "e",
    "open": "(", "close": ")", "decimal": ".",
    "add": "+", "subtract": "-", "multiply": "*", "divide": "/",
    "power": "^", "modulo": "%", "zero": "0", "one": "1",
    "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9",
}

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-only-change-me")

from portfolio import portfolio

app.register_blueprint(portfolio)


def apply_key():
    expression = request.form.get("expression", session.get("expression", ""))
    expression = expression[:120]
    key = request.form.get("key", "")
    result = session.get("result")
    error = None

    if request.method == "POST":
        if key == "clear":
            expression, result = "", None
        elif key == "backspace":
            expression, result = expression[:-1], None
        elif key == "equals":
            try:
                result = evaluate(expression)
            except CalculatorError as calculation_error:
                error = str(calculation_error)
                result = None
        else:
            expression = (expression + KEYS.get(key, ""))[:120]
            result = None

    session["expression"] = expression
    session["result"] = result
    return expression, result, error


@app.get("/")
def calculator():
    return render_template("index.html", theme=THEME)


@app.route("/display", methods=["GET", "POST"])
def display():
    if request.method == "POST":
        expression, result, error = apply_key()
    else:
        expression = session.get("expression", "")
        result = session.get("result")
        error = None
    return render_template(
        "display.html", expression=expression, result=result, error=error, theme=THEME
    )


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")