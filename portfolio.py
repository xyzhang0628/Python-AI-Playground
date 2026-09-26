"""Server-rendered sample designer portfolio."""

from flask import Blueprint, abort, render_template, send_from_directory


portfolio = Blueprint("portfolio", __name__, url_prefix="/designer")

PROFILE = {
    "name": "Mina Park",
    "email": "hello@minapark.design",
    "location": "Brooklyn, New York",
}

PROJECTS = [
    {
        "number": "01",
        "name": "A more human map",
        "type": "DIGITAL PRODUCT · WAYFINDING",
        "description": "Helping people make sense of a place before they arrive.",
        "image": "Group 634399.png",
        "tone": "blue",
        "art": "photo",
    },
    {
        "number": "02",
        "name": "The changing room",
        "type": "SPATIAL TECHNOLOGY · INTERACTION",
        "description": "A responsive environment that makes change easier to read.",
        "image": "Group 634400.png",
        "tone": "lilac",
        "art": "photo",
    },
    {
        "number": "03",
        "name": "Room to arrive",
        "type": "SERVICE DESIGN · PHYSICAL SPACE",
        "description": "A calmer arrival for a busy neighborhood care clinic.",
        "image": None,
        "tone": "peach",
        "art": "arrival",
    },
    {
        "number": "04",
        "name": "Signals in the city",
        "type": "VISUAL SYSTEM · PUBLIC REALM",
        "description": "A flexible visual language for navigating public places.",
        "image": None,
        "tone": "yellow",
        "art": "signals",
    },
    {
        "number": "05",
        "name": "Small decisions",
        "type": "DIGITAL PRODUCT · RESEARCH",
        "description": "Making the next useful action feel like the obvious one.",
        "image": None,
        "tone": "green",
        "art": "decisions",
    },
    {
        "number": "06",
        "name": "A softer landing",
        "type": "EXPERIENCE DESIGN · SPATIAL",
        "description": "A thoughtful transition between the digital and the physical.",
        "image": None,
        "tone": "pink",
        "art": "landing",
    },
]

EXTRAS = [
    {"number": "01", "name": "Collected colors", "type": "PHOTOGRAPHY", "image": "Group 634399.png", "tone": "blue"},
    {"number": "02", "name": "Things in a row", "type": "VISUAL STUDY", "image": None, "tone": "lilac"},
    {"number": "03", "name": "A city in fragments", "type": "PHOTO NOTES", "image": "Group 634400.png", "tone": "peach"},
    {"number": "04", "name": "Room for a thought", "type": "SPATIAL SKETCH", "image": None, "tone": "yellow"},
    {"number": "05", "name": "Soft geometry", "type": "GRAPHIC EXPERIMENT", "image": None, "tone": "green"},
    {"number": "06", "name": "After the rain", "type": "FIELD NOTES", "image": None, "tone": "pink"},
]

VIEWS = {"work", "extra", "about"}
ASSETS = {"Group 634399.png", "Group 634400.png"}


@portfolio.get("/")
def work():
    return render_template(
        "portfolio.html", view="work", profile=PROFILE, projects=PROJECTS, extras=EXTRAS
    )


@portfolio.get("/<view>")
def page(view):
    if view not in VIEWS - {"work"}:
        abort(404)
    return render_template(
        "portfolio.html", view=view, profile=PROFILE, projects=PROJECTS, extras=EXTRAS
    )


@portfolio.get("/assets/<path:filename>")
def asset(filename):
    if filename not in ASSETS:
        abort(404)
    return send_from_directory("Home page images", filename)


@portfolio.get("/resume")
def resume():
    contents = (
        "MINA PARK | DESIGNER\n"
        "\n"
        "Practice\n"
        "Digital products, physical environments, spatial technology, and wayfinding.\n"
        "\n"
        "Approach\n"
        "Research, prototyping, visual systems, and interaction design.\n"
        "\n"
        f"Contact\n{PROFILE['email']}\n"
        "\n"
        "Sample portfolio résumé. Replace this placeholder with the designer's verified details.\n"
    )
    return contents, 200, {
        "Content-Type": "text/plain; charset=utf-8",
        "Content-Disposition": 'attachment; filename="mina-park-resume.txt"',
    }