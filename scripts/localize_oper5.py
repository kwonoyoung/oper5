from pathlib import Path
import re, json
p=Path('index.html')
t=p.read_text(encoding='utf-8',errors='replace')
SITE='https://kwonoyoung.github.io/oper5/'
BLANK='data:image/gif;base64,R0lGODlhAQABAAAAACwAAAAAAQABAAA='

def between(start,end,repl):
    global t
    a=t.find(start)
    if a<0: return False
    b=t.find(end,a)
    if b<0: return False
    t=t[:a]+repl+t[b:]
    return True

t=re.sub(r'<style id="oper5-no-ads">.*?</style>','',t,flags=re.S)
t=re.sub(r'<style id="oper5-local-mode-style">.*?</style>','',t,flags=re.S)
t=re.sub(r'<script id="oper5-cleanup-runtime">.*?</script>','',t,flags=re.S)
t=re.sub(r'<script id="oper5-local-network-guard">.*?</script>','',t,flags=re.S)
t=re.sub(r'<script>\(function\(\)\{var C=.*?</script>','',t,count=1,flags=re.S)
t=re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]+">','',t)
t=re.sub(r'<script[^>]+googletagmanager\.com/gtag/js[^>]*></script>','',t,flags=re.I)
t=re.sub(r'<script>window\.dataLayer=window\.dataLayer\|\|\[\];function gtag\(\)\{dataLayer\.push\(arguments\);\}.*?</script>','',t,count=1,flags=re.S)

t=t.replace("const PRODUCT_ORIGIN = 'https://youre-next.app/';",f"const PRODUCT_ORIGIN = '{SITE}';")
t=t.replace("const SELF_HOSTS = [location.hostname, 'youre-next.app', 'youre-next.web.app'];","const SELF_HOSTS = [location.hostname];")
for old in ['YOU’RE NEXT',"YOU'RE NEXT",'YOU&amp;#39;RE NEXT','YOU&#39;RE NEXT','YOU&APOS;RE NEXT']:
    t=t.replace(old,'오춘기 권오영')
t=t.replace("const STORY_DOMAIN = 'youre-next.app';","const STORY_DOMAIN = location.hostname;")
t=t.replace("mark: 'youre-next.app · @' + IG_HANDLE","mark: location.hostname + ' · @' + IG_HANDLE")
t=re.sub(r"const FS_DOCS = `projects/\$\{FS\.project\}/databases/\(default\)/documents`, FS_URL = `https://firestore\.googleapis\.com/v1/\$\{FS_DOCS\}`;","const FS_DOCS = `projects/${FS.project}/databases/(default)/documents`, FS_URL = '';",t,count=1)
t=t.replace('https://youre-next.app/ko/?lang=ko&amp;cc=KR#/','./?lang=ko&amp;cc=KR#/')
t=t.replace('https://youre-next.app/ko/?lang=ko&cc=KR#/','./?lang=ko&cc=KR#/')
t=t.replace('https://youre-next.app/ko/?lang=ko&cc=KR',SITE)
t=t.replace('https://youre-next.app/ko/',SITE)
t=t.replace('https://youre-next.app/en/',SITE+'?lang=en&cc=US#/')
t=t.replace('https://youre-next.app/ja/',SITE+'?lang=ja&cc=JP#/')
t=t.replace('https://youre-next.app/us/es/',SITE+'?lang=es&cc=US#/')
t=t.replace('https://youre-next.app/privacy/','#')
t=t.replace('https://youre-next.app/',SITE)
t=re.sub(r'https://kwonoyoung\.github\.io/oper5/house/[^"\'\s)<>]+',BLANK,t)
t=re.sub(r'https://kwonoyoung\.github\.io/oper5/og/[^"\'\s)<>]+',BLANK,t)
t=re.sub(r'https://youre-next\.app/house/[^"\'\s)<>]+',BLANK,t)
t=re.sub(r'https://youre-next\.app/og/[^"\'\s)<>]+',BLANK,t)
t=re.sub(r'<meta property="og:url" content="[^"]*">',f'<meta property="og:url" content="{SITE}">',t,count=1)
t=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{SITE}">',t,count=1)
t=re.sub(r'<link rel="alternate"[^>]+>','',t)

between('async function geoCC() {','const by =',"async function geoCC() { return ''; }\n")
fscreate='''async function fsCreate(docs) {\n  try {\n    const key='oper5.local.records';\n    const rows=JSON.parse(localStorage.getItem(key)||'[]');\n    const now=new Date().toISOString();\n    for(const [col,data] of (docs||[])) rows.push({id:fsId(),collection:col,data,createdAt:now});\n    localStorage.setItem(key,JSON.stringify(rows.slice(-300)));\n  } catch(e) {}\n  return true;\n}\n'''
between('async function fsCreate(docs) {','/* 자체 유입 집계',fscreate)
between('function logVisit() {','const PARTNER_EMAIL',"function logVisit() { return; }\n")
between('function houseCount(kind, id, slot) {','const SIDE_ON',"function houseCount(kind,id,slot) { return; }\n")
t=t.replace("const SIDE_ON = () => !!(window.matchMedia && window.matchMedia('(min-width:1280px)').matches);","const SIDE_ON = () => false;")

