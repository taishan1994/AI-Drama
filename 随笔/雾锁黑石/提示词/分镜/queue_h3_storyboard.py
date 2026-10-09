#!/usr/bin/env python3
"""Queue and collect the 62 MiniMax-H3 Ref2VA storyboard shots via local ComfyUI."""
from pathlib import Path
import json, time, urllib.request, urllib.parse, sys, re

ROOT = Path('/nfs/FM/gongoubo/new_project/github/aigc/短剧/雾锁黑石')
COMFY = 'http://127.0.0.1:8188'
TEMPLATE = Path('/nfs/FM/gongoubo/new_project/github/aigc/ComfyUI/output/bund_replacement/request_motion_segment_01.json')
SHOTS = json.loads((ROOT/'提示词/分镜/script_shots_with_assets.json').read_text())
VIDEO_DIR = ROOT/'分镜视频'
PROMPT_DIR = ROOT/'提示词/分镜/optimized_prompts'
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR=VIDEO_DIR/'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROMPT_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST = ROOT/'分镜视频/生成清单.json'
SKILL_DIR = Path('/nfs/FM/gongoubo/new_project/github/aigc/AI-Drama/skills/minimax-h3-skills/h3-prompt-writing')
LLAMA = 'http://127.0.0.1:18080/v1/chat/completions'


def role_for(asset):
    a = Path(asset)
    if a.parent.name == '人物设定':
        if '妻子' in a.name: return 'warm domestic-memory appearance and setting reference; not a close-up identity portrait'
        return 'character identity and clothing reference; use the large portrait area for face identity and the turnaround figures only for clothing/body proportions, never reproduce the reference sheet layout'
    if a.parent.name == '怪物设定':
        return 'monster design reference only; preserve distinctive anatomy and silhouette, ignore any unrelated background, captions, borders, and watermark'
    if a.parent.name == '道具设定':
        return 'prop appearance reference only; preserve the recognizable shape and markings without copying the image layout'
    return 'environment and spatial-layout reference; preserve architecture and screen direction without copying any reference-sheet layout'


def source_prompt(shot):
    refs = shot['asset_files']
    names = shot['comfy_input_files']
    lines = [
        f"Single MiniMax H3 Reference to Video shot. Generate exactly {shot['duration']} seconds for storyboard Shot {shot['shot']}.",
        'Use the minimax-h3-writing skill Ref2VA six-section format. Write prompt sections in English. This request has still-image references only; the screenplay below is text, not a source video or audio asset. Sound/effect/music descriptions in the screenplay are instructions for newly generated target audio, not external audio references. Use only the listed <Picture N> labels. Never invent <Video N> or <Audio N> labels or claim a source video/audio exists. The listed pictures define appearance, props, or environments, not target-frame anchors. Preserve every Chinese dialogue line exactly and identify its speaker. Use stable speaker IDs across the whole film: Lin Mo (S1), Su Wan (S2), and Old Zhou (S3). Keep their voice qualities consistent: S1 male, young adult, slightly breathless and anxious; S2 female, calm, clear, controlled; S3 male, middle-aged, rough and forceful. Describe only this shot; do not invent other shots, dialogue, or visual actions.',
    ]
    if refs:
        lines.append('Reference asset roles (use each asset only for the stated role):')
        for i, (asset, fname) in enumerate(zip(refs, names), 1):
            lines.append(f'@pic{i} ({fname}) = {role_for(asset)}.')
        lines.append('Only the listed Picture references exist in this request. Keep their numbering consistent. They are design/environment references, not first-frame, last-frame, keyframe, or storyboard anchors.')
    lines.append('Story shot source (preserve its visible action, framing, mood, sound, and spoken words):')
    lines.append(shot['source_description'])
    lines.append('Editorial transition note (for the editor only; MUST NOT be included in the generated video, detailed_description, soundscape, or music): ' + (shot['transition_to_next'] or 'Cut after the final frame.'))
    lines.append('Generate only the actions, framing, and sounds explicitly in this shot source. Do not borrow any action, sound, framing, or event from the editorial transition note. End on this shot only. Do not show, describe, or preview the next shot. Show no text unless the script specifies visible text. Avoid extra limbs, duplicated people or creatures, unrelated creatures, and graphic gore.')
    return '\n\n'.join(lines)


