import time
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Square")

BACKGROUND = (
    random.randint(175, 255),
    random.randint(175, 255),
    random.randint(175, 255),
)
FOREGROUND = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))


class Game:
    def __init__(self):
        # Player properties
        self.player_size = 30
        self.player_pos = [WIDTH // 4, HEIGHT // 2]

        # Obstacle properties
        self.obstacle_width = 70
        self.obstacle_height = random.randint(150, 300)
        self.obstacle_color = FOREGROUND
        self.obstacle_gap = 150

        self.obstacle_list = [
            [WIDTH, 0, self.obstacle_width, self.obstacle_height],
            [
                WIDTH,
                self.obstacle_height + self.obstacle_gap,
                self.obstacle_width,
                HEIGHT - self.obstacle_height - self.obstacle_gap,
            ],
        ]

        # Game variables
        self.gravity = 0.5
        self.jump_height = -5
        self.player_velocity = 0
        self.game_over = False
        self.clock = pygame.time.Clock()

    def draw_window(self):
        win.fill(BACKGROUND)
        pygame.draw.rect(
            win,
            FOREGROUND,
            (
                self.player_pos[0],
                self.player_pos[1],
                self.player_size,
                self.player_size,
            ),
        )
        for obstacle in self.obstacle_list:
            pygame.draw.rect(win, self.obstacle_color, obstacle)
        pygame.display.update()

    def update_obstacles(self):
        needs_to_be_removed = []
        for obstacle in self.obstacle_list:
            obstacle[0] -= 5  # Move obstacle to the left
            if obstacle[0] < -self.obstacle_width:
                needs_to_be_removed.append(obstacle)

        for obstacle in needs_to_be_removed:
            self.obstacle_list.remove(obstacle)

        if len(self.obstacle_list) < 2:
            self.obstacle_gap = random.randint(150, 300)
            new_obstacle_height = random.randint(20, 300)
            self.obstacle_list.append(
                [WIDTH, 0, self.obstacle_width, new_obstacle_height]
            )
            self.obstacle_list.append(
                [
                    WIDTH,
                    new_obstacle_height + self.obstacle_gap,
                    self.obstacle_width,
                    HEIGHT - new_obstacle_height - self.obstacle_gap,
                ]
            )

    def check_collision(self):
        for obstacle in self.obstacle_list:
            if (
                self.player_pos[0] < obstacle[0] + self.obstacle_width
                and self.player_pos[0] + self.player_size > obstacle[0]
            ):
                if (
                    self.player_pos[1] < obstacle[1] + obstacle[3]
                    and self.player_pos[1] + self.player_size > obstacle[1]
                ):
                    return True
        if self.player_pos[1] > HEIGHT - self.player_size or self.player_pos[1] < 0:
            return True
        return False

    def show_game_over_screen(self):
        win.fill(BACKGROUND)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Game Over", True, FOREGROUND)
        win.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2),
        )
        pygame.display.update()
        pygame.time.wait(2000)

    def wait_for_new_game(self):
        win.fill(BACKGROUND)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Press SPACE to start", True, FOREGROUND)
        win.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2),
        )
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.clock.tick(30)

    def game_loop(self):
        self.wait_for_new_game()

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player_velocity = self.jump_height

            self.player_velocity += self.gravity
            self.player_pos[1] += self.player_velocity

            if self.player_pos[1] > HEIGHT - self.player_size or self.player_pos[1] < 0:
                self.game_over = True

            self.update_obstacles()
            self.game_over = self.check_collision()

            self.draw_window()
            self.clock.tick(30)


if __name__ == "__main__":
    random.seed(time.time())

    while True:
        game = Game()
        game.game_loop()
        game.show_game_over_screen()
