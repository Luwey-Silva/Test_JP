import pygame
from button import Button

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)

        # Buttons
        self.play_button = Button(300, 300, 200, 50, "Play", self.play)
        self.music_button = Button(300, 360, 200, 50, "Toggle Music", self.toggle_music)
        self.quit_button = Button(300, 420, 200, 50, "Quit", self.quit_game)

        self.action = None

    def play(self):
        self.action = 'play'

    def toggle_music(self):
        self.action = 'toggle_music'

    def quit_game(self):
        self.action = 'quit'

    def run(self):
        running = True
        while running:
            self.screen.fill((135, 206, 235))  # Sky blue background

            # Title
            title_text = self.font.render("The Meowdieval Quest", True, (0, 0, 0))
            self.screen.blit(title_text, (150, 100))

            # Tutorial
            tutorial_lines = [
                "Catch flying cats by pressing arrow keys at the right time.",
                "Up for cats from above, Left for left, Right for right.",
                "Collect points to win!"
            ]
            for i, line in enumerate(tutorial_lines):
                tutorial_text = self.small_font.render(line, True, (0, 0, 0))
                self.screen.blit(tutorial_text, (150, 180 + i * 30))

            # Draw buttons
            self.play_button.draw(self.screen)
            self.music_button.draw(self.screen)
            self.quit_button.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                self.play_button.handle_event(event)
                self.music_button.handle_event(event)
                self.quit_button.handle_event(event)

            if self.action:
                running = False

        return self.action
