import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root, level):
        self.root = root
        self.root.title(f"Snake Game - Level {level}")
        self.width = 600
        self.height = 400
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        self.snake = [(30, 30), (20, 30), (10, 30)]
        self.direction = 'Right'
        self.running = False  
        self.score = 0
        self.game_speed = 120
        self.level = level
        self.walls = self.create_walls()
        self.food = self.create_food()

        self.canvas.focus_set()

        self.root.bind("<KeyPress>", self.change_direction)
        self.draw()
        self.update()

    def create_food(self):
        while True:
            x = random.randint(0, (self.width // 10) - 1) * 10
            y = random.randint(0, (self.height // 10) - 1) * 10
            if (x, y) not in self.snake and (x, y) not in self.walls:
                return (x, y)

    def create_walls(self):
        wall_positions = []

        for i in range(0, self.width, 10):
            wall_positions.append((i, 0))
            wall_positions.append((i, self.height - 10))
        for i in range(0, self.height, 10):
            wall_positions.append((0, i))
            wall_positions.append((self.width - 10, i))

        if self.level == 2:
            # Add walls for Level 2
            for i in range(100, 300, 10):
                wall_positions.append((300, i))
        
        elif self.level == 3:
            # Add more walls for Level 3
            for i in range(100, 300, 10):
                wall_positions.append((200, i))
            for i in range(100, 300, 10):
                wall_positions.append((400, i))
        
        elif self.level == 4:
            # Add even more walls for Level 4
            for i in range(100, 300, 10):
                wall_positions.append((i, 150))
            for i in range(150, 250, 10):
                wall_positions.append((400, i))
            for i in range(200, 400, 10):
                wall_positions.append((i, 250))
            for i in range(100, 200, 10):
                wall_positions.append((300, i))
        
        return wall_positions

    def change_direction(self, event):
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            if not self.running:
                self.running = True 
            if (event.keysym == 'Up' and self.direction != 'Down') or \
               (event.keysym == 'Down' and self.direction != 'Up') or \
               (event.keysym == 'Left' and self.direction != 'Right') or \
               (event.keysym == 'Right' and self.direction != 'Left'):
                self.direction = event.keysym

    def update(self):
        if self.running:
            self.move_snake()
            if self.check_collisions():
                self.running = False
                self.game_over()
            else:
                self.check_food_collision()
                self.draw()
        self.root.after(self.game_speed, self.update)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'Up':
            new_head = (head_x, head_y - 10)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 10)
        elif self.direction == 'Left':
            new_head = (head_x - 10, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 10, head_y)

        self.snake = [new_head] + self.snake[:-1]

    def check_collisions(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            return True
        if (head_x, head_y) in self.walls:
            return True
        if len(self.snake) != len(set(self.snake)):
            return True
        return False

    def check_food_collision(self):
        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.create_food()
            self.score += 1
            self.game_speed = max(50, self.game_speed - 2)

    def draw(self):
        self.canvas.delete(tk.ALL)
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0]+10, segment[1]+10, fill="green")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0]+10, self.food[1]+10, fill="red")
        for wall in self.walls:
            self.canvas.create_rectangle(wall[0], wall[1], wall[0]+10, wall[1]+10, fill="blue")
        self.canvas.create_text(50, 10, text=f"Score: {self.score}", fill="white", font=('Arial', 14))

    def game_over(self):
        self.canvas.create_text(self.width/2, self.height/2, text="GAME OVER", fill="red", font=('Arial', 24))
        self.canvas.create_text(self.width/2, self.height/2 + 30, text=f"Final Score: {self.score}", fill="white", font=('Arial', 16))
        self.create_restart_button()
        self.create_change_level_button()

    def create_restart_button(self):
        self.restart_button = tk.Button(self.root, text='Restart', command=self.restart_game, width=10, bg='green', fg='white', font=('Arial', 14))
        self.restart_button_window = self.canvas.create_window(self.width/2, self.height/2 + 60, window=self.restart_button)

    def create_change_level_button(self):
        self.change_level_button = tk.Button(self.root, text='Change Level', command=self.change_level, width=10, bg='blue', fg='white', font=('Arial', 14))
        self.change_level_button_window = self.canvas.create_window(self.width/2, self.height/2 + 100, window=self.change_level_button)

    def change_level(self):
        self.root.destroy() 
        show_level_selection() 

    def restart_game(self):
        self.snake = [(10, 30), (90, 100), (80, 100)]
        self.food = self.create_food()
        self.direction = 'Right'
        self.running = False
        self.score = 0
        self.game_speed = 120
        self.canvas.delete(tk.ALL)
        self.canvas.delete(self.restart_button_window)
        self.canvas.delete(self.change_level_button_window)
        self.draw()
        self.update()

def select_level(level):
    root = tk.Tk()
    SnakeGame(root, level)
    root.mainloop()

def show_level_selection():
    root = tk.Tk()
    root.title("Select Level")

    label = tk.Label(root, text="Select a Level", font=('Arial', 18))
    label.pack(pady=20)

    for level in range(1, 5):
        button = tk.Button(root, text=f"Level {level}", command=lambda l=level: start_game(root, l), width=20, height=2, font=('Arial', 14))
        button.pack(pady=10)

    root.mainloop()

def start_game(root, level):
    root.destroy()
    select_level(level)

if __name__ == "__main__":
    show_level_selection()
