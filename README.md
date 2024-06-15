# Ospredje za Delilnico

Spletna aplikacija, ki se ukvarja s spletno stranjo Delilnice in pripadajočo komunikacijo z zaledjem.

Osnovana je na Flasku za ključne strani (ogled in dodajanje fragmenta, registracija, administracija), preostanek pa je zaradi hitrejšega povratnega odziva izdelan z Javascriptom. Flask tudi nudi spletni strežnik.

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
