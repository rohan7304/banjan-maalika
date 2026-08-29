import os

os.makedirs('assets/images', exist_ok=True)

# 1. Ganesha SVG
ganesha_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <radialGradient id="g_bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFF3E0"/>
      <stop offset="70%" stop-color="#FFE0B2"/>
      <stop offset="100%" stop-color="#FFB74D"/>
    </radialGradient>
    <linearGradient id="g_gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE082"/>
      <stop offset="50%" stop-color="#FFA000"/>
      <stop offset="100%" stop-color="#FF6F00"/>
    </linearGradient>
    <linearGradient id="g_red" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF5252"/>
      <stop offset="100%" stop-color="#C62828"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#g_bg)" stroke="#E65100" stroke-width="4"/>
  <circle cx="100" cy="100" r="88" fill="none" stroke="#FFA000" stroke-width="1.5" stroke-dasharray="4,4"/>
  <!-- Crown / Mukut -->
  <path d="M70 65 L100 20 L130 65 Z" fill="url(#g_gold)" stroke="#B71C1C" stroke-width="2"/>
  <path d="M85 45 L100 22 L115 45 Z" fill="url(#g_red)"/>
  <circle cx="100" cy="40" r="5" fill="#FFF"/>
  <circle cx="100" cy="20" r="4" fill="#FFD54F"/>
  <!-- Ears -->
  <path d="M60 75 C30 65 25 110 55 120 C65 115 65 95 60 75 Z" fill="#FFA726" stroke="#E65100" stroke-width="2"/>
  <path d="M140 75 C170 65 175 110 145 120 C135 115 135 95 140 75 Z" fill="#FFA726" stroke="#E65100" stroke-width="2"/>
  <!-- Head & Trunk -->
  <path d="M65 75 C65 60 135 60 135 75 C135 110 118 120 115 145 C112 165 130 170 135 160 C138 152 130 148 122 152 C115 156 112 142 110 125 C105 95 95 85 65 75 Z" fill="#FFB74D" stroke="#E65100" stroke-width="2.5"/>
  <!-- Tilak -->
  <path d="M92 68 Q100 60 108 68 Q100 75 92 68 Z" fill="url(#g_red)"/>
  <line x1="88" y1="65" x2="112" y2="65" stroke="#FFE082" stroke-width="2"/>
  <line x1="90" y1="70" x2="110" y2="70" stroke="#FFE082" stroke-width="2"/>
  <circle cx="100" cy="62" r="3" fill="#D50000"/>
  <!-- Eyes -->
  <path d="M78 80 Q85 76 90 82" stroke="#3E2723" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M110 82 Q115 76 122 80" stroke="#3E2723" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <!-- Tusk -->
  <path d="M85 115 L68 122 L83 125 Z" fill="#FFF" stroke="#E0E0E0" stroke-width="1"/>
  <!-- Modak -->
  <circle cx="60" cy="140" r="16" fill="url(#g_gold)" stroke="#FF6F00" stroke-width="1.5"/>
  <path d="M60 126 L64 140 L56 140 Z" fill="#FFF8E1"/>
  <!-- Om symbol -->
  <text x="100" y="186" font-size="16" font-family="'Rozha One', serif" font-weight="bold" fill="#B71C1C" text-anchor="middle">श्री गणेश</text>
