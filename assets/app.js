(function(){'use strict';
const prefix='seoHandbook2026:';const tryStorage={get(k){try{return localStorage.getItem(prefix+k)}catch(e){return null}},set(k,v){try{localStorage.setItem(prefix+k,v)}catch(e){}}};
const byId=id=>document.getElementById(id);const all=sel=>Array.from(document.querySelectorAll(sel));
function refresh(){const checks=all('[data-task]');checks.forEach(el=>{el.checked=tryStorage.get(el.dataset.task)==='1'});let done=checks.filter(el=>el.checked).length;let total=checks.length;const p=byId('currentProgress');if(p&&p.dataset.total){total=Number(p.dataset.total);done=0;try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.startsWith(prefix)&&(k.slice(prefix.length).match(/^(lesson-\d{2}-\d+|day-\d{2})$/))&&localStorage.getItem(k)==='1')done++}}catch(e){}}if(byId('currentProgress'))byId('currentProgress').textContent=`${done} / ${total} 项`;if(byId('progressBar'))byId('progressBar').style.width=(total?done/total*100:0)+'%';all('[data-day]').forEach(x=>{x.classList.toggle('done',!!x.querySelector('input:checked'))});}
all('[data-task]').forEach(el=>el.addEventListener('change',()=>{tryStorage.set(el.dataset.task,el.checked?'1':'0');refresh()}));refresh();
const q=byId('courseSearch');let stage='全部';function filter(){const needle=(q?.value||'').trim().toLocaleLowerCase();let visible=0;all('[data-course]').forEach(x=>{const hitStage=stage==='全部'||x.dataset.stage===stage;const hitWord=(x.dataset.search||'').toLocaleLowerCase().includes(needle);x.classList.toggle('hidden',!(hitStage&&hitWord));if(hitStage&&hitWord)visible++});if(byId('filterCount'))byId('filterCount').textContent=visible+' 章';}
if(q)q.addEventListener('input',filter);all('[data-filter]').forEach(b=>b.addEventListener('click',()=>{stage=b.dataset.filter;all('[data-filter]').forEach(x=>x.classList.toggle('active',x===b));filter()}));filter();
function num(id,defaultValue=0){const el=byId(id);let n=Number(el?.value);return Number.isFinite(n)?n:defaultValue}function money(v){return new Intl.NumberFormat('zh-CN',{maximumFractionDigits:0}).format(v)}
function keyword(){let rel=num('relevance'),intent=num('intent'),proof=num('proof'),cost=Math.max(1,num('cost',1));let score=(rel*intent*proof/cost);if(byId('keywordResult'))byId('keywordResult').innerHTML=`相对优先级 <b>${score.toFixed(1)}</b><p>它只比较你自己的候选题，不是搜索量、排名概率或商业收入预测。请给每个评分写依据。</p>`}
['relevance','intent','proof','cost'].forEach(id=>byId(id)?.addEventListener('input',keyword));keyword();
function roi(){const impressions=Math.max(0,num('impressions')),ctr=Math.max(0,Math.min(100,num('ctr'))),leadRate=Math.max(0,Math.min(100,num('leadRate'))),closeRate=Math.max(0,Math.min(100,num('closeRate'))),price=Math.max(0,num('price')),cost=Math.max(0,num('deliveryCost'));const visits=impressions*ctr/100,leads=visits*leadRate/100,orders=leads*closeRate/100,profit=orders*(price-cost);if(byId('roiResult'))byId('roiResult').innerHTML=`模拟自然点击 <b>${money(visits)}</b> · 线索 <b>${leads.toFixed(1)}</b> · 成交 <b>${orders.toFixed(2)}</b><p>模拟毛贡献：${money(profit)} 元（不含内容、人力、税费等其他成本）。所有输入是你自己设定的假设，非承诺。</p>`}
['impressions','ctr','leadRate','closeRate','price','deliveryCost'].forEach(id=>byId(id)?.addEventListener('input',roi));roi();
function snippet(){if(!byId('snTitle'))return;const title=byId('snTitle').value||'页面标题';const desc=byId('snDesc').value||'页面摘要';byId('serpTitle').textContent=title;byId('serpDesc').textContent=desc;byId('snInfo').textContent=`标题 ${[...title].length} 字符｜摘要 ${[...desc].length} 字符（只作编辑参考，不是 Google 截断阈值）`}
['snTitle','snDesc'].forEach(x=>byId(x)?.addEventListener('input',snippet));snippet();
byId('exportProgress')?.addEventListener('click',()=>{const tasks={};try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.startsWith(prefix))tasks[k.slice(prefix.length)]=localStorage.getItem(k)}}catch(e){}const blob=new Blob([JSON.stringify({schema:'seoHandbook2026',exportedAt:new Date().toISOString(),tasks},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='seo-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1200)});
byId('importProgress')?.addEventListener('change',async e=>{const file=e.target.files?.[0];if(!file)return;try{const p=JSON.parse(await file.text());if(p.schema!=='seoHandbook2026'||!p.tasks||typeof p.tasks!=='object')throw Error('不是本项目的进度文件');Object.entries(p.tasks).forEach(([k,v])=>{if(/^(lesson-\d{2}-\d+|day-\d{2})$/.test(k)&&['0','1'].includes(v))tryStorage.set(k,v)});refresh();alert('进度已导入')}catch(err){alert('无法导入：'+err.message)}});
const progressline=byId('readProgress');if(progressline){let raf=false;window.addEventListener('scroll',()=>{if(raf)return;raf=true;requestAnimationFrame(()=>{const h=document.documentElement.scrollHeight-window.innerHeight;progressline.style.width=(h>0?window.scrollY/h*100:0)+'%';raf=false})},{passive:true})}
all('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{const el=byId(b.dataset.copy);if(!el)return;try{await navigator.clipboard.writeText(el.textContent);b.textContent='已复制'}catch(e){b.textContent='请手动选择复制'}setTimeout(()=>b.textContent='复制',1600)}));
// Personalized seven-day route: all route content is also plain HTML for users without JS.
const routeSelect=byId('routeSelect');
function applyRoute(){if(!routeSelect)return;const value=routeSelect.value;all('[data-route]').forEach(x=>x.classList.toggle('hidden',value!=='all'&&x.dataset.route!==value));}
routeSelect?.addEventListener('change',applyRoute);
const routeFromHash=location.hash.match(/^#route-([a-z-]+)$/);
if(routeSelect&&routeFromHash&&all('[data-route]').some(x=>x.dataset.route===routeFromHash[1])){routeSelect.value=routeFromHash[1];applyRoute();}

// Deterministic diagnostic. Never suggests that a real site was crawled or measured.
let diagnosisMarkdown='';
const routes={
 'no-site':['还没有网站：验证需求','先确定客户需求与一个能交付的页面。','no-site',['收集 10 条来自真实用户的原始问题','为 5 个问题做目标 SERP 观察','发布一页可访问的实际内容']],
 'new-site':['新站：先修技术与数据链路','先判断发现、抓取、索引在哪层停止。','new-site',['验证 GSC/Bing 站点属性或记录权限待办','核查重要页 HTTP、robots、canonical 和真实内链','保存索引状态截图与下次复查日期']],
 'existing-site':['已有展示：先用数据选页面','优先检查有真实用户需求且与业务有关的页面。','existing-site',['同口径导出 GSC 查询、页面报表','逐页判断搜索意图和缺失的独特证据','只改一页并记录修改前后及复查日期']],
 'b2b':['转化链路：把访客变成有效咨询','先验证咨询或试用是否真实成功。','b2b',['用一段话定义合格商机和下一步行为','检查落地页是否准确说明交付、证据和入口','完成 3 次成功与 1 次失败的端到端线索测试']],
 'local':['本地门店：验证真实服务和来电','把服务页、地图信息、电话和到店连接起来。','local',['核对名称、地址/服务区、营业时间和联系方式','补真实服务流程、照片及费用口径','测一次手机拨号/预约并记录真实来源']],
 'global-ai':['国际与 AI 工具：验证地区和工具价值','先明确哪些国家可交付，再量化使用与咨询。','global-ai',['检查目标语言 URL、实际可用的服务信息','测试目标地区工具/表单的真实任务完成','使用 GSC/Bing 可用数据建立有来源的观察基线']]
};
const diagForm=byId('diagnosisForm');
function saveText(text,filename,type){const blob=new Blob([text],{type});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=filename;a.click();setTimeout(()=>URL.revokeObjectURL(url),1200);}
diagForm?.addEventListener('submit',e=>{
 e.preventDefault();const site=byId('diagSite').value,search=byId('diagSearch').value,leads=byId('diagLeads').value,business=byId('diagBusiness').value;
 const hours=Math.max(1,Math.min(80,Math.round(num('diagHours',5))));
 let key='new-site',reason='还没有足够搜索数据，先验证数据来源和索引状态。';
 if(site==='none'){key='no-site';reason='没有可访问网站，先用真实问题确定最小的可交付内容。';}
 else if(site==='broken'){key='new-site';reason='网站访问障碍优先于标题和关键词。';}
 else if(search==='unknown'){key='new-site';reason='缺少可核查的站点搜索数据，不能推断有无索引。';}
 else if(search==='notindex'){key='new-site';reason='已有证据显示关键页未索引，优先查抓取和规范信号。';}
 else if(search==='noimp'){key='new-site';reason='已索引但没有展示，需要核实目标用户是否搜索这个问题和页面价值。';}
 else if(search==='imp'){key='existing-site';reason='有展示但点击少，先按查询和页面检查搜索意图，不是盲目加文章。';}
 else if(search==='clicks'&&leads!=='yes'){key=business==='local'?'local':business==='global'?'global-ai':'b2b';reason='已有点击但没有可确认的有效线索，优先检查落地页和测量链路。';}
 else if(search==='clicks'&&leads==='yes'){key=business==='local'?'local':business==='global'?'global-ai':business==='content'?'existing-site':'b2b';reason='已存在可确认的线索，下一步分析质量、成交率与边际成本。';}
 const route=routes[key];const output=byId('diagOutput');output.replaceChildren();
 const h=document.createElement('h2');h.textContent=route[0];output.append(h);
 const p=document.createElement('p');p.textContent='判断依据：'+reason+' 每周可投入约 '+hours+' 小时。';output.append(p);
 const ul=document.createElement('ol');route[3].forEach(action=>{const li=document.createElement('li');li.textContent=action;ul.append(li)});output.append(ul);
 const a=document.createElement('a');a.href='routes.html#route-'+route[2];a.textContent='查看完整 7 天路线 →';output.append(a);
 diagnosisMarkdown=['# SEO 下一步行动清单','',`生成日期：${new Date().toISOString().slice(0,10)}`,`当前诊断：${route[0]}`,`判断依据：${reason}`,`每周时间：${hours} 小时`,'','## 本周 3 件事',...route[3].map((x,i)=>`${i+1}. ${x}`),'','## 验收标准','每个动作保留 URL / CSV / 截图或日志。未验证的数据写“未知”，不写假设成绩。',`路线：routes.html#route-${route[2]}`,''].join('\n');
 byId('downloadDiagnosis').disabled=false;output.focus();
});
byId('downloadDiagnosis')?.addEventListener('click',()=>{if(diagnosisMarkdown)saveText(diagnosisMarkdown,'seo-diagnosis.md','text/markdown;charset=utf-8')});

// Search Console CSV: parse locally, including quoted commas, escaped double-quotes and embedded newlines.
const gscFile=byId('gscFile');let gscResults=[];
function parseCsv(raw){
 if(raw.charCodeAt(0)===0xFEFF)raw=raw.slice(1);
 const records=[];let row=[],field='',quoted=false;
 for(let i=0;i<raw.length;i++){
  const c=raw[i];
  if(quoted){if(c==='"'&&raw[i+1]==='"'){field+='"';i++;}else if(c==='"')quoted=false;else field+=c;}
  else if(c==='"'){if(field.trim())throw Error('CSV 引号位置不正确');quoted=true;}
  else if(c===','){row.push(field);field='';}
  else if(c==='\n'||c==='\r'){if(c==='\r'&&raw[i+1]==='\n')i++;row.push(field);if(row.some(v=>v.trim()))records.push(row);row=[];field='';}
  else field+=c;
  if(records.length>20001)throw Error('文件行数超过 20,000 行限制');
 }
 if(quoted)throw Error('CSV 有未闭合的双引号');
 row.push(field);if(row.some(v=>v.trim()))records.push(row);
 return records;
}
function findCol(headers,names){return headers.findIndex(x=>names.includes(x.trim().toLocaleLowerCase()));}
function metric(v,name){const str=String(v??'').trim().replace(/,/g,'');if(!str)return 0;const n=Number(str);if(!Number.isFinite(n)||n<0)throw Error(name+' 不是有效的非负数字：'+str);return n;}
function pct(v){const s=String(v??'').trim();if(!s)return 0;const n=metric(s.replace('%',''),'CTR');if(s.endsWith('%')){if(n>100)throw Error('CTR 超过 100%');return n/100;}if(n>1)throw Error('CTR 需要带 % 或使用 0–1 小数');return n;}
function gscAnalyze(text){
 const rows=parseCsv(text);if(rows.length<2)throw Error('没有数据行');
 const cols=rows[0].map(s=>s.trim().toLocaleLowerCase());
 const label=findCol(cols,['top queries','query','queries','查询','热门查询','热门搜索查询','最热门的查询','top pages','page','pages','网页','页面','热门网页','最热门的网页']);
 const click=findCol(cols,['clicks','点击次数','点击量','点击']);
 const imp=findCol(cols,['impressions','展示次数','展示量','展示']);
 const ctr=findCol(cols,['ctr','点击率','平均点击率']);
 const pos=findCol(cols,['position','average position','平均排名','平均排名位置','排名']);
 if([label,click,imp,ctr,pos].some(i=>i<0))throw Error('找不到 GSC 的查询/页面、点击、展示、CTR 或平均排名列。请从“搜索结果→查询/网页”导出 CSV。');
 const minimum=Number(byId('gscMin')?.value||100);if(!Number.isFinite(minimum)||minimum<0)throw Error('展示阈值无效');
 const out=[];
 for(let n=1;n<rows.length;n++){
   const r=rows[n];if(!r[label]?.trim())continue;
   const impressions=metric(r[imp],'展示'),clicks=metric(r[click],'点击'),rate=pct(r[ctr]),position=metric(r[pos],'平均排名');
   if(impressions<minimum)continue;
   out.push({label:r[label].trim(),clicks,impressions,ctr:rate,position,score:impressions*(1-rate)});
 }
 out.sort((a,b)=>b.score-a.score||b.impressions-a.impressions);return out;
}
function renderGsc(){const tbody=byId('gscTable')?.querySelector('tbody');if(!tbody)return;tbody.replaceChildren();const limit=Number(byId('gscTop').value);for(const r of gscResults.slice(0,limit)){
 const tr=document.createElement('tr');for(const value of [r.label,r.clicks.toLocaleString(),r.impressions.toLocaleString(),(r.ctr*100).toFixed(1)+'%',r.position.toFixed(1),r.score.toFixed(0)]){const td=document.createElement('td');td.textContent=value;tr.appendChild(td);}tbody.appendChild(tr);
 }}
byId('gscRun')?.addEventListener('click',async()=>{
 gscResults=[];byId('gscDownload').disabled=true;
 const file=gscFile?.files?.[0];if(!file){byId('gscStatus').textContent='先选择 CSV 文件。';return;}
 try{if(file.size>2*1024*1024)throw Error('文件超过 2 MB');gscResults=gscAnalyze(await file.text());renderGsc();byId('gscStatus').textContent=`解析完成，${gscResults.length} 行达到观察阈值。结果不代表流量预测；请人工核查排名、意图和业务价值。`;byId('gscDownload').disabled=gscResults.length===0;}
 catch(e){byId('gscTable')?.querySelector('tbody')?.replaceChildren();byId('gscStatus').textContent='分析失败：'+e.message;}
});
byId('gscTop')?.addEventListener('change',renderGsc);
function csvSafe(value){let s=String(value??'');if(/^[\s]*[=+@-]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';}
byId('gscDownload')?.addEventListener('click',()=>{
 const header=['查询或页面','点击','展示','CTR','平均排名','观察优先值','人工判断','下一步动作','复核日期'];
 const rows=gscResults.slice(0,Number(byId('gscTop').value)).map(r=>[r.label,r.clicks,r.impressions,(r.ctr*100).toFixed(1)+'%',r.position.toFixed(1),r.score.toFixed(0),'待核对搜索意图和业务价值','先检查页面质量与实际查询','']);
 saveText('\uFEFF'+[header,...rows].map(r=>r.map(csvSafe).join(',')).join('\r\n'),'gsc-review-tasks.csv','text/csv;charset=utf-8');
});
})();
