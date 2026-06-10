import tkinter as tk
import math
import random
import time

# --- CONFIGURATION & CONSTANTS ---
WIDTH, HEIGHT = 800, 600
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 16
MAP_SIZE = 16

# ── LEVEL THEMES ─────────────────────────────────────────────────────────────
LEVEL_THEMES = {
    "default": {
        "name": "The Backrooms",
        "wall_color": (185, 170, 105),
        "ceiling_color": "#ded6a6",
        "floor_color": "#786d43",
        "entity_color": (20, 10, 30),
        "entity_outline": "#ff0000",
        "entity_label": "ENTITY",
        "projectile_color": "#ff0000",
        "projectile_label": "●",
        "pickup_label": "almond water",
        "pickup_color": "#88ffcc",
        "ambient_lines": [
            "you shouldn't be here.",
            "it knows where you are.",
            "did you hear that?",
            "the lights are getting worse.",
            "level 0 has no exit.",
            "stop. listen.",
            "how long have you been walking?",
            "it's getting closer.",
        ],
        "death_msg": "YOU LINGERED TOO LONG",
        "pickups_label": "ALMOND WATER",
        "hud_color": "yellow",
        "sanity_label": "SANITY",
        "scatter_items": [],
        "scatter_color": "#888888",
        "scatter_label": "~",
    },
    "timmy": {
        "name": "Timmy's Blue Diamond",
        "wall_color": (60, 80, 180),
        "ceiling_color": "#1a2a6c",
        "floor_color": "#0d1a4a",
        "entity_color": (200, 50, 20),
        "entity_outline": "#ff4400",
        "entity_label": "PASTA MONSTER",
        "projectile_color": "#cc2200",
        "projectile_label": "🍝",
        "pickup_label": "baseball bat",
        "pickup_color": "#88aaff",
        "ambient_lines": [
            "mama mia, get back here!",
            "the sauce... it burns.",
            "batter up... or batter DOWN.",
            "SPLAT.",
            "is that marinara?!",
            "swing and a miss—OH NO.",
            "the pasta never misses.",
            "blue walls. red sauce. run.",
        ],
        "death_msg": "COVERED IN PASTA SAUCE",
        "pickups_label": "BASEBALL BATS",
        "hud_color": "#88aaff",
        "sanity_label": "SANITY",
        "scatter_items": "bats",
        "scatter_color": "#bbccff",
        "scatter_label": "⌐",
    },
    "felix": {
        "name": "Felix's Ugly Dungeon",
        "wall_color": (80, 60, 40),
        "ceiling_color": "#2a1a0a",
        "floor_color": "#1a0f05",
        "entity_color": (60, 20, 80),
        "entity_outline": "#cc00ff",
        "entity_label": "FELIX",
        "projectile_color": "#cc00ff",
        "projectile_label": "🥁",
        "pickup_label": "broken golf club",
        "pickup_color": "#aaaa00",
        "ambient_lines": [
            "DOUBLE KICK INCOMING.",
            "the drumsticks are everywhere.",
            "that's not a golf swing.",
            "tat tat tat tat TAT.",
            "this place looks terrible.",
            "is that a 9-iron?",
            "he's behind the kit again.",
            "BOOM BOOM CRASH.",
        ],
        "death_msg": "DOUBLE KICKED INTO OBLIVION",
        "pickups_label": "GOLF CLUBS",
        "hud_color": "#cc00ff",
        "sanity_label": "RHYTHM",
        "scatter_items": "clubs",
        "scatter_color": "#aaaa44",
        "scatter_label": "╱",
    },
    "lucas": {
        "name": "Lucas's Tiger Woods Zone",
        "wall_color": (30, 80, 30),
        "ceiling_color": "#0a2a0a",
        "floor_color": "#051505",
        "entity_color": (40, 140, 40),
        "entity_outline": "#ffdd00",
        "entity_label": "CHILD TIGER",
        "projectile_color": "#ffdd00",
        "projectile_label": "🚗",
        "pickup_label": "golf ball",
        "pickup_color": "#ffffff",
        "ambient_lines": [
            "FORE!",
            "vroom vroom... oh no.",
            "he's driving again.",
            "this is a par 5 nightmare.",
            "watch out for the cart path.",
            "UNDER PAR... UNDER A CAR.",
            "tiny cleats. big problems.",
            "is he allowed on this course?",
        ],
        "death_msg": "DRUNK DRIVEN INTO THE ROUGH",
        "pickups_label": "GOLF BALLS",
        "hud_color": "#ffdd00",
        "sanity_label": "FOCUS",
        "scatter_items": "flags",
        "scatter_color": "#44cc44",
        "scatter_label": "⚑",
    },
    "marshall": {
        "name": "Marshall's Lucky Charms",
        "wall_color": (150, 50, 150),
        "ceiling_color": "#3a0a3a",
        "floor_color": "#200a20",
        "entity_color": (0, 160, 0),
        "entity_outline": "#ffdd00",
        "entity_label": "LEPRECHAUN",
        "projectile_color": "#ffdd00",
        "projectile_label": "🌈",
        "pickup_label": "marshmallow",
        "pickup_color": "#ffaaff",
        "ambient_lines": [
            "they're after me lucky charms!",
            "catch me pot o' gold!",
            "magically delicious... AND DEADLY.",
            "rainbow incoming!",
            "green with envy? you should be.",
            "hearts, stars, and HORSESHOES.",
            "the leprechaun has no mercy.",
            "lucky? not today.",
        ],
        "death_msg": "PELTED WITH MARSHMALLOWS",
        "pickups_label": "MARSHMALLOWS",
        "hud_color": "#ffaaff",
        "sanity_label": "LUCK",
        "scatter_items": "clovers",
        "scatter_color": "#44ff44",
        "scatter_label": "☘",
    },
    "ricky": {
        "name": "Ricky's Yankee Stadium",
        "wall_color": (10, 10, 60),
        "ceiling_color": "#000020",
        "floor_color": "#050510",
        "entity_color": (180, 180, 180),
        "entity_outline": "#c0c0c0",
        "entity_label": "RICKY",
        "projectile_color": "#ffffff",
        "projectile_label": "⚾",
        "pickup_label": "hot dog",
        "pickup_color": "#ffbb44",
        "ambient_lines": [
            "PLAY BALL.",
            "fastball, 98 mph. you're dead.",
            "yankees win. you lose.",
            "the crowd goes wild.",
            "take me out to the BALL GAME.",
            "STRIKE THREE. you're out.",
            "he winds up... he throws.",
            "pinstripes in the dark.",
        ],
        "death_msg": "HIT BY PITCH — YOU'RE OUT",
        "pickups_label": "HOT DOGS",
        "hud_color": "#c0c0ff",
        "sanity_label": "FOCUS",
        "scatter_items": "bases",
        "scatter_color": "#ffffff",
        "scatter_label": "◇",
    },
}

