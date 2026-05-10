# Game of Thrones: A Python Text Adventure

A terminal-based Object-Oriented Programming (OOP) game set in the world of Westeros. This project was developed as part of the NCC Level 3 Diploma in Computing.

## ⚔️ The Quest
You are a minor noble in Westeros seeking to claim the Iron Throne. To win, you must navigate the dangerous lands of the Seven Kingdoms, collect legendary items, and defeat the enemies of the realm.

### Objectives
* **Slay the Night King** at The Wall using the **Dragonglass Dagger**.
* **Defeat Gregor "The Mountain" Clegane** at King’s Landing with the **Valyrian Steel Sword**.
* **Claim the Throne:** You must possess the **Seal of the Hand** and reach King's Landing to win.

## 🛠️ Features
* **Object-Oriented Design:** Built using Python classes for `Character`, `Location`, `NPC`, and `Item`.
* **Dynamic World:** Explore 10+ iconic locations including Winterfell, Dragonstone, and The Eyrie.
* **Inventory Management:** Custom satchel system with a 4-item limit and GOT-themed error handling.
* **Interactive NPCs:** Encounter characters that block progress until specific conditions are met.

## 🚀 How to Run
1. Ensure you have **Python 3.x** installed.
2. Clone this repository:
   ```bash
   git clone [https://github.com/EmeraldKingg/game-of-thrones-adventure.git](https://github.com/EmeraldKingg/game-of-thrones-adventure.git)

   python game_of_thrones.py
## 📜 Commands
* **`north`, `south`, `east`, `west`: Move between regions.

* **`take [item]`: Add an item to your satchel.**

* **`use [item]`: Interact with NPCs or the environment.**

* **`satchel`: View your current inventory.**

* **`help`: Display the command list.**

## 🗺️ Map Layout
The game features a connected world map. Note that every character and space in the box below is important for the alignment:

```text
          [Dragonstone]
               |
[The Neck] <-> [Winterfell] <-> [Harrenhal] <-> [King's Landing] <-> [The Eyrie]
    |                               |                  |
[Castle Black]                 [Riverrun]         [The Twins]
    |
[The Wall]
