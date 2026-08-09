import html
import re

def diagram_svg(spec):
    title = spec['title']
    steps = spec['steps']
    
    base = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    svg_id = f"{base}-diagram"
    title_id = f"{base}-title"
    desc_id = f"{base}-desc"
    
    title_text = html.escape(title, quote=False)
    desc_text = f"{title}. Process flow: {' then '.join(html.escape(s['label'], quote=False) for s in steps)}."
    
    W, H = 320, 12 + len(steps)*(56+34) + (len(steps)-1)*34 + 12
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 {W} {H}" width="100%" style="height:auto;max-width:520px;display:block;margin:1.5rem auto;" aria-labelledby="{title_id} {desc_id}">'
    svg += f'<title id="{title_id}">{title_text}</title>'
    svg += f'<desc id="{desc_id}">{desc_text}</desc>'
    
    for i, step in enumerate(steps):
        label = html.escape(step['label'], quote=False)
        desc = html.escape(step['desc'], quote=False)
        
        box_y = 12 + i*(56+34)
        box_bottom = box_y + 56
        
        svg += f'<rect x="30" y="{box_y}" width="260" height="56" rx="10" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-opacity="0.35"/>'
        svg += f'<text x="160" y="{box_y+24}" text-anchor="middle" font-weight="600" font-size="15">{label}</text>'
        svg += f'<text x="160" y="{box_y+42}" text-anchor="middle" font-size="12.5" opacity="0.75">{desc}</text>'
        
        if i < len(steps) - 1:
            next_box_top = box_y + 56 + 34
            svg += f'<line x1="160" y1="{box_bottom}" x2="160" y2="{next_box_top-8}" stroke="currentColor" stroke-opacity="0.5"/>'
            svg += f'<polygon points="157, {next_box_top-8} 163, {next_box_top-4} 163, {next_box_top-8}" fill="currentColor"/>'
    
    svg += '</svg>'
    return svg
