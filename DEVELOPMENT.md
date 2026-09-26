# Development Notes

## Requirements

- Python 3.10 or later
- Flask 3.x
- A web browser; the calculator uses HTML forms and CSS, with no JavaScript

## Setup and run

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
flask --app app run --debug
```

Open <http://127.0.0.1:5000/>. On Windows, activate the environment with
`.venv\Scripts\activate` instead of the second command above.

Set `SECRET_KEY` to a private random value before deployment. The built-in
development key is only suitable for local use. Leave debug mode off in a
deployed environment.

## Checks

Run the calculator and request tests with:

```sh
python -m unittest discover -s tests -v
```

The evaluator parses a limited arithmetic grammar and visits only numeric
constants, the `pi` and `e` constants, arithmetic operators, and an explicit
list of mathematical functions. It never executes user input as Python code.
Expressions are limited to 120 characters and powers are range-checked.

## Development steps

1. Translate the requirements into the supported controls: arithmetic,
   parentheses, powers and roots, trigonometry and inverse trigonometry,
   logarithms, `pi`, and `e`.
2. Create a Flask route that retains the expression and result in the signed
   session cookie between HTML form submissions; target submissions at the
   display frame so the keypad and page shell remain in place without scripts.
3. Implement an AST-based evaluator with a strict allowlist and friendly errors
   instead of using Python `eval`.
4. Build a semantic, responsive HTML keypad and display, with CSS-only visual
   states and no client-side scripts.
5. Add standard-library tests for arithmetic, rejected input, the no-script
   page, and a complete keypad submission.
6. Install dependencies from `requirements.txt`, run the tests, then start the
   local Flask development server.

## Designer portfolio

The sample designer portfolio is available at <http://127.0.0.1:5000/designer/>;
the calculator remains at <http://127.0.0.1:5000/>. Work, Extra, and About are
independent Flask-rendered pages. The portfolio uses HTML, CSS, and normal
navigation, with no client-side scripts. Its background glow shifts between
hovered regions using CSS; following the exact pointer position requires
JavaScript and is therefore not used. The page references Oscar Health's
publicly served TT Commons and Parafina fonts and Unsplash project photography.

Project names and the Mina Park profile are illustrative portfolio placeholders.
Replace the sample name, email, images, project descriptions, and downloadable
resume text in `portfolio.py` and `templates/portfolio.html` with the designer's
real content before publication. The standard library test suite covers both
the calculator and the portfolio routes.