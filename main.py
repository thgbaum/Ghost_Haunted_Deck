# Complete your game here
import pygame
import math


class Player():
    def __init__(self, x, y):
        self.game_scale_x = 50*25
        self.game_scale_y = 50*15
        self.x = x
        self.y = y
        self.to_left = False
        self.to_right = False
        self.to_up = False
        self.to_down = False
        self.points = 0
        self.robot = pygame.image.load("templates/robot.png")
        
    
    def movement(self): 
        if self.to_right and self.x < (self.game_scale_x) - self.robot.get_width():
            self.x += 2
        if self.to_left and self.x > 0:
            self.x -= 2
        if self.to_up and self.y > 0:
            self.y-=2
        if self.to_down and self.y < (self.game_scale_y) - self.robot.get_height():
            self.y+=2
    

class Mob():
    def __init__(self, x, y, x_destiny, y_destiny, x_gain = 0, y_gain = 0):
        self.game_scale_x = 50*25
        self.game_scale_y = 50*15
        self.x = x
        self.y = y
        self.orig_x = x
        self.orig_y = y
        self.x_destiny = x + x_destiny
        self.y_destiny= y + y_destiny
        self.x_gain = x_gain
        self.y_gain = y_gain
        self.to_left = False
        self.to_right = False
        self.to_up = False
        self.to_down = False
        self.points = 0
        self.monster = pygame.image.load("templates/monster.png")
        self.angle = 0
        
        
    
    def movement(self):
        
        if self.x_gain == 1:
            if self.x == self.x_destiny:
                self.x_gain = -1

        if self.x_gain == -1:
            if self.x == self.orig_x:
                self.x_gain = 1


        if self.y_gain == 1:
            if self.y == self.y_destiny:
                self.y_gain = -1

        if self.y_gain == -1:
            if self.y == self.orig_y:
                self.y_gain = 1

        

        self.x += self.x_gain
        self.y += self.y_gain
        
        
    
    def special_mov(self):
        self.pos = []
        
        for i in range(4):
            self.x = 700+math.cos(self.angle+i*(2*math.pi/4))*190-self.monster.get_width()/2 
            self.y = 270+math.sin(self.angle+i*(2*math.pi/4))*190-self.monster.get_height()/2
            self.pos.append((self.x, self.y))
        
        self.angle += 0.01
        

    def mob_collider(self, obj):
        r1 = pygame.Rect(self.x+10, self.y+10, self.monster.get_width()-20, self.monster.get_height()-10)
        r2 = pygame.Rect(obj.x, obj.y, obj.robot.get_width(), obj.robot.get_height())

        if r1.colliderect(r2):
            return 1
        
        return 0
    
    def special_mob_collider(self, obj):
        for pos in self.pos:
            r1 = pygame.Rect(pos[0]+10, pos[1]-10, self.monster.get_width()-20, self.monster.get_height()-10)
            r2 = pygame.Rect(obj.x, obj.y, obj.robot.get_width(), obj.robot.get_height())
        
        if r1.colliderect(r2):
            return 1
        
        return 0

class GridEvent:
    def __init__(self):
        self.coins = 0

    def collider(self, player, grid):
        
        x_collider = player.x//50
        y_collider = player.y//50

        if player.to_right:
            if grid[y_collider][x_collider+1] == 9:
                grid[y_collider][x_collider+1] = 0
                self.coins +=1
            
            if grid[y_collider+1][x_collider+1] == 9:
                grid[y_collider+1][x_collider+1] = 0
                self.coins +=1
            
        
        if player.to_left:
            if grid[y_collider][x_collider] == 9:
                grid[y_collider][x_collider] = 0
                self.coins +=1
                
            if grid[y_collider+1][x_collider] == 9:
                grid[y_collider+1][x_collider] = 0
                self.coins +=1

        
        if player.to_up and (grid[y_collider][x_collider] == 9):
            grid[y_collider][x_collider] = 0
            self.coins +=1   
        
        if player.to_down and (grid[y_collider+2][x_collider] == 9): 
            grid[y_collider+2][x_collider] = 0
            self.coins +=1    

        grid = self.liberate_wall(grid)

        return grid

    def liberate_wall(self, grid):
        
        if self.coins >= 10:
            grid[8][21] = 0
            grid[8][22] = 0
        
        if self.coins >= 20:
            grid[11][5] = 0
            grid[12][5] = 0
            grid[13][5] = 0

        if self.coins >= 35:
            grid[4][21] = 0
            grid[4][22] = 0
        
        return grid
    
       
        
    
