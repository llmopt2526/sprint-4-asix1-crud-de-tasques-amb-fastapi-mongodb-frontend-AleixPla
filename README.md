README Aleix Pla


Aquest srpint l'he fet en una màquina virtual Ubuntu 24.04

El primer que vaig fer, va ser si ja tenia instal·lat de fàbric el python, i com que ja el tenia, vaig passar a crear i activar un nou entorn virtual.

Seguidament, vaig agafar tot el repositori del GitHub, i me'l vaig clonar i seguidament passar-lo al Visual Studio per a treballar de forma més còmoda.

Vaig començar per el backend, instal·lant els requirements.txt, que el vaig agafar del repositori oficial de GitHub de FastAPI, cosa, que només vaig modificar l'última línea.
Després amb el app.py, per a tindre'l de tal forma de que tingui connectada la base de dades (MongoDB Altas).
També he fet una modificació al backend, que és el fitxer .env, el qual fa que no tinguis que posar manualment cada cop que arrnaques la màquina per connectar el backend al frontend, cosa que t'ho automaititza, i et lleva mals de cap.
Un cop creat tot el backend, fent testos de que funciona tot, passariem a fer el fontend.

Al frontend, creenm un html i css (sketleton) simples, i també un javascript, el més important és el javascript, ja que és el que connectem el backend amb el propi frontend, per a que pugui funcionar correctament amb les 4 funcionalitats CRUD, que en el meu cas sería crear, llegir, editar i esborrar les pel·lícules.

Finalment, anem al Postman, i allí farem 5 operacions, la primera es fer 2 tipus de GET, un de normal i l'altre filtrant el id de la pel·lícula en el meu cas, seguidament, fem un post per a llegir-ho, fem un PUT per a actulilitzar-ho, que com ho tinc al fitxer app.py, només es pot modificar l'estat de la pel·lícula, és a dir, que si està pendent de veure o si ja està vista, i finalment per a esborrar les pel·lícules.

També he grabat un petit vídeo, fent proves al frontend, el que he fet ha segut crear una pel·lícula, amb la seva respectiva informació als diferents camps, i un cop creada, editar-la i quan ja estava editada, esborrant-la.


ERRORS QUE HE TINGUT: 

He tingut algunes petites inconveniències, pero les he pogut solucionar.
La primera, va ser que intentava fer proves al frontend i no hem funcionava, ja que no tenia l'etorn virtual en funcioanment.
L'altra, que tenía un error de sintaxi al fitxer app.py, en concret, a la línea 5, que tenia que afegir ().
I l'últim "error" (despiste) que he tingut és que cada cop que encens la màquina tens que posar el "MONGO_URL=..." i clar no el vaig posar i no hem funcionava de cap forma, el que vaig implementar per solucionar-ho va ser a partir del fitxer .env (explicat a la documentació de dalt), de forma que ja no s'ha de posar cada cop que encens la màquina aquesta comanda.
