import tkinter as tk
import random
from PIL import Image, ImageTk  
import webbrowser
import json

# Default controls 
controls = {
    "jump": "Up",
    "slide": "Down",
    "pause": "p",
    "boss_key": "b",
    "restart": "r",
    "cheat": "m",
}


# my Constants
GAME_WIDTH = 900
GAME_HEIGHT = 600 
GROUND_HEIGHT = 100
RUNNER_WIDTH = 50
RUNNER_HEIGHT = 50
OBSTACLE_WIDTH = 50    
OBSTACLE_MIN_HEIGHT = 50
OBSTACLE_MAX_HEIGHT = 150
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30
BACKGROUND_SCROLL_SPEED = 2
RUNNER_START_X = 100
RUNNER_START_Y = GAME_HEIGHT - GROUND_HEIGHT - RUNNER_HEIGHT
RUNNER_COLOR = "#0000FF" #blue
OBSTACLE_COLOR = "#FF0000" #red
POWERUP_COLOR = "#FFFF00" # yellow 
BACKGROUND_COLOR = "#87CEEB" # light blue 
JUMP_HEIGHT = 150
JUMP_DURATION = 500 
SLIDE_DURATION = 300
OBSTACLE_SPEED = 15
FPS = 60
POWERUP_SPAWN_CHANCE = 0.01
OBSTACLE_SPAWN_CHANCE = 0.02
INITIAL_LIVES = 3
INITIAL_SCORE = 0
CHEAT_CODE = "IMMORTAL"
cheat_buffer = ""  # Keeps track of recently typed keys
invincible = False
next_threshold = 1000  # Start with the first threshold at 1000 points 
SAVE_FILE = "game_save.json" 
# Advanced Features
HIGH_SCORE_FILE = "high_scores.txt"
FONT_LARGE = ("Helvetica", 24)
FONT_MEDIUM = ("Helvetica", 18)
FONT_SMALL = ("Helvetica", 14)

class Runner: # how I want to make my runneer 
    def __init__(self, canvas):
        """Initializes the runner's position and state."""
        self.canvas = canvas
        self.runner = self.canvas.create_rectangle(
            RUNNER_START_X, RUNNER_START_Y,
            RUNNER_START_X + RUNNER_WIDTH, RUNNER_START_Y + RUNNER_HEIGHT,
            fill=RUNNER_COLOR, outline="black", width=2
        )
        self.jump_state = False
        self.slide_state = False
        self.original_coords = self.canvas.coords(self.runner)

    def jump(self): # ability to jump 
        """Handles the jump action."""
        if not self.jump_state:
            self.jump_state = True
            self.canvas.move(self.runner, 0, -JUMP_HEIGHT)
            self.canvas.after(JUMP_DURATION, self.land)

    def land(self): # ability to land 
        """Returns the runner to the ground after a jump."""
        current_coords = self.canvas.coords(self.runner)
        self.canvas.coords(
            self.runner,
            current_coords[0],
            self.original_coords[1],
            current_coords[2],
            self.original_coords[3]
        )
        self.jump_state = False

    def slide(self): # ability to slide 
        """Handles the slide action."""
        if not self.slide_state:
            self.slide_state = True
            current_coords = self.canvas.coords(self.runner)
            self.canvas.coords(
                self.runner,
                current_coords[0],
                GAME_HEIGHT - GROUND_HEIGHT - RUNNER_HEIGHT // 2,
                current_coords[2],
                GAME_HEIGHT - GROUND_HEIGHT
            )
            self.canvas.after(SLIDE_DURATION, self.stand)

    def stand(self):
        """Returns the runner to the standing position."""
        current_coords = self.canvas.coords(self.runner)
        self.canvas.coords(
            self.runner,
            current_coords[0],
            RUNNER_START_Y,
            current_coords[2],
            RUNNER_START_Y + RUNNER_HEIGHT
        )
        self.slide_state = False

    def reset_position(self): # be able to reset my position 
        """Resets the runner's position to the start."""
        self.canvas.coords(
            self.runner,
            RUNNER_START_X, RUNNER_START_Y,
            RUNNER_START_X + RUNNER_WIDTH, RUNNER_START_Y + RUNNER_HEIGHT
        )
        self.jump_state = False
        self.slide_state = False  

# Menu button to navigate to controls customization
# = tk.Button(window, text="Menu", font=FONT_MEDIUM, command=lambda: open_menu())
#menu_button.pack(side="right", padx=10)

