
import pygame
from startscreen import StartScreen
from gamescreen import GameScreen
from endscreen import EndScreen

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Meowdieval Quest")
clock = pygame.time.Clock()

# --- Musik sicher laden (wenn Datei fehlt → einfach aus) ---
music_on = True
try:
    pygame.mixer.music.load("music/background.mp3")  # nur wenn die Datei echt da ist
    if music_on:
        pygame.mixer.music.play(-1)
except pygame.error:
    print("Keine background_music.mp3 gefunden → Musik deaktiviert")
    music_on = False

highscore = 0
current_screen = "start"

running = True
while running:
    # =============== STARTSCREEN ===============
    if current_screen == "start":
        start_screen = StartScreen(screen)
        action = start_screen.run()

        if action == "play":
            current_screen = "game"
        elif action == "toggle_music":
            music_on = not music_on
            if music_on and pygame.mixer.music.get_busy() == False:
                try:
                    pygame.mixer.music.play(-1)
                except:
                    pass
            else:
                pygame.mixer.music.stop()
        elif action == "quit":
            running = False

    # =============== GAMESCREEN ===============
    elif current_screen == "game":
        game = GameScreen(screen)
        score = game.run(music_on)              # music_on wird hier nur weitergegeben
        highscore = max(highscore, score)
        current_screen = "end"

    # =============== ENDSCREEN ===============
    elif current_screen == "end":
        end_screen = EndScreen(screen, score, highscore, score >= 10)
        action = end_screen.run()

        if action == "restart":
            current_screen = "game"
        elif action == "menu":
            current_screen = "start"
        elif action == "toggle_music":
            music_on = not music_on
            if music_on:
                try:
                    pygame.mixer.music.play(-1)
                except:
                    pass
            else:
                pygame.mixer.music.stop()
        elif action == "quit":
            running = False

    clock.tick(60)

pygame.quit()
