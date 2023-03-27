implementation details with versioning

# MQTT teszt környezet felállítása 
Tartalmaz:1 broker, 1 subsriber, 1 publisher

Mindegyik egy külön docker konténerben
A broker 1883 porton lesz majd elérhető

.env.example nevezd át .env 
Ezt a fájlt kikell tölteni és majd egy új felhasználót létre kell hozzni a brokeren az .env fájl alapján

Alábbi parancsokat a `test` mappában szükséges kiadni
 
Alábbi parancsot kiadva a `test` mappában a környezet feláll.
```
docker-compose up -d
```
Új felhasználó létrehozzása brokeren, szintén a `test` mappában
```
docker-compose exec broker mosquitto_passwd -c /mosquitto/config/mosquitto.passwd <Username>
```
Felhasználó törlése
```
docker-compose exec broker mosquitto_passwd -D /mosquitto/config/mosquitto.passwd <Username>
```
Felhasználó változása esetén szükséges lehet egy újraindítás
```
docker-compose restart
```