def _prompt_system():
    skill=(SKILL_DIR/'SKILL.md').read_text(encoding='utf-8').strip()
    guide=(SKILL_DIR/'references/ref-en.txt').read_text(encoding='utf-8').strip()
    return ('Follow the complete MiniMax H3 prompt-writing skill and Ref2VA guide below. Return exactly six sections in this order: '
        'subject_definitions, summary, retention_analysis, detailed_description, overall_soundscape, non_diegetic_music. '
        'This is one reference-generation shot; match the exact requested duration. Only still images are supplied. Sound/effect/music '
        'descriptions are instructions for generated target audio, not reference audio files. The screenplay is text, not a source video. '
        'Use only listed <Picture N> labels; never create <Video N> or <Audio N>. Define each '
        'listed still image inside its corresponding target <Subject N> because it is a design reference, not a target frame. Do not '
        'add standalone Picture entries unless a keyframe is explicitly requested (none are). Preserve spoken Chinese exactly and '
        'identify its speaker. Describe one continuous shot only: do not add internal cuts, fades, black frames, or extra camera setups '
        'unless the screenplay explicitly includes them. Do not add timestamps not present in the source. The transition is an editorial '
        'event after the final frame. The editorial transition note is metadata only and must be ignored when generating video, audio, '
        'or writing any prompt section; do not depict/preview the next shot, its sound, or any transition action. Do not mention the next shot '
        'in detailed_description. Do not invent reference assets, speakers, actions, or soundtrack elements. Return only the final prompt.\n\n'
        'BEGIN SKILL\n'+skill+'\n\n--- ref-en.txt ---\n'+guide+'\nEND SKILL')


def _validate_prompt(text, shot):
    headings=['subject_definitions:','summary:','retention_analysis:','detailed_description:','overall_soundscape:','non_diegetic_music:']
    positions=[text.find(h) for h in headings]
    issues=[]
    if min(positions)<0 or positions!=sorted(positions):
        issues.append('The six required Ref2VA headings are missing or out of order.')
    if '[Shot 2]' in text or '[Shot 3]' in text:
        issues.append('The output describes a second shot.')
    detail=text.split('detailed_description:',1)[1].split('overall_soundscape:',1)[0] if 'detailed_description:' in text and 'overall_soundscape:' in text else text
    if re.search(r'\b(?:the shot|camera|scene)\s+(?:hard\s+)?cuts?\s+to\b|\bfades?\s+(?:to\s+black|out)\b|\bnext shot\b',detail,re.I):
        issues.append('The detailed description contains an internal cut/fade or previews the next shot.')
    duration_stamp=f"{shot['duration']:02d}.000"
    end_mark=re.search(rf'At\s+00:{duration_stamp}[^.]*\.',detail,re.I)
    if end_mark and re.search(r'\b(?:cuts? to|fades? to|new scene|close-up of|wide shot of|medium shot of)\b',end_mark.group(0),re.I):
        issues.append('The output adds new visual content at the clip boundary.')
    if re.search(r'\b(?:next scene|next shot|following shot)\b|\b(?:setting up|leading into|bridging to|transition to)\s+(?:the\s+)?(?:next|following)\s+(?:scene|shot|sequence)\b',detail,re.I):
        issues.append('The detailed description previews or bridges into the next shot.')
    labels=set(re.findall(r'<(Picture|Video|Audio)\s+(\d+)>',text,re.I))
    allowed={('picture',str(i)) for i in range(1,len(shot['asset_files'])+1)}
    unsupported=sorted((kind.lower(),idx) for kind,idx in labels if (kind.lower(),idx) not in allowed)
    if unsupported:
        issues.append(f'Unsupported reference labels: {unsupported}.')
    subject_section=text.split('summary:',1)[0] if 'summary:' in text else text
    missing=[f'<Picture {i}>' for i in range(1,len(shot['asset_files'])+1) if f'<Picture {i}>' not in subject_section]
    if missing:
        issues.append(f'Pictures must be defined under subject_definitions; missing {missing}.')
    for line in shot['source_description'].splitlines():
        if line.strip().startswith('台词') and '：' in line:
            dialogue=line.split('：',1)[1].strip()
            if dialogue and dialogue!='无' and dialogue not in text:
                issues.append(f'Exact dialogue changed or omitted: {dialogue}')
    if issues:
        raise ValueError(' '.join(issues))


