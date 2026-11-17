INK='#1B1A2E'
BODY={'you':'#3DDC97','maya':'#5FD6A3','jordan':'#FF9B80','sam':'#A99BF0','priya':'#F5C84C','alex':'#7DB7F0'}
BG={'you':'#B8E8D3','maya':'#B8E8D3','jordan':'#FFD3C7','sam':'#D6D2F0','priya':'#F5E3A8','alex':'#CFE3F5'}
def ears(i,c):
    if i=='maya': return f'<ellipse cx="17" cy="11" rx="4.2" ry="10" fill="{c}"/><ellipse cx="31" cy="11" rx="4.2" ry="10" fill="{c}"/><ellipse cx="17" cy="11" rx="1.8" ry="6.5" fill="#FFB8C6"/><ellipse cx="31" cy="11" rx="1.8" ry="6.5" fill="#FFB8C6"/>'
    if i=='jordan': return f'<polygon points="10,20 12,5 23,14" fill="{c}"/><polygon points="38,20 36,5 25,14" fill="{c}"/><polygon points="13,16 14,9 19,14" fill="#FFB8C6"/><polygon points="35,16 34,9 29,14" fill="#FFB8C6"/>'
    if i=='sam': return f'<circle cx="12" cy="15" r="5.5" fill="{c}"/><circle cx="36" cy="15" r="5.5" fill="{c}"/><circle cx="12" cy="15" r="2.5" fill="#D9D3FA"/><circle cx="36" cy="15" r="2.5" fill="#D9D3FA"/>'
    if i=='priya': return f'<path d="M24 14 Q22 6 18 5 M24 14 Q24 5 24 3 M24 14 Q26 6 30 5" stroke="{c}" stroke-width="3.2" stroke-linecap="round" fill="none"/>'
    if i=='alex': return f'<path d="M24 14 L24 7" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/><circle cx="24" cy="6" r="3.2" fill="#FFD84D"/>'
    return '<path d="M24 14 Q24 8 24 6" stroke="#0B7A4F" stroke-width="2.6" stroke-linecap="round" fill="none"/><ellipse cx="19" cy="7" rx="5" ry="2.8" fill="#0B7A4F" transform="rotate(-25 19 7)"/><ellipse cx="29" cy="7" rx="5" ry="2.8" fill="#0B7A4F" transform="rotate(25 29 7)"/>'
def face(m):
    eyes=f'<circle cx="18" cy="27" r="2.4" fill="{INK}"/><circle cx="30" cy="27" r="2.4" fill="{INK}"/>'
    blush='<ellipse cx="12.5" cy="32" rx="3" ry="2" fill="#FF8FA8" opacity=".55"/><ellipse cx="35.5" cy="32" rx="3" ry="2" fill="#FF8FA8" opacity=".55"/>'
    smile=f'<path d="M20 32.5 Q24 37.5 28 32.5" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" fill="none"/>'
    if m=='study': return f'<circle cx="18" cy="27" r="5" fill="#fff" fill-opacity=".5" stroke="{INK}" stroke-width="1.8"/><circle cx="30" cy="27" r="5" fill="#fff" fill-opacity=".5" stroke="{INK}" stroke-width="1.8"/><path d="M23 27 h2" stroke="{INK}" stroke-width="1.8"/>{eyes}<path d="M21 34 Q24 35.5 27 34" stroke="{INK}" stroke-width="2" stroke-linecap="round" fill="none"/>{blush}'
    if m=='gym': return f'<path d="M9.5 21.5 Q24 16.5 38.5 21.5" stroke="#FF5C7A" stroke-width="3.4" stroke-linecap="round" fill="none"/>{eyes}<path d="M19 32 Q24 40 29 32 Z" fill="{INK}"/>{blush}'
    if m=='dinner': return f'{eyes}<ellipse cx="24" cy="34" rx="3" ry="3.4" fill="{INK}"/><ellipse cx="24" cy="35.5" rx="1.6" ry="1.4" fill="#FF8FA8"/>{blush}'
    if m=='dnd': return f'<path d="M15 27.5 Q18 24.5 21 27.5 M27 27.5 Q30 24.5 33 27.5" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" fill="none"/><path d="M22 34 Q24 35.5 26 34" stroke="{INK}" stroke-width="2" stroke-linecap="round" fill="none"/>{blush}'
    if m=='busy': return f'{eyes}<path d="M21 34 h6" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>{blush}'
    return eyes+smile+blush
def star(x,y,c):
    return f'<path d="M{x} {y-4} Q{x} {y} {x+4} {y} Q{x} {y} {x} {y+4} Q{x} {y} {x-4} {y} Q{x} {y} {x} {y-4}Z" fill="{c}"/>'
def props(m):
    pg=f'<path d="M24 39 Q31.5 36 39 39 L39 48 Q31.5 45 24 48Z" fill="#fff" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
    if m=='study': return f'<path d="M9 39 Q16.5 36 24 39 L24 48 Q16.5 45 9 48Z" fill="#fff" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>{pg}<path d="M12 42 Q16.5 40.5 21 42 M12 45 Q16.5 43.5 21 45 M27 42 Q31.5 40.5 36 42 M27 45 Q31.5 43.5 36 45" stroke="#B9B5D6" stroke-width="1" fill="none"/>'+star(41,9,'#FFD84D')+star(6,16,'#FFD84D')
    if m=='gym': return f'<path d="M9 43 H39" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/><rect x="5" y="37" width="5" height="12" rx="2" fill="#FF5C7A" stroke="{INK}" stroke-width="1.2"/><rect x="38" y="37" width="5" height="12" rx="2" fill="#FF5C7A" stroke="{INK}" stroke-width="1.2"/><path d="M40 14 Q37.5 18 40 20 Q42.5 18 40 14Z" fill="#7DD3FC"/>'
    if m=='dinner': return f'<path d="M16 38 Q13.5 35 16 32 Q18.5 29 16 26 M32 38 Q29.5 35 32 32 Q34.5 29 32 26" stroke="#B9B5D6" stroke-width="1.8" stroke-linecap="round" fill="none"/><path d="M11 40 H37 Q37 49 24 49 Q11 49 11 40Z" fill="#fff" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/><path d="M15 42.5 Q24 45 33 42.5" stroke="#FFB86B" stroke-width="2" stroke-linecap="round" fill="none"/>'
    if m=='dnd':
        z='<path d="M0 0 h5 l-5 5.5 h5" stroke="%s" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'%INK
        return f'<g transform="translate(31 20) scale(.8)">{z}</g><g transform="translate(35 13) scale(1)">{z}</g><g transform="translate(39 5) scale(1.2)">{z}</g>'
    if m=='busy': return '<circle cx="34" cy="9" r="2" fill="#8E8AA8"/><circle cx="39" cy="9" r="2" fill="#8E8AA8"/><circle cx="44" cy="9" r="2" fill="#8E8AA8"/>'
    return star(41,9,'#FFD84D')+star(6,14,'#FF8FA8')
def ch(i,m,size,label):
    k=size/48
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" aria-label="{label}">'
      f'<circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{BG[i]}"/>'
      f'<g transform="scale({k:.4f})">{ears(i,BODY[i])}<ellipse cx="24" cy="30" rx="16.5" ry="15" fill="{BODY[i]}"/>{face(m)}{props(m)}</g></svg>')
