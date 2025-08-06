# dependencies
import requests
import time
import pygame
import sys

# core variables
url = "https://zkvscr.pythonanywhere.com/send"
playernum = "2"

# extracts opponent choice and determines result
def getopchoice(result):
    # simplify opponent number definition
    if playernum == "1":
        opnum = "2"
    elif playernum == "2":
        opnum = "1"

    # sends get request for opponent choice
    x = requests.get("https://zkvscr.pythonanywhere.com/rpschoice" + opnum)

    # decompile html format
    opchoice = str(x.text).split("<pre>")[1].split("</pre>")[0]

    print("you chose " + result + ", they chose " + opchoice)

    # determine result
    if opchoice == "rock" and result == "rock":
        print("it's a tie")
    elif opchoice == "rock" and result == "scissors":
        print("rock beats scissors")
    elif opchoice == "scissors" and result == "rock":
        print("rock beats scissors")
    elif opchoice == "rock" and result == "paper":
        print("paper beats rock")
    elif opchoice == "paper" and result == "rock":
        print("paper beats rock")
    elif opchoice == "scissors" and result == "paper":
        print("scissors beats paper")
    elif opchoice == "paper" and result == "scissors":
        print("scissors beats paper")
    elif opchoice == "scissors" and result == "scissors":
        print("it's a tie")
    elif opchoice == "paper" and result == "paper":
        print("it's a tie")
    else:
        print("unable to determine result.")

# sends choice to web server by post request
def send(choice):
    obj = {"player": playernum, "result": choice}
    x = requests.post(url, json = obj)
    time.sleep(2)
    getopchoice(choice)

# initiate pygame source
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
RADIUS = 75

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ROCK PAPER SCISSORS")
clock = pygame.time.Clock()

# loads image in circle mask
def loadcimg(filename, radius):
    try:
        image = pygame.image.load(filename).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image {filename}: {e}")
        return None

    image = pygame.transform.smoothscale(image, (radius * 2, radius * 2))

    mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255, 255), (radius, radius), radius)

    circle_image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    circle_image.blit(image, (0, 0))
    circle_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return circle_image

# gets image source from root directory that corresponds to each choice
image_data = [
    ("1.png", "rock"),
    ("2.png", "paper"),
    ("3.png", "scissors")
]

positions = [
    (WIDTH // 4, HEIGHT // 2),
    (WIDTH // 2, HEIGHT // 2),
    (3 * WIDTH // 4, HEIGHT // 2)
]

clickable_images = []

for (filename, choice), pos in zip(image_data, positions):
    img = loadcimg(filename, RADIUS)
    if img:
        rect = img.get_rect(center=pos)
        clickable_images.append((img, rect, choice))


running = True
while running:
    clock.tick(FPS)
    screen.fill((0,0,0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for img, rect, choice in clickable_images:
                dx = mouse_pos[0] - rect.centerx
                dy = mouse_pos[1] - rect.centery
                if dx * dx + dy * dy <= RADIUS * RADIUS:
                    send(choice)

    for img, rect, _ in clickable_images:
        
        # display image to position
        screen.blit(img, rect)

    pygame.display.flip()

pygame.quit()
sys.exit()

