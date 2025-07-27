# 🎮 Endless Runner Adventure

A feature-rich endless runner game built with **Python** and **Tkinter**, simulating dynamic gameplay mechanics like jumping, sliding, cheat modes, and even a "boss key" that switches the game off and goes to the University's website.

---

## 🚀 Features

- ⛹️‍♂️ Jump & slide mechanics
- ❌ Obstacles and ⚡ power-ups
- 🎯 Progressive difficulty (increases every 1000 points)
- 🔐 Cheat mode (`IMMORTAL` code or M key)
- 🏁 Game save/load system using JSON
- 🏆 Leaderboard stored in a file
- ⏸ Pause, restart, and resume functions
- 🔒 "Boss Key" that opens [University of Manchester Blackboard](https://www.itservices.manchester.ac.uk/students/blackboard/)
- 🎮 Customizable controls from the menu
- 📈 Score and lives tracking
- 💾 JSON and TXT file handling
- 👾 Retro-style UI with `Tkinter.Canvas`

---



## 📂 File Structure
tkinter-game/
├── game_solution.py
├── game_save.json
├── leaderboard.txt
├── high_scores.txt
├── README.md
└── requirements.txt

---

## 🧠 How It Works

This game uses a `Runner` class for player movement, `Obstacle` and `PowerUp` classes for dynamic gameplay, and uses the `canvas` widget to simulate movement through object shifting.

Score increases automatically over time and the game gets harder every 1000 points. Collisions end the game unless cheat mode is activated.

---

## 🎮 Controls

| Action      | Default Key |
|-------------|-------------|
| Jump        | Up Arrow    |
| Slide       | Down Arrow  |
| Pause       | P           |
| Restart     | R           |
| Boss Key    | B           |
| Cheat Code  | M or type `IMMORTAL` |

---


## Tech Stack
Python 3.10+

Tkinter (built-in GUI)

Pillow (for image processing)

json, webbrowser, random modules