prep='''function prepFill(body, slug) {\n  if(body.dataset.slug===slug) return;\n  body.dataset.slug=slug;\n  const draw=d=>{if(body.dataset.slug!==slug||!document.body.contains(body))return;body.innerHTML=prepPanelHtml(d,slug);prepPaint(body.closest('.prep'));};\n  if(prepCache[slug]){draw(prepCache[slug]);return;}\n  const j=jobBy[slug];\n  if(!j){delete body.dataset.slug;body.innerHTML=`<p class="prep-err">${esc(t('prep_fail'))}</p>`;return;}\n  const tasks=((j.humanTasks_ko&&j.humanTasks_ko.filter(Boolean))||(j.humanTasks&&j.humanTasks.filter(Boolean))||[]);\n  const title=j.name_ko||j.name||slug, dif=j.years<3?2:j.years<7?3:j.years<15?4:3;\n  const d={\n    summary:{ko:`${title} 준비를 위한 간이 가이드입니다. 페이지에 내장된 직업 데이터를 사용합니다.`,en:`A lightweight prep guide for ${j.name||title}, generated from the job data embedded in this page.`,ja:`${j.name_ja||title} の簡易準備ガイドです。`},\n    difficulty:dif,difficulty_why_ko:'자격 요건·훈련 기간·직무 전문성을 기준으로 한 간이 추정입니다.',\n    time_to_entry_months:{typical:dif<=2?6:dif===3?12:24,min:dif<=2?3:dif===3?6:12},\n    cost_krw_manwon:{min:dif<=2?20:80,max:dif<=2?120:dif===3?300:600,note_ko:'교육·시험·포트폴리오 비용은 개인별로 다릅니다.'},\n    salary_krw_manwon:{basis:'내장 직업 데이터 기반 간이 예시',entry:3000,median:4200,senior:5600,variance_ko:'지역·회사·고용형태에 따라 차이가 큽니다.',refs:['실제 채용 공고','직무 소개 자료','자격 시험 안내']},\n    requirements:{education:'채용 공고별 상이 — 지원 전 확인',physical:'직무 특성에 따라 다름',age_note:'공고·제도 기준 확인',license:[]},\n    path:[\n      {step:1,title_ko:'직무 이해',what_ko:tasks[0]||'핵심 업무와 현장 역할을 파악합니다.',months:1,cost_manwon:0},\n      {step:2,title_ko:'기초 역량 준비',what_ko:tasks[1]||'필수 역량과 도구를 익힙니다.',months:dif<=2?2:4,cost_manwon:dif<=2?20:80},\n      {step:3,title_ko:'증빙 자료 만들기',what_ko:tasks[2]||'이력서·포트폴리오·실습 결과를 준비합니다.',months:dif<=2?2:4,cost_manwon:30},\n      {step:4,title_ko:'지원·면접',what_ko:tasks[3]||'공고를 분석하고 면접을 준비합니다.',months:1,cost_manwon:0}],\n    routes_ko:(j.alt||[]).filter(Boolean).slice(0,5),\n    plan:{weekly_hours:dif<=2?5:dif===3?7:10,phases:[\n      {name_ko:'1단계 · 탐색',weeks:2,goals_ko:['채용 공고 10개 읽기','필수 역량 정리'],checklist_ko:['관심 기관 목록 만들기','핵심 직무 3가지 요약']},\n      {name_ko:'2단계 · 역량 준비',weeks:dif<=2?4:8,goals_ko:tasks.slice(0,3).length?tasks.slice(0,3):['핵심 업무 연습'],checklist_ko:['학습 계획 세우기','샘플 작업 1개 완성','실전 연습 기록']},\n      {name_ko:'3단계 · 지원 준비',weeks:3,goals_ko:['이력서·자기소개서 정리','면접 대비'],checklist_ko:['이력서 초안','작업물 정리','모의 면접 1회']}],\n      resources_ko:[{name:'관련 채용 공고',type:'공고',note:'최신 요건 확인'},{name:'직무 소개 자료',type:'학습',note:'업무 흐름 파악'},{name:'자격·시험 기관 공지',type:'공식',note:'필수 자격 확인'}]},\n    pitfalls_ko:['회사·기관마다 요구 조건이 다를 수 있습니다.','실제 공고와 공식 기관 안내를 우선 확인하세요.'],\n    ai_note_ko:j.why_ko||'반복·정형 업무는 자동화 압력이 크고, 판단·소통·책임이 필요한 업무는 사람이 더 강합니다.'};\n  prepCache[slug]=d;draw(d);\n}\n'''
between('function prepFill(body, slug) {','/* one delegated pair',prep)

