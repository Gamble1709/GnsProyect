import pygame as pg, time

from pygame.locals import *

from Class import *

from Sprites import Icono, proyectil, desarrollador 

from Blocks import  bloques 

from Constants import ANCHO_PANTALLA, ALTO_PANTALLA, AZUL, BLANCO, ROJO, POSICIONES_LINEAS, bertram

from Sounds import *

import sys


def mostrarTexto(ventana, fuente, texto, tamanio, color, x, y):

    tipoFuente= pg.font.Font(fuente, tamanio)
    superficie= tipoFuente.render(texto, True, color) #El True es para el 'Aliased', que hace que el texto quede liso y no pixelado
    rectangulo= superficie.get_rect()
    rectangulo.x=x
    rectangulo.y=y
    ventana.blit(superficie, rectangulo)
    

#Iniciando Pygame
if __name__=="__main__":

    pg.init()



#Creación de ventana + ícono de la misma
Ventana=pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pg.display.set_icon(Icono)
    

#FPS
Fps=30
Reloj= pg.time.Clock()

#Tiempo del juego
tiempo= 500

#grupos de Sprites
sprites= pg.sprite.Group()
goombas= pg.sprite.Group()
magos= pg.sprite.Group()
caracoles= pg.sprite.Group()
bloquesBonus= pg.sprite.Group()
bloquesSimples= pg.sprite.Group()
bloquesDecoracion= pg.sprite.Group()
tuberias= pg.sprite.Group()
potenciadores= pg.sprite.Group()
proyectiles= pg.sprite.Group()


#======================Instanciaciones==========================00

#Creando bloques en orden
distanciaX=0
distanciaY=435

for x in range(75):
    sueloBasico= Bloque(bloques["Suelo"], distanciaX, distanciaY)
    bloquesSimples.add(sueloBasico)
    distanciaX+=45


#Creación de bloques vacíos (solo por decoración)

distanciaX=0
distanciaY+=23
cont=0

for x in range(80):
    
    bloque=Decoracion(bloques["Suelo"],distanciaX, distanciaY)
    bloquesDecoracion.add(bloque)

    distanciaX+=25
    cont+=1

    if cont==40:

        distanciaY+=23
        distanciaX=0



#Tuberías
nuevaTuberia= Bloque(bloques["Tuberia"], 900, 320)
tuberias.add(nuevaTuberia)

#Montañas
nuevaMontania= Decoracion(bloques["Montanias"][0], 100, 395)
bloquesDecoracion.add(nuevaMontania)

nuevaMontania= Decoracion(bloques["Montanias"][1], nuevaMontania.rect.right, 360 )
bloquesDecoracion.add(nuevaMontania)

#Nubes
nuevaNube= Decoracion(bloques["Nubes"][0], 300, 150)
bloquesDecoracion.add(nuevaNube)

nuevaNube= Decoracion(bloques["Nubes"][1], 500, 150)
bloquesDecoracion.add(nuevaNube)

#Árboles
arbol= Decoracion(bloques["Arbol"], 300, 350)
bloquesDecoracion.add(arbol)



#Instanciando personajePrincipalPrincipal principal
personajePrincipal=personaje()
sprites.add(personajePrincipal)


#Instanciación de enemigos    
nuevoEnemigo= Enemigo(700, 395)
goombas.add(nuevoEnemigo)


#Magos
nuevoMago= Mago(905, 340)
magos.add(nuevoMago)


#Instanciando Bloques
bonus= Bonus(bloques["Bonus"][0], 600, 275)
bloquesBonus.add(bonus)

#Instanciación de los potenciadores
hongos= Potenciador(desarrollador["Hongo"][0], bonus.rect.x, bonus.rect.y -3)
generacion=False

#Crear animación de subida y bajada bloque bonus (Pronto se pondrá en la clase para borrar este espacio)
animacionbonus=False
subir=-8
animacion=False


#Iniciar música de fondo
pg.mixer.music.play()

#========================== Bucle principal ===========================#

while True:

    Ventana.fill(AZUL)
    
    for eventos in pg.event.get():

        if eventos.type == QUIT:

            pg.quit()
            sys.exit()
            

    #Actualización de los sprites
    sprites.update()
    goombas.update()
    bloquesSimples.update()
    bloquesDecoracion.update()
    potenciadores.update()
    bloquesBonus.update()
    tuberias.update()
    proyectiles.update(personajePrincipal)
    magos.update()
    caracoles.update(personajePrincipal)


    #Dibujando sprites
    bloquesDecoracion.draw(Ventana)
    potenciadores.draw(Ventana)
    proyectiles.draw(Ventana)
    goombas.draw(Ventana)
    magos.draw(Ventana)
    bloquesBonus.draw(Ventana)
    tuberias.draw(Ventana)
    bloquesSimples.draw(Ventana)
    sprites.draw(Ventana)
    caracoles.draw(Ventana)


    #Mostrando texto
    pg.draw.rect(Ventana,(0,0,0), (350,5,325,53))

    for x in range(4):

        pg.draw.line(Ventana, ROJO, (POSICIONES_LINEAS[x][0], POSICIONES_LINEAS[x][1]), ( POSICIONES_LINEAS[x][2], POSICIONES_LINEAS[x][3]), 3)

    mostrarTexto(Ventana, bertram, "TIME", 25, BLANCO, 370, 23)
    mostrarTexto(Ventana, bertram, str(int(tiempo)), 25, BLANCO, 430, 23)
    mostrarTexto(Ventana, bertram, "SCORE", 25, BLANCO, 525, 23)
    mostrarTexto(Ventana, bertram, str(personajePrincipal.puntuacion).zfill(5), 25, BLANCO, 605, 23)

    tiempo-=.05


