#!/usr/bin/env python3
"""Submit exactly one approved-by-order v3 Shanxiao segment to local ComfyUI."""
from __future__ import annotations

import argparse
import json
import shutil
import time
import urllib.request
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path('/nfs/FM/gongoubo/new_project/github/aigc')
COMFY = ROOT / 'ComfyUI'
API = 'http://127.0.0.1:8188'
STORYBOARD = PROJECT / '山魈_分镜与MiniMax-H3视频Prompt_v4.md'
ASSETS = PROJECT / '资产'
REFS = {
    1: [ASSETS/'环境设定板/柳沟寺_书斋干净空间_2K.png',
        ASSETS/'角色设定板/孙生_角色设定板_真人电影质感_2K.png',
        ASSETS/'角色设定板/山魈_角色设定板_真人电影质感_2K.png'],
    2: [ASSETS/'环境设定板/柳沟寺_书斋干净空间_2K.png',
        ASSETS/'角色设定板/孙生_角色设定板_真人电影质感_2K.png',
        ASSETS/'道具设定板/书案油灯书囊短刀被褥_2K.png'],
    3: [ASSETS/'环境设定板/柳沟寺_书斋干净空间_2K.png',
        ASSETS/'角色设定板/孙生_角色设定板_真人电影质感_2K.png'],
    4: [ASSETS/'环境设定板/柳沟寺_书斋干净空间_2K.png',
        ASSETS/'角色设定板/孙生_角色设定板_真人电影质感_2K.png'],
    5: [ASSETS/'环境设定板/柳沟寺_书斋干净空间_2K.png',
        ASSETS/'角色设定板/孙生_角色设定板_真人电影质感_2K.png',
        ASSETS/'道具设定板/书案油灯书囊短刀被褥_2K.png'],
    6: [ASSETS/'环境设定板/柳沟寺_书斋干净空间_2K.png',
        ASSETS/'角色设定板/孙生_角色设定板_真人电影质感_2K.png',
        ASSETS/'角色设定板/山魈_角色设定板_真人电影质感_2K.png'],
    7: [ASSETS/'环境设定板/柳沟寺_书斋干净空间_2K.png',
        ASSETS/'角色设定板/孙生_角色设定板_真人电影质感_2K.png',
        ASSETS/'角色设定板/山魈_角色设定板_真人电影质感_2K.png',
        ASSETS/'道具设定板/书案油灯书囊短刀被褥_2K.png',
        ASSETS/'特效与道具设定板/山魈风压爪痕木屑_2K.png'],
    8: [ASSETS/'环境设定板/柳沟寺_书斋干净空间_2K.png',
        ASSETS/'角色设定板/孙生_角色设定板_真人电影质感_2K.png'],
}


def request(path: str, payload=None):
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(API + path, data=body,
        headers={'Content-Type': 'application/json'} if body else {})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read())


def prompt_for(shot: int) -> str:
    text = STORYBOARD.read_text(encoding='utf-8')
    start = text.index(f'### 段{shot} · S{shot:02d} /')
    end = text.find('\n### 段', start + 5)
    if end < 0:
        end = text.find('\n## 出稿自检', start + 5)
    block = text[start:end]
    marker = '**MiniMax H3 Ref2VA Prompt**'
    p0 = block.index(marker)
    p1 = block.index('```text\n', p0) + len('```text\n')
    p2 = block.index('\n```', p1)
    return block[p1:p2].strip()


