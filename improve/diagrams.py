import html
import re
import json

FENCE = '`' * 3

def diagram_svg(spec):
    W, PAD, BOX_X, BOX_W, BOX_H, GAP, RX = 320, 14, 30, 260, 58, 30, 10
    title = html.escape(spec['title'], quote=True)
    labels = [html.escape(step['label'], quote=False) for step in spec['steps']]
    desc = [html.escape(step['desc'], quote=False) for step in spec['steps']]
    labels_join = ' then '.join(labels)
    aria_label = f"{title}. Steps: {labels_join}."
    H = PAD * 2 + len(spec['steps']) * BOX_H + (len(spec['steps']) - 1) * GAP
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 {W} {H}" width="100%" style="height:auto;max-width:520px;display:block;margin:1.5rem auto;">',
        f'<title>{title}</title>',
        f'<desc>{labels_join}</desc>',
        f'<rect x="{BOX_X}" y="{PAD}" width="{BOX_W}" height="{BOX_H}" rx="{RX}" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-opacity="0.30" stroke-width="1"/>',
        f'<text x="160" y="{PAD + 24}" text-anchor="middle" fill="currentColor" font-weight="600" font-size="15">{labels[0]}</text>',
        f'<text x="160" y="{PAD + 43}" text-anchor="middle" fill="currentColor" fill-opacity="0.72" font-size="12.5">{desc[0]}</text>'
    ]
    for n in range(1, len(spec['steps'])):
        box_y = PAD + n * (BOX_H + GAP)
        svg_parts.extend([
            f'<rect x="{BOX_X}" y="{box_y}" width="{BOX_W}" height="{BOX_H}" rx="{RX}" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-opacity="0.30" stroke-width="1"/>',
            f'<text x="160" y="{box_y + 24}" text-anchor="middle" fill="currentColor" font-weight="600" font-size="15">{labels[n]}</text>',
            f'<text x="160" y="{box_y + 43}" text-anchor="middle" fill="currentColor" fill-opacity="0.72" font-size="12.5">{desc[n]}</text>'
        ])
        ay = box_y + BOX_H + GAP - 9
        svg_parts.extend([
            f'<line x1="160" y1="{box_y + BOX_H}" x2="160" y2="{ay}" stroke="currentColor" stroke-opacity="0.45" stroke-width="1.5"/>',
            f'<polygon points="154,{ay} 166,{ay} 160,{ay+8}" fill="currentColor" fill-opacity="0.6"/>'
        ])
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def consume_diagram(lines, i):
    head = lines[i].rstrip()
    if not (head.startswith(FENCE) and head[3:].strip() == 'diagram'):
        return None
    k = i + 1
    while k < len(lines) and not lines[k].rstrip().startswith(FENCE):
        k += 1
    if k == len(lines):
        raise ValueError('unterminated diagram fence')
    inner_lines = '\n'.join(lines[i+1:k])
    spec = json.loads(inner_lines)
    if not isinstance(spec, dict) or 'title' not in spec or 'steps' not in spec:
        raise ValueError("diagram spec needs 'title' and 'steps'")
    return diagram_svg(spec), k + 1