#======================================================================================================

    #Generando proyectiles
    if personajePrincipal.generar and personajePrincipal.activo == False:
        
        personajePrincipal.activo= True
        personajePrincipal.generar= False
        
        nuevoProyectil= Proyectil(personajePrincipal.rect.right, personajePrincipal.rect.centery + 5)

        proyectiles.add(nuevoProyectil)

        #Controla la dirección del proyectil 
        if personajePrincipal.Dir == 0:

            nuevoProyectil.dir= 20

        else:

            nuevoProyectil.dir= -20

    

    #Movimiento y ataque del mago    
    if personajePrincipal.rect.right >= (nuevaTuberia.rect.left - 200) and not personajePrincipal.muerte:

        if nuevoMago.rect.y == 340 and nuevoMago.comprobarMovimiento():

            nuevoMago.inicio= pg.time.get_ticks()
            nuevoMago.movimiento= True



            
#============================= Colisiones ==================================#
    

    #Creando colisión con enemigos + Muerte del enemigo
    
    colisionGoomba= pg.sprite.spritecollide(personajePrincipal, goombas, False)

    if colisionGoomba:

     #Sí la posición en Y es menor al enemigo, significa que el personajePrincipal colisionó estando en el aire y cayendo encima del enemigo
        if personajePrincipal.saltar or (personajePrincipal.rect.bottom < nuevoEnemigo.rect.y):

            #Si el enemigo ya está muriendo(mostrando animación de muerte) no hacemos nada
            if nuevoEnemigo.muerte:

                pass


            #Si no, eliminamos al enemigo
            else:

                personajePrincipal.puntuacion+=500
                personajePrincipal.aumento=-30
                jump.play()
                nuevoEnemigo.muerte=True
                nuevoEnemigo.inicio= pg.time.get_ticks()


        else:

            #Si colisionamos con el enemigo, pero el ya está muerto, no hacemos nada
            #Evita que la colisión continua se genere un bucle donde nunca desaparece
            if nuevoEnemigo.muerte or personajePrincipal.muerte:

                pass

            #Si el enemigo está vivo y colisiona de forma directa, destruimos el personaje
            else:

                if personajePrincipal.francotirador:

                    personajePrincipal.francotirador= False
                    nuevoEnemigo.muerte= True
                    nuevoEnemigo.inicio= pg.time.get_ticks()

                else:

                    personajePrincipal.muerte=True
                    personajePrincipal.inicio=pg.time.get_ticks()



    #colisión del personaje con el mago
    colisionMago= pg.sprite.spritecollide(personajePrincipal, magos, False) 

    if colisionMago:

        if nuevoMago.muerte or personajePrincipal.muerte:

            pass

        else:

            if personajePrincipal.francotirador:

                personajePrincipal.francotirador= False
                nuevoMago.muerte= True
                nuevoMago.inicio= pg.time.get_ticks()

            else:
               
                personajePrincipal.muerte= True
                personajePrincipal.inicio= pg.time.get_ticks()


    #Colisiones del proyectil mientrás esté activo

    if personajePrincipal.activo:

        colisionProyectil= pg.sprite.spritecollide(nuevoProyectil, goombas, False)
        proyectilMago= pg.sprite.spritecollide(nuevoProyectil, magos, False)
        proyectilTuberia= pg.sprite.spritecollide(nuevoProyectil, tuberias, False)
        proyectilBonus= pg.sprite.spritecollide(nuevoProyectil, bloquesBonus, False)

        if colisionProyectil:

            personajePrincipal.activo= False
            nuevoProyectil.kill()
            nuevoEnemigo.inicio= pg.time.get_ticks()
            nuevoEnemigo.muerte= True

        if proyectilMago:

            if nuevoMago.rect.top <= 320:

                personajePrincipal.activo= False
                nuevoProyectil.kill()
                nuevoEnemigo.inicio= pg.time.get_ticks()
                nuevoMago.muerte= True
                nuevoMago.movimiento= False
                personajePrincipal.puntuacion+=1000


        if proyectilTuberia or proyectilBonus:

            personajePrincipal.activo= False
            nuevoProyectil.kill()


   #Condicional que se encarga del tiempo antes de morir y de destruir el objeto
    if personajePrincipal.muerte:

        personajePrincipal.tiempoDeMuerte()


    if pg.sprite.spritecollide(personajePrincipal, caracoles, False):

        if nuevoCaracol.muerte:

            pass

        else:

            nuevoCaracol.inicio= pg.time.get_ticks()
            nuevoCaracol.muerte= True


    try:

        if nuevoCaracol.muerte:

            nuevoCaracol.tiempoDeMuerte()
        
    except Exception:

        pass


    #Colisión con Bloque bonus            
    colisionBonus= pg.sprite.spritecollide(personajePrincipal, bloquesBonus, False)

    if colisionBonus:

        if personajePrincipal.rect.right < bonus.rect.centerx and personajePrincipal.rect.top < bonus.rect.centery + 5:

            personajePrincipal.rect.right= bonus.rect.left

        if personajePrincipal.rect.left > bonus.rect.centerx and personajePrincipal.rect.top < bonus.rect.centery - 5:

            personajePrincipal.rect.left= bonus.rect.right

        if personajePrincipal.rect.top > bonus.rect.centery :

            #Esto para que al colisionar baje y no continue subiendo
            personajePrincipal.rect.y += 10
            personajePrincipal.aumento=0

            if not bonus.animacion and not bonus.activado:
                
                bonus.animacion=True
                bonus.activado= True
                inicio= pg.time.get_ticks()

        if personajePrincipal.rect.bottom < bonus.rect.centery - 8:

            personajePrincipal.saltar=False
            personajePrincipal.rect.bottom=bonus.rect.top + 1
            personajePrincipal.aumento= -30
        
    
    
    if bonus.animacion:

        if bonus.mover(inicio):

            bonus.animacion=False
            nuevaArma= Potenciador(pg.transform.scale(desarrollador["Arma"][0], (50,14)), bonus.rect.x - 6, bonus.rect.top -3)
            potenciadores.add(nuevaArma)
            generacion=True


    
    #Colisión del arma con el bloque bonus
    if generacion:

        armabonus= pg.sprite.spritecollide(nuevaArma, bloquesBonus, False)

        if armabonus:

            #Evitar que el sprite traspase el bloque bonus
            if nuevaArma.rect.bottom >= bonus.rect.top:

                nuevaArma.rect.bottom = bonus.rect.top+3
                nuevaArma.caida=False 

            else: 
                nuevaArma.caida=True


    #Colisión del arma con el suelo
    if generacion:
        armaSuelo= pg.sprite.spritecollide(nuevaArma, bloquesSimples, False)

        if armaSuelo:

            if nuevaArma.rect.bottom >= sueloBasico.rect.top:
                
                nuevaArma.rect.bottom= sueloBasico.rect.top+3
                nuevaArma.caida=False
            

        else:

            nuevaArma.caida= True
    


    #Colsisión del personaje con el suelo
    colisionSuelo= pg.sprite.spritecollide(personajePrincipal, bloquesSimples, False)

    if colisionSuelo and not personajePrincipal.muerte:
 
        personajePrincipal.saltar=False
        personajePrincipal.aumento=-30
        personajePrincipal.rect.bottom= sueloBasico.rect.top+1


    #Colisión del enemigo con el suelo
    colisionSueloEnemigo= pg.sprite.spritecollide(nuevoEnemigo, bloquesSimples, False)

    if colisionSueloEnemigo:
        
        if nuevoEnemigo.rect.bottom >= sueloBasico.rect.top:

            nuevoEnemigo.caer=False 
            nuevoEnemigo.rect.bottom = sueloBasico.rect.top+1


    else:

        nuevoEnemigo.caer=True


    #Colisión con potenciadores
    personajeArmas= pg.sprite.spritecollide(personajePrincipal, potenciadores, True)

    if personajeArmas:

        personajePrincipal.puntuacion+=1000
        personajePrincipal.francotirador=True
        nuevaArma.kill()



    #Colisión tubería
    colisionTuberia= pg.sprite.spritecollide(personajePrincipal, tuberias, False)

    if colisionTuberia:

        #Comprobamos si está encima de la tubería
        if personajePrincipal.rect.bottom < nuevaTuberia.rect.centery - 10:

            personajePrincipal.rect.bottom = nuevaTuberia.rect.top +1
            personajePrincipal.saltar=False
            personajePrincipal.aumento= -30

        
        #Si no lo está, verificamos si ha colisionado con uno de los lados del sprite (left, right)
        else:
            
            if personajePrincipal.rect.right >= nuevaTuberia.rect.left:

                 personajePrincipal.rect.right= nuevaTuberia.rect.left
        

    if nuevoMago.invocar:
        
        nuevoCaracol= Caracol(400, 397, personajePrincipal)
        caracoles.add(nuevoCaracol)


    try:

        nuevoCaracol.comprobar(personajePrincipal)

    except:

        pass


#========================== Movimiento de los personajes ====================================#
        
    if nuevoMago.movimiento:
        nuevoMago.mover()

    #Movimiento de potenciadores
    if generacion:

        if nuevaArma.mover:

            nuevaArma.moverPotenciador()

        if nuevaArma.caida:

            nuevaArma.caer()
            

#====================== Otros ============================#

    if not personajePrincipal.saltar and not colisionBonus and not colisionSuelo and not colisionTuberia:

        personajePrincipal.saltar = True
        personajePrincipal.aumento=0
        


    Reloj.tick(Fps)
    pg.display.update()
