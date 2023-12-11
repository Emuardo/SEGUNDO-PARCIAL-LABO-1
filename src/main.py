import pygame
from funciones_principales import *
import csv
import sys
from configuraciones import *
from imagenes_y_sonidos import *
from jugador import Jugador
from hoja_de_sprite import HojaDeSprites
from plataformas import Plataforma

# Otras constantes



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

        pygame.display.set_icon(pygame.Surface((32, 32)))  # Ajusta según sea necesario

        self.reloj = pygame.time.Clock()
        self.en_menu_principal = True
        self.en_menu_opciones = False
        self.seleccion_de_niveles = False
        self.jugando = False
        self.volumen = 0
        self.nivel_elegido = ""
        self.plataformas = pygame.sprite.Group()
        self.todos_los_sprites = pygame.sprite.Group()
        
        hoja_sprite_jugador = HojaDeSprites(pygame.image.load(r"src\resources\sprites\harry_gf_sprite.png").convert_alpha(), 2, 4, ANCHO_JUGADOR, LARGO_JUGADOR, ["izquierda", "derecha"])

### INSTANCIO UN JUGADOR Y LE PASO EL GRUPO DONDE VA A PERTENECER
        
        self.jugador = Jugador([self.todos_los_sprites], hoja_sprite_jugador)

       

    def menu_principal(self):
        self.ventana.blit(fondo_menus, (0, 0))
        mostrar_texto(self.ventana, "Harry Potter y La Batalla de Hogwarts", 119, ((self.ancho // 2) - 6, 400), color_negro)
        mostrar_texto(self.ventana, "Harry Potter y La Batalla de Hogwarts", 119, (self.ancho //2, 400), color_dorado)
        self.boton_iniciar_juego = dibujar_boton(self.ventana, 750, 550, 400, 95, "Iniciar", 90, color_dorado, color_negro)
        self.boton_menu_opciones = dibujar_boton(self.ventana, 750, 700, 400, 95, "Ajustes", 90, color_dorado, color_negro)
        self.boton_salir_del_juego = dibujar_boton(self.ventana, 750, 850, 400, 95, "Salir del juego", 90, color_dorado, color_negro)
        

    def menu_opciones(self):
        self.ventana.blit(fondo_menus, (0, 0))
        mostrar_texto(self.ventana, "Harry Potter y La Batalla de Hogwarts", 119, ((self.ancho // 2) - 6, 400), color_negro)
        mostrar_texto(self.ventana, "Harry Potter y La Batalla de Hogwarts", 119, (self.ancho //2, 400), color_dorado)
        self.boton_subir_volumen = dibujar_boton(self.ventana, 750, 550, 400, 95, "Subir volumen", 90, color_dorado, color_negro)
        self.boton_bajar_volumen = dibujar_boton(self.ventana, 750, 700, 400, 95, "Bajar volumen", 90, color_dorado, color_negro)
        self.boton_volver_al_menu = dibujar_boton(self.ventana, 750, 850, 400, 95, "Volver al menu", 90, color_dorado, color_negro)
        
        
    def seleccion_de_nivel(self):
        self.ventana.fill(color_negro)
        mostrar_texto(self.ventana, "Elija su casa para defender Hogwarts de los Mortifagos", 100, (self.ancho //2, 90), color_dorado)
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
            mapa = [list(map(int, fila)) for fila in lector_csv]
        return mapa

    def nivel_1(self):
        self.ventana.blit(fondo_niveles,(0,0))

        # Dibuja el mapa cargado desde el archivo CSV
        for y, fila in enumerate(self.mapa_1):
            for x, celda in enumerate(fila):
                if celda == 64:
                    imagen_plataforma = pygame.image.load(r"src\resources\img\imagen_plataforma.png")
                    imagen_plataforma = pygame.transform.scale(imagen_plataforma, (self.ancho_celda, self.largo_celda))
                    
                    plataforma = Plataforma(x * self.ancho_celda, y * self.largo_celda, imagen_plataforma)
                    self.ventana.blit(imagen_plataforma, (x * self.ancho_celda, y * self.largo_celda))
                    self.plataformas.add(plataforma)

        self.jugador.verificar_colision(self.plataformas)
        self.todos_los_sprites.draw(self.ventana)

        
    def nivel_2(self):
        self.ventana.blit(fondo_niveles,(0,0))

        # Dibuja el mapa cargado desde el archivo CSV
        for y, fila in enumerate(self.mapa_2):
            for x, celda in enumerate(fila):
                if celda == 64:
                    imagen_plataforma = pygame.image.load(r"src\resources\img\imagen_plataforma.png")
                    # imagen_plataforma = pygame.transform.scale(imagen_plataforma, (self.ancho_celda, self.largo_celda))
                    plataforma = Plataforma(x * self.ancho_celda, y * self.largo_celda, imagen_plataforma)
                    self.ventana.blit(imagen_plataforma, (x * self.ancho_celda, y * self.largo_celda))
                    self.plataformas.add(plataforma)

        self.jugador.verificar_colision(self.plataformas)
        self.todos_los_sprites.draw(self.ventana)


    def eventos_menu_principal(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_iniciar_juego.collidepoint(pygame.mouse.get_pos()):
                    self.seleccion_de_niveles = True
                    self.en_menu_principal = False
                elif self.boton_menu_opciones.collidepoint(pygame.mouse.get_pos()):
                    self.en_menu_opciones = True
                    self.en_menu_principal = False
                elif self.boton_salir_del_juego.collidepoint(pygame.mouse.get_pos()):
                    self.en_menu_principal = False

    def eventos_seleccion_niveles(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_nivel_1.collidepoint(pygame.mouse.get_pos()):
                    self.jugando = True
                    self.seleccion_de_niveles = False
                    self.nivel_elegido = "1"
                elif self.boton_nivel_2.collidepoint(pygame.mouse.get_pos()):
                    self.jugando = True
                    self.seleccion_de_niveles = False
                    self.nivel_elegido = "2"
                    
                elif self.boton_nivel_3.collidepoint(pygame.mouse.get_pos()):
                    self.seleccion_de_niveles = False
                    self.nivel_elegido = "3"

    def eventos_juego(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:   
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar()
                       

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
        self.jugador.mascara.to_surface(self.ventana)
    def actualizar_sprites(self):
        self.todos_los_sprites.update()

    def ejecutar(self):
        pygame.mixer.music.set_volume(0)
        
        pygame.mixer.music.play(-1)

        self.reloj.tick(FPS)

        while self.en_menu_principal:
            self.menu_principal()

            self.eventos_menu_principal()

            self.actualizar()

            while self.en_menu_opciones:
                self.menu_opciones()
                self.eventos_menu_opciones()

                self.actualizar()

            while self.seleccion_de_niveles:
                self.seleccion_de_nivel()
                self.eventos_seleccion_niveles()

                self.actualizar()

            while self.jugando:
                if self.nivel_elegido == "1":
                    self.nivel_1()
                elif self.nivel_elegido == "2":
                    self.nivel_2()
                # else self.nivel_elegido == "3":
                #     self.nivel_3()
                self.eventos_juego()

                self.actualizar_sprites()

                self.actualizar()

        self.cerrar()


# Instancia el juego y ejecútalo
segundo_juego = Juego()
segundo_juego.ejecutar()