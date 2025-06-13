# ...existing code...
from flask import render_template, abort
import datetime # Import the datetime module
from app import app

# Dummy project data
PROJECTS = [
    {
        "slug": "ai-chatbot",
        "title": "AI Chatbot",
        "logo": "img/logos/miku.jpeg", # Assuming logos are in static/img/logos
        "view_type": "video",
        "video_link": "https://www.youtube.com/embed/dQw4w9WgXcQ?si=lEFaTBriE7Urk9WU", # Example YouTube embed
        "description_markdown": """
An AI-powered chatbot using Large Language Models (LLMs) and a Flask backend.

**Key Features:**
*   Intent Recognition
*   Contextual Memory
*   API Integration for external services
*   Scalable architecture
        """,
        "github": "https://github.com/luqman/ai-chatbot",
        "demo": "https://ai-chatbot-demo.example.com"
    },
    {
        "slug": "portfolio-website",
        "title": "Portfolio Website",
        "logo": "img/logos/miku.jpeg",
        "view_type": "pseudo_demo", # Changed to pseudo_demo
        "description_markdown": """
My personal portfolio website, built with Python (Flask) and Bootstrap 5.

**Highlights:**
*   Responsive design for all devices.
*   Dynamic project showcase (you're looking at it!).
*   Clean and modern UI.
        """,
        "samples": [
            {
                "name": "Homepage View",
                "thumbnail_url": "img/logos/miku.jpeg", # Example path
                "output_url": "img/samples/rem.jpg",    # Example path
                "output_type": "image"
            },
            {
                "name": "Projects Page",
                "thumbnail_url": "img/logos/miku.jpeg",
                "output_url": "img/samples/rem.jpg",
                "output_type": "image"
            }
        ],
        "github": "https://github.com/luqman/portfolio",
        "demo": ""
    },
    {
        "slug": "data-pipeline",
        "title": "Data Pipeline",
        "logo": "img/logos/miku.jpeg",
        "view_type": "video", # Can be 'video' even if no video_link, will show message
        "video_link": "https://www.youtube.com/embed/dQw4w9WgXcQ?si=lEFaTBriE7Urk9WU", # No video available, template will handle this
        "description_markdown": """
An ETL (Extract, Transform, Load) pipeline designed for processing and managing large datasets efficiently.

**Technologies Used:**
*   Python for scripting and data manipulation.
*   Apache Airflow for workflow orchestration.
*   Integration with various data sources and destinations.
        """,
        "github": "",
        "demo": ""
    },
    {
        "slug": "cv-object-detection",
        "title": "CV Object Detection Demo",
        "logo": "img/logos/miku.jpeg", # Example path
        "view_type": "pseudo_demo",
        "description_markdown": """
A pseudo-live demo showcasing an object detection model. Select different input images or short video clips to see the model's output.
This demonstrates the model's capability to identify and locate various objects within a scene.
        """,
        "samples": [
            {"name": "Street Scene (Image)", "thumbnail_url": "img/logos/miku.jpeg", "output_url": "img/samples/rem.jpg", "output_type": "image"},
            {"name": "Traffic Flow (Video)", "thumbnail_url": "img/logos/miku.jpeg", "output_url": "https://www.youtube.com/embed/dQw4w9WgXcQ?si=lEFaTBriE7Urk9WU", "output_type": "video"},
            {"name": "Indoor Objects (Image)", "thumbnail_url": "img/logos/miku.jpeg", "output_url": "img/samples/rem.jpg", "output_type": "image"}
        ],
        "github": "https://github.com/luqman/cv-object-detection",
        "demo": ""
    }
]

@app.context_processor
def inject_current_year():
    """Injects the current year into all templates."""
    return {'current_year': datetime.datetime.now().year}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects/<slug>")
def project_detail(slug):
    project = next((p for p in PROJECTS if p["slug"] == slug), None)
    if not project:
        abort(404)
    return render_template("project_detail.html", project=project)
# ...existing code...
