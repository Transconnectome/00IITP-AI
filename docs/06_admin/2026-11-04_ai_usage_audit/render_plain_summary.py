import os
os.environ.setdefault('SOURCE_DATE_EPOCH', '1700000000')
from pathlib import Path
import markdown,fitz,hashlib,json
from weasyprint import HTML
r=Path(__file__).resolve().parent
body=markdown.markdown((r/'summary_plain_v3.md').read_text(),extensions=['tables'])
css='''@page{size:A4;margin:12mm 14mm 11mm;@bottom-right{content:"1 / 1";font-size:7pt;color:#657580}}body{font-family:"Noto Sans CJK KR",sans-serif;color:#243b44;font-size:9.3pt;line-height:1.44}h1{font-size:18pt;color:#173e4d;margin:0 0 4px;border-bottom:2.5px solid #167c80;padding-bottom:5px}h2{font-size:10.8pt;color:#167c80;margin:9px 0 3px}p{margin:4.5px 0}blockquote{margin:6px 0;padding:6px 10px;background:#edf5f3;border-left:3px solid #167c80;font-size:8.7pt;line-height:1.36}blockquote p{margin:1px 0}table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:8.5pt;line-height:1.32;margin:6px 0}th{background:#173e4d;color:white;text-align:left;padding:5px 7px}th:first-child{width:32%}td{padding:5px 7px;border-bottom:1px solid #d5e0e3;vertical-align:top}tr:nth-child(even){background:#f1f6f7}strong{font-weight:700}code{font-family:"DejaVu Sans Mono",monospace;font-size:7.5pt}body>p:last-child{font-size:7.7pt;color:#61727b;border-top:1px solid #c7d5da;padding-top:5px;margin-top:7px;line-height:1.32}'''
s='<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>AI 서비스 과제 연구 활용 소명서</title><style>'+css+'</style></head><body>'+body+'</body></html>'
(r/'summary_plain_v3.html').write_text(s)
p=r/'연구용_AI서비스_활용소명서_쉬운설명_1쪽.pdf';HTML(string=s,base_url=str(r)).write_pdf(p)
d=fitz.open(p);print('pages',len(d));assert len(d)==1
for b in d[0].get_text('blocks'):assert 0<=b[0]<b[2]<=d[0].rect.width and 0<=b[1]<b[3]<=d[0].rect.height
(r/'preview').mkdir(exist_ok=True);d[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(r/'preview/summary_plain_v3.png');print('PASS: one A4 page; text within bounds')

# Recompute PLAIN_V3_SHA256SUMS
manifest_files = [
    '연구용_AI서비스_활용소명서_쉬운설명_1쪽.pdf',
    'summary_plain_v3.md',
    'summary_plain_v3.html'
]
lines = []
for fn in manifest_files:
    h = hashlib.sha256((r / fn).read_bytes()).hexdigest()
    lines.append(f'{h}  {fn}')
(r / 'PLAIN_V3_SHA256SUMS').write_text('\n'.join(lines) + '\n')

# Sync review_candidate_sha256 in delivery_status.json
status_file = r / 'delivery_status.json'
if status_file.exists():
    try:
        data = json.loads(status_file.read_text())
        data['review_candidate_sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
        status_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    except Exception as e:
        print(f'Warning: delivery_status.json update skipped: {e}')
print('PASS: PLAIN_V3_SHA256SUMS and delivery_status.json updated')

