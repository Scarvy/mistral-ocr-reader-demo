import tempfile
import webbrowser
import jinja2


def render_clean_html_compare(original_html: str, modified_html: str, title: str):
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        autoescape=jinja2.select_autoescape(["html"]),
    )
    template = jinja_env.get_template("clean_html_preview-compare.html")
    rendered_html = template.render(
        original_html=original_html, modified_html=modified_html, title=title
    )
    return rendered_html


def render_clean_html_single(original_html: str, title: str):
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        autoescape=jinja2.select_autoescape(["html"]),
    )
    template = jinja_env.get_template("clean_html_preview-single.html")
    rendered_html = template.render(html=original_html, title=title)
    return rendered_html


def serve_html(html):
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
        file_path = f.name  # Save the path before closing the file
        f.write(html)

    webbrowser.open(f"file://{file_path}")
