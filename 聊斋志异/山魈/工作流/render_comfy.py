#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,shutil,time,urllib.request
from datetime import datetime
from pathlib import Path
from prompts_v2 import PROMPTS

PROJECT=Path(__file__).resolve().parents[1]
COMFY=Path('/nfs/FM/gongoubo/new_project/github/aigc/ComfyUI')
API='http://127.0.0.1:8188'
ENV=PROJECT/'资产/环境设定板/柳沟寺_书斋干净空间_2K.png'
SUN=PROJECT/'资产/角色设定板/孙生_角色设定板_真人电影质感_2K.png'
MON=PROJECT/'资产/角色设定板/山魈_角色设定板_真人电影质感_2K.png'
PROP=PROJECT/'资产/道具设定板/书案油灯书囊短刀被褥_2K.png'
FX=PROJECT/'资产/特效与道具设定板/山魈风压爪痕木屑_2K.png'
S05_KEY=PROJECT/'资产/关键帧/S05_家人破窗_关门构图_2K.png'
S01_KEY=PROJECT/'资产/关键帧/S01_门闩里的爪_2K.png'
S02_KEY=PROJECT/'资产/关键帧/S02_回到柳沟寺_清洁构图_2K.png'
REFS={1:[S01_KEY],2:[S02_KEY],3:[ENV,SUN],4:[ENV,SUN],5:[ENV,SUN,S05_KEY],6:[ENV,SUN,PROP],7:[ENV,SUN,PROP],8:[ENV,SUN,PROP,FX],9:[ENV,SUN,PROP,FX],10:[ENV,SUN],11:[ENV,SUN,PROP,FX],12:[ENV,SUN,FX]}
LOG=PROJECT/'state/generation.log'

def req(path,data=None):
    body=None if data is None else json.dumps(data).encode(); r=urllib.request.Request(API+path,data=body,headers={'Content-Type':'application/json'} if body else {})
    with urllib.request.urlopen(r,timeout=60) as h:return json.loads(h.read())
def log(s):
    LOG.parent.mkdir(parents=True,exist_ok=True); line=f'{datetime.now().astimezone().isoformat(timespec="seconds")} {s}'; print(line,flush=True); LOG.open('a',encoding='utf-8').write(line+'\n')
def graph(prompt,seed,prefix,refs,frames,sage):
    g={'1':{'class_type':'ClipProjLoader','inputs':{'clip_name':'qwen3vl_4b_int8_convrot.safetensors','type':'krea2','projection':'mmh3-4b-ClipProj-v3-mlp.safetensors','device':'cuda:0','mode':'streaming'}},'2':{'class_type':'UNETLoader','inputs':{'unet_name':'minimax_h3_ref2va_pruned_int8_convrot.safetensors','weight_dtype':'default'}},'3':{'class_type':'MiniMaxH3SigmaShift','inputs':{'model':['2',0],'shift_video':12.0,'shift_audio':3.0}},'4':{'class_type':'VAELoader','inputs':{'vae_name':'minimax_h3_video_vae_fp16.safetensors'}},'5':{'class_type':'VAELoader','inputs':{'vae_name':'minimax_h3_audio_vae_fp32.safetensors'}},'6':{'class_type':'MiniMaxH3ReferenceToVideo','inputs':{'clip':['1',0],'vae':['4',0],'audio_vae':['5',0],'prompt':prompt,'width':1344,'height':768,'length':frames,'ref_image_size':'match'}},'7':{'class_type':'BasicGuider','inputs':{'model':['30',0] if sage else ['9',0],'conditioning':['6',0]}},'8':{'class_type':'KSamplerSelect','inputs':{'sampler_name':'euler'}},'9':{'class_type':'MiniMaxH3PDDAccApply','inputs':{'model':['3',0],'pdd_file':'MiniMax-H3-Ref2VA-Acc-8Step.safetensors','nfe':'8','lora_strength':1.0,'head_strength':1.0,'on_off_grid':'error','partition_check':'error'}},'10':{'class_type':'RandomNoise','inputs':{'noise_seed':seed}},'11':{'class_type':'SamplerCustomAdvanced','inputs':{'noise':['10',0],'guider':['7',0],'sampler':['8',0],'sigmas':['9',1],'latent_image':['6',1]}},'12':{'class_type':'VAEDecode','inputs':{'samples':['11',0],'vae':['4',0]}},'13':{'class_type':'VAEDecodeAudio','inputs':{'samples':['11',0],'vae':['5',0]}},'14':{'class_type':'CreateVideo','inputs':{'images':['12',0],'audio':['13',0],'fps':24.0,'bit_depth':8,'color_space':'sRGB','codec':'none'}},'15':{'class_type':'SaveVideo','inputs':{'video':['14',0],'filename_prefix':prefix,'format':'mp4','format.codec':'h264'}}}
    for i,p in enumerate(refs): g[str(16+i)]={'class_type':'LoadImage','inputs':{'image':p.name}}; g['6']['inputs'][f'ref_images.ref_image_{i}']=[str(16+i),0]
    if sage:g['30']={'class_type':'PathchSageAttentionKJ','inputs':{'model':['9',0],'sage_attention':'auto','allow_compile':False}}
    return g
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--shot',type=int,choices=range(1,13)); ap.add_argument('--frames',type=int,default=243); ap.add_argument('--timeout',type=int,default=7200); ap.add_argument('--sage',action='store_true'); a=ap.parse_args(); shots=[a.shot] if a.shot else list(range(1,13))
    for n in shots:
        local=[]
        for i,p in enumerate(REFS[n]):
            name=f'shanxiao_s{n:02d}_{i}.png'; shutil.copy2(p,COMFY/'input'/name); local.append(Path(name))
        text=PROMPTS[n-1]
        if n not in (3,4):
            # S02 and the other pre-reveal shots must not expose the Shanxiao
            # character definition to the reference-to-video model.
            text='\n'.join(line for line in text.splitlines() if not line.startswith('<Picture 3>'))
        g=graph(text,881001+n,f'video/shanxiao_live_action/shot_{n:02d}',local,a.frames,a.sage)
        wf=PROJECT/'工作流'/f'S{n:02d}_api.json'; wf.write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
        q=req('/prompt',{'prompt':g,'client_id':'shanxiao-live-action'}); 
        if 'error' in q: raise RuntimeError(json.dumps(q,ensure_ascii=False))
        pid=q['prompt_id']; log(f'queued S{n:02d} {pid}; 1344x768 {a.frames}f; INT8 ConvRot + ACC 8-step; Sage={a.sage}')
        start=time.monotonic()
        while time.monotonic()-start<a.timeout:
            item=req('/history/'+pid).get(pid)
            if item:
                st=item.get('status',{})
                if st.get('completed'):
                    (PROJECT/'视频/source'/f'S{n:02d}_history.json').write_text(json.dumps(item,ensure_ascii=False,indent=2),encoding='utf-8'); log(f'completed S{n:02d}'); break
                if st.get('status_str')=='error': raise RuntimeError(json.dumps(st,ensure_ascii=False))
            time.sleep(3)
        else: raise TimeoutError(f'S{n:02d}')
if __name__=='__main__': main()
