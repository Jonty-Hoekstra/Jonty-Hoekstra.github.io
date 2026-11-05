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

# Output folder, output name, source file (relative to content/), and optional widths.
STILLS = [
    ('about', 'headshot', 'Headshot.jpg'),
    # Thumbnail of the YouTube reel (youtu.be/zC75iq0rj6k), used as the click-to-play poster.
    ('vfx-material-showcase', 'reel-poster', 'VFX & Material Showcase/reel-thumbnail.jpg'),
    ('mythos-party', 'map-1', 'MythosParty/Mythos Map 1.png'),
    ('mythos-party', 'map-2', 'MythosParty/Mythos Map 2.png'),
    ('solace', 'set-dressing', 'Solace/Personal_Project-SetDressing.png'),
    ('solace', 'current-build', 'Solace/image 109.png'),
    ('solace', 'engine-prototype', 'Solace/Group 415.png'),
    ('solace', 'paper-prototype', 'Solace/20230705_144133 (1).jpg'),
    ('solace', 'ui-wireframe', 'Solace/Game UI.png'),
    ('solace', 'power-rule', 'Solace/Powered lines and the core.png'),
    # A very wide chart: shown in a sideways-scrolling frame, so it needs a large width to stay readable.
    ('solace', 'roadmap', 'Solace/Gantt chart.png', (1280, 2400)),
    ('cathedral-scene', 'blockout-1', 'Cathedral Scene (WIP)/be0a908c-dd2f-4693-be07-90d6e1e59f43.jpg'),
    ('cathedral-scene', 'blockout-2', 'Cathedral Scene (WIP)/cc61248f-6d1c-4c9a-b29b-31bf7538fe89.jpg'),
    ('cathedral-scene', 'blockout-3', 'Cathedral Scene (WIP)/3cdb3f29-c9e0-4dcd-9d37-ea44232b60be.jpg'),
    ('cathedral-scene', 'interior-01', 'Cathedral Scene (WIP)/HighresScreenshot00035.png'),
    ('cathedral-scene', 'interior-02', 'Cathedral Scene (WIP)/HighresScreenshot00036.png'),
    ('cathedral-scene', 'interior-03', 'Cathedral Scene (WIP)/HighresScreenshot00037.png'),
    ('cathedral-scene', 'interior-04', 'Cathedral Scene (WIP)/HighresScreenshot00038.png'),
    ('cathedral-scene', 'interior-05', 'Cathedral Scene (WIP)/HighresScreenshot00039.png'),
    ('cathedral-scene', 'interior-06', 'Cathedral Scene (WIP)/HighresScreenshot00040.png'),
    ('cathedral-scene', 'interior-07', 'Cathedral Scene (WIP)/HighresScreenshot00041.png'),
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


def save_still(folder, name, source, step_widths=STILL_WIDTHS):
    image = Image.open(CONTENT / source).convert('RGB')
    widths = [width for width in step_widths if width < image.width]
    if image.width <= step_widths[-1]:
        widths.append(image.width)
    else:
        widths.append(step_widths[-1])
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


# Link preview images (og:image), one per page. JPG, because some sites do not show WebP previews.
PREVIEW_SIZE = (1200, 630)
PREVIEW_QUALITY = 85
PREVIEWS = [
    ('home', 'Spaceship Level/HighresScreenshot00027.png'),
    ('spaceship-level', 'Spaceship Level/HighresScreenshot00023.png'),
    ('solace', 'Solace/Personal_Project_Tile_Animation.gif'),
    ('mythos-party', 'MythosParty/Mythos Map 1.png'),
    ('game-jam-map', 'Game Jam/GameJamMap.gif'),
    ('cathedral-scene', 'Cathedral Scene (WIP)/HighresScreenshot00035.png'),
    ('vfx-material-showcase', 'VFX & Material Showcase/reel-thumbnail.jpg'),
]


def save_preview(name, source):
    # The first frame of a GIF; the image is scaled to cover the preview size and cropped to its centre.
    image = Image.open(CONTENT / source)
    image.seek(0)
    image = image.convert('RGB')
    target_width, target_height = PREVIEW_SIZE
    scale = max(target_width / image.width, target_height / image.height)
    scaled = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)
    left = (scaled.width - target_width) // 2
    top = (scaled.height - target_height) // 2
    preview = scaled.crop((left, top, left + target_width, top + target_height))

    target = OUTPUT / 'previews'
    target.mkdir(parents=True, exist_ok=True)
    preview.save(target / f'{name}.jpg', 'JPEG', quality=PREVIEW_QUALITY, optimize=True, progressive=True)
    print(f'previews/{name}.jpg')


def main():
    for still in STILLS:
        save_still(*still)
    for folder, name, source in ANIMATIONS:
        save_animation(folder, name, source)
    for name, source in PREVIEWS:
        save_preview(name, source)


if __name__ == '__main__':
    main()
