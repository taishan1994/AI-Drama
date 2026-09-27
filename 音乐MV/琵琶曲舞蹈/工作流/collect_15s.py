import json,time,urllib.request,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[1];COMFY=P.parents[2]/'ComfyUI'
pid=json.loads((P/'工作流/H3_15秒任务.json').read_text())['prompt_id']
while True:
 h=json.load(urllib.request.urlopen('http://127.0.0.1:8188/history/'+pid)).get(pid)
 if h:
  (P/'工作流/H3_15秒历史.json').write_text(json.dumps(h,ensure_ascii=False,indent=2))
  st=h.get('status',{})
  if st.get('status_str')=='error': print(json.dumps(st,ensure_ascii=False),flush=True);raise SystemExit(1)
  if st.get('completed'):
   for items in h.get('outputs',{}).get('15',{}).values():
    if isinstance(items,list):
     for x in items:
      if isinstance(x,dict) and x.get('filename','').endswith('.mp4'):
       src=COMFY/'output'/x.get('subfolder','')/x['filename'];dst=P/'视频/双人古装舞_15秒_唯一椅子_待验收.mp4';shutil.copy2(src,dst);print(dst,flush=True)
   break
 time.sleep(6)
