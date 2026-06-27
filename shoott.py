"""
Space Shooter - a simple arcade game built with pygame.

Controls:
    Arrow keys / WASD : move ship
    Space             : fire
    R                 : restart after game over
    Esc               : quit

Run with:
    pip install pygame
    python space_shooter.py
"""

import pygame
import random
import sys

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
pygame.init()

WIDTH, HEIGHT = 480, 640
FPS = 60

WHITE = (255, 255, 255)
BLACK = (10, 10, 20)
RED = (220, 60, 60)
GREEN = (60, 220, 100)
YELLOW = (240, 220, 60)
CYAN = (60, 200, 220)
GREY = (120, 120, 140)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("consolas", 48, bold=True)
font_med = pygame.font.SysFont("consolas", 28, bold=True)
font_small = pygame.font.SysFont("consolas", 18)


# ---------------------------------------------------------------------------
# Starfield background (random twinkling stars)
# ---------------------------------------------------------------------------
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 4)
        self.size = random.choice([1, 1, 2, 2, 3])
        self.brightness = random.randint(120, 255)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
            self.speed = random.uniform(1, 4)

    def draw(self, surf):
        c = self.brightness
        pygame.draw.circle(surf, (c, c, c), (int(self.x), int(self.y)), self.size)


# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
class Player:
    def __init__(self):
        self.w, self.h = 40, 30
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 80
        self.speed = 6
        self.cooldown = 0
        self.cooldown_max = 12
        self.lives = 3
        self.invuln = 0

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(0, min(WIDTH - self.w, self.x))
        self.y = max(0, min(HEIGHT - self.h, self.y))

        if self.cooldown > 0:
            self.cooldown -= 1
        if self.invuln > 0:
            self.invuln -= 1

    def shoot(self, bullets):
        if self.cooldown == 0:
            cx = self.x + self.w // 2
            bullets.append(Bullet(cx, self.y, -10, CYAN))
            self.cooldown = self.cooldown_max

    def draw(self, surf):
        if self.invuln > 0 and self.invuln % 10 < 5:
            return  # flicker when invulnerable
        cx = self.x + self.w // 2
        points = [
            (cx, self.y),
            (self.x, self.y + self.h),
            (cx, self.y + self.h - 8),
            (self.x + self.w, self.y + self.h),
        ]
        pygame.draw.polygon(surf, GREEN, points)
        # engine flame (random flicker for fun)
        flame_h = random.randint(4, 12)
        pygame.draw.polygon(
            surf, YELLOW,
            [(cx - 6, self.y + self.h - 4),
             (cx + 6, self.y + self.h - 4),
             (cx, self.y + self.h - 4 + flame_h)]
        )


# ---------------------------------------------------------------------------
# Bullets (player + enemy)
# ---------------------------------------------------------------------------
class Bullet:
    def __init__(self, x, y, vy, color, w=4, h=10):
        self.x, self.y = x, y
        self.vy = vy
        self.color = color
        self.w, self.h = w, h

    @property
    def rect(self):
        return pygame.Rect(self.x - self.w // 2, self.y, self.w, self.h)

    def update(self):
        self.y += self.vy

    def offscreen(self):
        return self.y < -20 or self.y > HEIGHT + 20

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=2)


# ---------------------------------------------------------------------------
# Enemies - random type, random position, random speed
# ---------------------------------------------------------------------------
ENEMY_TYPES = {
    "drone":  {"color": RED,    "size": 28, "speed": (2, 4),   "hp": 1, "score": 10},
    "tank":   {"color": GREY,   "size": 40, "speed": (1, 2),   "hp": 3, "score": 30},
    "zigzag": {"color": YELLOW, "size": 24, "speed": (2, 3.5), "hp": 1, "score": 20},
}


