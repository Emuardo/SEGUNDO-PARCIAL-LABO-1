import pygame
import sqlite3
from funciones_principales import *
import csv
import sys
from configuraciones import *
from imagenes_y_sonidos import *
from jugador import Jugador
from enemigo import Enemigo
from hoja_de_sprite import HojaDeSprites
from plataformas import Plataforma
from hechizos import Hechizos
from hechizos_avanzados import HechizosAvanzados
from pociones import PocionesMagicas
from diadema import Diadema


conexion = sqlite3.connect('ranking.db')



class Juego:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.dimension_ventana = pygame.display.Info()
        self.ancho, self.largo = self.dimension_ventana.current_w, self.dimension_ventana.current_h
        self.ventana = pygame.display.set_mode((self.ancho, self.largo))
        pygame.display.set_caption("Harry Potter y La Batalla de Hogwarts")

        # Cargar el mapa desde el archivo CSV
        self.mapa_1 = self.cargar_mapa(r"src\resources\niveles\nivel_1.csv")  # Ajusta la ruta y el nombre del archivo
        self.mapa_2 = self.cargar_mapa(r"src\resources\niveles\nivel_2.csv")  # Ajusta la ruta y el nombre del archivo

        # Ajusta el tamaño de las celdas en función de las dimensiones de la ventana
        self.ancho_celda = self.ancho // 60  # Ajusta según sea necesario
        self.largo_celda = self.largo // 32  # Ajusta según sea necesario

        self.reloj = pygame.time.Clock()
        self.en_menu_principal = True
        self.en_menu_opciones = False
        self.seleccion_de_niveles = False
        self.perdiste = False
        self.cargar_nombre = False
        self.jugando = False
        self.tecla_izq_presionada = False
        self.tecla_der_presionada = False
        self.volumen = 0
        self.nivel_elegido = ""
        self.hechizos = pygame.sprite.Group()
        self.hechizos_enemigos = pygame.sprite.Group()
        self.hechizos_enemigos_2 = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()

        self.imagen_plataforma = pygame.image.load(r"src\resources\img\imagen_plataforma.png")
        self.imagen_plataforma = pygame.transform.scale(self.imagen_plataforma, (self.ancho_celda, self.largo_celda))

        self.imagen_pocion_magia = pygame.image.load(r"src\resources\img\imagen_pocion_magia.png")
        self.imagen_pocion_magia = pygame.transform.scale(self.imagen_pocion_magia, (self.ancho_celda,self.largo_celda))

        self.imagen_pocion_vida = pygame.image.load(r"src\resources\img\imagen_pocion_vida.png")
        self.imagen_pocion_vida = pygame.transform.scale(self.imagen_pocion_vida, (self.ancho_celda,self.largo_celda))
        
        self.ravenclaw_horrocrux = pygame.image.load(r"src\resources\img\Ravenclaw.jpg")
        self.ravenclaw_horrocrux = pygame.transform.scale(self.ravenclaw_horrocrux, (self.ancho_celda, self.largo_celda))

        self.gryffindor_horrocrux = pygame.image.load(r"src\resources\img\Gryffindor.png")
        self.gryffindor_horrocrux = pygame.transform.scale(self.gryffindor_horrocrux, (self.ancho_celda, self.largo_celda))
        
        self.plataformas = pygame.sprite.Group()    
        self.sprite_jugador = pygame.sprite.Group()
        self.pociones_vida = pygame.sprite.Group()
        self.pociones_magia = pygame.sprite.Group()
        self.diadema_r = pygame.sprite.GroupSingle()
        self.horrocrux_g = pygame.sprite.GroupSingle()
        self.fuente_puntaje_vidas_magia = pygame.font.SysFont("Harry P", 50)
        self.texto = ""
        self.disparo_enemigo = 0
        self.juega_nivel_2 = False
        self.juega_nivel_3 = False
        self.mostrar_pv1 = True
        self.mostrar_pv2 = True
        self.enemigos_2 = pygame.sprite.Group()
        self.mostrar_pm2 = True
        self.mostrar_pm1 = True
        self.contador_nivel_1 = 0
        self.contador_nivel_2 = 0
        self.mostrar_ddm = True
        self.mostrar_hg = True
        self.hoja_sprite_jugador = HojaDeSprites(pygame.image.load(r"src\resources\sprites\harry_gf_sprite.png").convert_alpha(), 2, 4, ANCHO_JUGADOR, LARGO_JUGADOR, ["izquierda", "derecha"])
        self.hoja_sprite_enemigo = HojaDeSprites(pygame.image.load(r"src\resources\sprites\mortifagos_sprite.png").convert_alpha(), 2, 4, ANCHO_JUGADOR, LARGO_JUGADOR, ["izquierda", "derecha"])
        self.jugador = Jugador([self.sprite_jugador], self.hoja_sprite_jugador)
        # self.informacion_jugador = {"nombre": self.texto, "puntaje": self.jugador.puntaje}
        self.mortifago_1 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 600, 290, 60, 120) 
        self.mortifago_2 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 900, 650, 60, 120)
        self.mortifago_3 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 1100,650, 60, 120)
        self.mortifago_4 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 700, 999, 60, 120)
        self.mortifago_5 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 900, 290, 60, 120)
        self.mortifago_6 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo, 600, 500, 60, 120) 
        self.mortifago_7 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo, 1200, 700, 60, 120)
        self.mortifago_8 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo, 750, 900, 60, 120)
        self.mortifago_9 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo, 500, 650, 60, 120)
        self.mortifago_10 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo,1400, 900, 60, 120)
        
        self.hechizo_avanzado = HechizosAvanzados([self.hechizos], color_dorado, self.jugador.rect.center, 35,0)

            
    def menu_principal(self):
        self.ventana.blit(fondo_menus, (0,0))
        mostrar_texto(self.ventana, "Harry Potter y La Batalla de Hogwarts", 119, ((self.ancho // 2) - 6, 200), color_negro)
        mostrar_texto(self.ventana, "Harry Potter y La Batalla de Hogwarts", 119, (self.ancho //2, 200), color_dorado)
        self.boton_iniciar_juego = dibujar_boton(self.ventana, 750, 550, 400, 95, "Iniciar", 90, color_dorado, color_negro)
        self.boton_menu_opciones = dibujar_boton(self.ventana, 750, 700, 400, 95, "Ajustes", 90, color_dorado, color_negro)
        self.boton_salir_del_juego = dibujar_boton(self.ventana, 750, 850, 400, 95, "Salir del juego", 90, color_dorado, color_negro)
        
         
    def menu_perdiste(self):
        self.ventana.blit(fondo_menu_perdiste, (0,0))
        mostrar_texto(self.ventana, "Perdiste, los mortifagos tomaron la escuela y gano Voldemort", 90, ((self.ancho // 2) - 6, 200), color_negro)
        mostrar_texto(self.ventana, "Perdiste, los mortifagos tomaron la escuela y gano Voldemort", 90, ((self.ancho // 2), 200), color_dorado)
        self.boton_intentar_otra_vez = dibujar_boton(self.ventana, 750, 700, 400, 95, "Reintentar", 90, color_dorado, color_negro)
        self.boton_volver_menu = dibujar_boton(self.ventana, 750, 900, 400, 95, "Volver al menu", 90, color_dorado, color_negro)
        


    def menu_opciones(self):
        self.ventana.blit(fondo_menus,(0,0))
        mostrar_texto(self.ventana, "Harry Potter y La Batalla de Hogwarts", 119, ((self.ancho // 2) - 6, 400), color_negro)
        mostrar_texto(self.ventana, "Harry Potter y La Batalla de Hogwarts", 119, (self.ancho //2, 400), color_dorado)
        self.boton_subir_volumen = dibujar_boton(self.ventana, 750, 550, 400, 95, "Subir volumen", 90, color_dorado, color_negro)
        self.boton_bajar_volumen = dibujar_boton(self.ventana, 750, 700, 400, 95, "Bajar volumen", 90, color_dorado, color_negro)
        self.boton_volver_al_menu = dibujar_boton(self.ventana, 750, 850, 400, 95, "Volver al menu", 90, color_dorado, color_negro)

    def entrada_nombre(self):
        self.ventana.fill(color_bordo)
        entrada_texto = self.fuente_puntaje_vidas_magia.render(self.texto, True, color_dorado)
        rect_entrada_texto = entrada_texto.get_rect()
        rect_entrada_texto.center = (950,400)
        
        pygame.draw.rect(self.ventana, color_negro, (590,350,700,80), 50)
        pygame.draw.rect(self.ventana, color_blanco, (590,350,700,80), 5)
        self.ventana.blit(entrada_texto, rect_entrada_texto)
    
    def seleccion_de_nivel(self):
        self.ventana.fill(color_negro)
        mostrar_texto(self.ventana, "Elija su casa para defender Hogwarts de los Mortifagos", 90, (self.ancho //2, 90), color_dorado)
        self.boton_nivel_1 = dibujar_boton(self.ventana, 200, 700, 400, 95, "Nivel 1", 90, color_negro, color_gris)
        self.boton_nivel_2 = dibujar_boton(self.ventana, 750, 700, 400, 95, "Nivel 2", 90, color_negro, color_gris)
        self.boton_nivel_3 = dibujar_boton(self.ventana, 1300, 700, 400, 95, "Nivel 3", 90, color_negro, color_gris)
        self.boton_ravenclaw = dibujar_boton(self.ventana, 400, 430, 250, 80, "Ravenclaw", 70, color_celeste, color_celeste_oscuro)
        self.boton_gryffindor = dibujar_boton(self.ventana, 700, 430, 250, 80, "Gryffindor", 70, color_rojo, color_bordo)
        self.boton_hufflepuff = dibujar_boton(self.ventana, 1000, 430, 250, 80, "Hufflepuff", 70, color_amarillo, color_amarillo_oscuro)
        self.boton_slytherin = dibujar_boton(self.ventana, 1300, 430, 250, 80, "Slytherin", 70, color_verde, color_verde_oscuro)

        self.ventana.blit(ravenclaw, (400, 150))
        self.ventana.blit(gryffindor, (700, 150))
        self.ventana.blit(hufflepuff, (1000, 150))
        self.ventana.blit(slytherin, (1300, 150))

    def cargar_mapa(self, ruta):
        with open(ruta, newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            mapa = []

            for fila in lector_csv:
                fila_enteros = []
                for valor in fila:
                    fila_enteros.append(int(valor))
                mapa.append(fila_enteros)

        return mapa
    def nivel_1(self):
        self.ventana.blit(fondo_niveles,(0,0))
       
        if self.jugador.puntaje > 0:  # Ajusta la condición según tus necesidades
            nombre_jugador = "Emiliano Centurion"  # Reemplaza esto con el nombre del jugador
            puntaje_jugador = self.jugador.puntaje
            conexion.execute('''
                INSERT INTO ranking (nombre, puntaje) VALUES (?, ?)
            ''', (nombre_jugador, puntaje_jugador))
            
            conexion.commit()
        for y, fila in enumerate(self.mapa_1):
            for x, celda in enumerate(fila):
                if celda == 63:
                        plataforma = Plataforma(x * self.ancho_celda, y * self.largo_celda, self.imagen_plataforma)
                        self.ventana.blit(self.imagen_plataforma, (x * self.ancho_celda, y * self.largo_celda))
                        self.plataformas.add(plataforma)
                elif celda == 67 and self.mostrar_pv1:
                    self.pocion_vida = PocionesMagicas(x * self.ancho_celda, y * self.largo_celda, self.imagen_pocion_vida)
                    self.pociones_vida.add(self.pocion_vida)
                    if self.jugador.rect.colliderect(self.pocion_vida.rect):
                        self.pociones_vida.remove(self.pocion_vida)
                        self.mostrar_pv1 = False
                elif celda == 840 and self.mostrar_pm1:
                    self.pocion_magia = PocionesMagicas(x * self.ancho_celda, y * self.largo_celda, self.imagen_pocion_magia)
                    self.pociones_magia.add(self.pocion_magia)
                    if self.jugador.rect.colliderect(self.pocion_magia.rect):
                        self.pociones_magia.remove(self.pocion_magia)
                        self.mostrar_pm1 = False
                elif celda == 317 and self.mostrar_ddm:
                    self.diadema = Diadema( x * self.ancho_celda, y * self.largo_celda, self.ravenclaw_horrocrux)
                    self.diadema_r.add(self.diadema)
                    if self.jugador.rect.colliderect(self.diadema.rect):
                        self.seleccion_de_niveles = True
                        self.jugando = False
                        self.juega_nivel_2 = True
        
        self.enemigos.draw(self.ventana)
       
        self.mortifago_1.update() 
        self.mortifago_2.update()
        self.mortifago_3.update()
        self.mortifago_4.update()
        self.mortifago_5.update()
        
        self.jugador.magia += 1
        
        if self.jugador.magia >= 100:
            self.jugador.magia = 100
        
        if self.jugador.vidas <= 0:
            self.jugando = False
            self.perdiste = True
    
     
   
    def nivel_2(self):
        self.ventana.blit(fondo_niveles,(0,0))    
        self.enemigos.empty()
        self.diadema_r.empty()    
        self.hechizos_enemigos.empty()
        self.plataformas.empty()
        self.pociones_magia.empty()
        self.pociones_vida.empty()

        
        for y, fila in enumerate(self.mapa_2):
            for x, celda in enumerate(fila):
                if celda == 63:
                    plataforma = Plataforma(x * self.ancho_celda, y * self.largo_celda, self.imagen_plataforma)
                    self.ventana.blit(self.imagen_plataforma, (x * self.ancho_celda, y * self.largo_celda))
                    self.plataformas.add(plataforma)
                elif celda == 65 and self.mostrar_pv1:
                    self.pocion_vida = PocionesMagicas(x * self.ancho_celda, y * self.largo_celda, self.imagen_pocion_vida)
                    self.pociones_vida.add(self.pocion_vida)
                    if self.jugador.rect.colliderect(self.pocion_vida.rect):
                        self.pociones_vida.remove(self.pocion_vida)
                        self.mostrar_pv1 = False
                elif celda == 64 and self.mostrar_pm1:
                    self.pocion_magia = PocionesMagicas(x * self.ancho_celda, y * self.largo_celda, self.imagen_pocion_magia)
                    self.pociones_magia.add(self.pocion_magia)
                    if self.jugador.rect.colliderect(self.pocion_magia.rect):
                        self.pociones_magia.remove(self.pocion_magia)
                        self.mostrar_pm1 = False
                elif celda == 67 and self.mostrar_pm2:
                    self.pocion_magia = PocionesMagicas(x * self.ancho_celda, y * self.largo_celda, self.imagen_pocion_magia)
                    self.pociones_magia.add(self.pocion_magia)
                    if self.jugador.rect.colliderect(self.pocion_magia.rect):
                        self.pociones_magia.remove(self.pocion_magia)
                        self.mostrar_pm2 = False
                elif celda == 66 and self.mostrar_pv2:
                    self.pocion_vida = PocionesMagicas(x * self.ancho_celda, y * self.largo_celda, self.imagen_pocion_vida)
                    self.pociones_vida.add(self.pocion_vida)
                    if self.jugador.rect.colliderect(self.pocion_vida.rect):
                        self.pociones_vida.remove(self.pocion_vida)
                        self.mostrar_pv2 = False
                elif celda == 2 and self.mostrar_hg:
                        self.horrocrux = Diadema( x * self.ancho_celda, y * self.largo_celda, self.gryffindor_horrocrux)
                        self.horrocrux_g.add(self.horrocrux)
                        if self.jugador.rect.colliderect(self.horrocrux.rect):
                            self.seleccion_de_niveles = True
                            self.jugando = False
                            self.juega_nivel_3 = True
                            self.mostrar_hg = False
                            
        self.enemigos_2.draw(self.ventana)
        self.hechizos_enemigos_2.draw(self.ventana)
        self.mortifago_6.update() 
        self.mortifago_7.update()
        self.mortifago_8.update()
        self.mortifago_9.update()
        self.mortifago_10.update()
        
        self.jugador.magia += 1
        
        if self.jugador.magia >= 100:
            self.jugador.magia = 100
        
        if self.jugador.vidas <= 0:
            self.jugando = False
            self.perdiste = True

    def reiniciar_nivel_1(self):
        self.enemigos.empty()
        self.jugador.rect = self.jugador.image.get_rect(center = (500,150))
        self.mortifago_1 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 500, 290, 30, 60) 
        self.mortifago_2 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 900, 650, 30, 60)
        self.mortifago_3 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 1100,650, 30, 60)
        self.mortifago_4 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 700, 999, 30, 60)
        self.mortifago_5 = Enemigo([self.enemigos], self.hoja_sprite_enemigo, 900, 290, 30, 60)
        self.hechizo_avanzado = HechizosAvanzados([self.hechizos], color_dorado, self.jugador.rect.center, 35,0)
        self.sprite_jugador.draw(self.ventana)
        self.hechizos.draw(self.ventana)
        self.hechizos_enemigos.draw(self.ventana)
        self.pociones_vida.draw(self.ventana)
        self.pociones_magia.draw(self.ventana)
        self.diadema_r.draw(self.ventana)
        self.pociones_magia.add(self.pocion_magia)
        self.pociones_vida.add(self.pocion_vida)
        self.diadema_r.add(self.diadema)
        self.mostrar_pm = True
        self.mostrar_pv = True
        self.mostrar_ddm = True
        self.jugador.vidas = 3
        
    def reiniciar_nivel_2(self):
        self.enemigos_2.empty()
        self.jugador.rect = self.jugador.image.get_rect(center = (500,150))
        self.mortifago_6 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo, 600, 500, 60, 120) 
        self.mortifago_7 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo, 1200, 700, 60, 120)
        self.mortifago_8 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo, 750, 900, 60, 120)
        self.mortifago_9 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo, 500, 650, 60, 120)
        self.mortifago_10 = Enemigo([self.enemigos_2], self.hoja_sprite_enemigo,1400, 900, 60, 120)
        self.hechizo_avanzado = HechizosAvanzados([self.hechizos], color_dorado, self.jugador.rect.center, 35,0)
        self.sprite_jugador.draw(self.ventana)
        self.hechizos.draw(self.ventana)
        self.hechizos_enemigos_2.draw(self.ventana)
        self.pociones_vida.draw(self.ventana)
        self.pociones_magia.draw(self.ventana)
        self.diadema_r.draw(self.ventana)
        self.pociones_magia.add(self.pocion_magia)
        self.pociones_vida.add(self.pocion_vida)
        self.horrocrux_g.add(self.horrocrux)
        self.mostrar_pm1 = True
        self.mostrar_pv1 = True
        self.mostrar_pm2 = True
        self.mostrar_pv2 = True
        self.mostrar_hg = True 
        self.jugador.vidas = 3   
        
    def textos(self):
        texto_score =self.fuente_puntaje_vidas_magia.render(f"Puntaje :{self.jugador.puntaje}", True, color_blanco,color_negro)
        rect_texto_score = texto_score.get_rect()

        rect_texto_score.center = (300 , 30)

        texto_vidas = self.fuente_puntaje_vidas_magia.render(f"Vidas : {self.jugador.vidas}", True, color_blanco,color_negro)
        rect_texto_vidas = texto_vidas.get_rect()

        rect_texto_vidas.center = (100, 30 )

        texto_magia = self.fuente_puntaje_vidas_magia.render(f"Magia :{self.jugador.magia}", True, color_blanco, color_negro)
        rect_texto_magia = texto_magia.get_rect()

        rect_texto_magia.center = (550, 30)
        
        self.ventana.blit(texto_magia, rect_texto_magia)
        self.ventana.blit(texto_score , rect_texto_score)
        self.ventana.blit(texto_vidas, rect_texto_vidas)
        

    def eventos_menu_principal(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar()
                

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_iniciar_juego.collidepoint(pygame.mouse.get_pos()):
                    self.cargar_nombre = True
                    self.en_menu_principal = False
                elif self.boton_menu_opciones.collidepoint(pygame.mouse.get_pos()):
                    self.en_menu_opciones = True
                    self.en_menu_principal = False
                elif self.boton_salir_del_juego.collidepoint(pygame.mouse.get_pos()):
                    self.en_menu_principal = False

    def evento_carga_nombre(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar()
            
                if evento.key == pygame.K_RETURN:
                    self.cargar_nombre = False
                    self.seleccion_de_niveles = True
                    nombre_jugador = self.texto
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                else:
                    self.texto += evento.unicode
                    
   

            
    def eventos_menu_perdiste(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_intentar_otra_vez.collidepoint(pygame.mouse.get_pos()):
                    self.seleccion_de_niveles = True
                    self.perdiste = False
                elif self.boton_volver_menu.collidepoint(pygame.mouse.get_pos()):
                    self.en_menu_principal = True
                    self.perdiste = False               
                    
    def eventos_seleccion_niveles(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_nivel_1.collidepoint(pygame.mouse.get_pos()):
                    self.contador_nivel_1 += 1
                    self.jugando = True
                    self.seleccion_de_niveles = False
                    self.nivel_elegido = "1"
                    if self.contador_nivel_1 >= 2:
                        self.reiniciar_nivel_1()
                elif self.boton_nivel_2.collidepoint(pygame.mouse.get_pos()) and self.juega_nivel_2:
                    self.contador_nivel_2 += 1
                    self.jugando = True
                    self.seleccion_de_niveles = False
                    self.nivel_elegido = "2"
                    if self.contador_nivel_2 >= 2:
                        self.reiniciar_nivel_2()
                elif self.boton_nivel_3.collidepoint(pygame.mouse.get_pos()):
                    self.seleccion_de_niveles = False
                    self.nivel_elegido = "3"
                    
    def dibujar_sprites(self):   
        self.sprite_jugador.draw(self.ventana)
        self.hechizos.draw(self.ventana)
        self.hechizos_enemigos.draw(self.ventana)
        self.pociones_vida.draw(self.ventana)
        self.pociones_magia.draw(self.ventana)
        self.diadema_r.draw(self.ventana)
        self.horrocrux_g.draw(self.ventana)
        
    def eventos_juego(self):
        todos_enemigos = [self.mortifago_1, self.mortifago_2, self.mortifago_3, self.mortifago_4, self.mortifago_5,
                          self.mortifago_6, self.mortifago_7, self.mortifago_8, self.mortifago_9, self.mortifago_10]

        self.disparo_enemigo += 1
        if self.disparo_enemigo == 30:
            for enemigo in todos_enemigos:
                if enemigo in [self.mortifago_1, self.mortifago_2, self.mortifago_3, self.mortifago_4, self.mortifago_5]:
                    Hechizos([self.hechizos_enemigos], color_verde, 20, enemigo.rect.midleft, 20, 5, "izquierda")
                else:
                    Hechizos([self.hechizos_enemigos_2], color_verde, 20, enemigo.rect.midleft, 20, 5, "izquierda")
            
        elif self.disparo_enemigo == 85:
            for enemigo in todos_enemigos:
                if enemigo in [self.mortifago_1, self.mortifago_2, self.mortifago_3, self.mortifago_4, self.mortifago_5]:
                    Hechizos([self.hechizos_enemigos], color_verde, 20, enemigo.rect.midleft, 20, 5, "derecha")
                else:
                    Hechizos([self.hechizos_enemigos_2], color_verde, 20, enemigo.rect.midleft, 20, 5, "derecha")
            self.disparo_enemigo = 0
            self.hechizos_enemigos.remove(self.ventana)


        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar()

                if evento.key == pygame.K_LEFT:
                    self.tecla_izq_presionada= True
                    self.tecla_der_presionada = False

                if evento.key == pygame.K_RIGHT:
                    self.tecla_der_presionada = True
                    self.tecla_izq_presionada = False

                if evento.key == pygame.K_e and self.jugador.magia >= 25:
                    if self.tecla_izq_presionada:
                        Hechizos([self.hechizos], color_rojo, 20, self.jugador.rect.midright, 20, 5, "izquierda")
                        self.jugador.magia -= 25
                    if self.tecla_der_presionada:
                        Hechizos([self.hechizos], color_rojo, 20, self.jugador.rect.midleft, 20, 5, "derecha")
                        self.jugador.magia -= 25
                if evento.key == pygame.K_q  and self.jugador.magia >= 30:
                    if self.tecla_izq_presionada:
                        Hechizos([self.hechizos], color_celeste, 0, self.jugador.rect.midleft, 5, 40, "izquierda")
                        self.jugador.magia -= 30
                    if self.tecla_der_presionada:
                        Hechizos([self.hechizos], color_celeste, 0, self.jugador.rect.midright, 5, 40, "derecha")
                        self.jugador.magia -= 30
                if evento.key == pygame.K_w and self.jugador.magia == 100 :
                    self.hechizo_avanzado = HechizosAvanzados([self.hechizos], color_dorado, self.jugador.rect.center, 35, 85)
                    self.jugador.magia -= 100
    
    def colisiones(self):
        self.jugador.verificar_colision(self.plataformas)
        self.jugador.verificar_colision_pocion_vida(self.pociones_vida)
        self.jugador.verificar_colision_pocion_magia(self.pociones_magia)
        self.jugador.verificar_colision_hechizos_enemigos(self.hechizos_enemigos)
        self.jugador.verificar_colision_hechizos_enemigos(self.hechizos_enemigos_2)
        self.hechizo_avanzado.verificar_colision_entre_hechizos_avanzados(self.hechizos_enemigos)
        self.hechizo_avanzado.verificar_colision_entre_hechizos_avanzados(self.hechizos_enemigos_2)

        mortifagos = [self.mortifago_1, self.mortifago_2, self.mortifago_3, self.mortifago_4, self.mortifago_5,
                      self.mortifago_6, self.mortifago_7, self.mortifago_8, self.mortifago_9, self.mortifago_10]
        
        for mortifago in mortifagos:
            mortifago.verificar_colision(self.plataformas)
            mortifago.verificar_colision_hechizos(self.hechizos, self.jugador)
            
    def eventos_menu_opciones(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_volver_al_menu.collidepoint(pygame.mouse.get_pos()):
                    self.en_menu_opciones = False
                    self.en_menu_principal = True
                elif self.boton_subir_volumen.collidepoint(pygame.mouse.get_pos()):
                    self.volumen += 0.1
                    if self.volumen <= 1.0:
                        pygame.mixer.music.set_volume(self.volumen)
                    elif self.volumen > 1.0:
                        self.volumen = 1.0
                elif self.boton_bajar_volumen.collidepoint(pygame.mouse.get_pos()):
                    self.volumen -= 0.1
                    if self.volumen >= 0:
                        pygame.mixer.music.set_volume(self.volumen)
                    elif self.volumen < 0:
                        self.volumen = 0


    def cerrar(self):
        pygame.quit()
        sys.exit()

    def actualizar(self):
        pygame.display.flip()

    def actualizar_sprites_jugador(self):
        self.sprite_jugador.update()

    
        
    def actualizar_hechizos(self):
        self.hechizos.update()
        self.hechizos_enemigos.update()
        self.hechizos_enemigos_2.update()

    def actualizar_pociones(self):
        self.pociones_vida.update()
        self.pociones_magia.update()

    def ejecutar(self):
        pygame.mixer.music.set_volume(0)

        pygame.mixer.music.play(-1)

        self.reloj.tick(FPS)

        while self.en_menu_principal:
            self.reloj.tick(FPS)

            self.menu_principal()

            self.eventos_menu_principal()

            self.actualizar()

            while self.en_menu_opciones:


                self.menu_opciones()
                self.eventos_menu_opciones()

                self.actualizar()

            while self.cargar_nombre :
                self.entrada_nombre()
                
                self.evento_carga_nombre()
                
                self.actualizar()
            while self.seleccion_de_niveles:


                self.seleccion_de_nivel()
                self.eventos_seleccion_niveles()

                self.actualizar()

                while self.jugando:
                    self.reloj.tick(FPS)

                    self.colisiones()
                    self.actualizar_pociones()
                    self.dibujar_sprites()
                    self.actualizar_sprites_jugador()
                    self.textos()
                    self.eventos_juego()
                    self.actualizar()
                    self.actualizar_hechizos()  
                    
                    if self.nivel_elegido == "1":
                        self.nivel_1()
                    
                    if self.nivel_elegido == "2":
                        self.nivel_2()
                    
                    # else self.nivel_elegido == "3":
                    #     self.nivel_3()

                while self.perdiste:
                    self.menu_perdiste()
                    self.eventos_menu_perdiste()
                    
                    self.actualizar()

        self.cerrar()

# Instancia el juego y ejecútalo
segundo_juego = Juego()
segundo_juego.ejecutar()

conexion.close()