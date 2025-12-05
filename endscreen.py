import pygame
from button import Button

class EndScreen:
    def __init__(self, screen, score, highscore, victory):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)
        self.score = score
        self.highscore = highscore
        self.victory = victory

        # Buttons
        self.restart_button = Button(300, 300, 200, 50, "Restart", self.restart)
        self.menu_button = Button(300, 360, 200, 50, "Back to Menu", self.menu)
        self.music_button = Button(300, 420, 200, 50, "Toggle Music", self.toggle_music)
        self.quit_button = Button(300, 480, 200, 50, "Quit", self.quit_game)

        self.action = None

    def restart(self):
        self.action = 'restart'

    def menu(self):
        self.action = 'menu'

    def toggle_music(self):
        self.action = 'toggle_music'

    def quit_game(self):
        self.action = 'quit'

    def run(self):
        running = True
        while running:
            self.screen.fill((255, 215, 0) if self.victory else (139, 0, 0))  # Gold for victory, red for failure

            # Title
            title_text = self.font.render("Victory!" if self.victory else "Failure!", True, (0, 0, 0))
            self.screen.blit(title_text, (300, 100))

            # Scores
            score_text = self.small_font.render(f"Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (300, 180))
            highscore_text = self.small_font.render(f"Highscore: {self.highscore}", True, (0, 0, 0))
            self.screen.blit(highscore_text, (300, 210))

            # Draw buttons
            self.restart_button.draw(self.screen)
            self.menu_button.draw(self.screen)
            self.music_button.draw(self.screen)
            self.quit_button.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                self.restart_button.handle_event(event)
                self.menu_button.handle_event(event)
                self.music_button.handle_event(event)
                self.quit_button.handle_event(event)

            if self.action:
                running = False

        return self.action