auth='''async function authToken() {\n  let a=authLoad();\n  if(!a||!a.uid){a={idToken:'local',refreshToken:'',uid:'local-'+fsId(),expiresAt:Date.now()+315360000000};authSave(a);}\n  return 'local';\n}\n'''
between('async function authToken() {','/* one REST call',auth)
call='''async function fsCall(url,body,token) { const e=new Error('LOCAL_ONLY');e.status=404;e.code='LOCAL_ONLY';throw e; }\n'''
between('async function fsCall(url, body, token) {','const fsDec',call)
t=re.sub(r'const fsAuthCommit = async writes => .*?;\n','const fsAuthCommit = async writes => true;\n',t,count=1)
t=re.sub(r'const fsRunQuery = async structuredQuery => .*?;\n','const fsRunQuery = async structuredQuery => [];\n',t,count=1)
t=re.sub(r'^async function fsGetDoc\(path\).*$', 'async function fsGetDoc(path) { return null; }', t, count=1, flags=re.M)

local_inv_create='''async function invCreate() {\n  await authToken();\n  const code=fsId(),exp=new Date(Date.now()+INV_DAYS*864e5).toISOString();\n  track('inv_create',{});\n  fitUnlock('invite');\n  return invSave({code,n:INV_NEED,exp});\n}\n'''
between('async function invCreate() {','let invPending = null;',local_inv_create)
local_inv_ensure='''function invEnsure(force) {\n  let v=invLoad();\n  if(!v||force||invExpired(v)){const code=fsId(),exp=new Date(Date.now()+INV_DAYS*864e5).toISOString();v=invSave({code,n:INV_NEED,exp});}\n  if(!fitUnlocked()) fitUnlock('invite');\n  return Promise.resolve(v);\n}\n'''
between('function invEnsure(force) {','/* 현황 폴링',local_inv_ensure)
local_inv_poll='''async function invPoll() {\n  let v=invLoad();\n  if(!v) v=await invEnsure(false);\n  v=invSave({code:v.code,n:INV_NEED,exp:v.exp});\n  invUnlock();\n  return v;\n}\n'''
between('async function invPoll() {','/* 한 번 얻은 해제',local_inv_poll)
between('async function invCredit() {','/* 진행 표시',"async function invCredit() { return; }\n")
between('function track(name, params) {','let REF0_SENT',"function track(name, params) { return; }\n")
between('function trackPage(head, p) {','let RENDERED_HREF',"function trackPage(head,p) { return; }\n")

css='''<style id="oper5-no-ads">.ad-slot,.ad-side,.ad-gate,.ad-house,.ad-rec[data-ad-rec],ins.adsbygoogle,[aria-label="광고"],[aria-label="広告"]{display:none!important}</style>'''
t=t.replace('</head>',css+'</head>',1)
js='''<script id="oper5-cleanup-runtime">(()=>{\nconst exact=new Set(['개인정보처리방침','Instagram','한국어','KR KR','KR']);\nconst bad='.ad-slot,.ad-side,.ad-gate,.ad-house,.ad-rec[data-ad-rec],ins.adsbygoogle,[aria-label="광고"],[aria-label="広告"]';\nconst clean=root=>{if(!root)return;const q=root.querySelectorAll?root.querySelectorAll.bind(root):()=>[];try{q(bad).forEach(x=>x.remove());q('a,button,select,[role="button"]').forEach(el=>{const tx=(el.textContent||'').replace(/\\s+/g,' ').trim(),h=(el.getAttribute('href')||'').toLowerCase(),a=(el.getAttribute('aria-label')||'').toLowerCase(),tt=(el.getAttribute('title')||'').toLowerCase();if(tx==='개인정보처리방침'||tx==='Instagram'||exact.has(tx)||/privacy|instagram\\.com|language|locale|country/.test(h+' '+a+' '+tt))(el.closest('li,nav,.lang,.language,.locale,.country,.dropdown,.select-wrap')||el).remove();});}catch(e){}};\nclean(document);new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>n.nodeType===1&&clean(n)))).observe(document.documentElement,{childList:true,subtree:true});\nconst rf=window.fetch?window.fetch.bind(window):null;if(rf)window.fetch=(input,init)=>{try{const raw=typeof input==='string'?input:(input&&input.url)||'',u=new URL(raw,location.href);if(u.origin!==location.origin)return Promise.resolve(new Response(JSON.stringify({localOnly:true}),{status:503,headers:{'Content-Type':'application/json'}}));}catch(e){}return rf(input,init);};\n})();</script>'''
t=t.replace('</body>',js+'</body>',1)

p.write_text(t,encoding='utf-8')
Path('geo.json').write_text(json.dumps({'cc':'KR'},ensure_ascii=False),encoding='utf-8')