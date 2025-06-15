# ...existing code...
from flask import render_template, abort, request, redirect, url_for, flash
import datetime # Import the datetime module
from app import app # Flask app instance
import json
import os
import re
import markdown
import frontmatter
# Dummy project data


PROJECTS_JSON_PATH = os.path.join(app.root_path, 'projects.json')
with open(PROJECTS_JSON_PATH, "r") as f:
    PROJECTS = json.load(f)

@app.context_processor
def inject_current_year():
    """Injects the current year into all templates."""
    return {'current_year': datetime.datetime.now().year}

BLOG_POSTS_DIR = os.path.join(app.root_path, 'blog_posts')

def generate_slug(title_str):
    """Generates a URL-friendly slug from a title."""
    if not title_str:
        return "untitled-post"
    slug = title_str.lower()
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with hyphens
    slug = re.sub(r'[^\w\-]+', '', slug)  # Remove non-alphanumeric (excluding hyphen)
    slug = re.sub(r'\-\-+', '-', slug)  # Replace multiple hyphens with single
    slug = slug.strip('-')  # Remove leading/trailing hyphens
    if not slug: # If slug becomes empty after sanitization
        # Fallback to a unique slug using timestamp
        return f"post-{int(datetime.datetime.now().timestamp())}"
    return slug

def load_blog_posts():
    """Loads and parses all blog posts from the BLOG_POSTS_DIR."""
    posts_data = []
    if not os.path.isdir(BLOG_POSTS_DIR):
        app.logger.warning(f"Blog posts directory not found: {BLOG_POSTS_DIR}")
        return []

    for filename in os.listdir(BLOG_POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(BLOG_POSTS_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    post_fm_object = frontmatter.load(f) # frontmatter.Post object

                metadata = post_fm_object.metadata # Dictionary of frontmatter

                if 'title' not in metadata or 'date' not in metadata:
                    app.logger.warning(f"Skipping {filename}: missing title or date in frontmatter.")
                    continue

                # Process date
                raw_date = metadata['date']
                date_obj = None
                if isinstance(raw_date, datetime.datetime):
                    date_obj = raw_date
                elif isinstance(raw_date, datetime.date):
                    date_obj = datetime.datetime.combine(raw_date, datetime.datetime.min.time())
                elif isinstance(raw_date, str):
                    try:
                        date_obj = datetime.datetime.strptime(raw_date, '%Y-%m-%d')
                    except ValueError:
                        app.logger.warning(f"Could not parse date string '{raw_date}' for {filename}. Using current date as fallback.")
                        date_obj = datetime.datetime.now() # Fallback
                else:
                    app.logger.warning(f"Unknown date format for {filename}: {raw_date}. Using current date as fallback.")
                    date_obj = datetime.datetime.now() # Fallback

                current_post = {
                    **metadata, # Unpack all metadata
                    'slug': metadata.get('slug') or generate_slug(metadata['title']),
                    'date_obj': date_obj,
                    'content_html': markdown.markdown(post_fm_object.content)
                }
                posts_data.append(current_post)
            except Exception as e:
                app.logger.error(f"Error processing blog post {filename}: {e}")
    
    posts_data.sort(key=lambda p: p['date_obj'], reverse=True) # Newest first
    return posts_data

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

@app.route("/blog")
def blog():
    posts = load_blog_posts()
    return render_template("blog.html", posts=posts)

@app.route("/blog/<slug>")
def blog_post_detail(slug):
    # Consider caching posts if performance becomes an issue
    posts = load_blog_posts()
    post = next((p for p in posts if p.get("slug") == slug), None)
    if not post:
        abort(404)
    return render_template("blog_post_detail.html", post=post)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        description = request.form.get('description')

        # Basic validation
        if not first_name or not description:
            flash('Both First Name and Description are required.', 'danger') # 'danger' for Bootstrap error styling
            # Pass current form data back to pre-fill the form
            return render_template('contact.html', form_data=request.form)

        # --- Placeholder for sending email ---
        # In a real application, you would integrate an email library like Flask-Mail here.
        # For example:
        # 1. Install Flask-Mail: pip install Flask-Mail
        # 2. Configure Flask-Mail in your app/__init__.py or a config file (see notes below).
        # 3. Import and use the Mail object:
        #    from flask_mail import Message
        #    from app import mail # Assuming 'mail' is your initialized Flask-Mail instance
        #    msg = Message("New Contact Form Submission from your website",
        #                  sender="your_configured_sender_email@example.com", # This should be an email you control
        #                  recipients=["contact@muhammad-luqman.com"])
        #    msg.body = f"First Name: {first_name}\n\nDescription:\n{description}"
        #    mail.send(msg)
        print(f"Simulating email send to contact@muhammad-luqman.com:")
        print(f"First Name: {first_name}")
        print(f"Description: {description}")

        flash('Thank you! Your message has been received.', 'success')
        return redirect(url_for('contact')) # Redirect to clear form and prevent re-submission

    return render_template("contact.html", form_data={}) # Pass empty dict for initial GET
# ...existing code...