class Obstacle: # classing my obstacles
    def __init__(self, canvas):
        """Initializes the obstacle system."""
        self.canvas = canvas
        self.obstacles = []

    def create_obstacle(self): # create my obstacle which is a red square 
        """Creates a new obstacle with consistent spacing."""
        if not self.obstacles or self.canvas.coords(self.obstacles[-1])[0] < GAME_WIDTH - 200:
            obstacle = self.canvas.create_rectangle(
                GAME_WIDTH, GAME_HEIGHT - GROUND_HEIGHT - OBSTACLE_MIN_HEIGHT,
                GAME_WIDTH + OBSTACLE_WIDTH, GAME_HEIGHT - GROUND_HEIGHT,
                fill=OBSTACLE_COLOR, outline="black", width=2
            )
            self.obstacles.append(obstacle)
            print("Obstacle created at x=", self.canvas.coords(obstacle)[0])  # Debugging log

    def move(self):
        """Moves all obstacles and removes off-screen ones."""
        to_remove = []
        for obstacle in self.obstacles:
            self.canvas.move(obstacle, -OBSTACLE_SPEED, 0)
            if self.canvas.coords(obstacle)[2] < 0:  # Off-screen check
                to_remove.append(obstacle)
        for obs in to_remove:
            self.canvas.delete(obs)
            self.obstacles.remove(obs)








class PowerUp: # I try to make the hashtag for basic understaning
    def __init__(self, canvas):
        """Initializes the power-up system."""
        self.canvas = canvas
        self.powerups = []

    def create_powerup(self):
        """Creates a new power-up at a random height."""
        x = GAME_WIDTH
        y = random.randint(GAME_HEIGHT - GROUND_HEIGHT - POWERUP_HEIGHT - 200, GAME_HEIGHT - GROUND_HEIGHT - POWERUP_HEIGHT)
        powerup = self.canvas.create_oval(
            x, y, x + POWERUP_WIDTH, y + POWERUP_HEIGHT,
            fill=POWERUP_COLOR, outline="black", width=2
        )
        self.powerups.append(powerup)

    def move(self):
        """Moves all power-ups and removes off-screen ones."""
        to_remove = []
        for powerup in self.powerups:
            self.canvas.move(powerup, -OBSTACLE_SPEED, 0)
            if self.canvas.coords(powerup)[2] < 0:
                to_remove.append(powerup)
        for p in to_remove:
            self.canvas.delete(p)
            self.powerups.remove(p)