def make_graph(prompt: str, images: list[Path], frames: int, seed: int,
               prefix: str, use_sage: bool) -> dict:
    graph = {
        '1': {'class_type':'ClipProjLoader','inputs':{
            'clip_name':'qwen3vl_4b_int8_convrot.safetensors','type':'krea2',
            'projection':'mmh3-4b-ClipProj-v3-mlp.safetensors',
            'device':'cuda:0','mode':'streaming'}},
        '2': {'class_type':'UNETLoader','inputs':{
            'unet_name':'minimax_h3_ref2va_pruned_int8_convrot.safetensors',
            'weight_dtype':'default'}},
        '3': {'class_type':'MiniMaxH3SigmaShift','inputs':{
            'model':['2',0],'shift_video':12.0,'shift_audio':3.0}},
        '4': {'class_type':'VAELoader','inputs':{'vae_name':'minimax_h3_video_vae_fp16.safetensors'}},
        '5': {'class_type':'VAELoader','inputs':{'vae_name':'minimax_h3_audio_vae_fp32.safetensors'}},
        '6': {'class_type':'MiniMaxH3ReferenceToVideo','inputs':{
            'clip':['1',0],'vae':['4',0],'audio_vae':['5',0],
            'prompt':prompt,'width':1344,'height':768,'length':frames,
            'ref_image_size':'match'}},
        '7': {'class_type':'BasicGuider','inputs':{
            'model':['30',0] if use_sage else ['9',0], 'conditioning':['6',0]}},
        '8': {'class_type':'KSamplerSelect','inputs':{'sampler_name':'euler'}},
        '9': {'class_type':'MiniMaxH3PDDAccApply','inputs':{
            'model':['3',0],'pdd_file':'MiniMax-H3-Ref2VA-Acc-8Step.safetensors',
            'nfe':'8','lora_strength':1.0,'head_strength':1.0,
            'on_off_grid':'error','partition_check':'error'}},
        '10': {'class_type':'RandomNoise','inputs':{'noise_seed':seed}},
        '11': {'class_type':'SamplerCustomAdvanced','inputs':{
            'noise':['10',0],'guider':['7',0],'sampler':['8',0],
            'sigmas':['9',1],'latent_image':['6',1]}},
        '12': {'class_type':'VAEDecode','inputs':{'samples':['11',0],'vae':['4',0]}},
        '13': {'class_type':'VAEDecodeAudio','inputs':{'samples':['11',0],'vae':['5',0]}},
        '14': {'class_type':'CreateVideo','inputs':{
            'images':['12',0],'audio':['13',0],'fps':24.0,
            'bit_depth':8,'color_space':'sRGB','codec':'none'}},
        '15': {'class_type':'SaveVideo','inputs':{
            'video':['14',0],'filename_prefix':prefix,
            'format':'mp4','format.codec':'h264'}},
    }
    for i, image in enumerate(images):
        node = str(16+i)
        graph[node] = {'class_type':'LoadImage','inputs':{'image':image.name}}
        graph['6']['inputs'][f'ref_images.ref_image_{i}'] = [node,0]
    if use_sage:
        graph['30'] = {'class_type':'PathchSageAttentionKJ','inputs':{
            'model':['9',0],'sage_attention':'auto','allow_compile':False}}
    return graph


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shot', type=int, choices=range(1,9), required=True,
                    help='Submit exactly this one segment; do not queue subsequent segments.')
    ap.add_argument('--frames', type=int)
    ap.add_argument('--timeout', type=int, default=7200)
    ap.add_argument('--no-sage', action='store_true')
    ap.add_argument('--take', default='v3', help='Take label for workflow and output paths.')
    ap.add_argument('--seed', type=int, help='Noise seed; override to explore a different motion take.')
    ap.add_argument('--prompt-suffix', default='', help='Append a take-specific refinement to the selected storyboard prompt.')
    ap.add_argument('--prompt-file', type=Path, help='Use a complete take-specific prompt instead of the storyboard block.')
    ap.add_argument('--start-reference', type=Path, help='Optional existing still frame to lock the opening composition.')
    args = ap.parse_args()
    shot = args.shot
    frames = args.frames or round(int(re.search(rf'^### 段{shot} · S{shot:02d} / (\d+)s',
        STORYBOARD.read_text(encoding='utf-8'), re.M).group(1)) * 24)
    if not 96 <= frames <= 360:
        raise ValueError('H3 segment must be 4–15 seconds at 24fps.')
    for image in REFS[shot]:
        if not image.is_file():
            raise FileNotFoundError(image)
    info = request('/system_stats')
    sage = not args.no_sage
    if sage:
        request('/object_info/PathchSageAttentionKJ')
    local = []
    for i, source in enumerate(REFS[shot]):
        name = f'shanxiao_v3_s{shot:02d}_{i+1}.png'
        dest = COMFY/'input'/name
        shutil.copy2(source, dest)
        local.append(dest)
    if args.start_reference:
        if not args.start_reference.is_file():
            raise FileNotFoundError(args.start_reference)
        dest = COMFY/'input'/f'shanxiao_{args.take}_opening.png'
        shutil.copy2(args.start_reference, dest)
        local.append(dest)
    prompt = args.prompt_file.read_text(encoding='utf-8').strip() if args.prompt_file else prompt_for(shot)
    if args.prompt_suffix:
        prompt += '\n\n' + args.prompt_suffix.strip()
    graph = make_graph(prompt, local, frames, args.seed if args.seed is not None else 904270+shot,
                       f'video/shanxiao_{args.take}/S{shot:02d}', sage)
    wf = PROJECT/'工作流'/f'S{shot:02d}_{args.take}_api.json'
    wf.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding='utf-8')
    q = request('/prompt', {'prompt':graph,'client_id':'shanxiao-v3-single-shot'})
    if q.get('error'):
        raise RuntimeError(json.dumps(q, ensure_ascii=False))
    pid = q['prompt_id']
    LOG = PROJECT/'state'/'generation_v3.log'
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a', encoding='utf-8') as f:
        f.write(f'{datetime.now().astimezone().isoformat(timespec="seconds")} queued S{shot:02d} {pid}; {frames}f; Sage={sage}\n')
    print(json.dumps({'shot':shot,'prompt_id':pid,'workflow':str(wf),
                      'frames':frames,'references':[x.name for x in local],
                      'device':info.get('system',{}).get('argv',[])},ensure_ascii=False))
    started = time.monotonic()
    while time.monotonic()-started < args.timeout:
        item = request('/history/'+pid).get(pid)
        if item:
            state = item.get('status',{})
            if state.get('completed'):
                out = PROJECT/'视频'/'source'/f'S{shot:02d}_{args.take}_history.json'
                out.write_text(json.dumps(item,ensure_ascii=False,indent=2),encoding='utf-8')
                print(f'COMPLETED S{shot:02d} {pid}')
                return
            if state.get('status_str') == 'error':
                print(json.dumps(state,ensure_ascii=False))
                raise RuntimeError(f'S{shot:02d} failed')
        time.sleep(3)
    raise TimeoutError(f'S{shot:02d} {pid}')


if __name__ == '__main__':
    import re
    main()