def rewrite_prompt(shot, force=False):
    path=PROMPT_DIR/f"shot_{shot['shot']:02d}_optimized.txt"
    if path.exists() and not force:
        cached=path.read_text(encoding='utf-8')
        try:
            _validate_prompt(cached,shot)
            return cached
        except ValueError:
            pass
    messages=[{'role':'system','content':_prompt_system()},{'role':'user','content':source_prompt(shot)}]
    errors=[]
    for attempt in range(3):
        limit=4096
        while True:
            body={'model':'local-qwen','messages':messages,'temperature':0.1,'max_tokens':limit,'chat_template_kwargs':{'enable_thinking':False}}
            req=urllib.request.Request(LLAMA,data=json.dumps(body,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(req,timeout=300) as response:
                data=json.loads(response.read().decode())
            choice=data['choices'][0]
            if choice.get('finish_reason')!='length': break
            if limit>=8192: raise RuntimeError(f"Shot {shot['shot']} prompt rewrite hit 8192 tokens.")
            limit=min(limit*2,8192)
        candidate=choice['message']['content'].strip()
        try:
            _validate_prompt(candidate,shot)
            path.write_text(candidate+'\n',encoding='utf-8')
            return candidate
        except ValueError as exc:
            errors.append(str(exc))
            messages.extend([{'role':'assistant','content':candidate},{'role':'user','content':'Revise the complete prompt. Validation failed: '+str(exc)+' Follow the skill and all media-role and clip-boundary rules. Return only the corrected six-section prompt.'}])
    raise RuntimeError(f"Shot {shot['shot']} failed prompt validation after 3 attempts: {' | '.join(errors)}")


def build_payload(shot, base, final_prompt):
    p = json.loads(json.dumps(base['prompt']))
    p['3']['inputs'].update({
        'mode':'Reference to Video', 'resolution':'768p Native 1344x768',
        'custom_width':1344, 'custom_height':768, 'duration_seconds':shot['duration'],
        'steps':8, 'video_shift':12.0, 'audio_shift':3.0, 'aspect_ratio':'16:9'
    })
    p['62']['inputs']['resolution_factor'] = 1.0
    p['42']['inputs']['noise_seed'] = 20261007 + shot['shot'] * 1009
    p['5']['inputs'].update({f'image_{i}':'' for i in range(1,10)})
    p['5']['inputs'].update({f'video_{i}':'' for i in range(1,4)})
    p['5']['inputs'].update({f'audio_{i}':'' for i in range(1,4)})
    for i, fname in enumerate(shot['comfy_input_files'], 1):
        p['5']['inputs'][f'image_{i}'] = fname
    ref = p['34']['inputs']
    for key in list(ref):
        if key.startswith('ref_images.ref_image_'):
            del ref[key]
    for i in range(len(shot['comfy_input_files'])):
        ref[f'ref_images.ref_image_{i}'] = ['5', i]
    p['4']['inputs']['prompt'] = final_prompt
    p['56']['inputs'].update({'mode':['3',8], 'optimize':False, 'max_tokens':4096, 'temperature':0.1})
    p['50']['inputs']['filename_prefix'] = f"video/雾锁黑石/shot_{shot['shot']:02d}"
    return {'prompt':p, 'client_id':'codex-wusuo-blackstone'}


def get_json(url, timeout=20):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


def post_json(url, data, timeout=60):
    req = urllib.request.Request(url, data=json.dumps(data,ensure_ascii=False).encode('utf-8'), headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


def collect(prompt_id, shot):
    while True:
        h = get_json(f'{COMFY}/history/{prompt_id}').get(prompt_id)
        if h and h.get('status',{}).get('completed'):
            break
        time.sleep(5)
    status = h.get('status',{}).get('status_str')
    record = {'shot':shot['shot'],'prompt_id':prompt_id,'status':status,'duration':shot['duration'],'resolution':'pending'}
    if status != 'success':
        record['error'] = h.get('status',{}).get('messages',[])
        return record
    outputs = h.get('outputs',{})
    ptxt = outputs.get('60',{}).get('text')
    if ptxt:
        prompt_path = PROMPT_DIR/f"shot_{shot['shot']:02d}_optimized.txt"
        prompt_path.write_text(ptxt[0],encoding='utf-8')
        record['optimized_prompt'] = str(prompt_path)
    videos = outputs.get('50',{}).get('images',[])
    if videos:
        f = videos[0]
        query = urllib.parse.urlencode({'filename':f['filename'],'subfolder':f.get('subfolder',''),'type':f.get('type','output')})
        data = urllib.request.urlopen(f'{COMFY}/view?{query}',timeout=120).read()
        raw = RAW_DIR/f"shot_{shot['shot']:02d}_raw.mp4"
        raw.write_bytes(data)
        out = VIDEO_DIR/f"shot_{shot['shot']:02d}.mp4"
        import subprocess
        # H3's temporal latent grid can round a requested duration upward; trim to the exact script duration.
        subprocess.run(['ffmpeg','-y','-i',str(raw),'-t',str(shot['duration']),'-map','0:v:0','-map','0:a?','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],capture_output=True,text=True,check=True)
        record['video'] = str(out)
        record['raw_video'] = str(raw)
        record['bytes'] = out.stat().st_size
        try:
            raw_probe = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(raw)],capture_output=True,text=True,check=True)
            record['raw_duration'] = float(json.loads(raw_probe.stdout).get('format',{}).get('duration',0))
            probe = subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height','-show_entries','format=duration','-of','json',str(out)],capture_output=True,text=True,check=True)
            info=json.loads(probe.stdout); stream=next((x for x in info.get('streams',[]) if 'width' in x),{})
            record['resolution']=f"{stream.get('width')}x{stream.get('height')}"
            record['actual_duration']=float(info.get('format',{}).get('duration',0))
        except Exception as exc:
            record['probe_error']=str(exc)
    return record


def main():
    base=json.loads(TEMPLATE.read_text())
    start=int(sys.argv[1]) if len(sys.argv)>1 else 1
    end=int(sys.argv[2]) if len(sys.argv)>2 else 62
    selected=[x for x in SHOTS if start<=x['shot']<=end]
    manifest={'objective':'雾锁黑石 62-shot MiniMax H3 storyboard generation','model':'MiniMax-H3 Ref2VA INT8 ConvRot + official Ref2VA 8-step Acc LoRA','text_encoder':'Qwen3-VL-32B MiniMax-H3 INT8 ConvRot','prompt_optimizer':'local Qwen3.5-4B GGUF; minimax-h3-writing skill + Ref2VA guide; six-section/reference-label/dialogue validation before sampling','resolution':'1344x768 (resolution_factor=1.0)','steps':8,'shots':[]}
    if MANIFEST.exists():
        try:
            prior=json.loads(MANIFEST.read_text())
            manifest['shots']=prior.get('shots',[])
        except Exception:
            pass
    records={int(x['shot']):x for x in manifest['shots'] if 'shot' in x}
    for shot in selected:
        previous=records.get(shot['shot'])
        if previous and previous.get('status')=='success' and Path(previous.get('video','')).exists():
            print(f"skip shot {shot['shot']:02d}: successful video already exists",flush=True)
            continue
        try:
            final_prompt=rewrite_prompt(shot)
            result=post_json(f'{COMFY}/prompt',build_payload(shot,base,final_prompt))
            if result.get('node_errors'):
                records[shot['shot']]={'shot':shot['shot'],'status':'submit_error','error':result['node_errors']}
                manifest['shots']=sorted(records.values(),key=lambda x:int(x['shot']))
                MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
                print(f"submit error shot {shot['shot']:02d}: {result['node_errors']}",flush=True)
                continue
            print(f"queued shot {shot['shot']:02d} ({shot['duration']}s), prompt_id={result['prompt_id']}",flush=True)
            record=collect(result['prompt_id'],shot)
            records[shot['shot']]=record
            manifest['shots']=sorted(records.values(),key=lambda x:int(x['shot']))
            MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
            print(f"finished shot {shot['shot']:02d}: {record['status']} {record.get('resolution','')}",flush=True)
        except Exception as exc:
            rec={'shot':shot['shot'],'status':'runner_error','error':repr(exc)}
            records[shot['shot']]=rec
            manifest['shots']=sorted(records.values(),key=lambda x:int(x['shot']))
            MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
            print(f"failed shot {shot['shot']:02d}: {exc!r}",flush=True)
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"all selected shots finished; manifest={MANIFEST}",flush=True)

if __name__=='__main__': main()
