#!/usr/bin/env python3
"""
生成 discover-skill 演示 GIF（showcase）。
模拟"一句话触发 → 读取三源 → 产出五板块中文榜单报告 → 行业适配标注"的完整闭环。

用真实运行产物（examples/skill榜单-2026-08-31.md）的内容，不编造数据。
输出：discover-skill-demo.gif
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ---------- 常量 ----------
W, H = 960, 600
BG = (15, 17, 23)          # 深色终端背景
PANEL = (22, 26, 34)       # 面板
BORDER = (45, 52, 66)      # 边框
FG = (225, 228, 235)       # 主文字
MUTED = (130, 138, 152)    # 次要文字
ACCENT = (88, 166, 255)    # 蓝（主强调）
GREEN = (63, 185, 80)      # 绿（成功）
YELLOW = (210, 153, 34)    # 黄（提醒）
RED = (248, 81, 73)        # 红（报警）
PURPLE = (163, 113, 247)   # 紫（数据源）
CYAN = (56, 189, 248)      # 青
ORANGE = (210, 139, 54)    # 橙

FONT_DIR = "/usr/share/fonts/opentype/noto"
FONT_REG = os.path.join(FONT_DIR, "NotoSansCJK-Regular.ttc")
FONT_BOLD = os.path.join(FONT_DIR, "NotoSansCJK-Bold.ttc")

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

# ---------- 工具函数 ----------
def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def title_bar(d, text, right=None):
    """顶部标题栏"""
    d.rectangle([0, 0, W, 56], fill=PANEL)
    d.line([0, 56, W, 56], fill=BORDER)
    # 三个圆点（macOS 风格）
    for i, c in enumerate([RED, YELLOW, GREEN]):
        d.ellipse([20+i*24, 20, 20+i*24+12, 32], fill=c)
    d.text((100, 16), text, font=font(20, bold=True), fill=FG)
    if right:
        d.text((W-20-len(right)*12, 18), right, font=font(16), fill=MUTED)

def terminal_line(d, y, text, color=FG, size=17, prefix="", indent=24):
    """一行终端文字"""
    x = indent
    if prefix:
        d.text((x, y), prefix, font=font(size, bold=True), fill=ACCENT)
        x += len(prefix) * (size//2) + 4
    d.text((x, y), text, font=font(size), fill=color)
    return y + size + 12

def wrap_text(d, text, x, y, max_w, f, color):
    """自动换行，返回结束 y"""
    lines = []
    line = ""
    for ch in text:
        test = line + ch
        if d.textlength(test, font=f) <= max_w:
            line = test
        else:
            lines.append(line)
            line = ch
    if line:
        lines.append(line)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=color)
        y += f.size + 6
    return y

# ---------- 各帧绘制 ----------
def frame1_input():
    """帧1：触发词输入"""
    img, d = new_canvas()
    title_bar(d, "discover-skill · 每日 AI Skill 发现雷达", "1 / 7")
    d.text((24, 90), "用户输入：", font=font(17), fill=MUTED)
    d.rounded_rectangle([24, 130, W-24, 210], radius=10, fill=PANEL, outline=ACCENT, width=2)
    d.text((48, 150), "帮我看看 skill 圈最近有什么动静", font=font(28, bold=True), fill=FG)
    d.text((48, 205), "一句话触发 · 无需安装依赖", font=font(16), fill=MUTED)
    # 触发词示例
    d.text((24, 250), "更多触发方式：", font=font(17), fill=MUTED)
    triggers = ['「发现skill」', '「生成今天的 skill 榜单」', '「最近什么 skill 在涨？」', '「有什么新 skill 值得看？」']
    f_trig = font(17)
    y = 292
    for t in triggers:
        # 单独画引号在胶囊外（左括号放在胶囊左侧外缘，作为视觉装饰）
        # 简化：直接用 ASCII 引号避免 CJK 引号字形问题
        plain = t.replace('「', '"').replace('」', '"')
        tw = d.textlength(plain, font=f_trig)
        d.rounded_rectangle([24, y, 24+int(tw)+32, y+40], radius=8, fill=PANEL, outline=BORDER)
        d.text((40, y+10), plain, font=f_trig, fill=FG)
        y += 52
    return img

def frame2_sources():
    """帧2：读取三源"""
    img, d = new_canvas()
    title_bar(d, "discover-skill · 取数中", "2 / 7")
    d.text((24, 80), "并行读取三个数据源（三源平权）", font=font(18, bold=True), fill=FG)
    sources = [
        ("ClawHub Top100", "累计下载存量榜 · 严格日环比", CYAN, "✓ 已取 99/100 条"),
        ("skills.sh Trending", "近期安装热度 · 页面解析", GREEN, "✓ 前 8 条"),
        ("腾讯 SkillHub 热榜", "近期飙升下载榜 · 中文生态", ORANGE, "✓ 前 8 条"),
    ]
    y = 130
    for name, desc, color, status in sources:
        d.rounded_rectangle([24, y, W-24, y+72], radius=10, fill=PANEL, outline=BORDER)
        d.ellipse([44, y+22, 60, y+38], fill=color)
        d.text((76, y+14), name, font=font(19, bold=True), fill=FG)
        d.text((76, y+42), desc, font=font(15), fill=MUTED)
        d.text((W-200, y+24), status, font=font(15, bold=True), fill=GREEN)
        y += 88
    d.text((24, y+10), "口径契约：每个源的排序键 / 展示字段 / 已知坑都预先写清", font=font(15), fill=MUTED)
    return img

def frame3_health():
    """帧3：健康度 + 增速榜"""
    img, d = new_canvas()
    title_bar(d, "discover-skill · ClawHub 平台健康度", "3 / 7")
    # 健康度结论
    d.rounded_rectangle([24, 80, W-24, 150], radius=10, fill=PANEL, outline=BORDER)
    d.text((48, 92), "Top10 日增合计 694 vs 7日均值 829", font=font(20, bold=True), fill=YELLOW)
    d.text((48, 122), "-16.3% · 连续 3 日低于均值 · 判定：偏弱", font=font(17), fill=FG)
    # 增速榜
    d.text((24, 170), "下载增速榜（真实数据 · Top 4）", font=font(17, bold=True), fill=FG)
    rows = [
        ("#1", "Planning with files", "+164", GREEN),
        ("#2", "self-improving agent", "+134", FG),
        ("#3", "Feishu Evolver Wrapper", "+105", FG),
        ("#4", "Evolver", "+103", FG),
    ]
    y = 205
    for rk, name, delta, color in rows:
        d.rounded_rectangle([24, y, W-24, y+44], radius=6, fill=PANEL, outline=BORDER)
        d.text((40, y+10), rk, font=font(16, bold=True), fill=ACCENT)
        d.text((90, y+10), name, font=font(17), fill=FG)
        d.text((W-110, y+10), delta, font=font(17, bold=True), fill=color)
        y += 52
    d.text((24, y+8), "「无变化」≠ 生态繁荣 → 已用健康度指标揭示", font=font(15), fill=MUTED)
    return img

def frame4_report():
    """帧4：五板块报告"""
    img, d = new_canvas()
    title_bar(d, "discover-skill · 产出报告", "4 / 7")
    d.text((24, 78), "Skill 榜单 - 2026-08-31.md", font=font(20, bold=True), fill=ACCENT)
    d.text((24, 112), "固定五板块结构", font=font(16), fill=MUTED)
    sections = [
        ("一", "元数据说明", "快照日期 · 三源并列 · limitations"),
        ("二", "ClawHub 榜单", "健康度 + 提升榜 + 增速榜 + 新进榜"),
        ("三", "skills.sh Trending", "前 8 条 · 中文简介"),
        ("四", "腾讯 SkillHub 榜单", "前 8 条 · 口径注记"),
        ("五", "今日榜单小结", "值得关注清单 + 入选维度"),
    ]
    y = 150
    for num, name, desc in sections:
        d.rounded_rectangle([24, y, W-24, y+56], radius=8, fill=PANEL, outline=BORDER)
        d.text((44, y+12), num, font=font(22, bold=True), fill=ACCENT)
        d.text((86, y+8), name, font=font(19, bold=True), fill=FG)
        d.text((86, y+34), desc, font=font(14), fill=MUTED)
        y += 66
    d.text((24, y+4), "每条上榜技能一句中文简介，不认识英文名也能 3 秒判断", font=font(15), fill=MUTED)
    return img

def frame5_industry():
    """帧5：行业适配标注"""
    img, d = new_canvas()
    title_bar(d, "discover-skill · 值得关注（按行业适配）", "5 / 7")
    d.text((24, 78), "今日小结 · 入选维度标注", font=font(18, bold=True), fill=FG)
    items = [
        ("热点选题", "SkillHub #5", "行业 + 个人", GREEN),
        ("直播带货脚本工作台", "SkillHub #4", "行业 + 个人", GREEN),
        ("招投标商机筛选", "SkillHub #8", "行业", YELLOW),
        ("smart-charts", "SkillHub #3", "个人", YELLOW),
        ("Planning with files", "ClawHub #67", "普适 + 个人", PURPLE),
    ]
    f_dim = font(15, bold=True)
    y = 125
    for name, src, dim, color in items:
        d.rounded_rectangle([24, y, W-24, y+50], radius=8, fill=PANEL, outline=BORDER)
        d.text((44, y+12), name, font=font(18, bold=True), fill=FG)
        d.text((44+len(name)*22+8, y+14), src, font=font(14), fill=MUTED)
        # 维度标签（按真实宽度自适应）
        dw = d.textlength(dim, font=f_dim)
        bx2 = W - 40
        bx1 = int(bx2 - dw - 24)
        d.rounded_rectangle([bx1, y+10, bx2, y+40], radius=14, fill=PANEL, outline=color, width=2)
        d.text((bx1+12, y+16), dim, font=f_dim, fill=color)
        y += 60
    d.text((24, y+6), "行业 = 地产适配 · 普适 = 任何知识工作者 · 个人 = 你的日常场景", font=font(14), fill=MUTED)
    return img

def frame6_cross():
    """帧6：跨源信号"""
    img, d = new_canvas()
    title_bar(d, "discover-skill · 跨源信号洞察", "6 / 7")
    d.text((24, 78), "一句话总结", font=font(18, bold=True), fill=FG)
    d.rounded_rectangle([24, 120, W-24, 230], radius=10, fill=PANEL, outline=PURPLE, width=2)
    wrap_text(d, "两个生态、两种语言圈同向走热——内容生产自动化是本周最强信号：", 
              48, 140, W-96, font(20, bold=True), FG)
    wrap_text(d, "skills.sh 的 ai-video-generation / video-edit / ai-music 与 SkillHub 的直播脚本 / 电商套图同向走热。", 
              48, 190, W-96, font(17), FG)
    d.text((24, 260), "ClawHub 存量榜僵化（仅 2 条位次上升）· 发现类结论主要来自 SkillHub", font=font(16), fill=MUTED)
    return img

def frame7_done():
    """帧7：交付完成"""
    img, d = new_canvas()
    title_bar(d, "discover-skill · 完成", "7 / 7")
    # 大对勾
    d.ellipse([W//2-60, 120, W//2+60, 240], fill=PANEL, outline=GREEN, width=4)
    d.text((W//2-25, 155), "✓", font=font(60, bold=True), fill=GREEN)
    d.text((W//2, 290), "报告已生成", font=font(26, bold=True), fill=FG, anchor="mm")
    d.text((W//2, 340), "skill榜单-2026-08-31.md", font=font(18), fill=ACCENT, anchor="mm")
    # 关键特征
    feats = ["三源平权 · 只报变化", "口径说清 · 不编造", "行业适配 · 换画像即换行业"]
    y = 395
    for f in feats:
        d.text((W//2, y), f, font=font(16), fill=MUTED, anchor="mm")
        y += 34
    d.text((W//2, H-40), "npx skills add kool18/discover-skill", font=font(15, bold=True), fill=FG, anchor="mm")
    return img

# ---------- 生成 GIF ----------
def main():
    frames = [
        frame1_input(),
        frame2_sources(),
        frame3_health(),
        frame4_report(),
        frame5_industry(),
        frame6_cross(),
        frame7_done(),
    ]
    # 每帧停留时长（毫秒）：首帧和末帧稍长，让观者看清
    durations = [1600, 1400, 1600, 1500, 1700, 1500, 2200]
    out = "/workspace/discover-skill/assets/discover-skill-demo.gif"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    frames[0].save(
        out, save_all=True, append_images=frames[1:],
        duration=durations, loop=0, optimize=False,
    )
    print(f"GIF 已生成：{out}")
    print(f"大小：{os.path.getsize(out)/1024:.1f} KB，帧数：{len(frames)}")

if __name__ == "__main__":
    main()
