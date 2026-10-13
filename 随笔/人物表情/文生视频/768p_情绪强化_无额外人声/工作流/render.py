#!/usr/bin/env python3
import json, time, urllib.parse, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COMFY='http://127.0.0.1:8188'
GRAPH=ROOT/'工作流'/'人物表情_T2VA_768p_情绪强化_无额外人声_API.json'
OUT=ROOT/'成片'/'人物表情_MinimaxH3_T2V_768p_情绪强化_自然环境声无说话声_24fps.mp4'
def api(path, body=None, timeout=90):
    data=None if body is None else json.dumps(body,ensure_ascii=False).encode()
    req=urllib.request.Request(COMFY+path,data=data,headers={'Content-Type':'application/json'} if data else {})
    with urllib.request.urlopen(req,timeout=timeout) as r: return json.loads(r.read())
g=json.loads(GRAPH.read_text(encoding='utf-8'))
q=api('/prompt',{'prompt':g,'client_id':'expression-h3-local'})
if 'error' in q: raise SystemExit(json.dumps(q,ensure_ascii=False,indent=2))
pid=q['prompt_id']; (ROOT/'工作流'/'prompt_id.txt').write_text(pid+'\n')
print('queued:',pid,flush=True)
start=time.monotonic(); last=''
while time.monotonic()-start < 3*3600:
    h=api('/history/'+pid).get(pid)
    if h:
        status=h.get('status',{}); msg=json.dumps(status,ensure_ascii=False)
        if msg != last: print('status:',msg,flush=True); last=msg
        if status.get('completed'):
            (ROOT/'工作流'/'history.json').write_text(json.dumps(h,ensure_ascii=False,indent=2),encoding='utf-8')
            outputs=h.get('outputs',{}).get('15',{}).get('images',[])
            if not outputs: raise RuntimeError('completed but SaveVideo node has no output')
            item=outputs[0]; qs=urllib.parse.urlencode({'filename':item['filename'],'subfolder':item.get('subfolder',''),'type':item.get('type','output')})
            with urllib.request.urlopen(COMFY+'/view?'+qs,timeout=180) as r: data=r.read()
            OUT.write_bytes(data); print('saved:',OUT,'bytes:',len(data),flush=True); break
        if status.get('status_str')=='error':
            (ROOT/'工作流'/'failure.json').write_text(json.dumps(h,ensure_ascii=False,indent=2),encoding='utf-8')
            raise RuntimeError('ComfyUI generation failed; see failure.json')
    time.sleep(5)
else: raise TimeoutError('generation exceeded 3 hours')
