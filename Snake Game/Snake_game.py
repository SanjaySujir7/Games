import pygame,sys
import random

#Some global varibles
SCREEN_HEIGHT,SCREEN_WIDTH = 600,600
RUNNING = True
FPS = 15
CLOCK = pygame.time.Clock()
SCORE = 0

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.Font(None, 36)

class Snake:
    snake_size = 15
    snake_length = 1
    snake_position = [[SCREEN_WIDTH/2,SCREEN_HEIGHT/2]]
    Direction = "LEFT"
    Snake_Speed = 15
    Head = None

    def Draw_Snake(self):
        First = True
        for i in range(self.snake_length):
            if First:
                self.Head = pygame.draw.rect(SCREEN,'green',pygame.Rect(self.snake_position[i][0],self.snake_position[i][1],self.snake_size,15))
                First = False
            else:
                pygame.draw.rect(SCREEN,'green',pygame.Rect(self.snake_position[i][0],self.snake_position[i][1],self.snake_size,15))



    def Change_Position(self,Direction:str):
        if Direction == "TOP" and self.Direction != "BOTTOM" or Direction == "BOTTOM" and self.Direction != "TOP":
            self.Direction = Direction
        
        elif Direction == "RIGHT" and self.Direction != "LEFT" or Direction == "LEFT" and self.Direction != "RIGHT":
            self.Direction = Direction
         



    def Move(self):
        prev_pos = self.snake_position[0][:]

        if self.Direction == "TOP":
            self.snake_position[0][1] -= self.Snake_Speed
        
        elif self.Direction == "LEFT":
            self.snake_position[0][0] -= self.Snake_Speed

        elif self.Direction == "RIGHT":
            self.snake_position[0][0] += self.Snake_Speed

        else:
            self.snake_position[0][1] += self.Snake_Speed

        if self.snake_position[0][1] > SCREEN_HEIGHT:
            self.snake_position[0][1] = 0

        elif self.snake_position[0][1] < 0:
            self.snake_position[0][1] = SCREEN_HEIGHT

        if self.snake_position[0][0] > SCREEN_WIDTH:
            self.snake_position[0][0] = 0

        elif self.snake_position[0][0] < 0:
            self.snake_position[0][0] = SCREEN_WIDTH

        for i in range(1,self.snake_length):
            temp = self.snake_position[i][:]
            self.snake_position[i] = prev_pos
            prev_pos = temp



    def Add(self):

        prev = self.snake_position[-1]
        if self.Direction == "TOP":
            self.snake_position.append([prev[0],prev[1] + 15])

        elif self.Direction == "LEFT":
            self.snake_position.append([prev[0] + 15,prev[1]])

        elif self.Direction == "RIGHT":
            self.snake_position.append([prev[0] - 15,prev[1]])
        
        else:
            self.snake_position.append([prev[0],prev[1] - 15])

        self.snake_length += 1

    def Is_Food_Eaten(self,food):
        if self.Head.colliderect(food):
            return True
        
        return False

    def clear(self):
        self.snake_size = 15
        self.snake_length = 1
        self.snake_position = [[SCREEN_WIDTH/2,SCREEN_HEIGHT/2]]
        self.Direction = "LEFT"
        self.Snake_Speed = 15
        self.Head = None


class Food:
    Food_Exist = False
    pos_x = None
    pos_y = None

    def Draw_Food(self):
        if not self.Food_Exist:
            Position_x = random.randint(0,(SCREEN_WIDTH // 15) -1) * 15
            Position_y = random.randint(0,(SCREEN_HEIGHT// 15) - 1) * 15
            self.pos_x,self.pos_y = Position_x,Position_y
            self.Food_Exist = True

            return pygame.draw.rect(SCREEN,'red',pygame.Rect(Position_x,Position_y,15,15))

        else:
            return pygame.draw.rect(SCREEN,'red',pygame.Rect(self.pos_x,self.pos_y,15,15))
            


SNAKE = Snake()
FOOD = Food()

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    SCREEN.fill('black')

    # Keyboard Logic
    Keys = pygame.key.get_pressed()

    if Keys[pygame.K_w]:
        SNAKE.Change_Position('TOP')

    elif Keys[pygame.K_s]:
        SNAKE.Change_Position('BOTTOM')

    elif Keys[pygame.K_a]:
        SNAKE.Change_Position('LEFT')

    elif Keys[pygame.K_d]:
        SNAKE.Change_Position('RIGHT')

    SNAKE.Draw_Snake()
    SNAKE.Move()

    score_text = font.render(f"Score: {SCORE}", True, 'white')
    SCREEN.blit(score_text, (10,10))

    if SNAKE.Is_Food_Eaten(FOOD.Draw_Food()):
        SCORE += 1
        FOOD.Food_Exist = False
        FOOD.Draw_Food()
        SNAKE.Add()
        if SCORE % 5 == 0:
            FPS += 1

    for i in range(1,len(SNAKE.snake_position)):
        if SNAKE.snake_position[0][0] == SNAKE.snake_position[i][0] and SNAKE.snake_position[0][1] == SNAKE.snake_position[i][1]:
            SCORE = 0
            SNAKE.clear()
    

    pygame.display.flip()
    CLOCK.tick(FPS)

sys.exit()