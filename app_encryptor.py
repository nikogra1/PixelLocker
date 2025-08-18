from encryption import Encryption
import pygame
import pygame_gui
pygame.init()
encryption = Encryption()
manager = pygame_gui.UIManager((800, 600))
text_input = pygame_gui.elements.UITextEntryLine(
   relative_rect=pygame.Rect((100, 100), (600, 50)),
   manager=manager
)

# Ustawienie wymiarów okna
szerokosc_okna = 800
wysokosc_okna = 600
ekran = pygame.display.set_mode((szerokosc_okna, wysokosc_okna))
clock = pygame.time.Clock()

# Ustawienie tytułu okna
pygame.display.set_caption("Encryptor")

czcionka = pygame.font.SysFont("comfortaa",24)

czarny = (0, 0, 0)
bialy = (255, 255, 255)

PIn = "n12"
PIn1 = "n12"

tekst = "Hasło: "
tekst_powierzchnia = czcionka.render(tekst, True, bialy, czarny)  # (tekst, wygładzanie, kolor, tło)
tekst_prostokat = tekst_powierzchnia.get_rect()
tekst_prostokat.center = (szerokosc_okna // 2, 80) # Wyśrodkowanie tekstu

# Główne pętla gry
dziala = True
while dziala:
    tekst_powierzchnia = czcionka.render(tekst, True, bialy, czarny)  # (tekst, wygładzanie, kolor, tło)
    tekst_prostokat = tekst_powierzchnia.get_rect()
    tekst_prostokat.center = (szerokosc_okna // 2, 80) # Wyśrodkowanie tekstu
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dziala = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                PIn1 = PIn
                PIn = f"Wprowadzony tekst: {text_input.get_text()}"
        manager.process_events(event)

    # Aktualizacja ekranu (rysowanie)
    if PIn != PIn1:
        file = open("text_to_encrypt.txt","r")
        read_content = file.read()
        file2 = open("encrypted_text.txt","a")
        for i in list(read_content):
            file2.write(str(encryption.encrypt(i,PIN=PIn))+"""                                                   
""")
        PIn1 = PIn
        file2.close()
    manager.update(time_delta)
    ekran.fill(czarny)  # Biały kolor tła
    manager.draw_ui(ekran)
    ekran.blit(tekst_powierzchnia, tekst_prostokat) # Rysowanie tekstu

    pygame.display.flip()

pygame.quit()