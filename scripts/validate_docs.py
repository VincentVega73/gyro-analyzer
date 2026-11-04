"""Public-only validation. No private repository or credentials required."""
from pathlib import Path
import re, json, sys
from pypdf import PdfReader
from pypdf.generic import ContentStream

ROOT=Path(__file__).resolve().parent.parent
errors=[]
required=['README.md','CHANGELOG.md','ROADMAP.md','CONTRIBUTING.md','CODE_OF_CONDUCT.md','SECURITY.md']
required+=['docs/'+s+'.md' for s in ('getting-started','user-guide','camera-setup','automatic-calibration','target-preparation','measuring-rpm','understanding-results','measurement-methodology','accuracy-and-uncertainty','troubleshooting','faq','compatibility','privacy','support')]
for name in required:
    if not (ROOT/name).is_file():errors.append('Missing required document: '+name)
allowed={'.md','.pdf','.svg','.png','.json','.yml','.yaml','.py','.txt'}
for p in ROOT.rglob('*'):
    if not p.is_file() or any(part in {'.git','node_modules','__pycache__'} for part in p.relative_to(ROOT).parts):continue
    relative=p.relative_to(ROOT).as_posix()
    if p.suffix not in allowed and p.name not in {'.gitignore'}:errors.append('Forbidden file type: '+relative)
    if p.suffix in {'.png','.pdf'}:continue
    text=p.read_text(encoding='utf-8')
    if re.search(r'[\u0400-\u052f\u4e00-\u9fff]',text):errors.append('Non-English script needs review: '+relative)
    # Common secret formats, local private paths and application-source markers.
    patterns=[r'gh[pousr]_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{30,}',r'AKIA[A-Z0-9]{16}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'[A-Z]:\\Users\\',r'package\s+ru\.gyro\.tachometer',r'(?i)(password|token|api_key)\s*[:=]\s*[\"\x27][A-Za-z0-9_-]{20,}']
    for pattern in patterns:
        if re.search(pattern,text):errors.append('Potential private material: '+relative)
    if p.suffix=='.md':
        if not text.startswith('# '):errors.append('Markdown needs a title: '+relative)
        if any(line.rstrip()!=line for line in text.splitlines()):errors.append('Markdown trailing whitespace: '+relative)
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if re.match(r'https?://|mailto:|#',link):continue
            target=link.split('#')[0]
            if target and not (p.parent/target).resolve().exists():errors.append(f'Broken local link: {relative} -> {target}')
spec=json.loads((ROOT/'targets/target-standard.json').read_text())
for name,dimensions in [('a4',(210,297)),('letter',(215.9,279.4))]:
    p=ROOT/f'targets/gyro-optical-target-{name}.pdf'
    if not p.is_file():errors.append('Missing PDF: '+p.name);continue
    pdf=PdfReader(p)
    if len(pdf.pages)!=1:errors.append('PDF must contain one page: '+p.name);continue
    page=pdf.pages[0]
    if any(abs(float(value)*25.4/72-expected)>.02 for value,expected in zip((page.mediabox.width,page.mediabox.height),dimensions)):errors.append('Incorrect PDF page size: '+p.name)
    metadata=json.loads(pdf.metadata.subject)
    if metadata!=spec or metadata.get('target_version')!='GYRO-TARGET-1.0':errors.append('Incorrect target metadata: '+p.name)
    if len(page.images)>0:errors.append('Target must be vector: '+p.name)
    if '50 mm' not in page.extract_text():errors.append('Missing control-line label: '+p.name)
    if pdf.is_encrypted:errors.append('Target must not be encrypted: '+p.name)
    paths=[];points=[];curves=0
    for args,op in ContentStream(page.get_contents(),pdf).operations:
        if op==b'm':points=[(float(args[0]),float(args[1]))];curves=0
        elif op==b'l':points.append((float(args[0]),float(args[1])))
        elif op==b'c':points.append((float(args[4]),float(args[5])));curves+=1
        elif op in (b'S',b's',b'f',b'f*',b'B',b'B*'):
            if points:paths.append((points,curves))
            points=[];curves=0
    circles=[(max(x for x,y in pts)-min(x for x,y in pts),max(y for x,y in pts)-min(y for x,y in pts)) for pts,count in paths if count==4]
    actual=sorted(width*25.4/72 for width,height in circles)
    if len(actual)!=3 or any(abs(a-b)>.02 for a,b in zip(actual,[7.5,12,180])):errors.append('Target vector geometry differs from standard: '+p.name)
    if not any(len(pts)==2 and abs(abs(pts[1][0]-pts[0][0])*25.4/72-50)<.02 for pts,count in paths if count==0):errors.append('Incorrect 50 mm vector control line: '+p.name)
if errors:
    print('\n'.join(errors));sys.exit(1)
print('PASS: required documents, local links, Markdown basics, English-script check, public-file/secret checks and vector PDF structure/version/page sizes.')
