# Pycraft

A 2D sandbox game in Python and Pygame inspired by Minecraft's creative mode: walk and jump across an endless world, and place or remove blocks wherever you like. I wrote it in high school as a side project to learn game loops, simple physics and procedural generation.

![Pycraft](https://github.com/user-attachments/assets/95125351-6839-4d92-8c58-ff66671c28da)

## How it works

- **Endless world.** The world is generated in chunks of 16 columns as the player walks past either edge. Each column gets a random terrain height (taller columns are rarer), and chunks that have been visited are kept, so blocks you placed are still there when you come back.
- **Physics.** Gravity, jumping and collision with blocks, including no jumping when a block is directly overhead.
- **Building.** Click a block to remove it or an empty space to place one, with the hovered cell highlighted.

## Running it

```bash
git clone https://github.com/MarcosSaade/Pycraft.git
cd Pycraft
pip install pygame
python main.py
```

## Controls

| Action | Keys |
|---|---|
| Move | Left / Right arrows, or A / D |
| Jump | Up arrow, W or Space |
| Place or remove a block | Mouse click |

## Code

- `main.py`: game loop, player physics, world generation and chunk management.
- `helper.py`: helper functions.
- `data/img/`: sprites and textures.

## Ideas for later

More block types and crafting, smoother terrain generation (for example Perlin noise instead of independent random columns), and saving worlds to disk.
