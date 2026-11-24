#!/usr/bin/env python3
"""news-23 b167 numbers-led: THE WORLD TODAY, Monday 23 November 2026 (31 stories).
Draws entry.png 1024x1024 with PIL. Layout: big number grid first, then
masthead, region bar, 3 hero scenes, 10 cards, map + ALSO, DATE CHECK, footer.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16  # margin

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(d, x, y, text, fill, fg="white"):
    """Small status chip; returns width used."""
    font = f(BOLD, 9)
    w_ = int(d.textlength(text, font=font)) + 10
    d.rounded_rectangle([x, y, x + w_, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), text, font=font, fill=fg)
    return w_


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    ink = (17, 17, 17)
    grey = (90, 90, 90)
    navy = (16, 34, 64)
    red = (178, 34, 34)
    gold = (198, 154, 30)

    # ---------- NUMBER GRID (top, 2 rows x 5) ----------
    numbers = [
        ("-3.3%", "KOSPI"),
        ("5.3", "US-CHINA GAP"),
        ("11,762", "EBOLA CASES DRC"),
        ("10T won", "SEOUL FUND"),
        ("2%", "BILLIONAIRE TAX"),
        ("$450M", "SKUBAL METS"),
        ("165", "MISSILES / WEEK"),
        ("12,000", "CLEARED MANCHESTER"),
        ("264 kg", "EXPLOSIVES LEBANON"),
        ("$107.3B", "ANTHROPIC IPO"),
    ]
    gx0, gy0 = M, 8
    cw = (W - 2 * M - 4 * 6) // 5
    ch = 58
    for i, (val, lab) in enumerate(numbers):
        r, c = divmod(i, 5)
        x = gx0 + c * (cw + 6)
        y = gy0 + r * (ch + 6)
        d.rectangle([x, y, x + cw, y + ch], fill=navy)
        vf = f(BOLD, 24)
        lf = f(BOLD, 10)
        vw = d.textlength(val, font=vf)
        d.text((x + (cw - vw) / 2, y + 6), val, font=vf, fill="white")
        lab_lines = wrap(d, lab, lf, cw - 10)
        ly = y + 34
        for ln in lab_lines[:2]:
            lw = d.textlength(ln, font=lf)
            d.text((x + (cw - lw) / 2, ly), ln, font=lf, fill=(200, 210, 230))
            ly += 11

    # ---------- MASTHEAD ----------
    y = 140
    tf = f(BOLD, 34)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=tf)) / 2, y), t, font=tf, fill=ink)
    y = 178
    sf = f(BOLD, 13)
    s = "MONDAY 23 NOVEMBER 2026"
    d.text(((W - d.textlength(s, font=sf)) / 2, y), s, font=sf, fill=red)
    y = 198
    kf = f(REG, 12)
    k = "AI rout hits Asia as Guterres urges AI rules — and America's lead over China hits a record low."
    d.text(((W - d.textlength(k, font=kf)) / 2, y), k, font=kf, fill=grey)

    # ---------- REGION BAR ----------
    y = 216
    d.rectangle([M, y, W - M, y + 22], fill=(240, 240, 240))
    rf = f(BOLD, 11)
    rtxt = "ASIA-PACIFIC 7   ·   AMERICAS 8   ·   MIDDLE EAST 6   ·   EUROPE 5   ·   AFRICA 3   ·   WORLD 2   —   31 STORIES"
    d.text(((W - d.textlength(rtxt, font=rf)) / 2, y + 5), rtxt, font=rf, fill=ink)

    # ---------- HEROES ----------
    hy = 246
    hw = (W - 2 * M - 2 * 8) // 3
    hh = 208
    heroes = [
        {
            "tag": "MARKETS",
            "scene": "kospi",
            "head": "AI ROUT HITS ASIA",
            "body": "Kospi -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
            "src": "SEOUL",
        },
        {
            "tag": "AI SUMMIT",
            "scene": "guterres",
            "head": "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
            "body": "Bridgetown summit: 150 delegates back a risk framework. A blueprint, not a treaty.",
            "src": "BARBADOS",
        },
        {
            "tag": "POWER INDEX",
            "scene": "bars",
            "head": "US LEAD OVER CHINA AT RECORD LOW",
            "body": "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India 3rd, 40.5.",
            "src": "SINGAPORE",
        },
    ]
    for i, hero in enumerate(heroes):
        x = M + i * (hw + 8)
        d.rectangle([x, hy, x + hw, hy + hh], outline=(200, 200, 200))
        # tag strip
        d.rectangle([x, hy, x + hw, hy + 20], fill=ink)
        d.text((x + 8, hy + 4), hero["tag"], font=f(BOLD, 11), fill="white")
        sy = hy + 20
        sh = 96
        if hero["scene"] == "kospi":
            d.rectangle([x, sy, x + hw, sy + sh], fill=(10, 22, 44))
            # skyline
            import random

            rnd = random.Random(7)
            bx = x + 6
            while bx < x + hw - 14:
                bw = rnd.randint(16, 30)
                bh = rnd.randint(28, 52)
                d.rectangle([bx, sy + sh - bh, bx + bw, sy + sh], fill=(30, 52, 92))
                for wy in range(sy + sh - bh + 5, sy + sh - 4, 9):
                    for wx in range(bx + 4, bx + bw - 3, 8):
                        d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
                bx += bw + 4
            # descending chart line
            pts = []
            for j in range(9):
                px = x + 14 + j * (hw - 28) / 8
                py = sy + 14 + j * (sh - 30) / 8 + (j % 2) * 3
                pts.append((px, py))
            d.line(pts, fill=(255, 120, 40), width=3)
            d.text((x + hw - 62, sy + 8), "-3.3%", font=f(BOLD, 16), fill=(255, 120, 40))
        elif hero["scene"] == "guterres":
            d.rectangle([x, sy, x + hw, sy + sh], fill=(12, 44, 66))
            cx, cy, cr = x + hw // 2, sy + sh // 2 + 6, 34
            d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(46, 130, 170), outline=(140, 200, 230), width=2)
            d.ellipse([cx - cr // 2, cy - cr, cx + cr // 2, cy + cr], outline=(140, 200, 230), width=1)
            d.line([cx - cr, cy, cx + cr, cy], fill=(140, 200, 230), width=1)
            d.line([cx - cr + 8, cy - 16, cx + cr - 8, cy - 16], fill=(140, 200, 230), width=1)
            d.line([cx - cr + 8, cy + 16, cx + cr - 8, cy + 16], fill=(140, 200, 230), width=1)
            d.text((x + 10, sy + 6), "BRIDGETOWN", font=f(BOLD, 12), fill=gold)
            d.text((x + 10, sy + 22), "SUMMIT", font=f(BOLD, 12), fill=gold)
            # small flags bottom-right
            for j, col in enumerate([(200, 40, 40), (40, 90, 200), (240, 200, 40), (40, 160, 80)]):
                fx = x + hw - 66 + j * 15
                d.rectangle([fx, sy + sh - 18, fx + 12, sy + sh - 8], fill=col)
        else:  # bars
            d.rectangle([x, sy, x + hw, sy + sh], fill=(245, 245, 245))
            bars = [("US", 78.9, navy), ("CHINA", 73.6, (178, 34, 34)), ("INDIA", 40.5, gold)]
            by = sy + 12
            for name, val, col in bars:
                d.text((x + 10, by), name, font=f(BOLD, 11), fill=ink)
                d.rectangle([x + 74, by + 2, x + 74 + (hw - 120) * val / 85.0, by + 14], fill=col)
                d.text((x + 78 + (hw - 120) * val / 85.0, by), f"{val}", font=f(BOLD, 11), fill=ink)
                by += 24
            d.text((x + 10, sy + sh - 18), "US DIPLOMATIC INFLUENCE -6 TO 76.7", font=f(BOLD, 9), fill=grey)
        # headline below scene, clear of the strip
        hyy = sy + sh + 8
        hf = f(BOLD, 14)
        hl = wrap(d, hero["head"], hf, hw - 16)
        hyy = draw_lines(d, hl[:2], x + 8, hyy, hf, ink, 17)
        bf = f(REG, 10)
        bl = wrap(d, hero["body"], bf, hw - 16)
        hyy = draw_lines(d, bl[:2], x + 8, hyy + 2, bf, grey, 12)
        d.text((x + 8, hy + hh - 18), hero["src"], font=f(BOLD, 9), fill=grey)
        chip(d, x + hw - 66, hy + hh - 19, "REPORTED", (34, 120, 60))

    # ---------- CARDS (2 rows x 5) ----------
    cards = [
        ("BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief presses chipmaker over China sales.", "REUTERS", "REPORTED"),
        ("FBI PROBES NCIC POLICE-DATABASE HACK", "Agents investigate a breach of the crime database.", "WASHINGTON", "REPORTED"),
        ("TRUMP: IRAN STRIKES MAY RESUME IN NEW YEAR", "President warns of renewed action if talks fail.", "WASHINGTON", "REPORTED"),
        ("NASDAQ FUTURES +3% IN HOLIDAY WEEK", "US stocks set for a calm Thanksgiving week.", "NEW YORK", "REPORTED"),
        ("SKUBAL SIGNS $450M METS DEAL", "Two-time Cy Young winner, nine years — the largest ever for a pitcher.", "NEW YORK", "REPORTED"),
        ("TOM JACKSON DIES AT 75", "The former NFL star and broadcaster is mourned.", "DENVER", "REPORTED"),
        ("STATES SUE SPACEX OVER AI SAFETY CLAIMS", "Attorneys general challenge its safety pledges.", "CALIFORNIA", "REPORTED"),
        ("ANTHROPIC IPO: $107.3B AT $83 A SHARE", "Shares debut at $97.17 after pricing on 19 Nov.", "NEW YORK", "REPORTED"),
        ("POLAND: 3 RUSSIAN KH-101 MISSILES CROSSED AIRSPACE", "Warsaw says the missiles entered its skies.", "WARSAW", "CLAIM"),
        ("INTEL WARNS OF RUSSIAN NUCLEAR SATELLITE", "Agencies flag a possible orbital weapon.", "WASHINGTON", "CLAIM"),
    ]
    cy0 = 466
    ccw = (W - 2 * M - 4 * 6) // 5
    cch = 76
    for i, (head, body, src, status) in enumerate(cards):
        r, c = divmod(i, 5)
        x = M + c * (ccw + 6)
        y = cy0 + r * (cch + 6)
        d.rectangle([x, y, x + ccw, y + cch], outline=(200, 200, 200))
        hf = f(BOLD, 10)
        hl = wrap(d, head, hf, ccw - 12)
        yy = draw_lines(d, hl[:2], x + 6, y + 5, hf, ink, 12)
        bf = f(REG, 9)
        bl = wrap(d, body, bf, ccw - 12)
        draw_lines(d, bl[:2], x + 6, yy + 1, bf, grey, 11)
        d.text((x + 6, y + cch - 17), src, font=f(BOLD, 8), fill=grey)
        chip(d, x + ccw - 62, y + cch - 18, status, (34, 120, 60) if status == "REPORTED" else red)

    # ---------- MAP + ALSO ----------
    my = 630
    mh = 238
    # map panel
    mx = M
    mw = 480
    d.rectangle([mx, my, mx + mw, my + mh], outline=(200, 200, 200))
    d.rectangle([mx, my, mx + mw, my + 20], fill=ink)
    d.text((mx + 8, my + 4), "WHERE IT HAPPENED", font=f(BOLD, 11), fill="white")
    # stylised continents
    d.ellipse([mx + 20, my + 60, mx + 150, my + 150], fill=(222, 232, 222))   # N America
    d.ellipse([mx + 60, my + 150, mx + 130, my + 210], fill=(222, 232, 222))  # S America
    d.ellipse([mx + 200, my + 50, mx + 330, my + 140], fill=(222, 232, 222))  # Eurasia
    d.ellipse([mx + 230, my + 140, mx + 300, my + 200], fill=(222, 232, 222)) # Africa
    d.ellipse([mx + 340, my + 140, mx + 420, my + 200], fill=(222, 232, 222)) # SE Asia / Oceania
    pins = [
        (1, 324, 106), (2, 92, 168), (3, 66, 92), (4, 306, 82), (5, 292, 118),
        (6, 222, 74), (7, 192, 56), (8, 180, 80), (9, 258, 62), (10, 282, 76),
        (11, 250, 104), (12, 272, 130), (13, 252, 168),
    ]
    pf = f(BOLD, 9)
    for n, px, py in pins:
        ax, ay = mx + px, my + py
        d.ellipse([ax - 8, ay - 8, ax + 8, ay + 8], fill=red, outline="white", width=1)
        tw = d.textlength(str(n), font=pf)
        d.text((ax - tw / 2, ay - 6), str(n), font=pf, fill="white")
    d.text((mx + 8, my + mh - 18), "1 SEOUL  2 BRIDGETOWN  3 WASHINGTON  4 BEIJING  5 NEW DELHI", font=f(REG, 8), fill=grey)
    d.text((mx + 8, my + mh - 8), "6 PARIS  7 LONDON  8 MANCHESTER  9 WARSAW  10 KYIV  11 GAZA  12 BAHRAIN  13 KINSHASA", font=f(REG, 8), fill=grey)

    # ALSO panel
    ax0 = mx + mw + 8
    aw = W - M - ax0
    d.rectangle([ax0, my, ax0 + aw, my + mh], outline=(200, 200, 200))
    d.rectangle([ax0, my, ax0 + aw, my + 20], fill=ink)
    d.text((ax0 + 8, my + 4), "ALSO ON MONDAY", font=f(BOLD, 11), fill="white")
    also = [
        "Paris 100+ back 2% billionaire tax",
        "Manchester: 12,000 cleared",
        "Zelenskyy: 165 Russian missiles in a week",
        "COP31: the day after Antalya pact rejected",
        "Israel unity talks resume",
        "Gaza: two killed in Israeli strike",
        "West Bank settler attacks",
        "Iran war: no deal in sight",
        "Lebanon seizes 264 kg explosives",
        "Bahrain Sat: Iranian strike hits plant, 2 hurt",
        "Benghazi: UN demands probe [CLAIM]",
        "Sudan: defences down drones [CLAIM]",
        "DRC: fighting traps Ebola teams",
        "Bangladesh: Hasina jailed if she returns",
        "Seoul minister quits over AI exam chaos",
        "SK Telecom -7.3%",
        "China eases margin rules, cuts to 80%",
        "Seoul readies 10T-won stabilisation fund",
    ]
    af = f(REG, 10)
    col_w = (aw - 24) // 2
    for i, item in enumerate(also):
        col, row = divmod(i, 9)
        x = ax0 + 8 + col * (col_w + 8)
        y = my + 26 + row * 23
        lines = wrap(d, f"{i+1}. {item}", af, col_w)
        draw_lines(d, lines[:2], x, y, af, ink, 12)

    # ---------- DATE CHECK ----------
    dy = 880
    dh = 108
    d.rectangle([M, dy, W - M, dy + dh], fill=(255, 238, 238), outline=red, width=2)
    d.text((M + 10, dy + 6), "DATE CHECK — LEFT OUT (NOT 23 NOV)", font=f(BOLD, 11), fill=red)
    left = [
        "Democrats reach 258 (22 Nov)",
        "Sparta II fire (22 Nov)",
        "El Chapo Isidro captured (22 Nov)",
        "EU-Indonesia pact (21 Nov)",
        "Nigeria boat (21 Nov)",
        "ICJ Myanmar ruling (19 Nov)",
    ]
    lf = f(REG, 10)
    for i, item in enumerate(left):
        col, row = divmod(i, 3)
        x = M + 10 + col * 320
        y = dy + 26 + row * 18
        d.text((x, y), f"✕ {item}", font=lf, fill=ink)
    d.text((M + 10, dy + 82), "NOT YET:  Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff", font=lf, fill=ink)

    # ---------- FOOTER ----------
    fy = 996
    ff = f(REG, 9)
    d.text((M, fy), "SOURCES: WIRES / AGENCIES  ·  REPORTED = confirmed by wires   CLAIM = one side's claim   ~ APPROX", font=ff, fill=grey)
    d.text((W - M - d.textlength("THE WORLD TODAY — 23 NOV 2026", font=ff), fy), "THE WORLD TODAY — 23 NOV 2026", font=ff, fill=grey)

    img.save("entry.png")


if __name__ == "__main__":
    main()
