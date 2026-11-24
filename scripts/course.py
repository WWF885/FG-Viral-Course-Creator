"""Local project-state helper, no model calls or network. Python 3.9+."""
import argparse, json, re, sys, os
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MODES = {'full':list(range(1,10)), 'quick':list(range(1,10)), 'lesson':[5,6,9], 'audit':[9], 'upgrade':[9], 'resume':list(range(1,10))}

def read(p):
    return json.loads((Path(p)/'project.json').read_text(encoding='utf-8'))
def write(p, data):
    file = Path(p)/'project.json'; tmp=file.with_suffix('.tmp')
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); os.replace(tmp,file)
def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def init(p,title,mode):
    p=Path(p).resolve()
    if p==ROOT or ROOT in p.parents: raise ValueError('项目须在技能目录之外')
    if not title.strip(): raise ValueError('课程名称不能为空')
    p.mkdir(parents=True,exist_ok=True)
    if (p/'project.json').exists(): raise ValueError('项目已存在，拒绝覆盖')
    d=json.loads((ROOT/'templates/project.json').read_text(encoding='utf-8')); d.update(title=title,mode=mode)
    write(p,d); return d

def next_stage(d):
    return next((i for i in MODES[d['mode']] if d['stages'][str(i)]['status']!='approved'),None)
def approve(p,stage,decision,evidence):
    d=read(p); p=Path(p).resolve(); route=MODES[d['mode']]
    if stage not in route: raise ValueError('阶段不在当前模式；先在项目方案中明确模式或使用完整模式')
    if stage!=next_stage(d): raise ValueError('须按当前模式顺序确认；已确认阶段请先revise')
    if not decision.strip() or not evidence: raise ValueError('必须记录明确决策和证据文件')
    for item in evidence:
        f=(p/item).resolve()
        if p not in f.parents or not f.is_file() or f.name=='project.json': raise ValueError('证据须为项目目录内的实际产物文件')
    d['stages'][str(stage)]={'status':'approved','decision':decision,'evidence':evidence,'date':now()}
    d['history'].append({'action':'approve','stage':stage,'date':now(),'decision':decision}); write(p,d); return d

def revise(p,stage,reason):
    d=read(p)
    if not reason.strip(): raise ValueError('需说明变更原因')
    for i in range(stage,10):
        s=d['stages'][str(i)]
        if s['status']=='approved':
            d['history'].append({'action':'invalidate','stage':i,'previous':dict(s),'date':now(),'reason':reason}); s['status']='review'
    d['publication_authorized']=False; write(p,d); return d

def switch_mode(p,mode):
    d=read(p)
    if mode=='resume': return d  # Resume existing route; never reset approvals.
    d['history'].append({'action':'mode','previous':d['mode'],'mode':mode,'date':now()}); d['mode']=mode
    write(p,d); return d

def validate():
    errors=[]; s=(ROOT/'SKILL.md').read_text(encoding='utf-8'); name=re.search(r'^name: (.+)$',s,re.M)
    if not name or name.group(1)!=ROOT.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',ROOT.name) or len(ROOT.name)>64: errors.append('name')
    desc=re.search(r'^description: (.+)$',s,re.M)
    if not desc or len(desc.group(1))>1024: errors.append('description')
    for path in re.findall(r'\]\((references/[^)]+)\)',s):
        if not (ROOT/path).is_file(): errors.append(path)
    for p in ('README.md','LICENSE','CHANGELOG.md','RELEASE-CHECKLIST.md','templates/lesson.html','templates/project.json','assets/catalog.html','assets/visuals.js','tests/scenarios.md'):
        if not (ROOT/p).is_file(): errors.append(p)
    if len(list((ROOT/'references').glob('*.md')))!=9: errors.append('nine references')
    if len(list((ROOT/'templates').glob('*.md')))!=13: errors.append('13 md templates')
    for f in ROOT.rglob('*'):
        if f.is_file() and f.suffix in {'.md','.json','.html','.js','.py'} and '__pycache__' not in str(f):
            data=f.read_text(encoding='utf-8');
            if re.search(r'(?i)(?:sk-[a-z0-9]{24,}|ghp_[a-z0-9]{24,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',data): errors.append('possible secret '+str(f.relative_to(ROOT)))
    if errors: raise ValueError('Validation failed: '+', '.join(errors))
    return {'structure':'pass','references':9,'markdown_templates':13,'name':ROOT.name}

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
    i=sub.add_parser('init'); i.add_argument('project'); i.add_argument('--title',required=True); i.add_argument('--mode',choices=MODES,default='full')
    s=sub.add_parser('status'); s.add_argument('project')
    a=sub.add_parser('approve'); a.add_argument('project'); a.add_argument('stage',type=int,choices=range(1,10)); a.add_argument('--decision',required=True); a.add_argument('--evidence',nargs='+',required=True)
    r=sub.add_parser('revise'); r.add_argument('project'); r.add_argument('stage',type=int,choices=range(1,10)); r.add_argument('--reason',required=True)
    m=sub.add_parser('mode'); m.add_argument('project'); m.add_argument('mode',choices=MODES)
    sub.add_parser('validate'); args=p.parse_args()
    try:
        if args.cmd=='validate': out=validate()
        else:
            if args.cmd=='init': d=init(args.project,args.title,args.mode)
            elif args.cmd=='approve': d=approve(args.project,args.stage,args.decision,args.evidence)
            elif args.cmd=='revise': d=revise(args.project,args.stage,args.reason)
            elif args.cmd=='mode': d=switch_mode(args.project,args.mode)
            else: d=read(args.project)
            out={**d,'next_stage':next_stage(d)}
        print(json.dumps(out,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError) as e: print(str(e),file=sys.stderr); return 1
    return 0
if __name__=='__main__': sys.exit(main())
