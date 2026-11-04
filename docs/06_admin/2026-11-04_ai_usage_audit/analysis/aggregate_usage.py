#!/usr/bin/env python3
"""Read local usage metadata only. Write aggregates, never conversation contents.
Claude: global message-ID/model dedupe; take max counters for split/stream records.
Codex: global response-ID dedupe, usage only (not cumulative turn/thread counters).
Codex cached and reasoning are subsets, not additions. Legacy token_count only
when no token_usage_record occurs anywhere in that file, using cumulative deltas.
Periods are KST. Local account/device coverage is not grant cost attribution.
"""
import argparse, collections, datetime as dt, hashlib, json, pathlib
P=pathlib.Path; KST=dt.timezone(dt.timedelta(hours=9))
FIELDS=['input_uncached','cache_write_5m','cache_write_1h','cache_write_unknown','cache_read','output','reasoning_subset']
def stamp(s):
 try:return dt.datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(KST).isoformat()
 except:return ''
def relevant(s): return bool(s and '2026-04-01'<=s[:10]<'2026-11-01')
def put(store,key,model,ts,vals,sid,iitp):
 if key in store:
  old=store[key]; old['copies']+=1
  old['different_values']+=int(old['values']!=vals)
  old['values']={k:max(v,old['values'][k]) for k,v in vals.items()}
  # Final observed usage is attached to the latest split record timestamp.
  old['timestamp']=max(old['timestamp'],ts);old['iitp']=old['iitp'] or iitp
 else:store[key]={'model':model,'timestamp':ts,'values':vals,'sid':sid,'iitp':iitp,'copies':1,'different_values':0}
def claude(root):
 store={}; files=malformed=missing_id=0
 for f in root.rglob('*.jsonl'):
  files+=1
  for line in f.open(errors='replace'):
   if '"usage"' not in line:continue
   try:d=json.loads(line)
   except:malformed+=1;continue
   if d.get('type')!='assistant':continue
   ts=stamp(d.get('timestamp',''))
   if not relevant(ts):continue
   m=d.get('message') or {};u=m.get('usage') or {};mid=m.get('id');model=m.get('model') or 'unknown'
   if not mid or not u:missing_id+=1;continue
   cc=u.get('cache_creation') or {};v=dict.fromkeys(FIELDS,0)
   v.update(input_uncached=int(u.get('input_tokens') or 0),cache_read=int(u.get('cache_read_input_tokens') or 0),output=int(u.get('output_tokens') or 0))
   v['cache_write_5m']=int(cc.get('ephemeral_5m_input_tokens') or 0);v['cache_write_1h']=int(cc.get('ephemeral_1h_input_tokens') or 0)
   v['cache_write_unknown']=max(0,int(u.get('cache_creation_input_tokens') or 0)-v['cache_write_5m']-v['cache_write_1h'])
   v['reasoning_subset']=int((u.get('output_tokens_details') or {}).get('thinking_tokens') or 0)
   put(store,(mid,model),model,ts,v,d.get('sessionId'), '00IITP-AI' in str(f))
 return store,{'files_scanned':files,'malformed_candidates':malformed,'missing_id_or_usage':missing_id}
def codex(roots):
 store={}; files=0; legacy=0; malformed=0; mismatch=0; missing_id=0
 for root in roots:
  for f in root.rglob('*.jsonl'):
   files+=1; model='unknown';sid=f.stem;iitp=False;pending=[];native=False;prev={}
   for line in f.open(errors='replace'):
    # Avoid parsing conversation payloads.
    if not any('"type": "'+t+'"' in line or '"type":"'+t+'"' in line for t in ('session_meta','turn_context','token_usage_record','event_msg')):continue
    try:d=json.loads(line)
    except:malformed+=1;continue
    p=d.get('payload') or {};typ=d.get('type');ts=stamp(d.get('timestamp',''))
    if typ=='session_meta':sid=p.get('id') or sid;iitp='00IITP-AI' in (p.get('cwd') or '')
    if typ=='turn_context':model=p.get('model') or model;iitp='00IITP-AI' in (p.get('cwd') or '') or iitp
    if typ=='token_usage_record':
     native=True
     if not relevant(ts):continue
     u=p.get('usage') or {};rid=p.get('response_id')
     if not rid:missing_id+=1;continue
     if u.get('total_tokens',0)!=int(u.get('input_tokens') or 0)+int(u.get('output_tokens') or 0):mismatch+=1
     v=dict.fromkeys(FIELDS,0);v.update(input_uncached=max(0,int(u.get('input_tokens') or 0)-int(u.get('cached_input_tokens') or 0)),cache_read=int(u.get('cached_input_tokens') or 0),cache_write_unknown=int(u.get('cache_write_input_tokens') or 0),output=int(u.get('output_tokens') or 0),reasoning_subset=int(u.get('reasoning_output_tokens') or 0))
     put(store,rid,model,ts,v,p.get('thread_id') or sid,iitp)
    elif typ=='event_msg' and p.get('type')=='token_count':
     info=p.get('info') or {};u=info.get('total_token_usage') or {}
     delta={k:max(0,int(v or 0)-int(prev.get(k) or 0)) for k,v in u.items()};prev=u
     if not relevant(ts) or not any(delta.values()):continue
     v=dict.fromkeys(FIELDS,0);v.update(input_uncached=max(0,delta.get('input_tokens',0)-delta.get('cached_input_tokens',0)),cache_read=delta.get('cached_input_tokens',0),cache_write_unknown=delta.get('cache_write_input_tokens',0),output=delta.get('output_tokens',0),reasoning_subset=delta.get('reasoning_output_tokens',0))
     pending.append((('legacy',sid,tuple(sorted(u.items()))),model,ts,v,sid,iitp))
   if not native:
    for args in pending:put(store,*args);legacy+=1
 return store,{'files_scanned':files,'legacy_cumulative_deltas':legacy,'malformed_candidates':malformed,'usage_total_mismatch':mismatch,'missing_response_id':missing_id}
