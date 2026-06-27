import pygame


import random
import math
import sys

# ── Init ──────────────────────────────────────────────────────────────────────
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
FPS = 60

# ── Colors ────────────────────────────────────────────────────────────────────
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
CYAN       = (0,   220, 255)
YELLOW     = (255, 220,   0)
RED        = (255,  50,  50)
ORANGE     = (255, 140,   0)
GREEN      = (50,  220,  80)
PURPLE     = (180,  80, 255)
DARK_BLUE  = (5,   10,  30)
STAR_COLOR = (180, 180, 220)

# ── Fonts ─────────────────────────────────────────────────────────────────────
font_lg = pygame.font.SysFont("consolas", 48, bold=True)
font_md = pygame.font.SysFont("consolas", 28, bold=True)
font_sm = pygame.font.SysFont("consolas", 20)

# ── Helpers ───────────────────────────────────────────────────────────────────
def draw_text(surf, text, font, color, cx, cy):
    img = font.render(text, True, color)
    surf.blit(img, img.get_rect(center=(cx, cy)))

def draw_text_left(surf, text, font, color, x, y):
    surf.blit(font.render(text, True, color), (x, y))

# ── Stars (parallax background) ───────────────────────────────────────────────
class Star:
    def __init__(self):
        self.reset(random.randint(0, HEIGHT))

    def reset(self, y=0):
        self.x = random.randint(0, WIDTH)
        self.y = y
        self.speed = random.uniform(0.5, 2.5)

        if self.speed < 1.2:
            self.size = 1
        elif self.speed < 2:
            self.size = 2
        else:
            self.size = 3

        # Prevent color overflow
        self.alpha = min(225, int(80 + self.speed * 60))

    def update(self):
        self.y += self.speed

        if self.y > HEIGHT:
            self.reset()

    def draw(self, surf):
        c = self.alpha

        color = (
            min(c, 255),
            min(c, 255),
            min(c + 30, 255)
        )

        pygame.draw.circle(
            surf,
            color,
            (int(self.x), int(self.y)),
            self.size
        )
stars = [Star() for _ in range(160)]
# class Star:
#     def __init__(self):
#         self.reset(random.randint(0, HEIGHT))
#
#     def reset(self, y=0):
#         self.x     = random.randint(0, WIDTH)
#         self.y     = y
#         self.speed = random.uniform(0.5, 2.5)
#         self.size  = 1 if self.speed < 1.2 else (2 if self.speed < 2 else 3)
#         self.alpha = int(80 + self.speed * 60)
#
#     def update(self):
#         self.y += self.speed
#         if self.y > HEIGHT:
#             self.reset()
#
#     def draw(self, surf):
#         c = min(255, self.alpha)
#         pygame.draw.circle(surf, (c, c, c + 30), (int(self.x), int(self.y)), self.size)
#
# stars = [Star() for _ in range(160)]

# ── Particle ──────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, life=None, size=None):
        self.x    = x
        self.y    = y
        self.color= color
        self.vx   = vx if vx is not None else random.uniform(-3, 3)
        self.vy   = vy if vy is not None else random.uniform(-3, 3)
        self.life = life if life is not None else random.randint(20, 45)
        self.max  = self.life
        self.size = size if size is not None else random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08
        self.life -= 1

    def draw(self, surf):
        alpha = self.life / self.max
        r = max(1, int(self.size * alpha))
        c = tuple(int(v * alpha) for v in self.color)
        pygame.draw.circle(surf, c, (int(self.x), int(self.y)), r)

