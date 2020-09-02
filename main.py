# Andrés Cortez, Fernando Lavarreda, Valeria Paiz, Alejandro Ortega
# Universidad del Valle, Programacion Orientada a Objetos
# Punto de partida, programq que representa una aplicación para determinar si un usuario padece de alguna enfermedad
# mental.

import inicio as st
import analytics as ant

lectura = ant.LecturaArchivos()
lectura.leer_preguntas("resources/prueba1.txt")
aplicacion = st.App(lectura)
aplicacion.mainloop()
