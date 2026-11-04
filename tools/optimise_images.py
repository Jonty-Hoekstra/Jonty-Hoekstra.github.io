"""Makes web-sized WebP images in assets/img from the original files in content/.

Each still image gets one WebP for each width in STILL_WIDTHS that is not wider than the original,
plus one at the original width if that is smaller than the largest step. Each GIF becomes an
animated WebP and a still poster from its first frame.

Run it after you add or change a file in content/, then copy the printed sizes into the HTML.
Needs Python 3 with Pillow (pip install pillow).
"""

from pathlib import Path

from PIL import Image, ImageSequence

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT_ROOT / 'content'
OUTPUT = PROJECT_ROOT / 'assets' / 'img'

STILL_WIDTHS = (640, 1280, 1920)
STILL_QUALITY = 80
ANIMATION_MAX_WIDTH = 800
ANIMATION_QUALITY = 70

# Output folder, output name, source file (relative to content/).
STILLS = [
    ('about', 'headshot', 'Headshot.jpg'),
    ('mythos-party', 'map-1', 'MythosParty/Mythos Map 1.png'),
    ('mythos-party', 'map-2', 'MythosParty/Mythos Map 2.png'),
    ('solace', 'set-dressing', 'Solace/Personal_Project-SetDressing.png'),
    ('cathedral-scene', 'blockout-1', 'Cathedral Scene (WIP)/be0a908c-dd2f-4693-be07-90d6e1e59f43.jpg'),
    ('cathedral-scene', 'blockout-2', 'Cathedral Scene (WIP)/cc61248f-6d1c-4c9a-b29b-31bf7538fe89.jpg'),
    ('cathedral-scene', 'blockout-3', 'Cathedral Scene (WIP)/3cdb3f29-c9e0-4dcd-9d37-ea44232b60be.jpg'),
] + [
    ('spaceship-level', f'shot-{index:02d}', f'Spaceship Level/HighresScreenshot{index:05d}.png')
    for index in range(35)
]

ANIMATIONS = [
    ('game-jam-map', 'flythrough', 'Game Jam/GameJamMap.gif'),
    ('solace', 'spline-roots', 'Solace/Personal_Project_Dynamic_Spline_Roots.gif'),
    ('solace', 'ship-animation', 'Solace/Personal_Project_Ship_Animation.gif'),
    ('solace', 'tile-animation', 'Solace/Personal_Project_Tile_Animation.gif'),
]


def resized(image, width):
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.LANCZOS)


def save_still(folder, name, source):
    image = Image.open(CONTENT / source).convert('RGB')
    widths = [width for width in STILL_WIDTHS if width < image.width]
    if image.width <= STILL_WIDTHS[-1]:
        widths.append(image.width)
    else:
        widths.append(STILL_WIDTHS[-1])
    widths = sorted(set(widths))

    target = OUTPUT / folder
    target.mkdir(parents=True, exist_ok=True)
    for width in widths:
        output = target / f'{name}-{width}.webp'
        resized(image, width).save(output, 'WEBP', quality=STILL_QUALITY, method=6)
    largest = resized(image, widths[-1])
    print(f'{folder}/{name}: widths {widths}, largest {largest.width}x{largest.height}')


def save_animation(folder, name, source):
    animation = Image.open(CONTENT / source)
    width = min(animation.width, ANIMATION_MAX_WIDTH)
    frames, durations = [], []
    for frame in ImageSequence.Iterator(animation):
        durations.append(frame.info.get('duration', 70))
        frames.append(resized(frame.convert('RGB'), width))

    target = OUTPUT / folder
    target.mkdir(parents=True, exist_ok=True)
    output = target / f'{name}.webp'
    frames[0].save(output, 'WEBP', save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, quality=ANIMATION_QUALITY, method=4)
    frames[0].save(target / f'{name}-poster.webp', 'WEBP', quality=STILL_QUALITY, method=6)
    size_mb = output.stat().st_size / 1_000_000
    print(f'{folder}/{name}: {frames[0].width}x{frames[0].height}, {len(frames)} frames, {size_mb:.1f} MB')


def main():
    for folder, name, source in STILLS:
        save_still(folder, name, source)
    for folder, name, source in ANIMATIONS:
        save_animation(folder, name, source)


if __name__ == '__main__':
    main()
