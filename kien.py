import pygame
import random
import time
pygame.init()

WIDTH, HEIGHT = 800, 650

win = pygame.display.set_mode((WIDTH, HEIGHT))
font_count_move = pygame.font.SysFont("comicsans",30)
IMGS = [pygame.image.load(f"C:\\Users\\PC\\Documents\\sliding_puzzle_{i}.png") for i in range(1, 3)]


class Buttons:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.x = x 
        self.y = y 
        self.width = width
        self.height = height
        self.color = color  

    def clicked(self, x, y):
        if (self.x<= x <= self.x + self.width and
                    self.y<= y <= self.y + self.height):
            
            return True

        return False


    def drawButton(self, win, font):
        pygame.draw.rect(win, self.color, (self.x, self.y,self.width, self.height))
        label = font.render(self.text, True, (255, 255, 255))

        win.blit(label, (self.x + self.width/2 - label.get_width()/2, self.y))  

class Block:
    blank_space = (0, 0)
    def __init__(self, x, y, text):
        self.x = x 
        self.y = y 
        self.text = text 
        self.img = None

    def drawBlock(self, win):
        pygame.draw.rect(win, "white", (
            (self.x)*BLOCK_SIZE + PADDING_X, (self.y)*BLOCK_SIZE + PADDING_Y, BLOCK_SIZE, BLOCK_SIZE))
        
        win.blit(self.img, ((self.x)*BLOCK_SIZE + PADDING_X,  (self.y)*BLOCK_SIZE + PADDING_Y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = BLOCK_TEXT_FONT.render(self.text, True, "black")
        pygame.draw.rect(win, "black", (
            (self.x)*BLOCK_SIZE + PADDING_X, (self.y)*BLOCK_SIZE + PADDING_Y, BLOCK_SIZE, BLOCK_SIZE), 5)

        x = (self.x)*BLOCK_SIZE + PADDING_X + 5
        y = (self.y)*BLOCK_SIZE + PADDING_Y - 5

        win.blit(text, (x, y))


def checkWin(all_pos):
    if all_pos[(DIFFICULTY - 1, DIFFICULTY - 1)] != None:
        return False

    for row in range(DIFFICULTY):
        for col in range(DIFFICULTY):
            if row == DIFFICULTY - 1 and col == DIFFICULTY - 1:
                return True

            if not all_pos[(row, col)]:
                return False

            if int(all_pos[(row, col)].text) !=  col * DIFFICULTY + row + 1:
                return False

    return True

                    

# init a pos for a block
def initBlockPos(all_pos):
    puzzle = list(range(DIFFICULTY**2))
    random.shuffle(puzzle)

    while not is_solvable(puzzle):
        random.shuffle(puzzle)

    puzzle =  [puzzle[i:i+DIFFICULTY] for i in range(0, len(puzzle), DIFFICULTY)]
    for y in range(DIFFICULTY):
        for x in range(DIFFICULTY):
            value = puzzle[y][x]
            if value == 0:
                all_pos[x, y] = None
                Block.blank_space = (x, y)
                continue


            all_pos[x, y] = Block(x, y, str(value))
            all_pos[x, y].img = IMG.subsurface(((value-1)%DIFFICULTY*BLOCK_SIZE, 
                (value-1)//DIFFICULTY*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def is_solvable(puzzle):
    inversion = sum(1 for i in range(len(puzzle))
                    for j in range(i + 1, len(puzzle))
                    if puzzle[i] > puzzle[j] and puzzle[i] != 0 and puzzle[j] != 0)

    empty_row = puzzle.index(0) // DIFFICULTY + 1

    if DIFFICULTY % 2 == 1:  # Odd-sized puzzle
        return inversion % 2 == 0
    else:  # Even-sized puzzle
        return (inversion + empty_row) % 2 == 0


def is_valid_move(all_pos, x, y):
    x, y = convertMousePos(x, y)

    # check if mouse clicked on the same row or col with the blank space
    if (x == Block.blank_space[0] and y != Block.blank_space[1] or 
        x != Block.blank_space[0] and y == Block.blank_space[1]) and (
        0 <= x <= DIFFICULTY - 1 and 0 <= y <= DIFFICULTY - 1):
        return True
        
    return False


        
def convertMousePos(x, y):
    x = (x - PADDING_X) / BLOCK_SIZE 
    y = (y - PADDING_Y) / BLOCK_SIZE 

    return (int(x), int(y))

# click the block
def clickBlock(x, y):
    pos_x, pos_y = convertMousePos(x, y)
    move_pos = []
    blank_x = Block.blank_space[0]
    blank_y = Block.blank_space[1]
    if pos_x < blank_x:

        move = "right"
        move_pos = [i for i in range(blank_x - 1,pos_x - 1 , -1)]           
    

    elif pos_x > blank_x:
        move = "left"
        move_pos = [i for i in range(blank_x + 1, pos_x + 1)]


    elif pos_y > blank_y:
        move = "up"
        move_pos = [i for i in range(blank_y + 1, pos_y + 1)]

    elif pos_y < blank_y:
        move = "down"
        move_pos = [i for i in range(blank_y - 1,pos_y -1, -1)]


    return (move_pos, move, pos_x, pos_y)

# draw the window
def redrawWindow(win, all_pos, moves):
    win.fill("black")
    for row in range(DIFFICULTY):
        for col in range(DIFFICULTY):
            if all_pos[(row, col)]:
                all_pos[(row, col)].drawBlock(win)

    move_text = font_count_move.render(str(moves), True, "black")
    pygame.draw.circle(win, "green", (0, 0), move_text.get_width()+ 30)
    win.blit(move_text, (0, 0))

def movePosAfterClick(move, move_pos, all_pos, pos_x, pos_y):
    if move == "right":
        for i in move_pos:
            all_pos[(i, pos_y)].x += 1
            all_pos[(i + 1, pos_y)] = all_pos[(i, pos_y)]
            
    elif move == "left":
        for i in move_pos:
            all_pos[(i, pos_y)].x -= 1
            all_pos[(i - 1, pos_y)] = all_pos[(i, pos_y)]


    elif move == "up":
        for i in move_pos:
            all_pos[(pos_x, i)].y -= 1
            all_pos[(pos_x, i - 1)] = all_pos[(pos_x, i)]


    elif move == "down":
        for i in move_pos:
            all_pos[(pos_x, i)].y += 1
            all_pos[(pos_x, i + 1)] = all_pos[(pos_x, i)]

# main function
def main(win):
    blocks = []
    all_pos = {}

    initBlockPos(all_pos)
    run = True
    moves = 0 # the number of moves to win

    while run:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if is_valid_move(all_pos, *pos):
                    move_pos, move, pos_x, pos_y = clickBlock(*pos)
                    click = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    win.fill("black")
                    menu_screen(win, False, 0)

        if click == True:
            movePosAfterClick(move, move_pos, all_pos, pos_x, pos_y)
            all_pos[(pos_x, pos_y)] = None
            Block.blank_space = (pos_x, pos_y)
            moves += 1 


        if checkWin(all_pos):
            redrawWindow(win, all_pos, moves)
            pygame.draw.rect(win, "green", (0, 0, WIDTH, HEIGHT), 30)

            pygame.display.update()
            time.sleep(1)
            run = False
            win.fill("black")
            menu_screen(win, True, moves)

        redrawWindow(win, all_pos, moves)

        pygame.display.update()

    pygame.quit()


is_won = False
def menu_screen(win, is_won, moves):
    run = True
    global DIFFICULTY, PADDING_X, PADDING_Y ,BLOCK_SIZE, BLOCK_TEXT_FONT, IMG
    IMG = random.choice(IMGS)

    # text, x, y, width, height, color
    x = WIDTH / 2 - ((WIDTH*37.5)//100) / 2
    buttons = [Buttons("Easy", x, 170, (WIDTH*37.5)//100, (HEIGHT*(40/3))//100, "green"),
               Buttons("Medium", x, 320, (WIDTH*37.5)//100, (HEIGHT*(40/3))//100, "yellow"),
               Buttons("Hard", x, 470, (WIDTH*37.5)//100, (HEIGHT*(40/3))//100, "red")
               ]

    font = pygame.font.SysFont("comicsans", 50)
    hello_font = pygame.font.SysFont("Segoe UI Symbol", 60)

    label1 = font.render("Choose a level to play", True, "white")
    hello_label = font.render("Welcome to sliding puzzle", True, "pink")


    if is_won:
        label_won = font.render(f"You won in {moves} moves", True, "white")
        label2 = font.render("Choose a level to play again", True, "white")

        

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in buttons:
                    if button.clicked(x, y):
                        if button.text == "Easy":
                            DIFFICULTY = 2
                            BLOCK_SIZE = (WIDTH  * 21.25) // 100
                            
                        elif button.text == "Medium":
                            DIFFICULTY = 4
                            BLOCK_SIZE = (WIDTH  * 16.25) // 100
                            
 
                        else:
                            DIFFICULTY = 5
                            BLOCK_SIZE = (WIDTH  * 13.25) // 100
                            
                        PADDING_X = WIDTH / 2 - (BLOCK_SIZE * DIFFICULTY) / 2
                        PADDING_Y = HEIGHT / 2 - (BLOCK_SIZE * DIFFICULTY) / 2 
                        BLOCK_TEXT_FONT = pygame.font.SysFont("comicsans", int(BLOCK_SIZE * 0.4))         
                        IMG = pygame.transform.scale(IMG, (BLOCK_SIZE*DIFFICULTY, BLOCK_SIZE*DIFFICULTY))
                        

                        run = False
                        main(win)


        if not is_won:
            win.blit(label1, (WIDTH/2 - label1.get_width()/2, 80))
            win.blit(hello_label, (WIDTH/2 - hello_label.get_width()/2, 0))
            


        else:
            space = 100
            total_height = label1.get_height() + space + label2.get_height()
            win.blit(label_won, (WIDTH/2 - label_won.get_width()/2, 0))

            win.blit(label2, (WIDTH/2 - label2.get_width()/2, 80))

            # draw the welcome text


        for button in buttons:
            button.drawButton(win, font)

        
        pygame.display.update()

menu_screen(win, is_won, 0)