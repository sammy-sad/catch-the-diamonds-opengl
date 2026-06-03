
# Catch the Diamonds 💎

An interactive 2D arcade game written in **Python** using **PyOpenGL**. Instead of relying on built-in OpenGL shape primitives, this project utilizes a custom-implemented **Midpoint Line Algorithm** to draw all shapes, including the catcher bowl, falling diamonds, and control buttons.

---

##  Game Features

* **Dynamic Speed Scaling:** The game gets progressively harder! Every diamond caught increases the velocity of the next falling gem.
* **Interactive Control Panel:**
    *  **Teal Arrow:** Restarts the game, resetting your score and diamond speed.
    *  **Amber Button:** Toggles between Play and Pause states seamlessly.
    *  **Red Cross:** Cleanly exits the game window and prints your final score to the console.
* **Collision Detection:** Uses bounding box alignment to check if the diamond landed safely inside the catcher bowl.
* **Game Over State:** Missing a diamond triggers a Game Over screen, shifting the catcher color to red to indicate defeat.

---

##  Behind the Code: Computer Graphics Concepts

This project showcases fundamental computer graphics techniques, specifically:
1. **8-Way Symmetry & Zone Selection:** Translates any line slope into Zone 0 to simplify rasterization processing, and maps it back accurately using the **Midpoint Line Algorithm**.
2. **Double Buffer / Timer Update Mechanics:** Leverages `glutTimerFunc` for smooth frame updates independent of computer rendering speeds.

---

## 🚀 Getting Started

### Prerequisites

You need Python 3.x installed alongside the standard PyOpenGL packages. Install the dependencies via pip:

```bash
pip install PyOpenGL PyOpenGL_accelerate
