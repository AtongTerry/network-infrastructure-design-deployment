#!/usr/bin/env python3
"""Render every device config from templates/ + variables/.

Usage:
  python render_configs.py                   # placeholders only (safe to commit)
  python render_configs.py --secrets secrets.yml --out build/   # real lab secrets, do NOT commit
"""
import argparse, pathlib, sys
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = pathlib.Path(__file__).parent
ap = argparse.ArgumentParser()
ap.add_argument('--secrets', default=str(ROOT / 'secrets.example.yml'))
ap.add_argument('--out', default=str(ROOT / 'rendered'))
args = ap.parse_args()

load = lambda p: yaml.safe_load(open(p))
g = load(ROOT / 'variables' / 'globals.yml')
s = load(args.secrets)
env = Environment(loader=FileSystemLoader(ROOT / 'templates'),
                  undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True,
                  keep_trailing_newline=True)
out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)

for vf in sorted((ROOT / 'variables').glob('*.yml')):
    if vf.name == 'globals.yml':
        continue
    v = load(vf)
    tmpl = env.get_template(v.pop('template'))
    text = tmpl.render(g=g, s=s, **v)
    (out / f"{v['hostname']}.txt").write_text(text.rstrip('\n') + '\n')
    print('rendered', v['hostname'])
