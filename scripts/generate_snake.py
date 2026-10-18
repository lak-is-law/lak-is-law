#!/usr/bin/env python3
"""
Luxury Synchronized Snake Generator (v4)
Features:
1. Zero-Discontinuity Continuous Slithering: 100% adjacent grid steps without jumps or teleports.
2. Sleek Compact Tapered Body: Initial length 3 growing up to 6, with tapered aerodynamic segments.
3. Luminous Trailing Aura: Ghost tail glow segments trailing behind the snake.
4. Persistent Dot-Eating & Elegant Flashes.
5. Fully Balanced Telemetry Header.
"""

import argparse
import random
import os
import sys

DEFAULT_DOT_COLORS = ["#1C0C15", "#451126", "#701A3D", "#A12556", "#E5B5C7"]
DEFAULT_SNAKE_COLOR = "#F8F0F3"
DEFAULT_TAIL_COLOR = "#701A3D"

def parse_args():
    parser = argparse.ArgumentParser(description="Generate synchronized growing contribution snake SVG.")
    parser.add_argument("--output", "-o", default="assets/contribution-snake-v2.svg", help="Output file path")
    parser.add_argument("--speed", "-s", default="36s", help="Animation loop duration (e.g. 32s, 36s, 42s)")
    parser.add_argument("--snake-color", default=DEFAULT_SNAKE_COLOR, help="Hex color for snake head")
    parser.add_argument("--tail-color", default=DEFAULT_TAIL_COLOR, help="Hex color for tail end")
    parser.add_argument("--dot-colors", default=",".join(DEFAULT_DOT_COLORS), help="5 comma-separated hex colors")
    parser.add_argument("--start-length", type=int, default=3, help="Initial snake segment length")
    parser.add_argument("--max-length", type=int, default=6, help="Maximum snake segment length")
    parser.add_argument("--growth-interval", type=int, default=8, help="Dots eaten per new segment added")
    return parser.parse_args()

