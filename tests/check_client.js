/** Dependency-free headless logic regression tests. Does not claim browser visual testing. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.resolve(__dirname,'../assets/app.js'),'utf8');
assert.match(source,/\}\)\(\);\s*$/);
const instrumented=source.replace(/\}\)\(\);\s*$/,'globalThis.__test={parseCsv,gscAnalyze,csvSafe};})();');
const mockInputs={gscMin:{value:'100',addEventListener(){}},gscTop:{value:'20',addEventListener(){}}};
const context={
  document:{getElementById:id=>mockInputs[id]||null,querySelectorAll:()=>[],documentElement:{scrollHeight:500}},
  location:{hash:''},window:{innerHeight:700,scrollY:0},
  console,Number,Intl,JSON,Math,Date,Blob,URL,
};
vm.createContext(context);
vm.runInContext(instrumented,context,{timeout:1500});
const {parseCsv,gscAnalyze,csvSafe}=context.__test;
const basic='Top queries,Clicks,Impressions,CTR,Position\r\n"AI tools, free",2,200,1%,9.5\r\n';
assert.equal(parseCsv(basic).length,2);
assert.equal(parseCsv(basic)[1][0],'AI tools, free');
const rows=gscAnalyze(basic);
assert.equal(rows.length,1);
assert.equal(rows[0].label,'AI tools, free');
assert.equal(rows[0].score,198);
const multi='Query,Clicks,Impressions,CTR,Position\n"test\ncase",1,100,1%,10\n';
assert.equal(gscAnalyze(multi)[0].label,'test\ncase');
assert.throws(()=>gscAnalyze('Query,Clicks,Impressions,CTR,Position\nhey,1,100,250%,10\n'),/超过 100%/);
assert.throws(()=>gscAnalyze('Query,Clicks,Impressions,CTR,Position\nhey,-1,100,1%,10\n'),/非负/);
assert.throws(()=>gscAnalyze('wrong,header\n1,2'),/找不到 GSC/);
assert.throws(()=>parseCsv('Query,Value\n"unfinished,value'),/未闭合/);
const injection=csvSafe('=HYPERLINK("https://bad.example","test")');
assert.ok(injection.startsWith('"\'=HYPERLINK'));
const normal=csvSafe('普通关键词');assert.equal(normal,'"普通关键词"');
const boms=gscAnalyze('\uFEFF'+basic);assert.equal(boms.length,1);
mockInputs.gscMin.value='300';assert.equal(gscAnalyze(basic).length,0);
console.log('PASS: 10 client-logic scenarios (CSV parsing, estimates, validation, formula neutralization)');
