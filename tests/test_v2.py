import csv,json,tempfile,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from gsc_compare import compare,load_file

class TestV2Content(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.sops=json.loads((ROOT/'data/sops.json').read_text(encoding='utf8'))
  cls.routes=json.loads((ROOT/'data/routes.json').read_text(encoding='utf8'))
 def test_deep_sops_are_actionable(self):
  self.assertEqual(len(self.sops),13)
  self.assertEqual(sum(len(x['steps']) for x in self.sops),65)
  for sop in self.sops:
   self.assertGreaterEqual(len(sop['steps']),5)
   self.assertGreater(len(sop['entry']),9)
   self.assertGreater(len(sop['deliverable']),9)
   self.assertTrue((ROOT/'_site/sops'/f'{sop["id"]}.html').is_file())
   for step in sop['steps']:
    for key in ('do','proof','stuck'):
     self.assertGreater(len(step[key]),8,(sop['id'],key))
 def test_routes_deep_links_resolve(self):
  self.assertEqual(len(self.routes),6)
  chapters=json.loads((ROOT/'data/chapters.json').read_text(encoding='utf8'))
  self.assertEqual(len({x['id'] for x in self.routes}),6)
  for route in self.routes:
   self.assertEqual(len(route['daily']),7)
   self.assertEqual(len(route['chapters']),7)
   for chap in route['chapters']:
    self.assertTrue(1<=chap<=len(chapters))
   for day in route['daily']:
    self.assertGreater(len(day[0]),8)
    self.assertGreater(len(day[1]),3)
 def test_v2_pages_and_sitemap(self):
  for path in ['routes.html','sops.html','diagnose.html','opportunities.html','plan-90.html']:
   self.assertTrue((ROOT/'_site'/path).is_file())
  self.assertIn('在本地分析',(ROOT/'_site/opportunities.html').read_text(encoding='utf8'))
  self.assertIn('人工审查任务',(ROOT/'_site/opportunities.html').read_text(encoding='utf8'))
  self.assertEqual(len(list((ROOT/'_site/sops').glob('*.html'))),13)
 def test_sources_integrity(self):
  sources={x['id']:x for x in json.loads((ROOT/'data/sources.json').read_text(encoding='utf8'))}
  self.assertIn('bing-ai-performance',sources)
  for sop in self.sops:
   for x in sop['sources']:self.assertIn(x,sources)

class TestGSCComparison(unittest.TestCase):
 def test_delta_and_quotes(self):
  r=compare(ROOT/'templates/gsc-before.csv',ROOT/'templates/gsc-after.csv')
  a={x['label']:x for x in r}
  self.assertEqual(len(r),3)
  self.assertEqual(a['seo tutorial']['delta_clicks'],12)
  self.assertEqual(a['site audit']['delta_clicks'],-1)
  self.assertEqual(a['AI tools, free']['delta_impressions'],10)
 def test_reject_incompatible_sheets(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'pages.csv';p.write_text('Page,Clicks,Impressions,CTR,Position\nhttps://example.org,10,100,10%,2\n')
   with self.assertRaisesRegex(ValueError,'同为'):compare(ROOT/'templates/gsc-before.csv',p)
 def test_reject_duplicate_labels(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'bad.csv';p.write_text('Query,Clicks,Impressions,CTR,Position\na,1,100,1%,4\na,1,100,1%,4\n')
   with self.assertRaisesRegex(ValueError,'重复'):load_file(p)
 def test_no_invented_rows(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'new.csv';p.write_text('Query,Clicks,Impressions,CTR,Position\nnew topic,1,40,2.5%,13\n')
   r=compare(ROOT/'templates/gsc-before.csv',p,min_impressions=40)
   a={x['label']:x for x in r}
   self.assertEqual(a['new topic']['status'],'新增于后期导出')
   self.assertEqual(a['new topic']['old_clicks'],0)

 def test_reject_blank_metrics_instead_of_making_up_zero(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'blank.csv'
   p.write_text('Query,Clicks,Impressions,CTR,Position\nterm,,100,0%,3\n',encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'留空'):load_file(p)