class Game:
    def __init__(self):
        pygame.init()

        self.load_images()
        self.new_game()

        
        self.game = 0 
        self.over = 0
        
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.scale = self.images[0].get_width() 
        
        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode((window_width, window_height))

        pygame.display.set_caption("Ghost Haunted Deck")

        self.grid_event = GridEvent()
        self.player = Player(6*50, 12*50)
        #self.player = Player(2*50, 6*50)
        self.mob1 = Mob(17*50, 12*50, 300, 0, x_gain = 1)
        self.mob2 = Mob(13*50+45, 2*50, 0, 300, y_gain = 1)
        self.mob3 = Mob(11*50, 2*50, 0, 525, y_gain = 1)
        self.mob4 = Mob(2*50, 2*50, 0, 525, y_gain = 1)
        self.mob5 = Mob(1*50, 1*50, 350, 100, x_gain = 1, y_gain = 1)
        self.mob6 = Mob(1*50, 4*50, 300, 200, x_gain = -1, y_gain = -1)

        self.mobs = [self.mob1, self.mob2, self.mob4, self.mob5, self.mob6]
        #self.mobs = []
        self.clock = pygame.time.Clock()
        self.main_loop()

    def load_images(self):
        self.images = []
        for name in ["box", "wall", "done", "door", "floor", "monster", "rock", "target_robot", "target", "coin"]:
            self.images.append(pygame.image.load(f"templates/{name}.png"))

    def new_game(self):
        
        self.grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 8, 8, 8, 1], 
                     [1, 0, 9, 9, 0, 0, 9, 9, 0, 1, 0, 9, 0, 0, 0, 0, 0, 9, 0, 1, 8, 8, 8, 8, 1], 
                     [1, 0, 9, 9, 0, 0, 9, 9, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 8, 8, 8, 1], 
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 1, 1, 6, 6, 1, 1], 
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                     [1, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                     [1, 0, 0, 0, 9, 9, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 9, 0, 0, 0, 0, 0, 9, 0, 1, 1, 6, 6, 1, 1], 
                     [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
                     [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 9, 9, 0, 1], 
                     [1, 0, 9, 9, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 1], 
                     [1, 0, 9, 9, 0, 6, 0, 0, 0, 0, 0, 9, 0, 9, 0, 9, 0, 9, 0, 0, 0, 9, 9, 0, 1], 
                     [1, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            if self.over == 1:
                self.game_over()
            if self.over == 2:
                self.win()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.player.to_right = True
                if event.key == pygame.K_UP:
                    self.player.to_up = True
                if event.key == pygame.K_DOWN:
                    self.player.to_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.player.to_right = False
                if event.key == pygame.K_UP:
                    self.player.to_up = False
                if event.key == pygame.K_DOWN:
                    self.player.to_down = False
        
        self.collider()
        self.player.movement()
        self.grid = self.grid_event.collider(self.player, self.grid)

        for mob in self.mobs:
            mob.movement()
            self.game = mob.mob_collider(self.player)
            if self.game:
                self.over = 1
        
        self.mob3.special_mov()
        self.game = self.mob3.special_mob_collider(self.player)

        if self.game:
                self.over = 1
        
        self.check_win()
        
        self.clock.tick(60)

    def check_win(self):
        if self.grid_event.coins >= 35 and self.player.x > 21 * 50 and self.player.y < 2 * 50:
            self.over = 2

    def collider(self):
        x_collider = self.player.x//50
        y_collider = self.player.y//50

        if self.player.to_right and (
            (self.grid[y_collider][x_collider+1] == 1) or 
            (self.grid[y_collider][x_collider+1] == 6) or
            (self.grid[y_collider+1][x_collider+1] == 1) or
            (self.grid[y_collider+1][x_collider+1] == 6)):

            self.player.to_right = False
            self.player.x -= 2
        
        if self.player.to_left and (
            (self.grid[y_collider][x_collider] == 1) or
            (self.grid[y_collider][x_collider] == 6) or 
            (self.grid[y_collider+1][x_collider] == 1) or
            (self.grid[y_collider+1][x_collider] == 6)):

            self.player.to_left = False
            self.player.x += 2            
        
        if self.player.to_up and (
            (self.grid[y_collider][x_collider] == 1) or
            (self.grid[y_collider][x_collider] == 6)):
            
            self.player.to_up = False
            self.player.y += 2
        
        if self.player.to_down and (
            (self.grid[y_collider+2][x_collider] == 1) or
            (self.grid[y_collider+2][x_collider] == 6)): 

            self.player.to_down = False
            self.player.y -= 2

        

    def draw_window(self):
        self.window.fill((20, 25, 30))

        for y in range(self.height):
            for x in range(self.width):
                square = self.grid[y][x]
                if square == 0:
                    ...
                else:
                    self.window.blit(self.images[square], (x * self.scale, y * self.scale))
        
        self.window.blit(self.player.robot, (self.player.x, self.player.y))

        for mob in self.mobs:
            self.window.blit(mob.monster, (mob.x, mob.y))
        
        for pos in self.mob3.pos:
            self.window.blit(self.mob3.monster, (pos[0], pos[1]))

        game_font = pygame.font.SysFont("Arial", 36)
        points_text = game_font.render(f"Score: {self.grid_event.coins}", True, (252, 226, 5))
        self.window.blit(points_text, (25*50 - points_text.get_width()-15, 5))
        
        game_font = pygame.font.SysFont("Arial", 36)
        instructions = game_font.render(f"Make your way out - Collect coins to take rocks out of the way!", True, (100, 59, 200))
        self.window.blit(instructions, (0, 15*50))
        pygame.display.flip()

    def game_over(self):
        game_font = pygame.font.SysFont("Arial", 100)
        text = game_font.render(f"GAME OVER", True, (255, 0, 0))
        self.window.blit(text, (50*25/2 - text.get_width()/2, 50*15/2- text.get_height()/2))
        pygame.display.flip()
        pygame.time.wait(300)
    
    def win(self):
        game_font = pygame.font.SysFont("Arial", 200)
        text = game_font.render(f"YOU WIN!", True, (0, 255, 0))
        self.window.blit(text, (50*25/2 - text.get_width()/2, 50*15/2- text.get_height()/2))
        pygame.display.flip()
        pygame.time.wait(300)

if __name__ == "__main__":
    Game()