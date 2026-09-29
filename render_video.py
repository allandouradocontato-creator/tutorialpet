import subprocess, math, sys, json, os, wave
CFG = {}
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
CREAM = (250, 241, 226)
TERRA = (196, 98, 62)
TERRA_D = (150, 66, 40)
BROWN = (74, 44, 32)
SAND = (238, 220, 192)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
fbig = ImageFont.truetype(FB, 88)
fmid = ImageFont.truetype(FB, 64)
fsmall = ImageFont.truetype(FB, 40)
fnum = ImageFont.truetype(FB, 120)

def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def paw(d, cx, cy, s, color):
    d.ellipse([cx - 0.55 * s, cy - 0.05 * s, cx + 0.55 * s, cy + 0.75 * s], fill=color)
    for dx, dy, r in [(-0.75, -0.35, 0.26), (-0.28, -0.8, 0.28), (0.28, -0.8, 0.28), (0.75, -0.35, 0.26)]:
        d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s], fill=color)


def bone(d, cx, cy, s, color, ang=0):
    pts = []
    # simple horizontal bone
    d.rounded_rectangle([cx - 0.7 * s, cy - 0.15 * s, cx + 0.7 * s, cy + 0.15 * s], radius=int(0.1 * s), fill=color)
    for sx in (-1, 1):
        for sy in (-1, 1):
            d.ellipse([cx + sx * 0.7 * s - 0.22 * s + sx * 0.12 * s, cy + sy * 0.17 * s - 0.22 * s,
                       cx + sx * 0.7 * s + 0.22 * s + sx * 0.12 * s, cy + sy * 0.17 * s + 0.22 * s], fill=color)


def ball(d, cx, cy, s, color, line):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=color)
    d.arc([cx - s * 0.7, cy - s * 1.3, cx + s * 1.3, cy + s * 0.7], 110, 250, fill=line, width=int(s * 0.12))
    d.arc([cx - s * 1.3, cy - s * 0.7, cx + s * 0.7, cy + s * 1.3], -70, 70, fill=line, width=int(s * 0.12))


def bg(d, t):
    d.rectangle([0, 0, W, H], fill=CREAM)
    # soft drifting circles
    for i, (x, y, r) in enumerate([(120, 260, 230), (980, 1500, 300), (900, 300, 140)]):
        off = math.sin(t * 0.8 + i) * 18
        d.ellipse([x - r, y - r + off, x + r, y + r + off], fill=SAND)
    # decorative paws
    for i, (x, y, s) in enumerate([(160, 1650, 34), (930, 520, 26), (250, 860, 22)]):
        paw(d, x, y + math.sin(t + i) * 8, s, (232, 205, 172))