# ── Bullet ────────────────────────────────────────────────────────────────────
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vy=-12, color=CYAN, damage=1):
        super().__init__()
        self.image = pygame.Surface((4, 16), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, 4, 16), border_radius=2)
        # glow
        glow = pygame.Surface((10, 22), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (*color, 60), (0, 0, 10, 22))
        self.image.blit(glow, (-3, -3))
        self.rect   = self.image.get_rect(center=(x, y))
        self.vy     = vy
        self.damage = damage

    def update(self):
        self.rect.y += self.vy
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# ── Enemy bullet ─────────────────────────────────────────────────────────────
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=90):
        super().__init__()
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (3, 3), 3)
        self.rect  = self.image.get_rect(center=(x, y))
        rad = math.radians(angle)
        spd = 5
        self.vx = math.cos(rad) * spd
        self.vy = math.sin(rad) * spd

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.top > HEIGHT or self.rect.bottom < 0 or
                self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()

# ── Player ────────────────────────────────────────────────────────────────────
def make_player_surf():
    s = pygame.Surface((48, 52), pygame.SRCALPHA)
    # body
    body = [(24, 0), (8, 42), (24, 34), (40, 42)]
    pygame.draw.polygon(s, CYAN, body)
    pygame.draw.polygon(s, WHITE, body, 2)
    # wings
    lwing = [(8, 42), (0, 52), (18, 44)]
    rwing = [(40, 42), (48, 52), (30, 44)]
    pygame.draw.polygon(s, CYAN, lwing)
    pygame.draw.polygon(s, CYAN, rwing)
    # cockpit
    pygame.draw.ellipse(s, (180, 240, 255), (18, 12, 12, 16))
    # engine glow
    pygame.draw.ellipse(s, ORANGE, (20, 40, 8, 6))
    return s

PLAYER_SURF = make_player_surf()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = PLAYER_SURF.copy()
        self.image  = self.image_orig.copy()
        self.rect   = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        self.speed  = 6
        self.lives  = 3
        self.score  = 0
        self.shoot_delay = 220       # ms
        self.last_shot   = 0
        self.invincible  = False
        self.inv_timer   = 0
        self.INV_DURATION= 2000      # ms
        self.blink       = 0
        self.engine_particles = []
        self.power_level = 1         # 1, 2, or 3
        self.power_timer = 0

    def update(self, keys, now, particles):
        # Movement
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.rect.x += self.speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect())

        # Engine particles
        if random.random() < 0.6:
            px = self.rect.centerx + random.randint(-6, 6)
            py = self.rect.bottom - 10
            particles.append(Particle(px, py, ORANGE,
                vx=random.uniform(-1, 1), vy=random.uniform(2, 5),
                life=random.randint(8, 18), size=random.randint(2, 4)))

        # Power-up decay
        if self.power_level > 1:
            if now - self.power_timer > 8000:
                self.power_level = max(1, self.power_level - 1)
                self.power_timer = now

        # Invincibility blink
        if self.invincible:
            self.blink += 1
            if self.blink % 6 < 3:
                self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
            else:
                self.image = self.image_orig.copy()
            if now - self.inv_timer > self.INV_DURATION:
                self.invincible = False
                self.image = self.image_orig.copy()
        else:
            self.image = self.image_orig.copy()

    def shoot(self, now, bullets):
        if now - self.last_shot < self.shoot_delay:
            return
        self.last_shot = now
        cx, cy = self.rect.centerx, self.rect.top + 5
        if self.power_level == 1:
            bullets.add(Bullet(cx, cy))
        elif self.power_level == 2:
            bullets.add(Bullet(cx - 10, cy + 8))
            bullets.add(Bullet(cx + 10, cy + 8))
        else:
            bullets.add(Bullet(cx, cy))
            bullets.add(Bullet(cx - 14, cy + 10))
            bullets.add(Bullet(cx + 14, cy + 10))

    def hit(self, now):
        if self.invincible:
            return False
        self.lives -= 1
        self.invincible = True
        self.inv_timer  = now
        return True