</svg>"""

with open('assets/images/ganesha.svg', 'w', encoding='utf-8') as f:
    f.write(ganesha_svg)

# 2. Vitthal SVG
vitthal_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <radialGradient id="v_bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFF8E1"/>
      <stop offset="70%" stop-color="#FFECB3"/>
      <stop offset="100%" stop-color="#FFE082"/>
    </radialGradient>
    <linearGradient id="v_body" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#37474F"/>
      <stop offset="50%" stop-color="#212121"/>
      <stop offset="100%" stop-color="#121212"/>
    </linearGradient>
    <linearGradient id="v_gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF176"/>
      <stop offset="100%" stop-color="#F57F17"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#v_bg)" stroke="#F57F17" stroke-width="4"/>
  <circle cx="100" cy="100" r="88" fill="none" stroke="#FFA000" stroke-width="1.5" stroke-dasharray="4,4"/>
  <!-- Crown (Shivalinga Top / Mukut) -->
  <path d="M78 60 C78 30 122 30 122 60 Z" fill="url(#v_gold)" stroke="#E65100" stroke-width="2"/>
  <circle cx="100" cy="30" r="6" fill="#FFD54F"/>
  <circle cx="100" cy="45" r="4" fill="#D50000"/>
  <!-- Face -->
  <path d="M72 58 C70 95 80 115 100 115 C120 115 130 95 128 58 Z" fill="url(#v_body)" stroke="#263238" stroke-width="2"/>
  <!-- Kundal (Fish Shaped Earrings) -->
  <path d="M66 75 C55 85 55 105 68 112 C72 100 70 85 66 75 Z" fill="url(#v_gold)" stroke="#E65100" stroke-width="1.5"/>
  <path d="M134 75 C145 85 145 105 132 112 C128 100 130 85 134 75 Z" fill="url(#v_gold)" stroke="#E65100" stroke-width="1.5"/>
  <!-- White & Kasturi Tilak -->
  <path d="M88 65 Q100 80 112 65 Q100 72 88 65 Z" fill="#FFFFFF"/>
  <path d="M96 68 L104 68 L100 78 Z" fill="#D50000"/>
  <circle cx="100" cy="84" r="2.5" fill="#FFFFFF"/>
  <!-- Lotus Eyes -->
  <path d="M80 82 Q90 78 96 85 Q90 89 80 82 Z" fill="#FFFFFF"/>
  <circle cx="89" cy="83" r="2" fill="#212121"/>
  <path d="M120 82 Q110 78 104 85 Q110 89 120 82 Z" fill="#FFFFFF"/>
  <circle cx="111" cy="83" r="2" fill="#212121"/>
  <!-- Kaustubha Mani & Garland (Kanthi) -->
  <path d="M80 115 Q100 135 120 115" stroke="url(#v_gold)" stroke-width="4" fill="none"/>
  <circle cx="100" cy="128" r="5" fill="#D50000" stroke="#FFD54F" stroke-width="1"/>
  <!-- Tulsi Garland -->
  <path d="M72 120 Q100 155 128 120" stroke="#33691E" stroke-width="3" stroke-dasharray="3,3" fill="none"/>
  <!-- Hands on Hips (Kateshivare Haath) -->
  <path d="M62 135 C50 145 65 165 78 158" stroke="url(#v_body)" stroke-width="8" stroke-linecap="round" fill="none"/>
  <path d="M138 135 C150 145 135 165 122 158" stroke="url(#v_body)" stroke-width="8" stroke-linecap="round" fill="none"/>
  <!-- Brick (Veet) -->
  <rect x="75" y="166" width="50" height="10" rx="3" fill="#D84315" stroke="#BF360C" stroke-width="1.5"/>
  <text x="100" y="190" font-size="15" font-family="'Rozha One', serif" font-weight="bold" fill="#4E342E" text-anchor="middle">श्री विठ्ठल</text>
</svg>"""

with open('assets/images/vitthal.svg', 'w', encoding='utf-8') as f:
    f.write(vitthal_svg)

# 3. Durga SVG
durga_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <radialGradient id="d_bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFEBEE"/>
      <stop offset="70%" stop-color="#FFCDD2"/>
      <stop offset="100%" stop-color="#EF9A9A"/>
    </radialGradient>
    <linearGradient id="d_red" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF1744"/>
      <stop offset="100%" stop-color="#B71C1C"/>
    </linearGradient>
    <linearGradient id="d_gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF59D"/>
      <stop offset="100%" stop-color="#FBC02D"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#d_bg)" stroke="#C62828" stroke-width="4"/>
  <circle cx="100" cy="100" r="88" fill="none" stroke="#D32F2F" stroke-width="1.5" stroke-dasharray="4,4"/>
  <!-- Crown / Mukut -->
  <path d="M65 65 L100 25 L135 65 Z" fill="url(#d_gold)" stroke="#C62828" stroke-width="2"/>
  <circle cx="100" cy="22" r="5" fill="#D50000"/>
  <circle cx="100" cy="45" r="4" fill="#D50000"/>
  <circle cx="82" cy="55" r="3" fill="#D50000"/>
  <circle cx="118" cy="55" r="3" fill="#D50000"/>
  <!-- Face -->
  <path d="M72 65 C70 100 80 118 100 118 C120 118 130 100 128 65 Z" fill="#FFE0B2" stroke="#FFA726" stroke-width="1.5"/>
  <!-- Third Eye (Trinetra) -->
  <path d="M96 68 Q100 60 104 68 Q100 76 96 68 Z" fill="url(#d_red)"/>
  <!-- Red Bindi & Chandrakor -->
  <circle cx="100" cy="62" r="4" fill="#B71C1C"/>
  <path d="M94 58 Q100 54 106 58 Q100 56 94 58 Z" fill="#B71C1C"/>
  <!-- Eyes -->
  <path d="M76 80 Q88 74 96 84 Q88 88 76 80 Z" fill="#FFF"/>
  <circle cx="87" cy="81" r="2.5" fill="#212121"/>
  <path d="M124 80 Q112 74 104 84 Q112 88 124 80 Z" fill="#FFF"/>
  <circle cx="113" cy="81" r="2.5" fill="#212121"/>
  <!-- Nose Ring (Nath) -->
  <circle cx="94" cy="94" r="5" fill="none" stroke="url(#d_gold)" stroke-width="2"/>
  <circle cx="91" cy="94" r="2" fill="#D50000"/>
  <circle cx="97" cy="94" r="2" fill="#00E676"/>
  <!-- Trishul Motif Background -->
  <path d="M42 90 L52 75 L52 140 L42 140 Z" fill="url(#d_gold)" opacity="0.8"/>
  <path d="M158 90 L148 75 L148 140 L158 140 Z" fill="url(#d_gold)" opacity="0.8"/>
  <!-- Lotus -->
  <path d="M90 145 C80 130 100 120 100 135 C100 120 120 130 110 145 Z" fill="#F06292"/>
  <text x="100" y="184" font-size="15" font-family="'Rozha One', serif" font-weight="bold" fill="#B71C1C" text-anchor="middle">श्री दुर्गा देवी</text>
