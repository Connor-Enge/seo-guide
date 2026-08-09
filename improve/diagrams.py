import html
import re

def diagram_svg(spec):
    title = spec['title']
    steps = spec['steps']
    
    base = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    title_id = f'{base}-title'
    desc_id = f'{base}-desc'
    
    n = len(steps)
    W, box_x, box_w, box_h, top_pad, gap = 320, 30, 260, 56, 12, 34
    H = top_pad + n * box_h + (n - 1) * gap + top_pad
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 {W} {H}" width="100%" style="height:auto;max-width:520px;display:block;margin:1.5rem auto" aria-labelledby="{title_id} {desc_id}">'
    svg += f'<title id="{title_id}">{html.escape(title, quote=False)}</title>'
    svg += f'<desc id="{desc_id}">{html.escape(title, quote=False)}. Process flow: ' + ' then '.join(html.escape(step['label'], quote=False) for step in steps) + '.</desc>'
    
    for i, step in enumerate(steps):
        box_y = top_pad + i * (box_h + gap)
        next_box_y = box_y + box_h
        svg += f'<rect x="{box_x}" y="{box_y}" width="{box_w}" height="{box_h}" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-opacity="0.35"/>'
        svg += f'<text x="160" y="{box_y + 24}" text-anchor="middle" font-weight="600" font-size="15">{html.escape(step["label"], quote=False)}</text>'
        svg += f'<text x="160" y="{box_y + 42}" text-anchor="middle" font-size="12.5" opacity="0.75">{html.escape(step["desc"], quote=False)}</text>'
        
        if i < n - 1:
            next_box_top = box_y + box_h
            svg += f'<line x1="160" y1="{next_box_top}" x2="160" y2="{next_box_top - 8}" stroke="currentColor" stroke-opacity="0.5"/>'
            svg += f'<polygon points="157,{next_box_top} 163,{next_box_top} 160,{next_box_top - 4}" fill="currentColor"/>'
    
    svg += '</svg>'
    return svg