def aggregate(store,diag):
 result={}
 for name,start,end in [('audit_2026_04_01_to_09_30','2026-04-01','2026-10-01'),('october_2026','2026-10-01','2026-11-01')]:
  models=collections.defaultdict(collections.Counter);daily=collections.defaultdict(collections.Counter);iitp=collections.defaultdict(collections.Counter);sessions=set();ids=[];copies=diff=0
  for key,row in store.items():
   day=row['timestamp'][:10]
   if not(start<=day<end):continue
   v=row['values'];v={**v,'total_processed':sum(v[x] for x in FIELDS if x!='reasoning_subset'),'requests':1}
   models[row['model']].update(v);daily[day].update(v)
   if row['iitp']:iitp[row['model']].update(v)
   sessions.add(row['sid']);ids.append(hashlib.sha256(str(key).encode()).hexdigest());copies+=row['copies']-1;diff+=row['different_values']
  total=collections.Counter()
  for v in models.values():total.update(v)
  result[name]={'start_inclusive':start,'end_exclusive':end,'timezone':'Asia/Seoul','totals':total,'sessions_with_metered_requests':len(sessions),'active_days':len(daily),'duplicate_records_merged':copies,'duplicate_records_with_different_values':diff,'models':models,'daily':daily,'iitp_path_subset_models':iitp,'request_id_hash_digest':hashlib.sha256('\n'.join(sorted(ids)).encode()).hexdigest()}
 return normalize({'diagnostics':diag,'periods':result})
def normalize(data):
 # Synthetic records carry zero tokens; remove them from model/response counts.
 # Session/duplicate counts remain raw metadata counts (not work/task counts).
 for period in data['periods'].values():
  synthetic=period['models'].pop('<synthetic>',{})
  assert not synthetic.get('total_processed',0)
  n=synthetic.get('requests',0)
  if period['totals']:period['totals']['requests']-=n
  period['synthetic_zero_token_responses_excluded']=n
  period['sessions_with_usage_records_including_zero_and_synthetic']=period.pop('sessions_with_metered_requests')
  period['active_days']=sum(x.get('total_processed',0)>0 for x in period['daily'].values())
  for row in period['daily'].values():row.pop('requests',None)
  period['count_note']='requests counts unique model-response records excluding synthetic; zero-token non-synthetic responses may remain. Session and duplicate counts include zero-token/synthetic records. No user-task count inferred.'
 return data

def main():
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);a.add_argument('--provider',choices=['claude','codex','all'],default='all');o=a.parse_args();out={'generated_at':dt.datetime.now(KST).isoformat(),'coverage':'Local host default Claude projects and Codex sessions + archived_sessions only. Not all devices, seats, browser usage or grant-attributed spending.','method':'Global response/message ID dedupe. Split record counters max. Cached input and reasoning counted as subsets for Codex. No conversation content exported.','providers':{}}
 if o.provider in ['claude','all']:
  print('Scanning Claude metadata...',flush=True);out['providers']['claude_code']=aggregate(*claude(P.home()/'.claude/projects'))
 if o.provider in ['codex','all']:
  print('Scanning Codex metadata...',flush=True);out['providers']['codex']=aggregate(*codex([P.home()/'.codex/sessions',P.home()/'.codex/archived_sessions']))
 P(o.output).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('Wrote',o.output)
if __name__=='__main__':main()
