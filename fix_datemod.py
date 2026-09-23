import glob, re, subprocess
from datetime import date

def visible_date(html):
    # A : <time datetime="D"...>...Mis a jour   (date puis libelle dans la balise)
    m = re.search(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})"[^>]*>[^<]*[Mm]is à jour', html)
    if m: return m.group(1)
    # B : Mis a jour ... <time datetime="D"   (libelle puis balise)
    m = re.search(r'[Mm]is à jour[^<]{0,40}<time[^>]*datetime="(\d{4}-\d{2}-\d{2})"', html)
    if m: return m.group(1)
    # C : repli - premiere balise time
    m = re.search(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})"', html)
    return m.group(1) if m else None

def git_date(f):
    try:
        o=subprocess.run(["git","log","-1","--format=%cs","--",f],capture_output=True,text=True,timeout=15).stdout.strip()
        return o or date.today().isoformat()
    except Exception: return date.today().isoformat()

fixed=[]
for f in sorted(glob.glob("*.html")):
    h=open(f,encoding='utf-8',errors='ignore').read()
    if 'dateModified' in h: continue
    if not re.search(r'"@type"\s*:\s*"(Article|BlogPosting|NewsArticle)"',h) and '"datePublished"' not in h: continue
    d=visible_date(h) or git_date(f)
    ins=', "dateModified": "%s"'%d
    new,n=re.subn(r'("datePublished"\s*:\s*"\d{4}-\d{2}-\d{2}(?:T[0-9:+\-]+)?")',r'\1'+ins,h,count=1)
    if n==0:
        new,n=re.subn(r'("@type"\s*:\s*"(?:Article|BlogPosting|NewsArticle)")',r'\1'+ins,h,count=1)
    if n==1:
        open(f,'w',encoding='utf-8').write(new); fixed.append((f,d))
print("Corrigees :",len(fixed))