</svg>"""

with open('assets/images/durga.svg', 'w', encoding='utf-8') as f:
    f.write(durga_svg)

# 4. Sai Baba / Datta SVG
sai_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <radialGradient id="s_bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFDE7"/>
      <stop offset="70%" stop-color="#FFF9C4"/>
      <stop offset="100%" stop-color="#FFF59D"/>
    </radialGradient>
    <linearGradient id="s_cloth" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF9800"/>
      <stop offset="100%" stop-color="#E65100"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#s_bg)" stroke="#E65100" stroke-width="4"/>
  <circle cx="100" cy="100" r="88" fill="none" stroke="#FB8C00" stroke-width="1.5" stroke-dasharray="4,4"/>
  <!-- Head Cloth (Kafni / Pagdi) -->
  <path d="M68 65 C68 35 132 35 132 65 C135 80 130 85 130 90 L70 90 C70 85 65 80 68 65 Z" fill="url(#s_cloth)" stroke="#BF360C" stroke-width="1.5"/>
  <path d="M65 65 Q100 78 135 65" stroke="#FFE0B2" stroke-width="3" fill="none"/>
  <!-- Face -->
  <path d="M72 70 C70 100 80 115 100 115 C120 115 130 100 128 70 Z" fill="#FFE0B2"/>
  <!-- White Beard -->
  <path d="M74 95 C75 140 125 140 126 95 C118 115 82 115 74 95 Z" fill="#FAFAFA" stroke="#E0E0E0" stroke-width="1"/>
  <!-- Compassionate Eyes -->
  <path d="M80 82 Q88 78 94 84" stroke="#424242" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M120 82 Q112 78 106 84" stroke="#424242" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <!-- Tilak -->
  <circle cx="100" cy="72" r="3" fill="#E65100"/>
  <line x1="94" y1="69" x2="106" y2="69" stroke="#E65100" stroke-width="1.5"/>
  <!-- Robe (Kafni) -->
  <path d="M50 145 Q100 120 150 145 L155 175 L45 175 Z" fill="url(#s_cloth)"/>
  <!-- Shlok/Blessing text -->
  <text x="100" y="190" font-size="14" font-family="'Rozha One', serif" font-weight="bold" fill="#BF360C" text-anchor="middle">श्री साई / दत्त</text>
</svg>"""

with open('assets/images/sai.svg', 'w', encoding='utf-8') as f:
    f.write(sai_svg)