# ── Enemy types ───────────────────────────────────────────────────────────────
def make_enemy_surf(kind):
    if kind == "grunt":
        s = pygame.Surface((36, 30), pygame.SRCALPHA)
        body = [(18, 0), (36, 20), (28, 30), (8, 30), (0, 20)]
        pygame.draw.polygon(s, RED, body)
        pygame.draw.polygon(s, (255, 120, 120), body, 2)
        pygame.draw.circle(s, ORANGE, (18, 16), 6)
    elif kind == "shooter":
        s = pygame.Surface((38, 34), pygame.SRCALPHA)
        body = [(19, 0), (38, 18), (30, 34), (8, 34), (0, 18)]
        pygame.draw.polygon(s, PURPLE, body)
        pygame.draw.polygon(s, (200, 140, 255), body, 2)
        pygame.draw.circle(s, (255, 200, 255), (19, 18), 7)
        pygame.draw.line(s, WHITE, (4, 34), (4, 26), 3)
        pygame.draw.line(s, WHITE, (34, 34), (34, 26), 3)
    elif kind == "tank":
        s = pygame.Surface((50, 40), pygame.SRCALPHA)
        pygame.draw.rect(s, (200, 60, 60), (5, 5, 40, 30), border_radius=6)
        pygame.draw.rect(s, (255, 100, 100), (5, 5, 40, 30), 2, border_radius=6)
        pygame.draw.circle(s, YELLOW, (25, 20), 10)
        pygame.draw.circle(s, ORANGE, (25, 20), 6)
    elif kind == "boss":
        s = pygame.Surface((100, 80), pygame.SRCALPHA)
        body = [(50, 0), (100, 40), (80, 80), (20, 80), (0, 40)]
        pygame.draw.polygon(s, (180, 30, 30), body)
        pygame.draw.polygon(s, YELLOW, body, 3)
        for cx, cy in [(20,50),(50,30),(80,50)]:
            pygame.draw.circle(s, ORANGE, (cx, cy), 8)
            pygame.draw.circle(s, YELLOW, (cx, cy), 4)
        pygame.draw.rect(s, RED, (10, 70, 80, 8), border_radius=4)
    return s

ENEMY_SURFS = {k: make_enemy_surf(k) for k in ("grunt","shooter","tank","boss")}

class Enemy(pygame.sprite.Sprite):
    STATS = {
        "grunt":   {"hp":1, "speed":1.8, "score":10,  "shoot_chance":0},
        "shooter": {"hp":2, "speed":1.4, "score":20,  "shoot_chance":0.003},
        "tank":    {"hp":5, "speed":0.9, "score":40,  "shoot_chance":0.001},
        "boss":    {"hp":40,"speed":0.7, "score":300, "shoot_chance":0.008},
    }
    def __init__(self, kind, x, y, wave=1):
        super().__init__()
        self.kind  = kind
        st         = self.STATS[kind]
        self.image_orig = ENEMY_SURFS[kind].copy()
        self.image = self.image_orig.copy()
        self.rect  = self.image.get_rect(center=(x, y))
        self.hp    = st["hp"] + wave // 3
        self.max_hp= self.hp
        self.speed = st["speed"] + wave * 0.05
        self.score_val = st["score"]
        self.shoot_chance = st["shoot_chance"]
        self.dx    = self.speed
        self.drop  = False
        self.drop_amount = 30
        self.dropping= 0

    def update(self, enemy_bullets):
        if self.dropping > 0:
            self.rect.y += 2
            self.dropping -= 2
        else:
            self.rect.x += self.dx

        # Shoot
        if self.shoot_chance and random.random() < self.shoot_chance:
            self.fire(enemy_bullets)

        # HP-based tint
        ratio = self.hp / self.max_hp
        if ratio < 0.4:
            tint = pygame.Surface(self.image_orig.get_size(), pygame.SRCALPHA)
            tint.fill((255, 0, 0, int((1 - ratio) * 120)))
            img = self.image_orig.copy()
            img.blit(tint, (0, 0))
            self.image = img
        else:
            self.image = self.image_orig.copy()

    def fire(self, enemy_bullets):
        cx, cy = self.rect.centerx, self.rect.bottom
        if self.kind == "boss":
            for angle in [80, 90, 100]:
                enemy_bullets.add(EnemyBullet(cx, cy, angle))
        else:
            enemy_bullets.add(EnemyBullet(cx, cy, 90))

    def draw_hp_bar(self, surf):
        if self.kind not in ("tank", "boss"):
            return
        bar_w = self.rect.width
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surf, (80, 0, 0),   (self.rect.x, self.rect.y - 8, bar_w, 5))
        pygame.draw.rect(surf, GREEN,          (self.rect.x, self.rect.y - 8, int(bar_w * ratio), 5))

