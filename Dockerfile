FROM debian
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TOKEN
ENV TEXT_FILE text.txt
ENV IMAGE_DIR images
ENV FONT_FILE Lobster-Regular.ttf
ENV REPOST_CHANNEL
WORKDIR /app/
COPY . .
RUN apt update && apt install -y --no-install-recommends python3-minimal python3-setuptools python3-pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "main.py" ]
