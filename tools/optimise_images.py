"""Makes web-sized WebP images in assets/img from the original files in content/.

Each still image gets one WebP for each width in STILL_WIDTHS that is not wider than the original,
plus one at the original width if that is smaller than the largest step. Each GIF becomes an
animated WebP and a still poster from its first frame.

Run it after you add or change a file in content/, then copy the printed sizes into the HTML.
Needs Python 3 with Pillow (pip install pillow).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageSequence

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT_ROOT / 'content'
OUTPUT = PROJECT_ROOT / 'assets' / 'img'

STILL_WIDTHS = (640, 1280, 1920)
STILL_QUALITY = 80
ANIMATION_MAX_WIDTH = 800
ANIMATION_QUALITY = 70
# Ability clips show as small tiles, so they are smaller to keep the page light.
ABILITY_WIDTH = 520
# The page background (--colour-bg in tokens.css). Images that pass it fill their transparent areas
# with it, so cut-out reference boards blend into the page.
PAGE_BACKGROUND = (11, 11, 16)

# Output folder, output name, source file (relative to content/), and optional widths.
STILLS = [
    ('about', 'headshot', 'Headshot.jpg'),
    # Thumbnail of the YouTube reel (youtu.be/zC75iq0rj6k), used as the click-to-play poster.
    ('vfx-material-showcase', 'reel-poster', 'VFX & Material Showcase/reel-thumbnail.jpg'),
    ('mythos-party', 'map-1', 'MythosParty/Mythos Map 1.png'),
    ('mythos-party', 'map-2', 'MythosParty/Mythos Map 2.png'),
    ('mythos-party', 'gameplay-00003', 'MythosParty/alex-coultas-highresscreenshot00003.jpg'),
    ('mythos-party', 'gameplay-00004', 'MythosParty/alex-coultas-highresscreenshot00004.jpg'),
    ('mythos-party', 'gameplay-00007', 'MythosParty/alex-coultas-highresscreenshot00007.jpg'),
    ('mythos-party', 'gameplay-00010', 'MythosParty/alex-coultas-highresscreenshot00010.jpg'),
    ('mythos-party', 'gameplay-00013', 'MythosParty/alex-coultas-highresscreenshot00013.jpg'),
    ('mythos-party', 'gameplay-00015', 'MythosParty/alex-coultas-highresscreenshot00015.jpg'),
    ('mythos-party', 'gameplay-00018', 'MythosParty/alex-coultas-highresscreenshot00018.jpg'),
    # Thumbnails of the YouTube videos, used as click-to-play posters.
    ('mythos-party', 'trailer-poster', 'MythosParty/video-FwoVMOu09Bg.jpg'),
    ('mythos-party', 'pre-alpha-poster', 'MythosParty/video-4_IFLiO7ObI.jpg'),
    ('mythos-party', 'capsule-art', 'MythosParty/Mythos_Party_Capsule_Art_Revised.png'),
    ('mythos-party', 'trailer-2019-poster', 'MythosParty/video-eAPEBaGp2xk.jpg'),
    ('mythos-party', 'early-00008', 'MythosParty/Old Content (from uni)/HighresScreenshot00008.png'),
    ('mythos-party', 'early-00025', 'MythosParty/Old Content (from uni)/HighresScreenshot00025.png'),
    ('mythos-party', 'early-00029', 'MythosParty/Old Content (from uni)/HighresScreenshot00029.png'),
    ('mythos-party', 'early-00031', 'MythosParty/Old Content (from uni)/HighresScreenshot00031.png'),
    ('mythos-party', 'early-00032', 'MythosParty/Old Content (from uni)/HighresScreenshot00032.png'),
    ('mythos-party', 'early-00033', 'MythosParty/Old Content (from uni)/HighresScreenshot00033.png'),
    ('mythos-party', 'early-00034', 'MythosParty/Old Content (from uni)/HighresScreenshot00034.png'),
    ('mythos-party', 'early-00035', 'MythosParty/Old Content (from uni)/HighresScreenshot00035.png'),
    ('mythos-party', 'early-00036', 'MythosParty/Old Content (from uni)/HighresScreenshot00036.png'),
    ('mythos-party', 'early-00037', 'MythosParty/Old Content (from uni)/HighresScreenshot00037.png'),
    ('mythos-party', 'early-hud-1', 'MythosParty/Old Content (from uni)/Desktop Screenshot 2019.11.15 - 13.35.36.74.png'),
    ('mythos-party', 'early-hud-2', 'MythosParty/Old Content (from uni)/Desktop Screenshot 2019.11.15 - 13.36.39.49.png'),
    ('mythos-party', 'early-hud-3', 'MythosParty/Old Content (from uni)/Desktop Screenshot 2019.11.15 - 13.39.51.75.png'),
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
    ('cathedral-scene', 'lighting-oculus', 'Cathedral Scene (WIP)/Lighting.jpg'),
    ('cathedral-scene', 'lighting-candle', 'Cathedral Scene (WIP)/Lighting2.png'),
    # Reference boards: transparent cut-outs, so they sit on the page background.
    # The Group boards are cropped (left, top, right, bottom) above their notes; the page shows the notes as text.
    ('cathedral-scene', 'refs-first', 'Cathedral Scene (WIP)/CathedralFirstRefs.png', STILL_WIDTHS, PAGE_BACKGROUND),
    ('cathedral-scene', 'refs-pillars', 'Cathedral Scene (WIP)/Group 4.png', STILL_WIDTHS, PAGE_BACKGROUND, (0, 0, 225, 585)),
    ('cathedral-scene', 'refs-windows', 'Cathedral Scene (WIP)/Group 5.png', STILL_WIDTHS, PAGE_BACKGROUND, (0, 0, 283, 220)),
    ('cathedral-scene', 'refs-framing', 'Cathedral Scene (WIP)/Group 6.png', STILL_WIDTHS, PAGE_BACKGROUND, (0, 0, 424, 221)),
    ('cathedral-scene', 'refs-textured-pillars', 'Cathedral Scene (WIP)/Group 7.png', STILL_WIDTHS, PAGE_BACKGROUND, (0, 0, 262, 349)),
    ('cathedral-scene', 'refs-sun-motif', 'Cathedral Scene (WIP)/Group 8.png', STILL_WIDTHS, PAGE_BACKGROUND, (0, 0, 642, 226)),
    ('cathedral-scene', 'refs-curves', 'Cathedral Scene (WIP)/Group 9.png', STILL_WIDTHS, PAGE_BACKGROUND, (0, 0, 516, 305)),
] + [
    ('spaceship-level', f'shot-{index:02d}', f'Spaceship Level/HighresScreenshot{index:05d}.png')
    for index in range(35)
] + [
    # Process images. The early blockout shots are cropped (left, top, right, bottom) to the screenshot itself:
    # each original sits on a white edge, shots 4-6 overlap the top of another screenshot, and several show a
    # Windows activation notice near the bottom. The sketches are cropped to the notebook page.
    # The brainstorm boards are split into their parts and trimmed, so each part is large enough to read.
    # The reference images sit on the page background instead of the board's white.
    ('spaceship-level', 'brainstorm-refs', 'Spaceship Level/Portfolio Brainstorming (1).png', STILL_WIDTHS, None, (226, 226, 2989, 1815), PAGE_BACKGROUND),
    ('spaceship-level', 'brainstorm-spaceship', 'Spaceship Level/Portfolio Brainstorming (1).png', STILL_WIDTHS, None, (707, 1860, 2507, 3796)),
    ('spaceship-level', 'brainstorm-cemetery', 'Spaceship Level/Portfolio Brainstorming (2).png', STILL_WIDTHS, None, (200, 200, 4744, 2508)),
    ('spaceship-level', 'layout-split', 'Spaceship Level/Portfolio Brainstorming (3).png', STILL_WIDTHS, None, (176, 230, 876, 970)),
    ('spaceship-level', 'layout-mix', 'Spaceship Level/Portfolio Brainstorming (3).png', STILL_WIDTHS, None, (955, 230, 1655, 970)),
    ('spaceship-level', 'layout-colosseum', 'Spaceship Level/Portfolio Brainstorming (3).png', STILL_WIDTHS, None, (1713, 230, 2413, 970)),
    ('spaceship-level', 'layout-fortress', 'Spaceship Level/Portfolio Brainstorming (3).png', STILL_WIDTHS, None, (2424, 230, 3124, 970)),
    ('spaceship-level', 'brainstorm-combined', 'Spaceship Level/Portfolio Brainstorming (4).png', STILL_WIDTHS, None, (200, 200, 4408, 2688)),
    ('spaceship-level', 'puzzle-plan', 'Spaceship Level/Group 26.png', STILL_WIDTHS, PAGE_BACKGROUND),
    ('spaceship-level', 'sketch-1', 'Spaceship Level/Sketch1.jpg', STILL_WIDTHS, None, (347, 510, 2734, 3794)),
    ('spaceship-level', 'sketch-2', 'Spaceship Level/Sketch2.jpg', STILL_WIDTHS, None, (286, 347, 2938, 3998)),
    ('spaceship-level', 'early-blockout-1', 'Spaceship Level/EarlyBlockin1.png', STILL_WIDTHS, None, (0, 0, 2366, 1205)),
    ('spaceship-level', 'early-blockout-2', 'Spaceship Level/EarlyBlockin2.png', STILL_WIDTHS, None, (0, 0, 2366, 1205)),
    ('spaceship-level', 'early-blockout-3', 'Spaceship Level/EarlyBlockin3.png', STILL_WIDTHS, None, (0, 0, 2344, 1205)),
    ('spaceship-level', 'early-blockout-4', 'Spaceship Level/EarlyBlockin4.png', STILL_WIDTHS, None, (0, 291, 2366, 1439)),
    ('spaceship-level', 'early-blockout-5', 'Spaceship Level/EarlyBlockin5.png', STILL_WIDTHS, None, (0, 291, 2366, 1325)),
    ('spaceship-level', 'early-blockout-6', 'Spaceship Level/EarlyBlockin6.png', STILL_WIDTHS, None, (0, 291, 2366, 1439)),
]

ANIMATIONS = [
    ('solace', 'spline-roots', 'Solace/Personal_Project_Dynamic_Spline_Roots.gif'),
    ('solace', 'ship-animation', 'Solace/Personal_Project_Ship_Animation.gif'),
    ('solace', 'tile-animation', 'Solace/Personal_Project_Tile_Animation.gif'),
    ('mythos-party', 'ability-ares', 'MythosParty/ARESwithparticlewEAS.gif', ABILITY_WIDTH),
    ('mythos-party', 'ability-artemis', 'MythosParty/ArtemisNewhegsss.gif', ABILITY_WIDTH),
    ('mythos-party', 'ability-bubble-bomb', 'MythosParty/BubbleBombThin!.gif', ABILITY_WIDTH),
    ('mythos-party', 'ability-link', 'MythosParty/DogCollar3.gif', ABILITY_WIDTH),
    ('mythos-party', 'ability-geyser', 'MythosParty/GyserVFX.gif', ABILITY_WIDTH),
    ('mythos-party', 'ability-hercules', 'MythosParty/HerculesDoneF.gif', ABILITY_WIDTH),
    ('mythos-party', 'ability-home-run', 'MythosParty/HomeRun.gif', ABILITY_WIDTH),
    ('mythos-party', 'ability-nyx', 'MythosParty/NyxApbea.gif', ABILITY_WIDTH),
    ('mythos-party', 'peaceful-day', 'MythosParty/PeacefuldayVol2smol.gif'),
    ('spaceship-level', 'basic-switch', 'Spaceship Level/WhiteSwitch.gif'),
    ('spaceship-level', 'pressure-switch', 'Spaceship Level/YellowSwitch.gif'),
    # These three are cropped below the editor notices ("Click for Mouse Control") in the top-left corner.
    ('spaceship-level', 'carry-cube', 'Spaceship Level/PowerOnSecondRoom.gif', ANIMATION_MAX_WIDTH, (0, 22, 770, 559)),
    ('spaceship-level', 'power-on', 'Spaceship Level/PowerOnFirstRoom.gif', ANIMATION_MAX_WIDTH, (0, 22, 770, 559)),
    ('spaceship-level', 'rising-platform', 'Spaceship Level/RisingPlatform.gif', ANIMATION_MAX_WIDTH, (0, 22, 770, 559)),
    ('spaceship-level', 'puzzle-platform', 'Spaceship Level/PuzzlePlatform.gif'),
    ('spaceship-level', 'complex-puzzle', 'Spaceship Level/ComplexPuzzleGif.gif'),
]


def resized(image, width):
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.LANCZOS)


def save_still(folder, name, source, step_widths=STILL_WIDTHS, matte=None, crop=None, fill=None):
    image = Image.open(CONTENT / source)
    if crop:
        image = image.crop(crop)
    if fill:
        # Repaint the white background that reaches the edges, leaving white inside the pictures alone.
        image = image.convert('RGB')
        ImageDraw.floodfill(image, (0, 0), fill, thresh=40)
    if matte:
        image = image.convert('RGBA')
        background = Image.new('RGBA', image.size, matte + (255,))
        background.alpha_composite(image)
        image = background
    image = image.convert('RGB')
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


def save_animation(folder, name, source, max_width=ANIMATION_MAX_WIDTH, crop=None):
    animation = Image.open(CONTENT / source)
    width = min(crop[2] - crop[0] if crop else animation.width, max_width)
    frames, durations = [], []
    for frame in ImageSequence.Iterator(animation):
        durations.append(frame.info.get('duration', 70))
        frame = frame.convert('RGB')
        if crop:
            frame = frame.crop(crop)
        frames.append(resized(frame, width))

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
    ('mythos-party', 'MythosParty/Mythos_Party_Capsule_Art_Revised.png'),
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
    for animation in ANIMATIONS:
        save_animation(*animation)
    for name, source in PREVIEWS:
        save_preview(name, source)


if __name__ == '__main__':
    main()
