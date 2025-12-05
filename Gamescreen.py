import pygame
import random
import math

class Cat(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
        self.speed = random.uniform(14.0, 18.0)
        self.state = "moving"
        self.alpha = 255
        self.scale = 1.0
        self.glow = 0
        self.particles = []

        # Start positions
        if direction == "top":
            self.rect = pygame.Rect(370, -100, 70, 70)
        elif direction == "left":
            self.rect = pygame.Rect(-100, 200, 70, 70)
        elif direction == "right":
            self.rect = pygame.Rect(830, 200, 70, 70)

        self.base_image = self.create_cat()
        self.image = self.base_image.copy()

    def create_cat(self):
        surf = pygame.Surface((70, 70), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 180, 120), (35, 40), 28)
        pygame.draw.circle(surf, (255, 210, 140), (35, 25), 22)
        pygame.draw.polygon(surf, (255, 160, 100), [(25, 10), (35, 5), (45, 10)])
        pygame.draw.circle(surf, (0, 0, 0), (28, 22), 5)
        pygame.draw.circle(surf, (0, 0, 0), (42, 22), 5)
        pygame.draw.circle(surf, (255, 255, 255), (30, 20), 3)
        pygame.draw.circle(surf, (255, 255, 255), (44, 20), 3)
        return surf

    def hit(self):
        self.state = "hit"
        self.glow = 80
        for _ in range(25):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(5, 12)
            self.particles.append([self.rect.centerx, self.rect.centery, math.cos(angle)*speed, math.sin(angle)*speed, 40])

    def update(self):
        if self.state == "moving":
            if self.direction == "top":
                self.rect.y += self.speed
                if self.rect.top > 480:
                    self.kill()
            elif self.direction == "left":
                self.rect.x += self.speed
                if self.rect.left > 780:
                    self.kill()
            elif self.direction == "right":
                self.rect.x -= self.speed
                if self.rect.right < 20:
                    self.kill()

        if self.state == "hit":
            self.glow = max(self.glow - 5, 0)
            self.scale += 0.25
            self.alpha = max(self.alpha - 18, 0)
            if self.alpha <= 0:
                self.kill()

        scaled = pygame.transform.smoothscale(self.base_image, (int(70 * self.scale), int(70 * self.scale)))
        scaled.set_alpha(self.alpha)
        self.image = scaled

        for p in self.particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
            if p[4] <= 0:
                self.particles.remove(p)


class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 90)
        self.cats = pygame.sprite.Group()
        self.score = 0
        self.spawn_timer = 0
        self.start_time = pygame.time.get_ticks()
        self.beat_interval = 50

        # Princess character
        self.princess = pygame.Surface((100, 120), pygame.SRCALPHA)
        pygame.draw.ellipse(self.princess, (255, 200, 255), (0, 0, 100, 120))
        pygame.draw.ellipse(self.princess, (255, 150, 220), (0, 0, 100, 120), 5)
        pygame.draw.polygon(self.princess, (255, 215, 0), [(50,0),(35,40),(45,20),(50,50),(55,20),(65,40),(50,0)])

        self.hit_feedback = 0
        self.hit_color = (120, 255, 170)
        self.fall_zone_y = 400  # area where cats can be caught

    def run(self, music_on=True):
        clock = pygame.time.Clock()
        if music_on:
            pygame.mixer.music.play(-1)

        while True:
            now = pygame.time.get_ticks()
            elapsed = (now - self.start_time) // 1000
            time_left = max(60 - elapsed, 0)
            if time_left <= 0:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.score
                if event.type == pygame.KEYDOWN:
                    correct = False
                    for cat in self.cats:
                        if cat.state == "moving" and abs(cat.rect.centery - self.fall_zone_y) < 50:
                            if (cat.direction == "top" and event.key == pygame.K_UP) or \
                               (cat.direction == "left" and event.key == pygame.K_LEFT) or \
                               (cat.direction == "right" and event.key == pygame.K_RIGHT):
                                cat.hit()
                                self.score += 10
                                self.hit_feedback = 20
                                self.hit_color = (180, 255, 120)
                                correct = True
                                break
                    if not correct:
                        self.score = max(0, self.score - 5)
                        self.hit_feedback = 20
                        self.hit_color = (255, 80, 80)

            self.spawn_timer += 1
            if self.spawn_timer >= self.beat_interval:
                direction = random.choice(["top", "left", "right"])
                self.cats.add(Cat(direction))
                self.spawn_timer = 0

            self.cats.update()

            self.screen.fill((30, 30, 40))

            # Full-screen feedback
            fb = pygame.Surface((800, 600), pygame.SRCALPHA)
            alpha = max(0, self.hit_feedback * 12)
            pygame.draw.rect(fb, (*self.hit_color, alpha), (0, 0, 800, 600))
            self.screen.blit(fb, (0, 0))
            if self.hit_feedback > 0:
                self.hit_feedback -= 2

            # Draw fall zone
            pygame.draw.line(self.screen, (255, 255, 255), (0, self.fall_zone_y), (800, self.fall_zone_y), 3)

            # Draw princess at bottom center
            self.screen.blit(self.princess, (350, 460))

            for cat in self.cats:
                if cat.glow > 0:
                    glow = pygame.Surface((220, 220), pygame.SRCALPHA)
                    pygame.draw.circle(glow, (255, 255, 255, cat.glow), (110, 110), 90)
                    self.screen.blit(glow, (cat.rect.centerx - 110, cat.rect.centery - 110))

                img_rect = cat.image.get_rect(center=cat.rect.center)
                self.screen.blit(cat.image, img_rect)

                for p in cat.particles:
                    pygame.draw.circle(self.screen, (255, 255, 200), (int(p[0]), int(p[1])), 3)

            score_txt = self.font.render(str(self.score), True, (255, 255, 200))
            self.screen.blit(score_txt, score_txt.get_rect(center=(150, 100)))

            timer_txt = self.font.render(str(time_left), True, (255, 255, 150))
            self.screen.blit(timer_txt, timer_txt.get_rect(center=(650, 100)))

            pygame.display.flip()
            clock.tick(60)

        if music_on:
            pygame.mixer.music.stop()

        return self.score

      