# 5. Diya / Aarti SVG
diya_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <radialGradient id="diya_bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFF8E1"/>
      <stop offset="70%" stop-color="#FFECB3"/>
      <stop offset="100%" stop-color="#FFD54F"/>
    </radialGradient>
    <radialGradient id="flame" cx="50%" cy="60%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="30%" stop-color="#FFEE58"/>
      <stop offset="70%" stop-color="#FF9800"/>
      <stop offset="100%" stop-color="#D50000"/>
    </radialGradient>
    <linearGradient id="brass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE082"/>
      <stop offset="50%" stop-color="#FFA000"/>
      <stop offset="100%" stop-color="#E65100"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#diya_bg)" stroke="#FF8F00" stroke-width="4"/>
  <circle cx="100" cy="100" r="88" fill="none" stroke="#FF6F00" stroke-width="1.5" stroke-dasharray="4,4"/>
  <!-- Aura / Glow -->
  <circle cx="100" cy="70" r="38" fill="rgba(255, 179, 0, 0.25)"/>
  <!-- Flame -->
  <path d="M100 28 C90 50 82 65 85 80 C88 95 112 95 115 80 C118 65 110 50 100 28 Z" fill="url(#flame)"/>
  <circle cx="100" cy="78" r="8" fill="#FFFDE7"/>
  <!-- Diya Lamp Base -->
  <path d="M55 95 C55 135 145 135 145 95 Q100 115 55 95 Z" fill="url(#brass)" stroke="#BF360C" stroke-width="2"/>
  <!-- Stand -->
  <path d="M92 120 L80 155 L120 155 L108 120 Z" fill="url(#brass)" stroke="#BF360C" stroke-width="1.5"/>
  <ellipse cx="100" cy="155" rx="35" ry="8" fill="url(#brass)" stroke="#BF360C" stroke-width="2"/>
  <text x="100" y="186" font-size="15" font-family="'Rozha One', serif" font-weight="bold" fill="#BF360C" text-anchor="middle">नित्य आरती</text>
</svg>"""

with open('assets/images/diya_aarti.svg', 'w', encoding='utf-8') as f:
    f.write(diya_svg)

# 6. Krishna SVG
krishna_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <radialGradient id="k_bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#E1F5FE"/>
      <stop offset="70%" stop-color="#B3E5FC"/>
      <stop offset="100%" stop-color="#81D4FA"/>
    </radialGradient>
    <linearGradient id="k_feather" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00E676"/>
      <stop offset="40%" stop-color="#00B0FF"/>
      <stop offset="80%" stop-color="#651FFF"/>
      <stop offset="100%" stop-color="#D50000"/>
    </linearGradient>
    <linearGradient id="k_gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF59D"/>
      <stop offset="100%" stop-color="#FBC02D"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#k_bg)" stroke="#0288D1" stroke-width="4"/>
  <circle cx="100" cy="100" r="88" fill="none" stroke="#039BE5" stroke-width="1.5" stroke-dasharray="4,4"/>
  <!-- Peacock Feather (Mor Pankh) -->
  <path d="M100 20 C85 30 75 55 100 70 C125 55 115 30 100 20 Z" fill="url(#k_feather)" stroke="#FFD54F" stroke-width="1.5"/>
  <ellipse cx="100" cy="45" rx="10" ry="14" fill="#00B0FF"/>
  <ellipse cx="100" cy="46" rx="6" ry="8" fill="#651FFF"/>
  <circle cx="100" cy="46" r="3" fill="#D50000"/>
  <!-- Crown / Hair -->
  <circle cx="100" cy="72" r="16" fill="#1A237E"/>
  <path d="M80 75 L120 75 L100 60 Z" fill="url(#k_gold)"/>
  <!-- Flute (Bansuri) -->
  <g transform="rotate(-25 100 120)">
    <rect x="40" y="115" width="120" height="12" rx="4" fill="url(#k_gold)" stroke="#E65100" stroke-width="1.5"/>
    <circle cx="70" cy="121" r="2.5" fill="#3E2723"/>
    <circle cx="85" cy="121" r="2.5" fill="#3E2723"/>
    <circle cx="100" cy="121" r="2.5" fill="#3E2723"/>
    <circle cx="115" cy="121" r="2.5" fill="#3E2723"/>
    <circle cx="130" cy="121" r="2.5" fill="#3E2723"/>
    <!-- Ghungroo / Tassel -->
    <path d="M150 125 L158 145" stroke="#D50000" stroke-width="2"/>
    <circle cx="158" cy="148" r="4" fill="#FFD54F"/>
  </g>
  <text x="100" y="186" font-size="15" font-family="'Rozha One', serif" font-weight="bold" fill="#0D47A1" text-anchor="middle">श्री कृष्ण</text>
</svg>"""

with open('assets/images/krishna.svg', 'w', encoding='utf-8') as f:
    f.write(krishna_svg)

print("Created all 6 deity SVGs successfully!")
