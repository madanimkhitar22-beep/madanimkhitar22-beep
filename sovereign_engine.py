#!/usr/bin/env python3
"""
Sovereign Engine v1.0
Generates a Live Animated Terminal SVG from profile.madi
Built with Intent by El Madani El Mkhitar
"""

import json
import re
import datetime
import os

class SovereignEngine:
    def __init__(self, madi_file="profile.madi", output="sovereign_node.svg"):
        self.madi_file = madi_file
        self.output = output
        self.config = self._parse_madi()
        
        # Safe defaults if parsing fails
        self.width = 850
        self.height = 420
        self.bg = self.config.get("LiveTerminal", {}).get("bg_color", "#000000")
        self.accent = self.config.get("LiveTerminal", {}).get("accent_color", "#4AF626")
        self.pillars = self.config.get("LiveTerminal", {}).get("pillars", [])
        self.architect = self.config.get("Architect", {})

    def _parse_madi(self):
        """Simple parser for our custom Madi.DSL structure"""
        config = {}
        try:
            with open(self.madi_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract blocks using regex (lightweight, no external deps)
            blocks = re.findall(r'(\w+)\s*\{([^}]+)\}', content, re.DOTALL)
            for block_name, block_content in blocks:
                data = {}
                # Simple key-value extraction
                for line in block_content.strip().split('\n'):
                    line = line.strip().rstrip(',')
                    if ':' in line:
                        key, val = line.split(':', 1)
                        key = key.strip()
                        val = val.strip().strip('"').strip('[]')
                        # Handle lists roughly
                        if '"' in val:
                            val = [v.strip().strip('"') for v in val.split(',')]
                        data[key] = val
                config[block_name] = data
        except Exception as e:            print(f"[WARN] Could not parse {self.madi_file}: {e}. Using defaults.")
        return config

    def generate_svg(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Sanitize all text to prevent SVG injection (Al-Satr Compliance)
        safe_arch = {k: str(v).replace('<', '&lt;').replace('>', '&gt;') 
                     for k, v in self.architect.items()}
        
        lines = [
            ("[INIT] Bootstrapping Sovereign Node...", None),
            (f"[SCAN] Hardware: {safe_arch.get('hardware', 'Unknown')} -> ", "OK"),
            ("[WARN] Resource Constraint -> Engaging 'Proof of Friction'", None),
            (f"[LINK] Pi Network Infrastructure Layer -> ", "SYNCED"),
            ("[VERIFY] Intent Signature: VALID (Al-Satr Compliant)", None),
            (f"[TIME] Node Time: {now}", None),
            (" ", None),
            ("> Loading Philosophical Pillars:", None),
        ]
        
        # Add pillars dynamically from Madi file
        for p in self.pillars:
            safe_p = str(p).replace('<', '&lt;').replace('>', '&gt;')
            lines.append((f"  ├── {safe_p}", None))
            
        lines.append((" ", None))
        lines.append(("> System is ALIVE. Awaiting architectural directives...", "ALIVE"))

        # Build SVG Elements
        y = 70
        delay = 0.0
        text_elements = []
        
        for text, highlight in lines:
            if highlight:
                clean = text.replace(highlight, "")
                svg_text = f'<text x="20" y="{y}" class="line" style="animation-delay:{delay}s">{clean}<tspan class="accent">{highlight}</tspan></text>'
            else:
                svg_text = f'<text x="20" y="{y}" class="line" style="animation-delay:{delay}s">{text}</text>'
            
            text_elements.append(svg_text)
            y += 24
            delay += 0.35

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="100%">
    <defs>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&amp;family=Orbitron:wght@700&amp;display=swap');
            .bg {{ fill: {self.bg}; stroke: #333; stroke-width: 2px; rx: 8px; }}            .title {{ font-family: 'Orbitron', sans-serif; font-size: 16px; fill: #fff; font-weight: 700; letter-spacing: 1px; }}
            .line {{ font-family: 'Fira Code', monospace; font-size: 13px; fill: #ccc; opacity: 0; animation: reveal 0.1s forwards; }}
            .accent {{ fill: {self.accent}; font-weight: bold; }}
            .cursor {{ animation: blink 1s step-end infinite; fill: {self.accent}; }}
            @keyframes reveal {{ to {{ opacity: 1; }} }}
            @keyframes blink {{ 50% {{ opacity: 0; }} }}
        </style>
    </defs>
    
    <rect width="{self.width}" height="{self.height}" class="bg"/>
    <text x="20" y="35" class="title">[ MKHITARIAN ONTOLOGY v2.0 - LIVE NODE ]</text>
    <line x1="20" y1="48" x2="{self.width-20}" y2="48" stroke="#333" stroke-width="1"/>
    
    {''.join(text_elements)}
    
    <text x="20" y="{y+15}" class="line cursor" style="animation-delay:{delay}s">_</text>
</svg>"""
        
        with open(self.output, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f"[+] Sovereign Node Updated: {self.output}")

if __name__ == "__main__":
    engine = SovereignEngine()
    engine.generate_svg()
