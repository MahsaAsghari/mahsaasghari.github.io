#!/usr/bin/env python3
"""The public image assets are already prepared; no private source PDF is shipped."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'assets/asset-manifest.json').read_text())
missing=[item['file'] for item in manifest if not (ROOT/item['file']).is_file()]
if missing:raise SystemExit('Missing assets: '+', '.join(missing))
print('The public publication figures and laboratory portrait are ready.')
