import json
import tempfile
import base64

from werkzeug.wsgi import wrap_file
from werkzeug.wrappers import Request, Response
from executor import execute


@Request.application
def application(request):
    """
    To use this application, the user must send a POST request with
    base64 or form encoded encoded HTML content and the wkhtmltopdf Options in
    request data, with keys 'base64_html' and 'options'.
    The application will return a response with the PDF file.
    """
    if request.method != "POST":
        return
    if request.content_type != "application/json":
        return

    payload = json.loads(request.data)

    options = payload.get("options", {})

    source_file = tempfile.NamedTemporaryFile(suffix=".html")
    source_file.write(base64.b64decode(payload["contents"]))
    source_file.flush()

    header_file = None
    if "header" in payload:
        header_file = tempfile.NamedTemporaryFile(suffix=".html")
        header_file.write(base64.b64decode(payload["header"]))
        header_file.flush()

    footer_file = None
    if "footer" in payload:
        footer_file = tempfile.NamedTemporaryFile(suffix=".html")
        footer_file.write(base64.b64decode(payload["footer"]))
        footer_file.flush()

    # Evaluate argument to run with subprocess
    args = ["wkhtmltopdf"]

    # Add Global Options
    if options:
        for option, value in options.items():
            args.append(f"--{option}")
            if value:
                args.append(f'"{value}"')

    if header_file:
        args.append("--header-html")
        args.append(f'"{header_file.name}"')
    if footer_file:
        args.append("--footer-html")
        args.append(f'"{footer_file.name}"')

    # Add source file name and output file name
    file_name = source_file.name
    args += [file_name, file_name + ".pdf"]

    # Execute the command using executor
    execute(" ".join(args))

    source_file.close()
    if header_file:
        header_file.close()
    if footer_file:
        footer_file.close()

    return Response(
        wrap_file(request.environ, open(file_name + ".pdf", "rb")), mimetype="application/pdf",
    )


if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("127.0.0.1", 5000, application,
               use_debugger=True, use_reloader=True)
