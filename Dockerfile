FROM gorialis/discord.py:minimal
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app/tmp && mkdir -p /usr/src/app/zip
COPY . .
RUN pip install -r requirements.txt --upgrade
CMD ["python", "main.py"]