def text_block(img, d, lines, y0, t_local, font, color, lh):
    for i, ln in enumerate(lines):
        a = ease((t_local - 0.25 - i * 0.18) / 0.4)
        if a <= 0:
            continue
        bbox = d.textbbox((0, 0), ln, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        y = y0 + i * lh + int((1 - a) * 40)
        layer = Image.new("RGBA", (tw + 40, lh + 40), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((20, 10), ln, font=font, fill=color + (int(255 * a),))
        img.paste(layer, (x - 20, y - 10), layer)


def frame(fi):
    t = fi / FPS
    SCENES = CFG['scenes']; TOTAL = CFG['total']
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    bg(d, t)
    sc = next(s for s in SCENES if s[0] <= t < s[1]) if t < TOTAL else SCENES[-1]
    st, en, kind, badge, lines = sc
    tl = t - st
    # progress bar
    d.rounded_rectangle([60, 70, W - 60, 90], radius=10, fill=SAND)
    d.rounded_rectangle([60, 70, 60 + int((W - 120) * t / TOTAL), 90], radius=10, fill=TERRA)

    if kind == "hook":
        s = 150 * ease(tl / 0.5)
        paw(d, W // 2, 420, s, TERRA)
        text_block(img, d, lines[:2], 720, tl, fbig, BROWN, 120)
        text_block(img, d, lines[2:], 1010, tl - 0.5, fmid, TERRA_D, 92)
        ball(d, 260, 1500, 70 * ease((tl - 0.8) / 0.4), TERRA, CREAM)
        bone(d, 800, 1500, 100 * ease((tl - 1.0) / 0.4), (216, 170, 120))
    elif kind == "point":
        r = 130 * ease(tl / 0.4)
        d.ellipse([W // 2 - r, 330 - r, W // 2 + r, 330 + r], fill=TERRA)
        nb = d.textbbox((0, 0), badge, font=fnum)
        d.text((W // 2 - (nb[2] - nb[0]) // 2, 330 - (nb[3] - nb[1]) // 2 - nb[1]), badge, font=fnum, fill=CREAM)
        text_block(img, d, lines[:2], 600, tl, fbig, BROWN, 120)
        text_block(img, d, lines[2:], 900, tl - 0.4, fmid, TERRA_D, 92)
        if badge == "1":
            ball(d, W // 2, 1400, 120 * ease((tl - 0.5) / 0.4), TERRA, CREAM)
        elif badge == "2":
            bone(d, W // 2 - 220, 1400, 110 * ease((tl - 0.5) / 0.4), (216, 170, 120))
            ball(d, W // 2 + 220, 1400, 80 * ease((tl - 0.7) / 0.4), TERRA, CREAM)
        else:
            paw(d, W // 2, 1380, 110 * ease((tl - 0.5) / 0.4), TERRA)
    else:  # end
        d.rounded_rectangle([90, 420, W - 90, 1420], radius=60, fill=SAND)
        paw(d, W // 2, 640, 130 * ease(tl / 0.5), TERRA)
        text_block(img, d, lines[:2], 860, tl - 0.2, fbig, BROWN, 120)
        text_block(img, d, lines[2:], 1110, tl - 0.6, fbig, TERRA, 120)
        u = "tutorialpet.com.br"
        a = ease((tl - 1.0) / 0.4)
        ub = d.textbbox((0, 0), u, font=fsmall)
        col = tuple(int(CREAM[i] + (TERRA_D[i] - CREAM[i]) * a) for i in range(3))
        d.text(((W - (ub[2] - ub[0])) // 2, 1530), u, font=fsmall, fill=col)
    # watermark
    wm = "@tutorialpet"
    wb = d.textbbox((0, 0), wm, font=fsmall)
    d.text((W - (wb[2] - wb[0]) - 60, H - 130), wm, font=fsmall, fill=(160, 120, 96))
    # fade in/out
    if t < 0.3:
        img = Image.blend(Image.new("RGB", (W, H), CREAM), img, t / 0.3)
    return img



def wav_len(p):
    with wave.open(p) as w:
        return w.getnframes() / w.getframerate()


def render(spec_path, out, voz="pf_dora"):
    """spec.json: {"scenes":[{"kind":"hook|point|end","badge":"1","lines":[..],"fala":"texto narrado"}]}
    Duração de cada cena = duração da narração + respiro (mín. 3s). Sem 'fala' -> 3.2s mudo."""
    spec = json.load(open(spec_path, encoding="utf-8"))
    tmp = os.path.splitext(out)[0] + "_tmp"
    os.makedirs(tmp, exist_ok=True)
    narrar = None
    if any(sc.get("fala") for sc in spec["scenes"]):
        from voz import narrar
    t = 0.0
    scenes, wavs = [], []
    for i, sc in enumerate(spec["scenes"]):
        dur, wp = 3.2, None
        if narrar and sc.get("fala"):
            wp = os.path.join(tmp, f"s{i}.wav")
            dur = max(3.2, narrar(sc["fala"], wp, voz=voz) + 0.7)
        scenes.append((t, t + dur, sc["kind"], sc.get("badge"), sc["lines"]))
        wavs.append((t + 0.15, wp))
        t += dur
    CFG["scenes"], CFG["total"] = scenes, t
    audio = None
    if any(w for _, w in wavs):
        import numpy as np
        SRA = 24000
        buf = np.zeros(int(t * SRA) + SRA, dtype=np.float32)
        for st, wp in wavs:
            if not wp: continue
            with wave.open(wp) as w:
                x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32767
            o = int(st * SRA); buf[o:o + len(x)] += x
        audio = os.path.join(tmp, "narracao.wav")
        pcm = (np.clip(buf[:int(t * SRA)], -1, 1) * 32767).astype("<i2")
        with wave.open(audio, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SRA); w.writeframes(pcm.tobytes())
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-"]
    cmd += ["-i", audio] if audio else ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    cmd += ["-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(t * FPS)):
        p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait()
    return t


if __name__ == "__main__":
    print("duração:", render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "pf_dora"))