class Enemy:
    def __init__(self):
        self.kind = random.choices(
            list(ENEMY_TYPES.keys()), weights=[60, 15, 25]
        )[0]
        info = ENEMY_TYPES[self.kind]
        self.size = info["size"]
        self.color = info["color"]
        self.hp = info["hp"]
        self.score_value = info["score"]
        self.speed = random.uniform(*info["speed"])
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.zig_dir = random.choice([-1, 1])
        self.zig_timer = random.randint(20, 50)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.y += self.speed
        if self.kind == "zigzag":
            self.zig_timer -= 1
            if self.zig_timer <= 0:
                self.zig_dir *= -1
                self.zig_timer = random.randint(20, 50)
            self.x += self.zig_dir * 3
            self.x = max(0, min(WIDTH - self.size, self.x))

    def offscreen(self):
        return self.y > HEIGHT + 40

    def draw(self, surf):
        rect = self.rect
        pygame.draw.rect(surf, self.color, rect, border_radius=6)
        pygame.draw.rect(surf, BLACK, rect, width=2, border_radius=6)


# ---------------------------------------------------------------------------
# Power-ups (random drop chance, random type)
# ---------------------------------------------------------------------------
class PowerUp:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.size = 18
        self.speed = 2.5
        self.kind = random.choice(["rapid", "life", "shield"])
        self.colors = {"rapid": CYAN, "life": GREEN, "shield": YELLOW}

    @property
    def rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2,
                            self.size, self.size)

    def update(self):
        self.y += self.speed

    def offscreen(self):
        return self.y > HEIGHT + 20

    def draw(self, surf):
        pygame.draw.circle(surf, self.colors[self.kind],
                            (int(self.x), int(self.y)), self.size // 2)
        label = {"rapid": "R", "life": "+", "shield": "S"}[self.kind]
        text = font_small.render(label, True, BLACK)
        surf.blit(text, text.get_rect(center=(self.x, self.y)))


# ---------------------------------------------------------------------------
# Particle explosion effect (random burst)
# ---------------------------------------------------------------------------
class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        angle = random.uniform(0, 6.28)
        speed = random.uniform(1, 5)
        self.vx = speed * random.uniform(-1, 1)
        self.vy = speed * random.uniform(-1, 1)
        self.life = random.randint(15, 30)
        self.color = color
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surf):
        if self.life > 0:
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.size)


def explode(x, y, color, particles, count=15):
    for _ in range(count):
        particles.append(Particle(x, y, color))


# ---------------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------------
def new_game():
    return {
        "player": Player(),
        "bullets": [],
        "enemy_bullets": [],
        "enemies": [],
        "powerups": [],
        "particles": [],
        "stars": [Star() for _ in range(80)],
        "score": 0,
        "spawn_timer": 0,
        "spawn_interval": 60,
        "rapid_timer": 0,
        "shield_timer": 0,
        "game_over": False,
    }


state = new_game()


