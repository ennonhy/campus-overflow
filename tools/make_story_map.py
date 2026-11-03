# -*- coding: utf-8 -*-
"""Draw the CampusOverflow user story map (Lab 2 deliverable 1)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1400
BG = (247, 249, 252)
INK = (33, 41, 54)
MUTED = (110, 122, 138)
DEEP = (31, 56, 100)
ACT = (46, 83, 149)

P0 = (214, 69, 30)     # 必修 / MVP
P1 = (30, 136, 229)    # 次要
P2 = (120, 144, 156)   # 未来
BAND = [(255, 243, 224), (232, 241, 251), (241, 243, 245)]

FONT_DIR = r'C:\Windows\Fonts'
def f(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_TITLE = f('msyhbd.ttc', 54)
F_SUB = f('msyh.ttc', 26)
F_ACT = f('msyhbd.ttc', 34)
F_ACT2 = f('msyh.ttc', 20)
F_BAND = f('msyhbd.ttc', 26)
F_ID = f('msyhbd.ttc', 19)
F_CARD = f('msyhbd.ttc', 23)
F_SP = f('msyhbd.ttc', 18)
F_NOTE = f('msyh.ttc', 21)

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

MARGIN = 48
# ---------------- header ----------------
d.rectangle([0, 0, W, 132], fill=DEEP)
d.text((MARGIN, 26), 'CampusOverflow 用户故事地图', font=F_TITLE, fill=(255, 255, 255))
d.text((MARGIN + 2, 92), '需求建模工作坊 · Lab 2 · Sprint 1 · 横轴＝用户活动序列，纵轴＝故事卡片，横切线＝发布批次',
       font=F_SUB, fill=(196, 212, 240))
d.text((W - MARGIN - 12, 40), 'v1.0', font=f('msyhbd.ttc', 40), fill=(255, 255, 255), anchor='ra')
d.text((W - MARGIN - 12, 94), '第 3 组 · 第 3 周', font=F_SUB, fill=(196, 212, 240), anchor='ra')

# ---------------- activity columns ----------------
ACT_H = 96
ACT_Y = 156
COL_W = (W - 2 * MARGIN) // 6
GAP = 8

activities = [
    ('① 注册', 'Sign up'), ('② 浏览', 'Discover'), ('③ 提问', 'Ask'),
    ('④ 回答', 'Answer'), ('⑤ 互动', 'Engage'), ('⑥ 成长', 'Grow'),
]

col_x = [MARGIN + i * COL_W for i in range(6)]
for i, (name, en) in enumerate(activities):
    x0 = col_x[i] + GAP // 2
    x1 = col_x[i] + COL_W - GAP // 2
    d.rounded_rectangle([x0, ACT_Y, x1, ACT_Y + ACT_H], radius=10, fill=ACT)
    d.text(((x0 + x1) / 2, ACT_Y + 12), name, font=F_ACT, fill=(255, 255, 255), anchor='ma')
    d.text(((x0 + x1) / 2, ACT_Y + 56), en, font=F_ACT2, fill=(186, 205, 236), anchor='ma')

# ---------------- story cards ----------------
R1 = {
    0: [('US-01', '邮箱注册与账号验证', 5, 0), ('US-02', '登录 / 登出 / 会话保持', 3, 0)],
    1: [('US-03', '问题列表（分页 + 最新排序）', 3, 0)],
    2: [('US-04', '发布问题（Markdown 预览）', 8, 0)],
    3: [('US-05', '问题详情页', 3, 0), ('US-06', '提交回答', 5, 0)],
    4: [],
    5: [],
}
R2 = {
    0: [('US-20', '第三方登录', 5, 2)],
    1: [('US-13', '关键词搜索', 5, 1)],
    2: [('US-10', '标签体系', 5, 1), ('US-15', '编辑 / 删除内容', 3, 1)],
    3: [('US-08', '采纳最佳答案', 5, 0)],
    4: [('US-07', '投票（赞 / 踩）', 5, 0), ('US-09', '评论', 3, 1), ('US-14', '通知中心', 5, 1)],
    5: [('US-11', '声誉积分累计与展示', 8, 0), ('US-12', '事件驱动声誉（跨模块）', 5, 1)],
}
R3 = {
    0: [('US-16', '个人主页', 3, 1)],
    1: [('US-21', '热门 / 未回答筛选', 2, 2), ('US-19', '举报与内容治理', 8, 2)],
    2: [('US-22', '草稿自动保存', 3, 2)],
    3: [('US-23', '@提及 用户', 3, 2)],
    4: [('US-24', '后台内容审核', 8, 2)],
    5: [('US-17', '徽章与等级', 5, 2), ('US-18', '贡献排行榜', 8, 2)],
}

CARD_H = 88
CARD_GAP = 16
PRIO_COLOR = [P0, P1, P2]
PRIO_NAME = ['P0 必修（MVP）', 'P1 次要', 'P2 未来']

def wrap(text, font, maxw):
    lines, cur = [], ''
    for ch in text:
        if d.textlength(cur + ch, font=font) <= maxw:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines

def band(y0, h, idx, label, sub):
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + h], fill=BAND[idx], outline=(214, 220, 228))
    d.rectangle([MARGIN, y0, MARGIN + 10, y0 + h], fill=(158, 170, 186))
    d.text((MARGIN + 26, y0 + 12), label, font=F_BAND, fill=(60, 72, 88))
    d.text((MARGIN + 26 + d.textlength(label, font=F_BAND) + 14, y0 + 16), sub, font=F_NOTE, fill=MUTED)

def draw_cards(data, y0, empty_note=False):
    for c, cards in data.items():
        x0 = col_x[c] + GAP // 2 + 12
        x1 = col_x[c] + COL_W - GAP // 2 - 12
        if not cards:
            if empty_note:
                d.rounded_rectangle([x0, y0 + 68, x1, y0 + 68 + CARD_H], radius=10,
                                    outline=(206, 212, 220), width=2)
                d.text(((x0 + x1) / 2, y0 + 68 + CARD_H / 2), '本批不切', font=F_CARD,
                       fill=(172, 180, 192), anchor='mm')
            continue
        for r, (uid, title, sp, prio) in enumerate(cards):
            ty = y0 + 64 + r * (CARD_H + CARD_GAP)
            col = PRIO_COLOR[prio]
            d.rounded_rectangle([x0, ty, x1, ty + CARD_H], radius=10, fill=col,
                                outline=(255, 255, 255), width=3)
            d.text((x0 + 14, ty + 8), uid, font=F_ID, fill=(255, 255, 255))
            lines = wrap(title, F_CARD, x1 - x0 - 28)[:2]
            for i, ln in enumerate(lines):
                d.text((x0 + 14, ty + 32 + i * 28), ln, font=F_CARD, fill=(255, 255, 255))
            d.text((x1 - 12, ty + CARD_H - 22), f'{sp} SP', font=F_SP, fill=(255, 255, 255), anchor='ra')

Y1 = ACT_Y + ACT_H + 14
H1 = 350
band(Y1, H1, 0, 'Release 1 · MVP 走骨架（Walking Skeleton）', '—— 注册 → 浏览 → 提问 → 详情；Sprint 1 承诺其中 22 SP（US-01~05），US-06 为 Stretch')
draw_cards(R1, Y1, empty_note=True)

Y2 = Y1 + H1 + 12
H2 = 380
band(Y2, H2, 1, 'Release 2 · 价值闭环（Sprint 3）', '—— 投票 / 采纳 / 评论 / 标签 / 声誉，让“好答案”自己浮现')
draw_cards(R2, Y2)

Y3 = Y2 + H2 + 12
H3 = 310
band(Y3, H3, 2, 'Release 3 · 增长与治理（Sprint 4）', '—— 搜索、通知、徽章、治理，撑住真实的校园流量')
draw_cards(R3, Y3)

# ---------------- MVP dashed outline ----------------
def dashed_rect(box, color, width=5, dash=18, gap=12):
    x0, y0, x1, y1 = box
    for x in range(x0, x1, dash + gap):
        d.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=width)
        d.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=width)
    for y in range(y0, y1, dash + gap):
        d.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=width)
        d.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=width)

dashed_rect([col_x[0] - 2, Y1 + 48, col_x[3] + COL_W - 2, Y1 + H1 - 12], (211, 47, 47))
tag_x = col_x[0] + 2
d.rectangle([tag_x + 10, Y1 + 284, tag_x + 392, Y1 + 320], fill=(211, 47, 47))
d.text((tag_x + 20, Y1 + 287), 'MVP 切片：少了它，后续故事无法开始', font=F_NOTE, fill=(255, 255, 255))

# ---------------- legend ----------------
LY = H - 66
lx = MARGIN
d.text((lx, LY + 2), '图例', font=F_BAND, fill=INK)
lx += d.textlength('图例', font=F_BAND) + 24
for c, n in zip(PRIO_COLOR, PRIO_NAME):
    d.rounded_rectangle([lx, LY + 2, lx + 24, LY + 26], radius=6, fill=c)
    d.text((lx + 34, LY), n, font=F_NOTE, fill=INK)
    lx += 34 + d.textlength(n, font=F_NOTE) + 34
d.text((lx + 8, LY), '｜ 卡片＝「US 编号 + 标题 + Story Point」，粒度以「一个 Sprint 内可完成、可演示」为准',
       font=F_NOTE, fill=MUTED)

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'backlog', 'user-story-map.png')
img.save(out, 'PNG')
print('saved', out, img.size)




