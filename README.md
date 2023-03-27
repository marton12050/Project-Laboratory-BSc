Detailed instructions for use are in the report

<a href="https://github.com/marton12050/Project-Laboratory-BSc/blob/master/report.pdf"><img src="https://user-images.githubusercontent.com/28195267/228021549-beff7929-d1c4-4670-83f3-edcf048aab18.png"  width="180" ></a>

Guide in Hungary:
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
