# Urizen

<img src="https://github.com/vurmux/urizen/blob/master/res/logo.svg" width="100" height="100" align="left"> Urizen is the roguelike dungeon generation library written on Python3. It has various algorithms that can be used to generate maps on scale of single rooms to the whole world.

```diff
- Note: This project is on early stage of development.
- It can contain bugs, API breaking changes and lack of documentation.
```

## Features

- Two main collections - generators and visualizers - that can be used in any variations.
- Easy-to-use map objects with no need of additional libraries.
- Modular architecture that allows simple extension.

## Examples

Here is some example maps that Urizen can generate:

<img src="https://github.com/vurmux/urizen/blob/master/res/examples.png" align="center">

---

## Quick Start

### Installation

Urizen can be installed with pip:

```
$ pip3 install --user urizen
```

Or manually. To do it, clone this repository:

```
$ git clone https://github.com/vurmux/urizen.git
$ cd urizen
$ virtualenv venv
```

And build it:

```
$ . venv/bin/activate
$ python3 setup.py install --user
```

### First script

Import this library:

```python
import urizen as uz
```

Create a 50x50 size map using BSP algorithm:

```python
M = uz.dungeon_bsp_tree(50, 50)
```

And visualize it using Pillow:

```python
uz.vg_pillow_pixelated(M, scale=5)
```

The result image will be automatically opened with a default image viewer.
