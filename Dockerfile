FROM python:3.8-slim

RUN apt-get update
# Download and install wkhtmltopdf
RUN apt-get install -y --no-install-recommends wget fontconfig libfreetype6 libpng16-16 libjpeg62-turbo libx11-6 libxcb1 libxext6 libxrender1 xfonts-75dpi xfonts-base
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb

# Install custom fonts
RUN mkdir -p /usr/share/fonts/opentype/cambon
COPY fonts/Cambon-Demi.otf /usr/share/fonts/opentype/cambon
COPY fonts/Cambon-DemiItalic.otf /usr/share/fonts/opentype/cambon
RUN chmod 644 /usr/share/fonts/opentype/cambon/*

RUN mkdir -p /usr/share/fonts/truetype/inter
COPY fonts/Inter-Regular.ttf /usr/share/fonts/truetype/inter
COPY fonts/Inter-SemiBold.ttf /usr/share/fonts/truetype/inter
RUN chmod 644 /usr/share/fonts/truetype/inter/*

# Install dependencies for running web service
RUN pip install werkzeug executor gunicorn

ADD app.py /app.py
EXPOSE 80

ENTRYPOINT ["/usr/local/bin/gunicorn"]

# Show the extended help
CMD ["-b", "0.0.0.0:80", "--log-file", "-", "app:application"]
