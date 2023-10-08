# Out of the box
Game for a Quantum Games Hackathon 2023

<img align="right" alt="cat" align="center" src="https://raw.githubusercontent.com/agolebiowska/out-of-the-box/main/assets/milton.png" width="40%">

## Lore
You take on the role of Erwin Schrödinger, the renowned physicist who finds himself in the most bizarre predicament of his life.

Once upon a time in the whimsical realm of quantum physics, Erwin Schrödinger's mischievous cat, Milton, hatched an ingenious plan for revenge. Fed up with all those thought experiments involving boxes, cats, and uncertainty, Milton decided it was high time to turn the tables on his human companion.

Milton, armed with a quantum wand (which may or may not exist), trapped Erwin inside a quantum box that was unlike any other. This wasn't your ordinary box — it was a quantum box, brimming with mad qubits that had somehow acquired a taste for chaos.

As Erwin Schrödinger, you find yourself inside this peculiar quantum box, surrounded by zany qubits and your mission, should you choose to accept it (and you have no choice, really), is to harness your physics knowledge and unravel the mysteries of the quantum box.

Each level is a puzzle waiting to be solved. From entanglement enigmas to superposition conundrums, you'll need to apply your understanding of quantum principles to set things right and escape from the clutches of Milton's quantum prank.

<img align="left" alt="erwin" align="center" src="https://raw.githubusercontent.com/agolebiowska/out-of-the-box/main/assets/erwin.png" width="45%">

## Rules
- Each level presents you with a collection of qubits and quantum gates.
- Your mission is to **manipulate the qubits using the available quantum gates to reach the specified quantum state** shown as a Q-sphere.
- Time is of the essence! **Poison is slowly engulfing the screen, and you must complete the level before it takes over**.
- Player movement with **WSAD** or **UP,LEFT,RIGHT,DOWN keys**
- After picking up the gate it lands in your inventory. You can then use it by pressing the corresponding key **(1, 2, 3, 4, 5)** to apply the gate on a qubit.
- Don't be afraid to experiment with different gate combinations to achieve the desired quantum state.

## Running the game
```bash
git clone https://github.com/agolebiowska/out-of-the-box
cd out-of-the-box
conda env create -f environment.yaml
conda activate out-of-the-box
python main.py

# game has 1920x1080 resolution
# beware of the music :)
```

## Screenshots
![](https://raw.githubusercontent.com/agolebiowska/out-of-the-box/main/assets/screenshot_0.png)
![](https://raw.githubusercontent.com/agolebiowska/out-of-the-box/main/assets/screenshot_1.png)
![](https://raw.githubusercontent.com/agolebiowska/out-of-the-box/main/assets/screenshot_2.png)
![](https://raw.githubusercontent.com/agolebiowska/out-of-the-box/main/assets/screenshot_3.png)

## Gameplay
[![Gameplay video](http://img.youtube.com/vi/OIu7boVGb2k/0.jpg)](http://www.youtube.com/watch?v=OIu7boVGb2k "Out of the Box - Gameplay")

## Possible level solutions
#### Level 1
1. X to Q0.
#### Level 2
1. H to Q0.
2. Z to Q0.
#### Level 3
1. H to both qubits.
#### Level 4
1. NOT to Q0.
2. CNOT to Q0.
#### Level 5
1. H to Q0.
2. CNOT to Q0.
#### Level 6
1. RY to Q0.
2. CNOT to Q0. 
3. NOT to Q1.
#### Level 7
1. X to Q0.
2. X to Q1.
3. CXX to Q0.
#### Level 8
1. H to Q0.
2. H to Q2.
3. CNOT to Q1.
4. CNOT to Q0.
#### Level 9
1. X to Q0. 
2. X to Q1. 
3. X to Q2. 
4. H to Q1.
5. CCX to Q1.
#### Levl 10
1. RY to Q0.
2. X to Q1.
3. H to Q2.
4. H to Q3. 
5. CX to Q0.

### Assets
- Cat & Erwin generated using app.scenario.com and then edited in Photopea & Aseprite.
- Player and qubits edited in Aseprite starting from: https://game-endeavor.itch.io/mystic-woods
- Gates: https://greatdocbrown.itch.io/gamepad-ui
- Other art created in Photopea & Aseprite.
- Music: https://pixabay.com/music/scary-childrens-tunes-creepy-devil-dance-166764/
- Color palette: https://lospec.com/palette-list/pear36
- Font: https://www.dafont.com/joystix.font

### TODOS
- Big list of possible levels with difficulty and randomly choosing them
- Increase qubits speed with levels
- Add items for player to take, like temporary speed, take-back etc.
- Adjust poison speed per level.
- Make kitty in the top corner say mean things
- Make difficulty levels to choose (poison speed)
- Key numbers under the inventory
- Indication on which level the player is currently at
- Better qubits "ai"