def draw_hud(state):
    score_text = font_small.render(f"Score: {state['score']}", True, WHITE)
    lives_text = font_small.render(f"Lives: {state['player'].lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 32))
    if state["rapid_timer"] > 0:
        screen.blit(font_small.render("RAPID FIRE!", True, CYAN), (WIDTH - 140, 10))
    if state["shield_timer"] > 0:
        screen.blit(font_small.render("SHIELD!", True, YELLOW), (WIDTH - 140, 32))


def draw_game_over(state):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    go_text = font_big.render("GAME OVER", True, RED)
    score_text = font_med.render(f"Final Score: {state['score']}", True, WHITE)
    hint_text = font_small.render("Press R to restart", True, GREY)

    screen.blit(go_text, go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
    screen.blit(hint_text, hint_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main():
    global state
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and state["game_over"]:
                    state = new_game()

        keys = pygame.key.get_pressed()

        # Stars always animate
        for star in state["stars"]:
            star.update()

        if not state["game_over"]:
            player = state["player"]
            player.update(keys)

            if keys[pygame.K_SPACE]:
                player.shoot(state["bullets"])

            # Rapid fire effect shortens cooldown
            if state["rapid_timer"] > 0:
                player.cooldown_max = 4
                state["rapid_timer"] -= 1
            else:
                player.cooldown_max = 12

            if state["shield_timer"] > 0:
                state["shield_timer"] -= 1

            # --- spawn enemies at random intervals ---
            state["spawn_timer"] += 1
            if state["spawn_timer"] >= state["spawn_interval"]:
                state["spawn_timer"] = 0
                state["enemies"].append(Enemy())
                # gradually speed up spawning, with randomness
                state["spawn_interval"] = max(20, state["spawn_interval"] - 1)

            # --- update bullets ---
            for b in state["bullets"]:
                b.update()
            state["bullets"] = [b for b in state["bullets"] if not b.offscreen()]

            # --- enemy random shooting ---
            for e in state["enemies"]:
                e.update()
                if random.random() < 0.004:  # random chance to fire
                    cx = e.x + e.size // 2
                    state["enemy_bullets"].append(Bullet(cx, e.y + e.size, 5, RED, 4, 10))

            for b in state["enemy_bullets"]:
                b.update()
            state["enemy_bullets"] = [b for b in state["enemy_bullets"] if not b.offscreen()]

            # --- powerups ---
            for p in state["powerups"]:
                p.update()
            state["powerups"] = [p for p in state["powerups"] if not p.offscreen()]

            # --- particles ---
            for pt in state["particles"]:
                pt.update()
            state["particles"] = [pt for pt in state["particles"] if pt.life > 0]

            # --- collisions: player bullets vs enemies ---
            for b in state["bullets"][:]:
                for e in state["enemies"][:]:
                    if b.rect.colliderect(e.rect):
                        e.hp -= 1
                        if b in state["bullets"]:
                            state["bullets"].remove(b)
                        if e.hp <= 0:
                            explode(e.x + e.size / 2, e.y + e.size / 2, e.color, state["particles"])
                            state["score"] += e.score_value
                            # random chance to drop a powerup
                            if random.random() < 0.18:
                                state["powerups"].append(
                                    PowerUp(e.x + e.size / 2, e.y + e.size / 2)
                                )
                            if e in state["enemies"]:
                                state["enemies"].remove(e)
                        break

            # remove offscreen enemies
            state["enemies"] = [e for e in state["enemies"] if not e.offscreen()]

            # --- collisions: enemy bullets vs player ---
            if state["shield_timer"] <= 0 and player.invuln <= 0:
                for b in state["enemy_bullets"][:]:
                    if b.rect.colliderect(player.rect):
                        state["enemy_bullets"].remove(b)
                        player.lives -= 1
                        player.invuln = 90
                        explode(player.x + player.w / 2, player.y + player.h / 2, GREEN, state["particles"])
                        if player.lives <= 0:
                            state["game_over"] = True

                # --- collisions: enemies vs player (crash) ---
                for e in state["enemies"][:]:
                    if e.rect.colliderect(player.rect):
                        state["enemies"].remove(e)
                        player.lives -= 1
                        player.invuln = 90
                        explode(player.x + player.w / 2, player.y + player.h / 2, GREEN, state["particles"])
                        if player.lives <= 0:
                            state["game_over"] = True

            # --- collisions: powerups vs player ---
            for p in state["powerups"][:]:
                if p.rect.colliderect(player.rect):
                    state["powerups"].remove(p)
                    if p.kind == "rapid":
                        state["rapid_timer"] = 300
                    elif p.kind == "life":
                        player.lives = min(5, player.lives + 1)
                    elif p.kind == "shield":
                        state["shield_timer"] = 300

        # ------------------- DRAW -------------------
        screen.fill(BLACK)
        for star in state["stars"]:
            star.draw(screen)

        for b in state["bullets"]:
            b.draw(screen)
        for b in state["enemy_bullets"]:
            b.draw(screen)
        for e in state["enemies"]:
            e.draw(screen)
        for p in state["powerups"]:
            p.draw(screen)
        for pt in state["particles"]:
            pt.draw(screen)

        if not state["game_over"]:
            state["player"].draw(screen)
            if state["shield_timer"] > 0:
                pygame.draw.circle(
                    screen, YELLOW,
                    (int(state["player"].x + state["player"].w / 2),
                     int(state["player"].y + state["player"].h / 2)),
                    30, width=2
                )

        draw_hud(state)

        if state["game_over"]:
            draw_game_over(state)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()