def save_game():
    """Saves the game progress to a file."""
    game_data = {
        "score": score,
        "lives": lives,
        "player_coords": canvas.coords(player.runner),
        "obstacles": [canvas.coords(obstacle) for obstacle in obstacle_manager.obstacles],
        "powerups": [canvas.coords(powerup) for powerup in powerup_manager.powerups]
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(game_data, file)
    print("Game saved!")  # Debugging message

def load_game():
    """Loads the game progress from a file."""
    global score, lives
    try:
        with open(SAVE_FILE, "r") as file:
            game_data = json.load(file)
        score = game_data["score"]
        lives = game_data["lives"]
        player_coords = game_data["player_coords"]
        obstacles_coords = game_data["obstacles"]
        powerups_coords = game_data["powerups"]

        # Update my runner's position
        canvas.coords(player.runner, *player_coords)

        # Recreate obstacles
        for obstacle in obstacle_manager.obstacles:
            canvas.delete(obstacle)
        obstacle_manager.obstacles = [
            canvas.create_rectangle(*coords, fill=OBSTACLE_COLOR, outline="black", width=2)
            for coords in obstacles_coords
        ]

        # Recreate power-ups
        for powerup in powerup_manager.powerups:
            canvas.delete(powerup)
        powerup_manager.powerups = [
            canvas.create_oval(*coords, fill=POWERUP_COLOR, outline="black", width=2)
            for coords in powerups_coords
        ]

        update_labels()
        print("Game loaded!")  # Debugging message
    except FileNotFoundError:
        print("No save file found!")  # Debugging message

def end_game():
    """Handles the end of the game, prompting for the player's name and displaying the leaderboard."""
    global score  # Ensure you have access to the player's score
    
    # Stop gama mechanics 
    # cleaning up 

    # Create a popup window to ask for the player's name
    def submit_name():
        name = name_entry.get().strip()  # Get the entered name
        if name:  # Check if the name is not empty
            update_leaderboard(name, score)  # Save the name and score to the leaderboard
            popup.destroy()  # Close the popup
            display_leaderboard()  # Show the updated leaderboard
        else:
            error_label.config(text="Please enter a valid name!")

    # Popup window
    popup = tk.Toplevel(window)
    popup.title("Game Over")
    popup.geometry("400x300") 

    tk.Label(popup, text="Game Over!", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(popup, text=f"Your Score: {score}", font=("Arial", 14)).pack(pady=5)
    tk.Label(popup, text="Enter your name:").pack(pady=5)

    name_entry = tk.Entry(popup, font=("Arial", 14))
    name_entry.pack(pady=5)

    error_label = tk.Label(popup, text="", fg="red", font=("Arial", 10))
    error_label.pack()

    tk.Button(popup, text="Submit", command=submit_name).pack(pady=10)





    # Display Game Over message
    game_over_label = tk.Label(window, text="Game Over", font=("Arial", 40, "bold"))
    game_over_label.pack(pady=20)

    # Prompt for player's name
    player_name_label = tk.Label(window, text="Enter your name for the leaderboard:", font=FONT_MEDIUM)
    player_name_label.pack(pady=10)

    player_name_entry = tk.Entry(window, font=FONT_MEDIUM)
    player_name_entry.pack(pady=5) 
    # Prompt for the player's name and add to leaderboard
    #name_prompt = tk.Toplevel(window)
    #name_prompt.title("Enter Name")
    #tk.Label(name_prompt, text="Enter your name or initials:", font=FONT_MEDIUM).pack()
    #name_entry = tk.Entry(name_prompt, font=FONT_MEDIUM)
    #name_entry.pack(pady=10)
    def submit_name():
        name = player_name_entry.get().strip()
        if name:
            update_leaderboard(name, score)  # Call the updated `update_leaderboard` function
            player_name_label.destroy()
            player_name_entry.destroy()
            submit_button.destroy()
            game_over_label.destroy()
            display_leaderboard()  # Function to display the leaderboard

    submit_button = tk.Button(window, text="Submit", font=FONT_MEDIUM, command=submit_name)
    submit_button.pack(pady=10)

def restart_game():
    """Resets the game to its initial state."""
    global score, lives, paused, game_over, next_threshold, invincible
    
    # Reset the game variables
    score = INITIAL_SCORE
    lives = INITIAL_LIVES
    paused = False
    game_over = False
    next_threshold = 1000
    invincible = False
    
    # Reset the player, obstacles, and power-ups
    player.reset_position()
    obstacle_manager.obstacles.clear()
    powerup_manager.powerups.clear()
    
    # Delete the canvas
    canvas.delete("all")
    
    # Redraw the start message and labels
    start_message = canvas.create_text(
        GAME_WIDTH // 2, GAME_HEIGHT // 2,
        text="Press Space to Start\nPress P to Pause/Unpause During Gameplay\nPress L to View Leaderboard",
        font=FONT_LARGE,
        fill="white"
    )
    score_label.config(text=f"Score: {score}")
    lives_label.config(text=f"Lives: {lives}")

    # Buttons for saving and loading the game
#save_button = tk.Button(window, text="Save Game", font=FONT_MEDIUM, command=save_game)
#save_button.pack(side="right", padx=10)
# these were in the wrong position 
#load_button = tk.Button(window, text="Load Game", font=FONT_MEDIUM, command=load_game)
#load_button.pack(side="right", padx=10)
    # Prompt for the player's name
    name_prompt = tk.Toplevel(window)
    name_prompt.title("Enter Name")
    tk.Label(name_prompt, text="Enter your name or initials:", font=FONT_MEDIUM).pack()
    name_entry = tk.Entry(name_prompt, font=FONT_MEDIUM)
    name_entry.pack(pady=10)

    def submit_name():
        player_name = name_entry.get() or "Player"
        update_leaderboard(player_name, score)  # Save to leaderboard
        name_prompt.destroy()
        display_leaderboard()  # Show leaderboard

    tk.Button(name_prompt, text="Submit", command=submit_name).pack(pady=10)

def update_labels():
    """Updates the score and lives labels."""
    score_label.config(text=f"Score: {score}")
    lives_label.config(text=f"Lives: {lives}")


#game_started = False
#start_message = canvas.create_text(
    #GAME_WIDTH // 2, GAME_HEIGHT // 2,
    #text="Press Space to Start",
    #font=FONT_LARGE,
    #fill="white"


# Default controls
controls = {
    "jump": "Up",
    "slide": "Down",
    "pause": "p",
    "boss_key": "b",
    "restart": "r",
    "cheat": "m",
}

def open_menu():
    """Opens the menu to display and customize controls."""
    menu_window = tk.Toplevel(window)
    menu_window.title("Customizable Controls")
    menu_window.geometry("400x400")
    
    tk.Label(menu_window, text="Customizable Controls", font=FONT_LARGE).pack(pady=10)
    tk.Label(menu_window, text="Press the new key for each action.", font=FONT_SMALL, fg="gray").pack(pady=5)

    for action, key in controls.items():
        frame = tk.Frame(menu_window)
        frame.pack(pady=5)
        tk.Label(frame, text=f"{action.capitalize()}: ", font=FONT_MEDIUM).pack(side="left")
        key_entry = tk.Entry(frame, font=FONT_MEDIUM, width=5)
        key_entry.insert(0, key)
        key_entry.pack(side="left")
        # Save the key changes in a dynamic way 
        def save_key(entry=key_entry, action=action):
            controls[action] = entry.get()
        tk.Button(frame, text="Save", command=save_key).pack(side="left")
    
    tk.Button(menu_window, text="Close", command=menu_window.destroy).pack(pady=20)

def game_loop():
    global paused, score, lives, OBSTACLE_SPEED, next_threshold

    if not game_started or paused:
        if paused and not game_over and game_started:  # Show resume message only if mid-game
            show_resume_message()
        window.after(int(1000 / FPS), game_loop)
        return

# finished my section 1 

    if not game_started or paused:
        window.after(int(1000 / FPS), game_loop)
        return

    if not paused:
        # Move obstacles and power-ups
        obstacle_manager.move()
        powerup_manager.move()

        #Randomly spawn new elements
        if random.random() < OBSTACLE_SPAWN_CHANCE:
            obstacle_manager.create_obstacle()
        if random.random() < POWERUP_SPAWN_CHANCE:
            powerup_manager.create_powerup()

        # Check for collisions
        if check_collision(player.runner, obstacle_manager.obstacles):
            if not invincible:
                lives -= 1
                update_labels()
                if lives <= 0:
                    end_game()  # End game only once
                    return  # Ensure no further actions occur after the game ends
                else:
                    player.reset_position()

        # Update score
        score += 1
        update_labels()

        # Increase difficulty and show checkpoint message
        if score >= next_threshold:
            OBSTACLE_SPEED += 0.5  # Increase speed
            next_threshold += 1000  # Update threshold for the next increase
            show_checkpoint_message()  # Display the checkpoint message

    # Schedule next frame
    window.after(int(1000 / FPS), game_loop)

        # Check collisions

    if check_collision(player.runner, obstacle_manager.obstacles):
        if not invincible:
            lives -= 1
        update_labels()  # Update lives on the screen
        if lives <= 0:
            end_game()
        else:
            # Reset runner position if a life is lost
            player.reset_position()

    runner_coords = canvas.coords(player.runner)
    for obs in obstacle_manager.obstacles:
        
        obs_coords = canvas.coords(obs)
        if (runner_coords[2] > obs_coords[0] and runner_coords[0] < obs_coords[2] and
                runner_coords[3] > obs_coords[1] and runner_coords[1] < obs_coords[3]):
            return True
    return False
 
        # Randomly spawn new elements
        #if random.random() < OBSTACLE_SPAWN_CHANCE:
            #obstacle_manager.create_obstacle()
       # if random.random() < POWERUP_SPAWN_CHANCE:     # this was a mistake 
            #powerup_manager.create_powerup()

        # Update score
        #score += 1
        #update_labels()

        # Increase difficulty and show checkpoint message
        #if score >= next_threshold:
            #OBSTACLE_SPEED += 0.5  # Increase speed
            #next_threshold += 1000  # Update threshold for the next increase
            #print(f"Difficulty increased! New OBSTACLE_SPEED: {OBSTACLE_SPEED}")  # Debugging log
            #show_checkpoint_message()  # Display the checkpoint message

    # Schedule next frame
    window.after(int(1000 / FPS), game_loop) 

def show_checkpoint_message():
    """Displays a checkpoint message temporarily."""
    checkpoint_message = canvas.create_text(
        GAME_WIDTH // 2, GAME_HEIGHT // 2 - 100,
        text="Checkpoint reached! The game will get harder!",
        font=FONT_MEDIUM,
        fill="white"
    )
    canvas.after(2000, lambda: canvas.delete(checkpoint_message))  # Remove after 2 seconds



def check_collision(runner, obstacles):
    """Checks if the runner collides with any obstacles."""
    if invincible:
        return False  # No collisions during invincibility

    runner_coords = canvas.coords(runner)
    for obs in obstacles:
        obs_coords = canvas.coords(obs)
        if (runner_coords[2] > obs_coords[0] and  # Runner's right edge > Obstacle's left edge
            runner_coords[0] < obs_coords[2] and  # Runner's left edge < Obstacle's right edge
            runner_coords[3] > obs_coords[1] and  # Runner's bottom edge > Obstacle's top edge
            runner_coords[1] < obs_coords[3]):   # Runner's top edge < Obstacle's bottom edge
            return True
    return False


def activate_invincibility():
    """Activates invincibility for 10 seconds."""
    global invincible
    invincible = True
    print("Invincibility Activated!")  # Debugging
    canvas.after(10000, deactivate_invincibility)  # Disable after 10 seconds

def deactivate_invincibility():
    """Disables invincibility."""
    global invincible
    invincible = False
    print("Invincibility Deactivated!")  # Debugging

# Setup game window and canvas
window = tk.Tk()
window.title("Endless Runner Adventure")
canvas = tk.Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BACKGROUND_COLOR)
canvas.pack()
game_started = False  # this part of the code should be after canvas.pack() 
start_message = canvas.create_text(
    GAME_WIDTH // 2, GAME_HEIGHT // 2,
    text="ENDLESS RUNNER ADVENTURE\nPress Space to start",
    font=FONT_LARGE,
    fill="white"
)

# Score and lives
score = INITIAL_SCORE
lives = INITIAL_LIVES
paused = False
game_over = False

# Setting up the Leaderboard 
def load_leaderboard():
    """Loads the leaderboard from a file or returns an empty list if the file doesn't exist."""
    try:
        with open("leaderboard.txt", "r") as file:
            return [tuple(line.strip().split(",")) for line in file]
    except FileNotFoundError:
        return []

def save_leaderboard(leaderboard):
    """Saves the leaderboard to a file."""
    with open("leaderboard.txt", "w") as file:
        for name, score in leaderboard:
            file.write(f"{name},{score}\n")

def update_leaderboard(name, score):
    """Updates the leaderboard with a new score."""
    leaderboard = load_leaderboard()
    # Remove existing entry for the player
    leaderboard = [entry for entry in leaderboard if entry[0] != name]
    leaderboard.append((name, str(score)))
    leaderboard = sorted(leaderboard, key=lambda x: int(x[1]), reverse=True)[:10]
    save_leaderboard(leaderboard)


def display_leaderboard():
    """Displays the leaderboard in a new window."""
    leaderboard = load_leaderboard()  # Load the leaderboard data

    # Create a new window to display the leaderboard
    leaderboard_window = tk.Toplevel(window)
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("400x400")

    tk.Label(leaderboard_window, text="Leaderboard", font=("Arial", 20, "bold")).pack(pady=10)

    # Display the top scores
    for i, (name, score) in enumerate(leaderboard, start=1):
        tk.Label(leaderboard_window, text=f"{i}. {name}: {score}", font=("Arial", 16)).pack(anchor="w", padx=20)

    tk.Button(leaderboard_window, text="Close", command=leaderboard_window.destroy).pack(pady=20)



score_label = tk.Label(window, text=f"Score: {score}", font=FONT_MEDIUM)
score_label.pack(side="left", padx=10)
lives_label = tk.Label(window, text=f"Lives: {lives}", font=FONT_MEDIUM)
lives_label.pack(side="left", padx=10)

# Game objects
player = Runner(canvas)
obstacle_manager = Obstacle(canvas)
powerup_manager = PowerUp(canvas)

def activate_boss_key():
    """Handles the Boss Key feature by pausing the game and opening Blackboard Manchester."""
    global paused, game_over
    if not game_over:  # Only pause if the game is not over
        paused = True  # Pause the game
        show_resume_message()  # Show resume message when Boss Key is triggered
        webbrowser.open("https://www.itservices.manchester.ac.uk/students/blackboard/")  # Open Blackboard Manchester


# Bindings and game loop
#window.bind("<KeyPress>", lambda e: player.jump() if e.keysym == "Up" else player.slide())
def handle_key_press(event):
    global game_started, paused, cheat_buffer, invincible

    if not game_started and event.keysym == "space":
        game_started = True
        paused = False
        canvas.delete(start_message)
    elif not game_started and event.keysym == "l":  # Show leaderboard in main menu
        display_leaderboard()
    elif game_started and not game_over:  # Allow key actions only if the game is not over
        if event.keysym == controls["jump"]:
            player.jump()
        elif event.keysym == controls["slide"]:
            player.slide()
        elif event.keysym == controls["boss_key"]:
            activate_boss_key()
        elif event.keysym == controls["pause"]:
            paused = not paused  # Toggle pause state
        elif event.keysym == controls["restart"] and game_over:  # Restart if game is over
            restart_game()
        elif event.keysym == controls["cheat"]:  # Cheat code
            activate_invincibility()
            show_cheat_code_message()
        else:
            cheat_buffer = (cheat_buffer + event.keysym).upper()[-len(CHEAT_CODE):]
            if cheat_buffer == CHEAT_CODE:
                activate_invincibility()


def show_cheat_code_message():
    """Displays a message when the cheat code is activated."""
    cheat_message = canvas.create_text(
        GAME_WIDTH // 2, GAME_HEIGHT // 2 - 50,
        text="CHEATCODE ACTIVATED",
        font=FONT_LARGE,
        fill="green"
    )
    canvas.after(2000, lambda: canvas.delete(cheat_message))  # Remove message after 2 seconds

def show_resume_message():
    """Displays a message when resuming the game after using the Boss Key."""
    if paused:  # Only show the message if the game is paused
        resume_message = canvas.create_text(
            GAME_WIDTH // 2, GAME_HEIGHT // 2,
            text="Press P to Resume the Game",
            font=FONT_LARGE,
            fill="white"
        )
        canvas.after(2000, lambda: canvas.delete(resume_message))  # Remove message after 2 seconds

def show_game_over_menu():
    """Displays the game over menu with a restart option."""
    global game_over, paused
    paused = True  # Pause the game when the game over menu is shown

    game_over_menu = tk.Toplevel(window)  # Create a new top-level window
    game_over_menu.title("Game Over")
    game_over_menu.geometry("300x200")
    
    # Game Over message
    game_over_label = tk.Label(game_over_menu, text="Game Over!", font=FONT_LARGE, fg="red")
    game_over_label.pack(pady=20)
    
    # Restart button
    restart_button = tk.Button(game_over_menu, text="Restart", font=FONT_MEDIUM, command=lambda: restart_game(game_over_menu))
    restart_button.pack(pady=10)
    
    # Close button to quit
    quit_button = tk.Button(game_over_menu, text="Quit", font=FONT_MEDIUM, command=window.quit)
    quit_button.pack(pady=10)
    
    # Focus on the game over window to prevent interaction with the main game
    game_over_menu.grab_set()

def restart_game(game_over_menu):
    """Restarts the game by resetting all necessary variables and starting the game again."""
    global score, lives, game_over, paused
    score = INITIAL_SCORE
    lives = INITIAL_LIVES
    game_over = False
    paused = False
    player.reset_position()  # Reset player position
    canvas.delete("all")  # Clear the canvas
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2,
                       text="Press Space to Start",
                       font=FONT_LARGE,
                       fill="white")  # Show start message
    game_over_menu.destroy()  # Close the game over menu
    game_loop()  # Restart the game loop



# Menu button to navigate to controls customization
menu_button = tk.Button(window, text="Menu", font=FONT_MEDIUM, command=lambda: open_menu())
menu_button.pack(side="right", padx=10) 

# Buttons for saving and loading the game
save_button = tk.Button(window, text="Save Game", font=FONT_MEDIUM, command=save_game)
save_button.pack(side="right", padx=10)

load_button = tk.Button(window, text="Load Game", font=FONT_MEDIUM, command=load_game)
load_button.pack(side="right", padx=10)

window.bind("<KeyPress>", handle_key_press)

game_loop()
window.mainloop() 