# ── Powerup ───────────────────────────────────────────────────────────────────
class PowerUp(pygame.sprite.Sprite):
    TYPES = ["triple", "double", "shield"]
    COLORS= {"triple": YELLOW, "double": GREEN, "shield": CYAN}

    def __init__(self, x, y):
        super().__init__()
        self.ptype = random.choice(self.TYPES)
        self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
        c = self.COLORS[self.ptype]
        pygame.draw.circle(self.image, c, (11, 11), 11)
        pygame.draw.circle(self.image, WHITE, (11, 11), 11, 2)
        label = font_sm.render(self.ptype[0].upper(), True, BLACK)
        self.image.blit(label, label.get_rect(center=(11, 11)))
        self.rect = self.image.get_rect(center=(x, y))
        self.vy   = 2

    def update(self):
        self.rect.y += self.vy
        if self.rect.top > HEIGHT:
            self.kill()

# ── Wave manager ──────────────────────────────────────────────────────────────
def spawn_wave(wave, enemies):
    enemies.empty()
    cols  = min(6 + wave, 11)
    rows  = min(2 + wave // 2, 5)
    kinds = ["grunt"] * 4 + ["shooter"] * 2 + ["tank"]
    start_x = (WIDTH - cols * 60) // 2 + 30
    for row in range(rows):
        for col in range(cols):
            if row == 0 and wave > 0 and wave % 3 == 0:
                kind = "tank"
            elif row < 2:
                kind = random.choice(["grunt","shooter"]) if wave > 2 else "grunt"
            else:
                kind = random.choice(kinds)
            x = start_x + col * 60
            y = 60 + row * 55
            enemies.add(Enemy(kind, x, y, wave))

def spawn_boss(wave, enemies):
    enemies.empty()
    enemies.add(Enemy("boss", WIDTH // 2, 80, wave))

# ── HUD ───────────────────────────────────────────────────────────────────────
def draw_hud(surf, player, wave, boss_hp=None, boss_max=None):
    # Score
    draw_text_left(surf, f"SCORE  {player.score:06d}", font_sm, CYAN, 10, 10)
    # Wave
    draw_text(surf, f"WAVE {wave}", font_sm, WHITE, WIDTH // 2, 12)
    # Lives
    for i in range(player.lives):
        sx = WIDTH - 30 - i * 26
        pts = [(sx, 0), (sx-8, 16), (sx, 11), (sx+8, 16)]
        pygame.draw.polygon(surf, CYAN, [(x, y+6) for x,y in pts])
    # Power level
    pw_color = [WHITE, GREEN, YELLOW][player.power_level - 1]
    draw_text_left(surf, f"PWR {'▮'*player.power_level}", font_sm, pw_color, 10, 32)
    # Boss HP bar
    if boss_hp is not None:
        bar_w = WIDTH - 100
        ratio = boss_hp / boss_max
        pygame.draw.rect(surf, (80, 0, 0),   (50, HEIGHT - 28, bar_w, 16), border_radius=8)
        pygame.draw.rect(surf, RED,           (50, HEIGHT - 28, int(bar_w * ratio), 16), border_radius=8)
        draw_text(surf, "BOSS", font_sm, YELLOW, WIDTH // 2, HEIGHT - 20)

# ── Screens ───────────────────────────────────────────────────────────────────
def draw_bg(surf):
    surf.fill(DARK_BLUE)
    for s in stars:
        s.update()
        s.draw(surf)

def title_screen():
    waiting = True
    t = 0
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                waiting = False

        draw_bg(screen)
        t += 1
        pulse = abs(math.sin(t * 0.04))
        draw_text(screen, "SPACE SHOOTER", font_lg, CYAN, WIDTH//2, 180)
        draw_text(screen, "ARROW KEYS / WASD  — move", font_sm, WHITE, WIDTH//2, 280)
        draw_text(screen, "SPACE / Z  — shoot", font_sm, WHITE, WIDTH//2, 310)
        draw_text(screen, "Collect power-ups to upgrade!", font_sm, GREEN, WIDTH//2, 345)
        c = tuple(int(200 + 55 * pulse) for _ in range(3))
        draw_text(screen, "PRESS SPACE TO START", font_md, c, WIDTH//2, 420)
        pygame.display.flip(); clock.tick(FPS)

def game_over_screen(score, wave):
    waiting = True
    t = 0
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
                waiting = False
        draw_bg(screen)
        t += 1
        draw_text(screen, "GAME OVER", font_lg, RED, WIDTH//2, 200)
        draw_text(screen, f"Score: {score:06d}", font_md, YELLOW, WIDTH//2, 290)
        draw_text(screen, f"Waves survived: {wave}", font_sm, WHITE, WIDTH//2, 340)
        pulse = abs(math.sin(t * 0.05))
        c = tuple(int(180 + 75 * pulse) for _ in range(3))
        draw_text(screen, "PRESS SPACE TO PLAY AGAIN", font_md, c, WIDTH//2, 410)
        pygame.display.flip(); clock.tick(FPS)

def wave_clear_screen(wave, score):
    for frame in range(90):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        draw_bg(screen)
        alpha = min(255, frame * 8)
        msg = font_md.render(f"WAVE {wave} CLEAR!", True, YELLOW)
        msg.set_alpha(alpha)
        screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
        sc = font_sm.render(f"Score: {score:06d}", True, WHITE)
        sc.set_alpha(alpha)
        screen.blit(sc, sc.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))
        pygame.display.flip(); clock.tick(FPS)

# ── Explosion helper ──────────────────────────────────────────────────────────
def explode(x, y, particles, count=30, colors=(RED, ORANGE, YELLOW, WHITE)):
    for _ in range(count):
        particles.append(Particle(x, y, random.choice(colors),
            vx=random.uniform(-4, 4), vy=random.uniform(-4, 4),
            life=random.randint(25, 55), size=random.randint(2, 6)))

# ── Main game loop ────────────────────────────────────────────────────────────
def run_game():
    player        = Player()
    all_sprites   = pygame.sprite.Group()
    enemies       = pygame.sprite.Group()
    bullets       = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    powerups      = pygame.sprite.Group()
    all_sprites.add(player)

    particles: list[Particle] = []
    wave      = 1
    boss_wave = False
    spawn_wave(wave, enemies)
    all_sprites.add(*enemies)

    powerup_drop_chance = 0.15
    running = True

    while running:
        now  = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # ── Events ──
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return  # back to title

        # ── Shoot ──
        if keys[pygame.K_SPACE] or keys[pygame.K_z]:
            player.shoot(now, bullets)
            all_sprites.add(*[b for b in bullets if b not in all_sprites])

        # ── Update ──
        player.update(keys, now, particles)
        for b in list(bullets):
            b.update()
        for eb in list(enemy_bullets):
            eb.update()
        for p in list(powerups):
            p.update()

        # Enemy edge-bounce + drop
        edge_hit = False
        for en in enemies:
            if en.rect.right >= WIDTH or en.rect.left <= 0:
                edge_hit = True; break
        if edge_hit:
            for en in enemies:
                en.dx     *= -1
                en.dropping= en.drop_amount

        for en in enemies:
            en.update(enemy_bullets)
            all_sprites.add(*[eb for eb in enemy_bullets if eb not in all_sprites])

        # Particle update
        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)

        # ── Collisions: bullets vs enemies ──
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for en, blist in hits.items():
            for b in blist:
                en.hp -= b.damage
                explode(b.rect.centerx, b.rect.centery, particles, 8, (ORANGE, YELLOW))
            if en.hp <= 0:
                player.score += en.score_val
                explode(en.rect.centerx, en.rect.centery, particles, 35)
                if random.random() < powerup_drop_chance:
                    pu = PowerUp(en.rect.centerx, en.rect.centery)
                    powerups.add(pu)
                    all_sprites.add(pu)
                en.kill()

        # ── Collisions: enemy bullets vs player ──
        if not player.invincible:
            if pygame.sprite.spritecollide(player, enemy_bullets, True):
                if player.hit(now):
                    explode(player.rect.centerx, player.rect.centery,
                            particles, 20, (CYAN, WHITE))
                    if player.lives <= 0:
                        explode(player.rect.centerx, player.rect.centery,
                                particles, 60)
                        running = False

        # ── Collisions: enemies vs player (ramming) ──
        if not player.invincible:
            ram = pygame.sprite.spritecollide(player, enemies, False)
            if ram:
                if player.hit(now):
                    for en in ram: en.hp -= 1
                    explode(player.rect.centerx, player.rect.centery,
                            particles, 20, (CYAN, RED))
                    if player.lives <= 0:
                        running = False

        # ── Enemies reach bottom ──
        for en in list(enemies):
            if en.rect.bottom > HEIGHT - 40:
                if player.hit(now):
                    explode(en.rect.centerx, en.rect.centery, particles, 20)
                    en.kill()
                    if player.lives <= 0:
                        running = False

        # ── Power-ups ──
        pu_hits = pygame.sprite.spritecollide(player, powerups, True)
        for pu in pu_hits:
            if pu.ptype in ("double", "triple"):
                player.power_level = 2 if pu.ptype == "double" else 3
                player.power_timer = now
            elif pu.ptype == "shield":
                player.invincible = True
                player.inv_timer  = now
                player.INV_DURATION = 3000
            explode(pu.rect.centerx, pu.rect.centery, particles,
                    15, (YELLOW, GREEN, WHITE))

        # ── Wave clear ──
        if len(enemies) == 0 and running:
            # clean up stray bullets
            enemy_bullets.empty()
            bullets.empty()
            wave_clear_screen(wave, player.score)
            wave += 1
            boss_wave = (wave % 5 == 0)
            if boss_wave:
                spawn_boss(wave, enemies)
            else:
                spawn_wave(wave, enemies)
            all_sprites.add(*enemies)

        # ── Draw ──
        draw_bg(screen)

        for p in particles:
            p.draw(screen)

        for en in enemies:
            screen.blit(en.image, en.rect)
            en.draw_hp_bar(screen)

        for b in bullets:
            screen.blit(b.image, b.rect)
        for eb in enemy_bullets:
            screen.blit(eb.image, eb.rect)
        for pu in powerups:
            screen.blit(pu.image, pu.rect)

        screen.blit(player.image, player.rect)

        # Boss HP bar
        boss_hp = boss_max = None
        for en in enemies:
            if en.kind == "boss":
                boss_hp  = en.hp
                boss_max = en.max_hp
        draw_hud(screen, player, wave, boss_hp, boss_max)

        pygame.display.flip()
        clock.tick(FPS)

    # Short death animation
    for _ in range(60):
        draw_bg(screen)
        for p in particles:
            p.update(); p.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    game_over_screen(player.score, wave)

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        title_screen()
        run_game()
