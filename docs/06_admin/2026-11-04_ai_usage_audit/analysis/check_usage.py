#!/usr/bin/env python3
"""Validate arithmetic and retained-period boundaries; does not validate billing attribution."""
import importlib.util,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('audit_usage',ROOT/'aggregate_usage.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
v=dict.fromkeys(m.FIELDS,0);v.update(input_uncached=10,cache_read=90,output=20,reasoning_subset=5)
d={};m.put(d,'a','test','2026-10-01T00:00:00+09:00',v,'s',False);m.put(d,'a','test','2026-10-01T00:00:01+09:00',v,'s',False)
r=m.aggregate(d,{})['periods']['october_2026'];assert r['totals']['total_processed']==120;assert r['totals']['requests']==1;assert r['duplicate_records_merged']==1
m.put(d,'b','<synthetic>','2026-10-01T00:00:00+09:00',dict.fromkeys(m.FIELDS,0),'z',False);assert m.aggregate(d,{})['periods']['october_2026']['totals']['requests']==1
assert m.stamp('2026-09-30T16:00:00Z').startswith('2026-10-01')
for f in [ROOT/'claude_deduplicated.json',ROOT/'codex_deduplicated.json']:
 data=json.loads(f.read_text())
 for provider in data['providers'].values():
  for period in provider['periods'].values():
   t=period['totals']
   if not t:continue
   assert t['total_processed']==sum(t[k] for k in m.FIELDS if k!='reasoning_subset')
   assert t['total_processed']==sum(x['total_processed'] for x in period['models'].values())
   assert t['total_processed']==sum(x['total_processed'] for x in period['daily'].values())
   assert all(period['start_inclusive']<=x<period['end_exclusive'] for x in period['daily'])
print('PASS: subset accounting; duplicate responses; synthetic exclusion; KST boundary; model/day/total arithmetic')