def generate_snake_svg(
    output_path="assets/contribution-snake-v2.svg",
    speed="36s",
    snake_color="#F8F0F3",
    tail_color="#701A3D",
    dot_colors=None,
    start_length=3,
    max_length=6,
    growth_interval=8
):
    if dot_colors is None:
        dot_colors = DEFAULT_DOT_COLORS
    elif isinstance(dot_colors, str):
        dot_colors = [c.strip() for c in dot_colors.split(",")]
    if len(dot_colors) < 5:
        dot_colors = DEFAULT_DOT_COLORS

    cols = 53
    rows = 7
    grid_x0 = 116.0
    grid_y0 = 192.0
    cell_w = 14.0
    gap = 4.5
    step = cell_w + gap

    # Real reduced 53-week contribution matrix
    REDUCED_GRID = [[2, 3, 3, 0, 2, 0, 4], [0, 0, 0, 0, 0, 0, 0], [0, 2, 4, 0, 1, 2, 0], [3, 1, 0, 0, 2, 0, 0], [1, 0, 4, 4, 2, 0, 2], [2, 3, 4, 0, 4, 2, 0], [0, 2, 1, 3, 0, 3, 1], [1, 1, 3, 3, 0, 0, 0], [4, 3, 1, 1, 2, 0, 0], [3, 2, 3, 0, 2, 0, 1], [0, 3, 3, 0, 0, 3, 1], [3, 3, 3, 1, 0, 0, 0], [0, 3, 1, 3, 1, 1, 0], [0, 3, 0, 0, 0, 4, 0], [3, 2, 0, 2, 4, 4, 4], [4, 4, 1, 1, 3, 1, 0], [2, 1, 2, 3, 0, 1, 0], [1, 0, 0, 4, 4, 2, 0], [1, 2, 0, 1, 0, 1, 1], [0, 1, 4, 3, 0, 0, 0], [0, 1, 3, 1, 0, 2, 2], [4, 2, 2, 3, 2, 3, 3], [2, 2, 2, 4, 0, 2, 0], [1, 3, 0, 1, 1, 3, 3], [0, 2, 0, 3, 1, 2, 4], [2, 2, 0, 1, 2, 4, 2], [0, 4, 2, 4, 2, 3, 0], [0, 1, 3, 4, 2, 0, 4], [4, 4, 2, 3, 1, 4, 0], [2, 2, 1, 0, 0, 4, 0], [4, 0, 2, 4, 1, 1, 4], [0, 0, 1, 4, 2, 0, 4], [1, 0, 1, 2, 1, 0, 0], [3, 4, 2, 1, 0, 1, 4], [2, 2, 0, 0, 1, 4, 4], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 1, 4], [0, 2, 2, 2, 4, 2, 3], [3, 4, 2, 4, 1, 0, 1], [3, 0, 4, 1, 0, 0, 2], [2, 1, 2, 0, 1, 2, 2], [0, 1, 2, 1, 3, 3, 1], [0, 2, 3, 3, 0, 2, 2], [1, 2, 2, 2, 3, 0, 1], [3, 1, 2, 2, 3, 2, 0], [1, 3, 1, 1, 0, 3, 0], [0, 1, 1, 1, 2, 4, 0], [3, 0, 0, 4, 1, 0, 3], [0, 2, 3, 2, 0, 2, 3], [1, 1, 3, 0, 3, 2, 0], [2, 1, 3, 0, 0, 0, 0], [1, 1, 1, 0, 2, 1, 3], [0, 2, 3, 4, 0, 2, 0]]
    levels = {}
    for c in range(cols):
        for r in range(rows):
            levels[(c, r)] = REDUCED_GRID[c][r]

    # Continuous 100% smooth, adjacent loop (zero teleportation)
    path = []
    # Strip 1: Rows 1 & 2 (cols 0..51)
    path.append((0, 0))
    path.append((0, 1))
    for c in range(1, 52):
        path.append((c, 1))
    path.append((51, 2))
    for c in range(50, -1, -1):
        path.append((c, 2))

    # Strip 2: Rows 3 & 4 (cols 0..51)
    path.append((0, 3))
    for c in range(1, 52):
        path.append((c, 3))
    path.append((51, 4))
    for c in range(50, -1, -1):
        path.append((c, 4))

    # Strip 3: Rows 5 & 6 (cols 0..51)
    path.append((0, 5))
    for c in range(1, 52):
        path.append((c, 5))
    path.append((51, 6))
    path.append((52, 6))

    # Elevator up Col 52
    for r in [5, 4, 3, 2, 1, 0]:
        path.append((52, r))

    # Runway across Row 0 back to (0, 0)
    for c in range(51, 0, -1):
        path.append((c, 0))

    total_steps = len(path)

    # Eating events
    eaten_events = {}
    dots_eaten_count = 0
    growth_schedule = {}
    current_length = start_length

    for idx, (pc, pr) in enumerate(path):
        if levels.get((pc, pr), 0) > 0:
            if (pc, pr) not in eaten_events:
                eaten_events[(pc, pr)] = []
            eaten_events[(pc, pr)].append(idx)
            dots_eaten_count += 1
            if dots_eaten_count % growth_interval == 0 and current_length < max_length:
                growth_schedule[current_length] = idx
                current_length += 1

    # Generate CSS Keyframes for Cells
    cell_keyframes = []
    cell_rects = []

    for c in range(cols):
        for r in range(rows):
            cx = grid_x0 + c * step
            cy = grid_y0 + r * step
            lvl = levels[(c, r)]
            initial_fill = dot_colors[lvl]
            cell_id = f"c_{c}_{r}"

            if (c, r) in eaten_events and lvl > 0:
                eat_idx = eaten_events[(c, r)][0]
                pct_eat = round((eat_idx / total_steps) * 100, 2)
                pct_pre = max(0.0, round(pct_eat - 0.25, 2))
                pct_flash = min(100.0, round(pct_eat + 0.35, 2))

                kf_body = f"""  0%, {pct_pre}% {{ fill: {initial_fill}; transform: scale(1); }}
  {pct_eat}% {{ fill: #FFFFFF; transform: scale(1.25); filter: drop-shadow(0 0 4px #E5B5C7); }}
  {pct_flash}%, 99.8% {{ fill: {dot_colors[0]}; transform: scale(1); filter: none; }}
  100% {{ fill: {initial_fill}; transform: scale(1); }}"""

                cell_keyframes.append(f"""@keyframes kf_{cell_id} {{
{kf_body}
}}
.{cell_id} {{
  animation: kf_{cell_id} {speed} linear infinite;
  transform-origin: {cx + cell_w/2:.1f}px {cy + cell_w/2:.1f}px;
}}""")
            else:
                cell_keyframes.append(f".{cell_id} {{ fill: {initial_fill}; }}")

            cell_rects.append(f'<rect id="{cell_id}" class="{cell_id}" x="{cx:.1f}" y="{cy:.1f}" width="{cell_w}" height="{cell_w}" rx="3"/>')

    # Generate CSS Keyframes for Snake Segments
    snake_keyframes = []
    snake_elements = []

    def interpolate_hex(c1, c2, factor):
        c1 = c1.lstrip("#")
        c2 = c2.lstrip("#")
        r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
        r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
        rf = int(r1 + (r2 - r1) * factor)
        gf = int(g1 + (g2 - g1) * factor)
        bf = int(b1 + (b2 - b1) * factor)
        return f"#{rf:02X}{gf:02X}{bf:02X}"

    # Snake Segments (Head + Body, compact and tapered)
    for s in range(max_length):
        seg_id = f"snk_seg_{s}"
        factor = min(1.0, s / max(1, max_length - 1))
        seg_fill = interpolate_hex(snake_color, tail_color, factor)
        # Taper smoothly from 12.5px down to 7.5px
        seg_size = max(7.5, 12.5 - (s * 0.95))
        offset = (cell_w - seg_size) / 2.0

        frames = []
        for i in range(total_steps):
            pct = round((i / total_steps) * 100, 2)
            pos_idx = max(0, i - s)
            pc, pr = path[pos_idx]
            sx = grid_x0 + pc * step + offset
            sy = grid_y0 + pr * step + offset
            frames.append(f"{pct}% {{ transform: translate({sx:.1f}px, {sy:.1f}px); }}")

        keyframes_str = "\n  ".join(frames)

        if s < start_length:
            vis_rule = "opacity: 1;"
        else:
            unlock_idx = growth_schedule.get(s, total_steps)
            unlock_pct = round((unlock_idx / total_steps) * 100, 2)
            vis_rule = f"animation: kf_{seg_id} {speed} linear infinite, vis_{seg_id} {speed} step-end infinite;"
            snake_keyframes.append(f"""@keyframes vis_{seg_id} {{
  0%, {unlock_pct}% {{ opacity: 0; }}
  {unlock_pct}%, 100% {{ opacity: 1; }}
}}""")

        if s < start_length:
            snake_keyframes.append(f"""@keyframes kf_{seg_id} {{
  {keyframes_str}
}}
.{seg_id} {{
  animation: kf_{seg_id} {speed} linear infinite;
  {vis_rule}
}}""")
        else:
            snake_keyframes.append(f"""@keyframes kf_{seg_id} {{
  {keyframes_str}
}}
.{seg_id} {{
  {vis_rule}
}}""")

        if s == 0:
            snake_elements.append(f"""    <g class="{seg_id}">
      <rect width="{seg_size:.1f}" height="{seg_size:.1f}" rx="4" fill="{seg_fill}" filter="url(#snk-head-glow)"/>
      <circle cx="{seg_size * 0.72:.1f}" cy="{seg_size * 0.28:.1f}" r="1.3" fill="#10070C"/>
      <circle cx="{seg_size * 0.72:.1f}" cy="{seg_size * 0.72:.1f}" r="1.3" fill="#10070C"/>
    </g>""")
        else:
            snake_elements.append(f"""    <g class="{seg_id}">
      <rect width="{seg_size:.1f}" height="{seg_size:.1f}" rx="3" fill="{seg_fill}" fill-opacity="{max(0.45, 1.0 - factor * 0.45):.2f}"/>
    </g>""")

    # 3 Glowing Ghost Trail Segments behind the tail
    num_trails = 3
    trail_opacities = [0.38, 0.22, 0.10]
    for t in range(num_trails):
        trail_id = f"snk_trail_{t}"
        trail_size = max(6.0, 7.5 - (t * 0.9))
        trail_offset = (cell_w - trail_size) / 2.0
        trail_fill = tail_color

        tframes = []
        for i in range(total_steps):
            pct = round((i / total_steps) * 100, 2)
            pos_idx = max(0, i - (max_length + t + 1))
            pc, pr = path[pos_idx]
            sx = grid_x0 + pc * step + trail_offset
            sy = grid_y0 + pr * step + trail_offset
            tframes.append(f"{pct}% {{ transform: translate({sx:.1f}px, {sy:.1f}px); }}")

        t_keyframes_str = "\n  ".join(tframes)
        snake_keyframes.append(f"""@keyframes kf_{trail_id} {{
  {t_keyframes_str}
}}
.{trail_id} {{
  animation: kf_{trail_id} {speed} linear infinite;
}}""")

        snake_elements.append(f"""    <g class="{trail_id}">
      <circle cx="{trail_offset + trail_size/2:.1f}" cy="{trail_offset + trail_size/2:.1f}" r="{trail_size/2:.1f}" fill="{trail_fill}" fill-opacity="{trail_opacities[t]}" filter="url(#snk-trail-glow)"/>
    </g>""")

    all_css = "\n".join(cell_keyframes) + "\n" + "\n".join(snake_keyframes)
    all_cells_svg = "\n    ".join(cell_rects)
    all_snake_svg = "\n".join(snake_elements)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420" role="img" aria-labelledby="hm-title hm-desc">
  <title id="hm-title">Synchronized Contribution Snake — @lak-is-law</title>
  <desc id="hm-desc">Configurable live contribution snake that grows in length as it consumes verified contributions across 2023–2026.</desc>
  <defs>
    <linearGradient id="hm-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#190B12"/>
      <stop offset="1" stop-color="#10070C"/>
    </linearGradient>
    <radialGradient id="hm-light" cx="88%" cy="0%" r="70%">
      <stop offset="0" stop-color="#701A3D" stop-opacity=".55"/>
      <stop offset="1" stop-color="#451126" stop-opacity="0"/>
    </radialGradient>
    <filter id="snk-head-glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="snk-trail-glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="3.0"/>
    </filter>
  </defs>

  <style>
    .hm-serif {{ font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif; }}
    .hm-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }}
    .hm-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
    {all_css}
  </style>

  <!-- Background Canvas -->
  <rect width="1200" height="420" rx="20" fill="url(#hm-bg)"/>
  <rect width="1200" height="420" rx="20" fill="url(#hm-light)"/>
  <rect x=".5" y=".5" width="1199" height="419" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".18"/>

  <!-- Telemetry Header (Clean Balanced Spacing, Zero Overlap) -->
  <g>
    <!-- Left: Title & Subtitle -->
    <text class="hm-mono" x="54" y="64" font-size="11" letter-spacing="2.4" fill="#C77B9B">COMMIT LOG · SYNCHRONIZED ENGINE</text>
    <text class="hm-serif" x="54" y="106" font-size="23" font-weight="300" fill="#F8F0F3">A year of building, <tspan font-style="italic" fill="#E5B5C7">one dot</tspan> at a time.</text>
    
    <!-- Col 1: Contributions -->
    <g transform="translate(640 54)">
      <text class="hm-mono" font-size="9.5" letter-spacing="1.6" fill="#C77B9B">CONTRIBUTIONS</text>
      <text class="hm-serif" y="42" font-size="30" font-weight="300" fill="#F8F0F3">3,871</text>
      <text class="hm-mono" y="62" font-size="9" fill="#B6A3AC">2023–2026</text>
    </g>

    <!-- Col 2: Active Days -->
    <g transform="translate(770 54)">
      <text class="hm-mono" font-size="9.5" letter-spacing="1.6" fill="#C77B9B">ACTIVE DAYS</text>
      <text class="hm-serif" y="42" font-size="30" font-weight="300" fill="#F8F0F3">200</text>
      <text class="hm-mono" y="62" font-size="9" fill="#B6A3AC">2026 year-to-date</text>
    </g>

    <!-- Col 3: Longest Streak -->
    <g transform="translate(895 54)">
      <text class="hm-mono" font-size="9.5" letter-spacing="1.6" fill="#C77B9B">LONGEST STREAK</text>
      <text class="hm-serif" y="42" font-size="30" font-weight="300" fill="#F8F0F3">13 Days</text>
      <text class="hm-mono" y="62" font-size="9" fill="#B6A3AC">Mar 2026 sprint</text>
    </g>

    <!-- Col 4: Busiest Day (Unclipped, Ample Right Margin) -->
    <g transform="translate(1030 54)">
      <text class="hm-mono" font-size="9.5" letter-spacing="1.6" fill="#C77B9B">BUSIEST DAY</text>
      <text class="hm-serif" y="42" font-size="30" font-weight="300" fill="#F8F0F3">24</text>
      <text class="hm-mono" y="62" font-size="9" fill="#B6A3AC">25 Jan 2026</text>
    </g>
  </g>

  <!-- Month Labels -->
  <g class="hm-mono" font-size="10.5" fill="#B6A3AC">
    <text x="156" y="174">Nov</text><text x="251" y="174">Dec</text><text x="327" y="174">Jan</text>
    <text x="422" y="174">Feb</text><text x="498" y="174">Mar</text><text x="574" y="174">Apr</text>
    <text x="650" y="174">May</text><text x="745" y="174">Jun</text><text x="821" y="174">Jul</text>
    <text x="897" y="174">Aug</text><text x="992" y="174">Sep</text><text x="1068" y="174">Oct</text>
  </g>
  <g class="hm-mono" font-size="10" fill="#B6A3AC" text-anchor="end">
    <text x="106" y="216">Mon</text>
    <text x="106" y="254">Wed</text>
    <text x="106" y="292">Fri</text>
  </g>

  <!-- Contribution Grid (Synchronously Eaten with Gentle Respawn) -->
  <g id="contribution-grid">
    {all_cells_svg}
  </g>

  <!-- Growing Snake Elements & Trailing Aura -->
  <g id="snake-body">
{all_snake_svg}
  </g>

  <!-- Footer Legend & Telemetry -->
  <g>
    <text class="hm-mono" x="56" y="392" font-size="10.5" fill="#B6A3AC">Real-time synchronized eating animation · sleek slithering engine with luminous trail</text>
    <text class="hm-mono" x="984" y="392" font-size="10.5" fill="#B6A3AC">Less</text>
    <rect x="1020" y="382" width="12" height="12" rx="3" fill="{dot_colors[0]}"/>
    <rect x="1038" y="382" width="12" height="12" rx="3" fill="{dot_colors[1]}"/>
    <rect x="1056" y="382" width="12" height="12" rx="3" fill="{dot_colors[2]}"/>
    <rect x="1074" y="382" width="12" height="12" rx="3" fill="{dot_colors[3]}"/>
    <rect x="1092" y="382" width="12" height="12" rx="3" fill="{dot_colors[4]}"/>
    <text class="hm-mono" x="1114" y="392" font-size="10.5" fill="#B6A3AC">More</text>
  </g>

  <!-- Interactive Arrow Key Control with 2s Auto-Resume (when SVG viewed directly) -->
  <script type="text/javascript">
  <![CDATA[
    document.addEventListener('DOMContentLoaded', function() {{
      let mode = 'auto';
      let autoTimer = null;
      let manualHead = {{ c: 20, r: 3 }};
      const headEl = document.querySelector('.snk_seg_0');
      const cols = 53, rows = 7;
      const step = 18.5, x0 = 116.0, y0 = 192.0;

      window.addEventListener('keydown', function(e) {{
        let dx = 0, dy = 0;
        if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {{ dy = -1; }}
        else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') {{ dy = 1; }}
        else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {{ dx = -1; }}
        else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {{ dx = 1; }}
        else return;

        e.preventDefault();
        mode = 'manual';
        manualHead.c = (manualHead.c + dx + cols) % cols;
        manualHead.r = (manualHead.r + dy + rows) % rows;
        
        if (headEl) {{
          headEl.style.animationPlayState = 'paused';
          headEl.style.transform = 'translate(' + (x0 + manualHead.c * step) + 'px, ' + (y0 + manualHead.r * step) + 'px)';
        }}

        const cell = document.getElementById('c_' + manualHead.c + '_' + manualHead.r);
        if (cell) {{
          cell.style.animation = 'none';
          cell.style.fill = '#1C0C15';
        }}

        clearTimeout(autoTimer);
        autoTimer = setTimeout(function() {{
          mode = 'auto';
          if (headEl) {{
            headEl.style.animationPlayState = 'running';
          }}
        }}, 2000);
      }});
    }});
  ]]>
  </script>
</svg>
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Successfully generated synchronized snake: {output_path}")
    print(f"  Speed: {speed}")
    print(f"  Length: {start_length} -> {max_length}")
    print(f"  Total Steps: {total_steps} (zero-jump continuous loop)")
    print(f"  Eaten Events: {len(eaten_events)}")

if __name__ == "__main__":
    args = parse_args()
    generate_snake_svg(
        output_path=args.output,
        speed=args.speed,
        snake_color=args.snake_color,
        tail_color=args.tail_color,
        dot_colors=args.dot_colors,
        start_length=args.start_length,
        max_length=args.max_length,
        growth_interval=args.growth_interval
    )
