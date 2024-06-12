# Ospredje za Delilnico

Aplikacija, izdelana v deloma z Javascriptom in deloma s Flaskom, ki se ukvarja s spletno stranjo Delilnice in pripadajočo komunikacijo z zaledjem.

## Zagon iz ukazne vrstice

```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt

$ ./zagon
```

## Zagon prek Dockerja

```
$ docker build -t delilnica/ospredje .
$ docker run -it -p 5000:5000 --rm delilnica/ospredje
```
