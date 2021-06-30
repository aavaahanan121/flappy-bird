import pygame
import classes

# init
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init(      )

# display
win_width = 288 * 2
win_height = 512

window = pygame.display.set_mode([win_width, win_height])

pygame.display.set_caption("flappy bird")
pygame.display.set_icon(pygame.image.load("big project/assets/pictures/player/yellowbird-midflap.png"))

# variables for easy understanding
fps = 60
background_image = pygame.image.load(
    r"big project\assets\pictures\background\background-day.png")


# other variables
running = True

out = False

score = 0

pipes = pygame.sprite.Group()

game_over = pygame.USEREVENT + 1

jumping = False

font = pygame.font.Font("big project/assets/SourceCodePro-Black.ttf", 25)

bird = classes.bird(pipes, game_over, win_height)
bird_group = pygame.sprite.Group()
bird_group.add(bird)
score = 0

pointsound = pygame.mixer.Sound("big project/assets/sound/point.ogg")

# code

def end_screen(window):
    pygame.font.init()
    text = font.render("game over", True, (0, 0, 0))
    pygame.draw.rect(window, (255, 0, 255), (int(win_width/2) - text.get_rect().width/2 - 7, win_height/2 - 7, text.get_rect().w + 15, text.get_rect().h + 15), border_radius = 5)
    window.blit(text,(win_width/2 - text.get_rect().width/2, win_height/2))
    pygame.display.flip()

def update():
    """things to do every frame""" 
    global score
    window.blit(background_image, (0, 0))
    window.blit(background_image, (288, 0))
    bird_group.draw(window)
    if len(pipes.sprites()) == 0:
        try:
            del obstacle1
        except UnboundLocalError:
            pass
        obstacle1 = classes.obstacle(window)
        pipes.add(obstacle1.pipe1)
        pipes.add(obstacle1.pipe2)
        score += 1
        if score % 2 == 1:
            classes.hole -= 15
        pointsound.play()
    pipes.draw(window)
    bird_group.update()
    pipes.update()
    score_text = font.render("Score = " + str(score), True, (0, 0, 0))
    pygame.draw.rect(window, (255, 0, 0), pygame.rect.Rect(20 - 8, 20 - 8, score_text.get_rect().width + 16, score_text.get_rect().height + 16), border_radius=7)
    window.blit(score_text, (20, 20))
    health_text = font.render("Health = " + str(bird.h), True, (0, 0, 0)) 
    pygame.draw.rect(window, (0, 0, 255), pygame.rect.Rect(win_width - health_text.get_width() - 27, 20 - 8, health_text.get_rect().width + 16, health_text.get_rect().height + 16), border_radius=7)
    window.blit(health_text, (win_width -health_text.get_width()- 20, 20))
    pygame.display.flip()


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == game_over:
            out = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if not jumping:
            bird.jump()
            jumping = True


    else:
        if jumping:
            jumping = False
    if not out:
        update()
    else:
            end_screen(window)
    clock.tick(fps)