LEVEL_ORDER = ["timmy", "felix", "lucas", "marshall", "ricky", "default"]
LEVEL_DISPLAY = {
    "timmy":   "Timmy",
    "felix":   "Felix",
    "lucas":   "Lucas",
    "marshall":"Marshall",
    "ricky":   "Ricky",
    "default": "Classic",
}


class Projectile:
    def __init__(self, x, y, tx, ty, color, label):
        self.x = x
        self.y = y
        dist = math.hypot(tx - x, ty - y)
        if dist > 0:
            self.vx = (tx - x) / dist * 0.12
            self.vy = (ty - y) / dist * 0.12
        else:
            self.vx, self.vy = 0.1, 0
        self.color = color
        self.label = label
        self.alive = True


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("The Backrooms — Level Select")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.current_level = "default"
        self.menu_open = False
        self.running = True

        # Game state
        self._init_state()

        # Bind keys
        self.root.bind("<KeyPress>",   self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)

        # Start on menu
        self.menu_open = True
        self.last_time = time.time()
        self.tick()

    # ── STATE INIT ────────────────────────────────────────────────────────────

    def _init_state(self):
        self.score   = 0
        self.sanity  = 100.0
        self.stamina = 100.0
        self.game_over = False
        self.px, self.py, self.pa = 2.5, 2.5, 0.0
        self.ex, self.ey = MAP_SIZE - 3, MAP_SIZE - 3
        self.entity_speed  = 0.02
        self.entity_active = False
        self.projectiles   = []
        self.proj_timer    = 0.0
        self.proj_interval = 3.0
        self.pickups       = []
        self.pickup_count  = 0
        self.flicker       = 1.0
        self.flicker_timer = 0.0
        self.flicker_duration = 0.0
        self.next_flicker  = random.uniform(4.0, 10.0)
        self.shake_x = self.shake_y = 0
        self.shake_timer = 0.0
        self.messages  = []
        self.msg_timer = 0.0
        self.next_msg  = random.uniform(8.0, 20.0)
        self.win_flash = 0.0
        self.scatter_cells = []
        self.keys = {
            "w": False, "s": False, "a": False, "d": False,
            "Left": False, "Right": False, "shift": False,
        }
        self.game_map = []
        self.exit_x = self.exit_y = 0

    def _load_level(self, level_key):
        self.current_level = level_key
        self._init_state()
        self.generate_map()

    # ── MAP ───────────────────────────────────────────────────────────────────

    def generate_map(self):
        self.game_map = []
        for y in range(MAP_SIZE):
            row = []
            for x in range(MAP_SIZE):
                if x == 0 or x == MAP_SIZE-1 or y == 0 or y == MAP_SIZE-1:
                    row.append(1)
                elif x < 5 and y < 5:
                    row.append(0)
                else:
                    row.append(1 if random.random() < 0.25 else 0)
            self.game_map.append(row)

        self.exit_x, self.exit_y = MAP_SIZE-2, MAP_SIZE-2
        self.game_map[self.exit_y][self.exit_x] = 2
        self.ex, self.ey = MAP_SIZE-3, MAP_SIZE-3
        self.entity_active = False

        # Scatter pickups
        self.pickups = []
        attempts = 0
        while len(self.pickups) < 4 and attempts < 200:
            cx = random.randint(1, MAP_SIZE-2)
            cy = random.randint(1, MAP_SIZE-2)
            if self.game_map[cy][cx] == 0 and not (cx < 4 and cy < 4) and (cx, cy) not in self.pickups:
                self.pickups.append((cx, cy))
            attempts += 1

        # Scatter decorative items (bats, clubs, etc.)
        self.scatter_cells = []
        theme = LEVEL_THEMES[self.current_level]
        if theme["scatter_items"]:
            attempts = 0
            while len(self.scatter_cells) < 6 and attempts < 300:
                cx = random.randint(1, MAP_SIZE-2)
                cy = random.randint(1, MAP_SIZE-2)
                if self.game_map[cy][cx] == 0 and not (cx < 4 and cy < 4):
                    self.scatter_cells.append((cx, cy))
                attempts += 1

    # ── INPUT ─────────────────────────────────────────────────────────────────

    def key_press(self, event):
        sym = event.keysym
        ch  = event.char
        if sym in self.keys:
            self.keys[sym] = True
        if ch in self.keys:
            self.keys[ch] = True
        if sym in ("Shift_L", "Shift_R"):
            self.keys["shift"] = True

        # Menu toggle
        if ch == "m" or ch == "M":
            self.menu_open = not self.menu_open

        # Restart on game over
        if self.game_over and sym == "space":
            self._load_level(self.current_level)

    def key_release(self, event):
        sym = event.keysym
        ch  = event.char
        if sym in self.keys:
            self.keys[sym] = False
        if ch in self.keys:
            self.keys[ch] = False
        if sym in ("Shift_L", "Shift_R"):
            self.keys["shift"] = False

    # ── UPDATE PLAYER ─────────────────────────────────────────────────────────

    def update_player(self, dt):
        spd = (5.5 if self.keys["shift"] and self.stamina > 0 else 3.0) * dt
        rot = 2.0 * dt

        if self.keys["Left"] or self.keys["a"]:
            self.pa -= rot
        if self.keys["Right"] or self.keys["d"]:
            self.pa += rot

        dx = math.cos(self.pa) * spd
        dy = math.sin(self.pa) * spd

        if self.keys["w"]:
            if self.game_map[int(self.py)][int(self.px + dx*1.5)] != 1:
                self.px += dx
            if self.game_map[int(self.py + dy*1.5)][int(self.px)] != 1:
                self.py += dy
        if self.keys["s"]:
            if self.game_map[int(self.py)][int(self.px - dx*1.5)] != 1:
                self.px -= dx
            if self.game_map[int(self.py - dy*1.5)][int(self.px)] != 1:
                self.py -= dy

        self.pa %= (2 * math.pi)

        # Sprint stamina
        if self.keys["shift"] and self.stamina > 0:
            self.stamina = max(0, self.stamina - dt * 25)
        else:
            self.stamina = min(100, self.stamina + dt * 12)

        # Pickup collection
        cell = (int(self.px), int(self.py))
        if cell in self.pickups:
            self.pickups.remove(cell)
            self.pickup_count += 1
            self.sanity = min(100, self.sanity + 20)
            theme = LEVEL_THEMES[self.current_level]
            self.messages.append([f"+20 {theme['sanity_label'].lower()} from {theme['pickup_label']}!", 2.5])

        # Win condition
        if int(self.px) == self.exit_x and int(self.py) == self.exit_y:
            self.score += 1
            self.sanity = min(100, self.sanity + 30)
            self.generate_map()

    # ── UPDATE ENTITY ─────────────────────────────────────────────────────────

    def update_entity(self, dt):
        self.entity_active = True
        edx = self.px - self.ex
        edy = self.py - self.ey
        dist = math.hypot(edx, edy)

        if dist > 0.1:
            speed = (self.entity_speed + self.score * 0.005) * (dt * 60)
            nx, ny = edx / dist, edy / dist
            new_ex = self.ex + nx * speed
            new_ey = self.ey + ny * speed
            if self.game_map[int(self.ey)][int(new_ex)] != 1:
                self.ex = new_ex
            if self.game_map[int(new_ey)][int(self.ex)] != 1:
                self.ey = new_ey

        if dist < 2.5:
            self.shake_timer = 0.12
            self.shake_x = random.randint(-4, 4)
            self.shake_y = random.randint(-3, 3)

        if dist < 0.4:
            self.game_over = True

        # Projectile launching
        self.proj_timer += dt
        if self.proj_timer >= self.proj_interval and dist < 10:
            self.proj_timer = 0
            theme = LEVEL_THEMES[self.current_level]
            self.projectiles.append(Projectile(
                self.ex, self.ey, self.px, self.py,
                theme["projectile_color"], theme["projectile_label"]
            ))

    # ── UPDATE PROJECTILES ────────────────────────────────────────────────────

    def update_projectiles(self, dt):
        for p in self.projectiles:
            p.x += p.vx
            p.y += p.vy
            # Hit wall
            if (self.game_map[int(p.y)][int(p.x)] == 1 or
                    int(p.x) < 0 or int(p.x) >= MAP_SIZE or
                    int(p.y) < 0 or int(p.y) >= MAP_SIZE):
                p.alive = False
            # Hit player
            if math.hypot(p.x - self.px, p.y - self.py) < 0.4:
                p.alive = False
                self.game_over = True
        self.projectiles = [p for p in self.projectiles if p.alive]

    # ── FLICKER / MESSAGES / SHAKE ───────────────────────────────────────────

    def update_flicker(self, dt):
        self.flicker_timer += dt
        if self.flicker_timer >= self.next_flicker:
            self.flicker_timer = 0
            self.flicker_duration = random.uniform(0.05, 0.3)
            self.flicker = random.uniform(0.3, 0.7)
            self.next_flicker = random.uniform(3.0, 12.0)
        if self.flicker_duration > 0:
            self.flicker_duration -= dt
            if self.flicker_duration <= 0:
                self.flicker = 1.0

    def update_messages(self, dt):
        self.msg_timer += dt
        self.messages = [[t, ttl - dt] for t, ttl in self.messages if ttl - dt > 0]
        if self.msg_timer >= self.next_msg:
            self.msg_timer = 0
            self.next_msg = random.uniform(8.0, 22.0)
            lines = LEVEL_THEMES[self.current_level]["ambient_lines"]
            self.messages.append([random.choice(lines), 3.5])

    def update_shake(self, dt):
        if self.shake_timer > 0:
            self.shake_timer -= dt
            if self.shake_timer <= 0:
                self.shake_x = self.shake_y = 0

    # ── RAYCASTING ────────────────────────────────────────────────────────────

    def render_3d(self):
        self.canvas.delete("all")
        theme = LEVEL_THEMES[self.current_level]

        sx, sy = self.shake_x, self.shake_y

        self.canvas.create_rectangle(sx, sy, WIDTH+sx, HEIGHT//2+sy,
                                     fill=theme["ceiling_color"], outline="")
        self.canvas.create_rectangle(sx, HEIGHT//2+sy, WIDTH+sx, HEIGHT+sy,
                                     fill=theme["floor_color"], outline="")

        ray_angle = self.pa - HALF_FOV
        step_angle = FOV / NUM_RAYS
        w_col = WIDTH / NUM_RAYS
        z_buffer = []

        wc = theme["wall_color"]

        for i in range(NUM_RAYS):
            dist = 0.0
            hit_wall = hit_exit = False
            ca = math.cos(ray_angle)
            sa = math.sin(ray_angle)

            while not hit_wall and dist < MAX_DEPTH:
                dist += 0.05
                tx = int(self.px + ca * dist)
                ty = int(self.py + sa * dist)
                if tx < 0 or tx >= MAP_SIZE or ty < 0 or ty >= MAP_SIZE:
                    hit_wall = True
                    dist = MAX_DEPTH
                else:
                    cell = self.game_map[ty][tx]
                    if cell == 1:
                        hit_wall = True
                    elif cell == 2:
                        hit_wall = True
                        hit_exit = True

            corr = dist * math.cos(ray_angle - self.pa)
            z_buffer.append(corr)

            lh = min(HEIGHT, int(HEIGHT / (corr + 0.0001)))
            lt = HEIGHT//2 - lh//2
            lb = HEIGHT//2 + lh//2

            shadow = (1.0 - min(1.0, corr / MAX_DEPTH)) * self.flicker
            if hit_exit:
                r, g, b = int(130*shadow), int(30*shadow), int(30*shadow)
            else:
                r = int(wc[0] * shadow)
                g = int(wc[1] * shadow)
                b = int(wc[2] * shadow)

            x1 = int(i * w_col) + sx
            x2 = int((i+1) * w_col) + sx
            self.canvas.create_rectangle(x1, lt+sy, x2, lb+sy,
                                         fill=f"#{r:02x}{g:02x}{b:02x}", outline="")
            ray_angle += step_angle

        self._render_sprite(z_buffer)
        self._render_projectiles(z_buffer)
        self._render_scatter(z_buffer)

    def _sprite_screen_pos(self, sx_world, sy_world, z_buffer):
        """Returns (screen_x, sprite_size, visible) for a world sprite."""
        edx = sx_world - self.px
        edy = sy_world - self.py
        dist = math.hypot(edx, edy)
        if dist < 0.2 or dist >= MAX_DEPTH:
            return None
        angle = math.atan2(edy, edx) - self.pa
        while angle >  math.pi: angle -= 2*math.pi
        while angle < -math.pi: angle += 2*math.pi
        if abs(angle) >= HALF_FOV:
            return None
        scr_x = int(WIDTH//2 + math.tan(angle)*(WIDTH//2))
        col = int((scr_x/WIDTH)*NUM_RAYS)
        if not (0 <= col < NUM_RAYS):
            return None
        if z_buffer[col] <= dist:
            return None
        size = min(HEIGHT, int(HEIGHT / dist))
        return scr_x, size, dist

    def _render_sprite(self, z_buffer):
        res = self._sprite_screen_pos(self.ex, self.ey, z_buffer)
        if res is None:
            return
        scr_x, size, dist = res
        theme = LEVEL_THEMES[self.current_level]
        shadow = 1.0 - min(1.0, dist / MAX_DEPTH)
        ec = theme["entity_color"]
        r = int(ec[0]*shadow)
        g = int(ec[1]*shadow)
        b = int(ec[2]*shadow)
        half = size // 4
        cx = scr_x + self.shake_x
        cy = HEIGHT//2 + self.shake_y
        outline = theme["entity_outline"] if random.random() > 0.85 else ""
        self.canvas.create_rectangle(cx-half, cy-size//2, cx+half, cy+size//2,
                                     fill=f"#{r:02x}{g:02x}{b:02x}", outline=outline)
        # Label above
        self.canvas.create_text(cx, cy-size//2-10,
                                text=theme["entity_label"],
                                fill=theme["entity_outline"],
                                font=("Courier", 8, "bold"))

    def _render_projectiles(self, z_buffer):
        for p in self.projectiles:
            res = self._sprite_screen_pos(p.x, p.y, z_buffer)
            if res is None:
                continue
            scr_x, size, dist = res
            ps = max(4, size // 6)
            self.canvas.create_oval(
                scr_x-ps, HEIGHT//2-ps, scr_x+ps, HEIGHT//2+ps,
                fill=p.color, outline="white"
            )

    def _render_scatter(self, z_buffer):
        theme = LEVEL_THEMES[self.current_level]
        if not theme["scatter_items"]:
            return
        for (cx, cy) in self.scatter_cells:
            res = self._sprite_screen_pos(cx + 0.5, cy + 0.5, z_buffer)
            if res is None:
                continue
            scr_x, size, _ = res
            ps = max(3, size // 8)
            self.canvas.create_text(
                scr_x, HEIGHT//2,
                text=theme["scatter_label"],
                fill=theme["scatter_color"],
                font=("Courier", ps+4)
            )

    # ── HUD ───────────────────────────────────────────────────────────────────

    def draw_ui(self):
        theme = LEVEL_THEMES[self.current_level]
        hc = theme["hud_color"]
        sl = theme["sanity_label"]
        pl = theme["pickups_label"]

        # Level name top-center
        self.canvas.create_text(WIDTH//2, 15, text=theme["name"].upper(),
                                fill=hc, font=("Courier", 11, "bold"))

        # Sanity bar
        self.canvas.create_text(70, 25, text=f"{sl}: {int(self.sanity)}%",
                                fill="white", font=("Courier", 11, "bold"))
        self.canvas.create_rectangle(20, 38, 150, 48, outline="white")
        sc = "green" if self.sanity > 50 else ("orange" if self.sanity > 20 else "red")
        self.canvas.create_rectangle(21, 39, 21+int(128*(self.sanity/100)), 47,
                                     fill=sc, outline="")

        # Stamina bar
        self.canvas.create_text(70, 60, text="STAMINA", fill="#aaaaaa",
                                font=("Courier", 9))
        self.canvas.create_rectangle(20, 68, 150, 76, outline="#555555")
        stc = "#4488ff" if self.stamina > 30 else "#ff6622"
        self.canvas.create_rectangle(21, 69, 21+int(128*self.stamina/100), 75,
                                     fill=stc, outline="")

        # Score
        self.canvas.create_text(WIDTH-100, 25, text=f"LEVELS: {self.score}",
                                fill=hc, font=("Courier", 12, "bold"))

        # Pickup counter
        self.canvas.create_text(WIDTH-100, 45, text=f"{pl}: {self.pickup_count}",
                                fill=theme["pickup_color"], font=("Courier", 9, "bold"))

        # Minimap
        m_scale = 6
        mx0 = 20
        my0 = HEIGHT - MAP_SIZE*m_scale - 20
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                cell = self.game_map[y][x]
                color = "#444433" if cell == 1 else ("red" if cell == 2 else "#111111")
                self.canvas.create_rectangle(
                    mx0+x*m_scale, my0+y*m_scale,
                    mx0+x*m_scale+m_scale, my0+y*m_scale+m_scale,
                    fill=color, outline="")
        # Player dot
        self.canvas.create_oval(
            mx0+int(self.px*m_scale)-2, my0+int(self.py*m_scale)-2,
            mx0+int(self.px*m_scale)+2, my0+int(self.py*m_scale)+2,
            fill="cyan", outline="")
        # Entity dot
        self.canvas.create_oval(
            mx0+int(self.ex*m_scale)-2, my0+int(self.ey*m_scale)-2,
            mx0+int(self.ex*m_scale)+2, my0+int(self.ey*m_scale)+2,
            fill="red", outline="")

        # M to menu hint
        self.canvas.create_text(WIDTH-30, HEIGHT-15, text="[M] MENU",
                                fill="#555555", font=("Courier", 9))

    def draw_messages(self):
        y_pos = HEIGHT//2 - 40
        for txt, ttl in self.messages[-3:]:
            alpha = min(1.0, ttl / 1.0)
            gray = int(160 * alpha)
            color = f"#{gray:02x}{gray:02x}{int(gray*0.6):02x}"
            self.canvas.create_text(WIDTH//2 + self.shake_x, y_pos + self.shake_y,
                                    text=txt, fill=color,
                                    font=("Courier", 13, "italic"))
            y_pos += 22

    def draw_vignette(self):
        intensity = int(180 * (1.0 - self.sanity/100.0))
        intensity = max(0, min(180, intensity))
        if intensity < 10:
            return
        color = f"#{intensity//2:02x}0000"
        edge = 80 + intensity
        for rect in [(0, 0, edge, HEIGHT), (WIDTH-edge, 0, WIDTH, HEIGHT),
                     (0, 0, WIDTH, edge//2), (0, HEIGHT-edge//2, WIDTH, HEIGHT)]:
            self.canvas.create_rectangle(*rect, fill=color, outline="", stipple="gray50")

    def render_game_over_screen(self):
        theme = LEVEL_THEMES[self.current_level]
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#050505")
        self.canvas.create_text(WIDTH//2, HEIGHT//2-60,
                                text=theme["death_msg"],
                                fill="#ff0000", font=("Courier", 28, "bold"))
        self.canvas.create_text(WIDTH//2, HEIGHT//2,
                                text=f"Levels Cleared: {self.score}",
                                fill="white", font=("Courier", 16))
        self.canvas.create_text(WIDTH//2, HEIGHT//2+50,
                                text="PRESS [SPACE] TO RESTART   |   [M] FOR MENU",
                                fill="yellow", font=("Courier", 13))

    # ── LEVEL SELECT MENU ────────────────────────────────────────────────────

    def draw_menu(self):
        self.canvas.delete("all")
        # Background
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#0a0a0a")

        # Title
        self.canvas.create_text(WIDTH//2, 70,
                                text="— LEVEL SELECT —",
                                fill="#e0c060", font=("Courier", 26, "bold"))
        self.canvas.create_text(WIDTH//2, 105,
                                text="Click a level to enter. Press M to close menu.",
                                fill="#555555", font=("Courier", 11))

        self.menu_buttons = []
        btn_w, btn_h = 320, 58
        cols = 2
        pad_x = (WIDTH - cols*btn_w - 20) // 2
        pad_y = 150

        descriptions = {
            "timmy":   "Blue walls. Pasta monster. Baseball bats for sanity.",
            "felix":   "Ugly dungeon. Broken clubs & drumsticks everywhere.",
            "lucas":   "Tiger Woods as a child. Drunk-drives into you.",
            "marshall":"Lucky Charms leprechaun throws marshmallows & rainbows.",
            "ricky":   "Yankees stadium. Ricky hurls fastballs at your skull.",
            "default": "The original Backrooms. Classic horror. No gimmicks.",
        }
        colors = {
            "timmy":   "#88aaff",
            "felix":   "#cc00ff",
            "lucas":   "#ffdd00",
            "marshall":"#ffaaff",
            "ricky":   "#c0c0ff",
            "default": "#e0c060",
        }

        for i, key in enumerate(LEVEL_ORDER):
            col = i % cols
            row = i // cols
            x1 = pad_x + col*(btn_w+20)
            y1 = pad_y + row*(btn_h+18)
            x2, y2 = x1+btn_w, y1+btn_h

            active = (key == self.current_level)
            border = colors[key] if active else "#333333"
            bg = "#1a1a2a" if not active else "#0d1520"

            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                    fill=bg, outline=border, width=2)
            self.canvas.create_text(x1+14, y1+16,
                                    text=LEVEL_DISPLAY[key],
                                    fill=colors[key],
                                    font=("Courier", 14, "bold"),
                                    anchor="w")
            self.canvas.create_text(x1+14, y1+36,
                                    text=descriptions[key],
                                    fill="#888888",
                                    font=("Courier", 9),
                                    anchor="w", width=btn_w-20)
            if active:
                self.canvas.create_text(x2-8, y1+8,
                                        text="★ ACTIVE",
                                        fill=colors[key],
                                        font=("Courier", 8, "bold"),
                                        anchor="ne")

            self.menu_buttons.append((x1, y1, x2, y2, key))

        # Bind click once
        self.canvas.bind("<Button-1>", self.menu_click)

    def menu_click(self, event):
        if not self.menu_open:
            return
        for (x1, y1, x2, y2, key) in self.menu_buttons:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.canvas.unbind("<Button-1>")
                self.menu_open = False
                self._load_level(key)
                return

    # ── MAIN LOOP ────────────────────────────────────────────────────────────

    def tick(self):
        now = time.time()
        dt = min(now - self.last_time, 0.1)
        self.last_time = now

        if self.menu_open:
            self.draw_menu()
        elif self.game_over:
            self.render_game_over_screen()
        else:
            self.update_player(dt)
            self.update_entity(dt)
            self.update_projectiles(dt)
            self.update_flicker(dt)
            self.update_messages(dt)
            self.update_shake(dt)

            self.sanity -= dt * 1.5
            if self.sanity <= 0:
                self.sanity = 0
                self.game_over = True

            self.render_3d()
            self.draw_ui()
            self.draw_messages()
            self.draw_vignette()

        self.root.after(16, self.tick)


# ── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = Game(root)
    root.mainloop()
