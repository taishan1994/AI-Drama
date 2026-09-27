import json,time,urllib.request,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[1]
COMFY=P.parents[2]/'ComfyUI'
pid=json.loads((P/'工作流/H3_首段任务.json').read_text())['prompt_id']
while True:
    history=json.load(urllib.request.urlopen('http://127.0.0.1:8188/history/'+pid)).get(pid)
    if history:
        (P/'工作流/H3_首段历史.json').write_text(json.dumps(history,ensure_ascii=False,indent=2))
        if history.get('status',{}).get('status_str')=='error':
            print(json.dumps(history['status'],ensure_ascii=False),flush=True);raise SystemExit(1)
        if history.get('status',{}).get('completed'):
            for node,label in [('15','首段_原始音频_待验收'),('41','首段_H3音频_对照')]:
                out=history['outputs'].get(node,{})
                for entries in out.values():
                    if not isinstance(entries,list):continue
                    for item in entries:
                        if isinstance(item,dict) and item.get('filename','').endswith('.mp4'):
                            src=COMFY/'output'/item.get('subfolder','')/item['filename']
                            dest=P/'视频'/f'{label}.mp4';shutil.copy2(src,dest);print(dest,flush=True)
            break
    time.sleep(5)
