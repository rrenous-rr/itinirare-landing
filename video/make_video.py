import subprocess, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG  = os.path.join(ROOT, "images")
OUT  = os.path.dirname(os.path.abspath(__file__))
FONT = "C\\:/Windows/Fonts/arialbd.ttf"
FONT_LIGHT = "C\\:/Windows/Fonts/arial.ttf"
W, H = 1080, 1920
FPS  = 30
BG   = "0x0d0d14"   # very dark navy — feels premium

os.makedirs(OUT, exist_ok=True)

# ── Scenes ──────────────────────────────────────────────────────────────────
# (type, image, duration_s, line1, line2)
scenes = [
    ("black", None,                         3.5, "You just booked a trip.",        ""),
    ("img",   "screenshot-emaillist.png",   5.5, "Confirmation emails.",           "Everywhere."),
    ("img",   "screenshot-emailconfirm.png",5.5, "Just forward it to Itinirare.", ""),
    ("img",   "screenshot-triplist.png",    6.0, "Your itinerary builds itself.",  ""),
    ("img",   "screenshot-firsttrip.png",   6.0, "Every booking. Every detail.",   ""),
    ("img",   "screenshot-multitrip.png",   5.0, "All your trips. One place.",     ""),
    ("img",   "screenshot-multiusers.png",  5.0, "Travel together.",               "Stay in sync."),
    ("img",   "screenshot-triptips.png",    5.0, "Smart tips for every day.",      ""),
    ("img",   "screenshot-suggestions.png", 5.0, "Restaurants. Activities.",       "Hidden gems."),
    ("img",   "screenshot-sharing.png",     5.5, "Share with anyone.",             "No login needed."),
    ("black", None,                         5.5, "Forward booking emails.",        "Your itinerary builds itself."),
]

FADE = 0.35   # fade in / fade out duration per clip

def esc(t):
    """Escape text for FFmpeg drawtext."""
    return t.replace("'", "\\'").replace(":", "\\:").replace(",", "\\,")

def text_filter(line1, line2, style="caption"):
    """Build drawtext vf fragment."""
    fs1 = 70 if style == "caption" else 78
    fs2 = 62 if style == "caption" else 68
    col1 = "white"
    col2 = "0xf59e0b"   # amber — matches the website highlight colour

    if style == "caption":
        # bottom-anchored caption bar
        y1 = "h-290" if line2 else "h-240"
        y2 = "h-200"
        base = (
            f"drawtext=fontfile='{FONT}':text='{esc(line1)}':"
            f"fontcolor={col1}:fontsize={fs1}:x=(w-tw)/2:y={y1}:"
            f"box=1:boxcolor=black@0.72:boxborderw=22"
        )
        if line2:
            base += (
                f",drawtext=fontfile='{FONT}':text='{esc(line2)}':"
                f"fontcolor={col1}:fontsize={fs2}:x=(w-tw)/2:y={y2}:"
                f"box=1:boxcolor=black@0.72:boxborderw=18"
            )
    else:
        # centred hero text (black slides)
        cy = "h/2-80" if line2 else "h/2-40"
        base = (
            f"drawtext=fontfile='{FONT}':text='{esc(line1)}':"
            f"fontcolor={col1}:fontsize={fs1}:x=(w-tw)/2:y={cy}:box=0"
        )
        if line2:
            base += (
                f",drawtext=fontfile='{FONT}':text='{esc(line2)}':"
                f"fontcolor={col2}:fontsize={fs2}:x=(w-tw)/2:y=h/2+20:box=0"
            )
    return base


def make_clip(i, stype, img, dur, line1, line2):
    out = f"{OUT}/clip_{i:02d}.mp4"

    # Scale image to fit portrait canvas — scale by height, pad sides
    img_scale = (
        f"scale=-2:{H},"
        f"pad={W}:{H}:(ow-iw)/2:0:color={BG}"
    )
    # Fade in / out
    n_frames = int(dur * FPS)
    fade_n   = int(FADE * FPS)
    fade_vf  = (
        f"fade=t=in:st=0:nb_frames={fade_n},"
        f"fade=t=out:st={dur - FADE:.3f}:nb_frames={fade_n}"
    )

    if stype == "black":
        vf = f"{text_filter(line1, line2, 'hero')},{fade_vf}"
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={BG}:size={W}x{H}:rate={FPS}",
            "-vf", vf,
            "-t", str(dur), "-c:v", "libx264", "-preset", "fast",
            "-pix_fmt", "yuv420p", "-an", out,
        ]
    else:
        vf = f"{img_scale},{text_filter(line1, line2, 'caption')},{fade_vf}"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-framerate", str(FPS), "-i", f"{IMG}/{img}",
            "-vf", vf,
            "-t", str(dur), "-r", str(FPS),
            "-c:v", "libx264", "-preset", "fast",
            "-pix_fmt", "yuv420p", "-an", out,
        ]

    print(f"  Clip {i:02d}: {line1}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("STDERR:", r.stderr[-800:])
        sys.exit(1)
    return out


# ── Generate clips ───────────────────────────────────────────────────────────
print("=== Generating clips ===")
clips = []
for i, (stype, img, dur, l1, l2) in enumerate(scenes):
    clips.append(make_clip(i, stype, img, dur, l1, l2))

# ── Concat list ──────────────────────────────────────────────────────────────
concat_txt = f"{OUT}/concat.txt"
with open(concat_txt, "w") as f:
    for c in clips:
        f.write(f"file '{c}'\n")

# ── Final concat ─────────────────────────────────────────────────────────────
final = f"{OUT}/itinirare-demo.mp4"
print("=== Concatenating ===")
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_txt,
    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-pix_fmt", "yuv420p", "-an",
    final,
]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("STDERR:", r.stderr[-800:])
    sys.exit(1)

print(f"\n✅ Done: {final}")
size_mb = os.path.getsize(final) / 1_000_000
print(f"   Size: {size_mb:.1f} MB")
