# Kontejner za ospredje Delilnice
# docker build -t delilnica/ospredje .
# docker run -it -p 5000:5000 --rm delilnica/ospredje

FROM python:3.10

WORKDIR /delilnica

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY static static/
COPY templates templates/
COPY delilnica.py ./

EXPOSE 5000
CMD ["flask", "--debug", "--app", "delilnica", "run", "--host=0.0.0.0"]
