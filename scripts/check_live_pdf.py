#!/usr/bin/env python3
"""Validate the live GitHub Pages PDF against the same job's produced bytes."""
import hashlib,time,sys,urllib.request
from pathlib import Path
local=Path(sys.argv[1])
base='https://aipmandy.github.io/seo-handbook/'
wanted=hashlib.sha256(local.read_bytes()).hexdigest()
for attempt in range(16):
    try:
        with urllib.request.urlopen(base+'pdf/seo-handbook-guide.pdf',timeout=25) as r:
            data=r.read();code=r.status
        with urllib.request.urlopen(base,timeout=25) as r:
            homepage=r.read().decode('utf-8');homecode=r.status
        got=hashlib.sha256(data).hexdigest()
        if code==200 and homecode==200 and got==wanted and 'pdf/seo-handbook-guide.pdf' in homepage:
            print('LIVE PASS: homepage/PDF 200; pdf SHA-256='+got+'; homepage download CTA found')
            break
        print(f'Attempt {attempt+1}: homepage={homecode}, pdf={code}, sha_match={got==wanted}')
    except Exception as ex:
        print(f'Attempt {attempt+1}: {ex}')
    if attempt==15:raise SystemExit('Live Pages PDF not verified')
    time.sleep(10)
