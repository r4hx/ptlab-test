FROM python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TOKEN
ENV TEXT_FILE text.txt
ENV IMAGE_DIR images
ENV FONT_FILE Lobster-Regular.ttf
ENV REPOST_CHANNEL
WORKDIR /app/
COPY . .
RUN apt update && apt install -y libgl1-mesa-dev
RUN python3 -m pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "main.py" ]
