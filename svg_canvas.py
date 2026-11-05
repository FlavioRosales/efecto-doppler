"""Adaptador pequeño de las operaciones de dibujo usadas por Visuals a SVG."""
from html import escape


class SVGCanvas:
    def __init__(self, width=1200, height=520):
        self.width, self.height = width, height
        self.parts = []

    @staticmethod
    def style(options, default_fill='none'):
        fill = escape(options.get('fill', default_fill) or 'none', quote=True)
        stroke = escape(options.get('outline', '') or 'none', quote=True)
        width = options.get('width', 1)
        return f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"'

    def create_oval(self, x0, y0, x1, y1, **options):
        self.parts.append(f'<ellipse cx="{(x0+x1)/2}" cy="{(y0+y1)/2}" '
                          f'rx="{abs(x1-x0)/2}" ry="{abs(y1-y0)/2}" {self.style(options)}/>')

    def create_rectangle(self, x0, y0, x1, y1, **options):
        self.parts.append(f'<rect x="{min(x0,x1)}" y="{min(y0,y1)}" '
                          f'width="{abs(x1-x0)}" height="{abs(y1-y0)}" {self.style(options)}/>')

    def create_line(self, *coords, **options):
        color = escape(options.get('fill', '#ffffff'), quote=True)
        points = ' '.join(f'{coords[i]},{coords[i+1]}' for i in range(0, len(coords), 2))
        dash = ' stroke-dasharray="5 5"' if options.get('dash') else ''
        self.parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" '
                          f'stroke-width="{options.get("width",1)}"{dash}/>')
        if options.get('arrow') == 'last':
            import math
            x, y = coords[-2:]
            angle = math.atan2(y-coords[-3], x-coords[-4])
            left = (x-12*math.cos(angle-.45), y-12*math.sin(angle-.45))
            right = (x-12*math.cos(angle+.45), y-12*math.sin(angle+.45))
            self.parts.append(f'<polygon points="{x},{y} {left[0]},{left[1]} '
                              f'{right[0]},{right[1]}" fill="{color}"/>')

    def create_text(self, x, y, **options):
        anchor = {'center':'middle', 'w':'start', 'e':'end'}[options.get('anchor','center')]
        size = options.get('font', ('Sans',16))[1] * 1.25
        color = escape(options.get('fill', '#ffffff'), quote=True)
        text = escape(str(options.get('text','')))
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
                          f'dominant-baseline="central" fill="{color}" '
                          f'font-family="sans-serif" font-size="{size}">{text}</text>')

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" '
                f'width="{self.width}" height="{self.height}" role="img">'
                '<rect width="100%" height="100%" fill="#0b1224"/>'
                + ''.join(self.parts) + '</svg>')
