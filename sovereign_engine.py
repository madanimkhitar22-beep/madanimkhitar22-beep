#!/usr/bin/env python3
"""
Sovereign Engine v2.0 (Minimal & Sharp)
Generates a compact, live SVG reflecting the new V2.0 README structure.
"""

import json
import re
import datetime
import urllib.request
import os

class SovereignEngine:
    def __init__(self, madi_file="profile.madi", output="sovereign_node.svg"):
        self.madi_file = madi_file
        self.output = output
        self.config = self._parse_madi()
        
        self.width = 900
        self.height = 520
        self.bg = self.config.get("LiveTerminal", {}).get("bg_color", "#000000")
        self.accent = self.config.get("LiveTerminal", {}).get("accent_color", "#4AF626")
        self.pillars = self.config.get("LiveTerminal", {}).get("pillars", [])
        self.architect = self.config.get("Architect", {})

    def _parse_madi(self):
        config = {}
        try:
            with open(self.madi_file, 'r', encoding='utf-8') as f:
                content = f.read()
            blocks = re.findall(r'(\w+)\s*\{([^}]+)\}', content, re.DOTALL)
            for block_name, block_content in blocks:
                data = {}
                for line in block_content.strip().split('\n'):
                    line = line.strip().rstrip(',')
                    if ':' in line:
                        key, val = line.split(':', 1)
                        key = key.strip()
                        val = val.strip().strip('"').strip('[]')
                        if '"' in val:
                            val = [v.strip().strip('"') for v in val.split(',')]
                        data[key] = val
                config[block_name] = data
        except Exception as e:
            print(f"[WARN] Parse error: {e}")
        return config

    def fetch_live_activity(self):
        """Fetches latest public push event"""
        url = "https://api.github.com/users/madanimkhitar22-beep/events/public"
        req = urllib.request.Request(url, headers={'User-Agent': 'Sovereign-Engine/2.0'})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                events = json.loads(response.read().decode())
                for event in events:
                    if event.get('type') == 'PushEvent':
                        repo = event['repo']['name'].split('/')[-1]
                        msg = event['payload']['commits'][0]['message'].split('\n')[0]
                        msg = msg.replace('<', '&lt;').replace('>', '&gt;')[:45]
                        return f"→ {repo}: {msg}"
        except Exception:
            return "Node in stealth mode"
        return "Awaiting directives"

    def generate_svg(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        live_activity = self.fetch_live_activity()
        
        safe_arch = {k: str(v).replace('<', '&lt;').replace('>', '&gt;') 
                     for k, v in self.architect.items()}
        
        # Compact, sharp layout matching V2.0 README
        lines = [
            ("═══ LIVE SOVEREIGN NODE v2.0 ═══", None, True),
            (f"[{safe_arch.get('id', 'SOURCE_ARCHITECT')}] {safe_arch.get('location', 'TETOUAN, MOROCCO')}", None, False),
            (f"[HW] {safe_arch.get('hardware', 'Dedicated Sovereign Workstation')}", "ACTIVE", False),
            (" ", None, False),
            ("⬛ THE SOVEREIGN STACK", None, True),
            ("  🧠 MadiLang         │ v0.5.4 │ PyPI │ Intent-driven language", None, False),
            ("  🛡️ SCE               │ Active │ 5 Ethical Gates │ AI Guardrail", None, False),
            ("  🔒 Sovereign-DevKit  │ v3.1.0 │ 35+ Patterns │ Secret Scanner", None, False),
            ("  🌊 Fayd Protocol     │ Phase 0│ Rust/WASM │ Verifiable Compute", None, False),
            (" ", None, False),
            ("🔷 RESEARCH CONTRIBUTIONS (Pi Network Proposals)", None, True),
            ("  PiTrust │ PiNet-OS │ PiStorage │ PiBridge │ PiQuantum-Nexus", None, False),
            ("  Status: Conceptual architectures for community peer review", None, False),
            (" ", None, False),
            (f"[SYNC] {live_activity}", "LIVE" if "→" in live_activity else None, False),
            (f"[TIME] {now}", None, False),
        ]

        y = 55
        delay = 0.0
        text_elements = []
        
        for text, highlight, is_title in lines:
            if is_title:
                svg_text = f'<text x="20" y="{y}" class="title line" style="animation-delay:{delay}s">{text}</text>'
            elif highlight:
                clean = text.replace(highlight, "")
                svg_text = f'<text x="20" y="{y}" class="line" style="animation-delay:{delay}s">{clean}<tspan class="accent">{highlight}</tspan></text>'
            else:
                svg_text = f'<text x="20" y="{y}" class="line" style="animation-delay:{delay}s">{text}</text>'
            
            text_elements.append(svg_text)
            y += 22 if not is_title else 28
            delay += 0.25

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="100%">
    <defs>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&amp;family=Orbitron:wght@700&amp;display=swap');
            .bg {{ fill: {self.bg}; stroke: #333; stroke-width: 2px; rx: 8px; }}
            .title {{ font-family: 'Orbitron', sans-serif; font-size: 14px; fill: {self.accent}; font-weight: 700; letter-spacing: 0.5px; }}
            .line {{ font-family: 'Fira Code', monospace; font-size: 12.5px; fill: #ddd; opacity: 0; animation: reveal 0.1s forwards; }}
            .accent {{ fill: {self.accent}; font-weight: bold; }}
            .cursor {{ animation: blink 1s step-end infinite; fill: {self.accent}; }}
            @keyframes reveal {{ to {{ opacity: 1; }} }}
            @keyframes blink {{ 50% {{ opacity: 0; }} }}
        </style>
    </defs>
    
    <rect width="{self.width}" height="{self.height}" class="bg"/>
    <text x="20" y="30" class="title" style="opacity:1;font-size:15px;">[ MKHITARIAN ONTOLOGY v2.0 • MINIMAL &amp; SHARP ]</text>
    <line x1="20" y1="42" x2="{self.width-20}" y2="42" stroke="#333" stroke-width="1"/>
    
    {''.join(text_elements)}
    
    <text x="20" y="{y+8}" class="line cursor" style="animation-delay:{delay}s">_</text>
</svg>"""
        
        with open(self.output, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f"[+] Sovereign Node Updated (V2.0): {self.output}")

if __name__ == "__main__":
    engine = SovereignEngine()
    engine.generate_svg()
