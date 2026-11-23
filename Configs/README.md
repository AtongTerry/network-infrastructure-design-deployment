# Configs

Device configurations for the lab, kept two ways:

| Path | What it is | Edit it? |
|---|---|---|
| `*.txt` (this folder) | **As-built** configs, one per device, with placeholders for secrets. Paste these into Packet Tracer. | No, regenerate |
| `templates/` | Jinja2 templates: the *shape* of each config type (access switch, core, edge router, branch router, ISP) | Yes |
| `variables/` | One YAML file per device (IPs, VLANs, ports) plus `globals.yml` (domain, NTP, syslog) | Yes |
| `secrets.example.yml` | The placeholder secrets used in committed configs | Only to add keys |
| `render_configs.py` | Builds the `.txt` files from templates + variables | Run it |

## Regenerate

```bash
pip install jinja2 pyyaml
python render_configs.py --out .          # rewrites the .txt files in this folder
git diff --stat                           # shows exactly what a change touched
```

For a private lab build with real passwords (never commit the output):

```bash
cp secrets.example.yml secrets.yml        # then edit the values; secrets.yml is git-ignored
python render_configs.py --secrets secrets.yml --out build/ # install yaml and jinja2 first (pip install pyyaml, pip install jinja2 )
```

## Change workflow
1. Edit a variables file (for example move a printer range on `BLD1-ACC-02.yml`).
2. Run `render_configs.py --out .`.
3. Review `git diff`, paste into Packet Tracer, test, commit.

Placeholders `{{ENABLE_SECRET}}`, `{{ADMIN_SECRET}}` and `{{OSPF_KEY}}` appear in the committed configs on purpose.
The core ACLs are in `templates/core-acls.j2` as static text.
