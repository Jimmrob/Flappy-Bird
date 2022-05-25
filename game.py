import pygame, sys, random


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.gravity = 0.25
        self.vel = 0
        self.ball = pygame.Rect(0, 0, 0, 0)


    def move(self):
        self.vel += self.gravity
        self.y = self.y + self.vel


    def jump(self):
        self.vel = 0
        self.vel -= 8
        self.y = self.y + self.vel


    def draw(self, screen):
        self.ball = pygame.Rect(self.x, self.y, 30, 30)
        pygame.draw.ellipse(screen, colours["ball"], self.ball)


class Obstacles:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.gap = 100
        self.top = 0
        self.bot = 0
        self.vel = 2
        self.passed = False
        self.top_rect = pygame.Rect(0, 0, 0, 0)
        self.bot_rect = pygame.Rect(0, 0, 0, 0)
        self.spawn()
    

    def spawn(self):
        self.y = random.randrange(150, 650)
        self.top = self.y - self.gap
        self.bot = self.y + self.gap


    def move(self):
            self.x -= self.vel


    def draw(self, screen):
        self.top_rect = pygame.Rect(self.x, 0, 50, self.top)
        self.bot_rect = pygame.Rect(self.x, self.bot, 50, screen_y - self.bot)
        pygame.draw.rect(screen, colours["obstacles"], self.top_rect)
        pygame.draw.rect(screen, colours["obstacles"], self.bot_rect)


def draw_game(screen, ball, obstacles=[]):
    screen.fill(colours["background"])

    for obstacle in obstacles:
        obstacle.draw(screen)

    ball.draw(screen)


def draw_text(text, font, colour, surface, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


#Initialise game
pygame.init()
clock = pygame.time.Clock()

colours = {"background" :  (30, 40, 50), 
           "ball"       :  pygame.Color("yellow"),
           "obstacles"  :  pygame.Color("limegreen"),
           "text"       :  pygame.Color("lightslategrey")}

font = {"big"       : pygame.font.SysFont("helvetica", 50, True),
        "medium"    : pygame.font.SysFont("helvetica", 35, True),
        "small"     : pygame.font.SysFont("helvetica", 20, True)}

screen_x = 500
screen_y = 800
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("ball game")


def start(screen, ball):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    running = False

        draw_game(screen, ball)
        draw_text("Press SPACE to start", font["small"], colours["text"], screen, 215, 200)

        pygame.display.update()
        clock.tick(120)


def pause_menu(screen, ball, obstacles):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    running = False

        draw_game(screen, ball, obstacles)
        draw_text("II", font["big"], colours["text"], screen, screen_x/2, screen_y/2)
        draw_text("Press SPACE to continue", font["small"], colours["text"], screen, screen_x/2, screen_y/2 - 50)
        draw_text("Press ESCAPE to quit", font["small"], colours["text"], screen, screen_x/2, screen_y/2 + 50)

        pygame.display.update()
        clock.tick(120)


def game_over_menu(screen, ball, obstacles, score):
    running = True
    allow_keys = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and allow_keys:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    running = False
                    game_loop()

        ball.move()
        draw_game(screen, ball, obstacles)
        if ball.y > screen_y:
            allow_keys = True
            draw_text("GAME OVER", font["big"], colours["text"], screen, screen_x/2, screen_y/2 - 100)
            draw_text(f"SCORE : {score}", font["medium"], colours["text"], screen, screen_x/2, screen_y/2 - 50)
            draw_text("Press SPACE to play again", font["small"], colours["text"], screen, screen_x/2, screen_y/2)
            draw_text("Press ESCAPE to quit", font["small"], colours["text"], screen, screen_x/2, screen_y/2 + 25)

        pygame.display.update()
        clock.tick(120)


def game_loop():
    ball = Ball(200, 250)
    obs_list = [Obstacles(600)]
    score = 0
    game_over = False

    start(screen, ball)

    #Game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu(screen, ball, obs_list)
                if event.key == pygame.K_SPACE:
                    ball.jump()

        #Game logic
        add_obs = False
        remove = []
        for obstacle in obs_list:
            if obstacle.x + 50 < 0:
                remove.append(obstacle)
            if not obstacle.passed and obstacle.x < ball.x:
                obstacle.passed = True
                add_obs = True
            if obstacle.top_rect.colliderect(ball.ball) or obstacle.bot_rect.colliderect(ball.ball):
                game_over = True
                
            obstacle.move()

        if ball.ball.top < 0 or ball.ball.bottom > screen_y:
            game_over = True

        if add_obs:
            score += 1
            obs_list.append(Obstacles(600))

        for obstacle in remove:
            obs_list.remove(obstacle)

        ball.move()

        #Visuals
        draw_game(screen, ball, obs_list)
        draw_text(f"{score}", font["big"], colours["text"], screen, screen_x/2, 30)

        pygame.display.update()
        clock.tick(120)

    game_over_menu(screen, ball, obs_list, score)


if __name__ == "__main__":
    game_loop()