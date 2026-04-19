Aquest srpint l'he fet en una màquina virtual Ubuntu 24.04

El primer que vaig fer, va ser si ja tenia instal·lat de fàbric el python, i com que ja el tenia, vaig passar a crear i activar un nou entorn virtual.

Seguidament, vaig agafar tot el repositori del GitHub, i me'l vaig clonar i seguidament passar-lo al Visual Studio per a treballar de forma més còmoda.

Vaig començar per el backend, instal·lant els requirements.txt, que el vaig agafar del repositori oficial de GitHub de FastAPI, cosa, que només vaig modificar l'última línea.
Després amb el app.py, per a tindre'l de tal forma de que tingui connectada la base de dades (MongoDB Altas).
També he fet una modificació al backend, que és el fitxer .env, el qual fa que no tinguis que posar manualment cada cop que arrnaques la màquina per connectar el backend al frontend, cosa que t'ho automaititza, i et lleva mals de cap.
Un cop creat tot el backend, fent testos de que funciona tot, passariem a fer el fontend.

Al frontend, creenm un html i css (sketleton) simples, i també un javascript, el més important és el javascript, ja que és el que connectem el backend amb el propi frontend, per a que pugui funcionar correctament amb les 4 funcionalitats CRUD, que en el meu cas sería crear, llegir, editar i esborrar les pel·lícules.

Finalment, anem al Postman, i allí farem 5 operacions, la primera es fer 2 tipus de GET, un de normal i l'altre filtrant el id de la pel·lícula en el meu cas, seguidament, fem un post per a llegir-ho, fem un PUT

ERRORS QUE HE TINGUT: 
