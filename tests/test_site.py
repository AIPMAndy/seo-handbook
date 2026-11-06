import json, re, shutil, tempfile, unittest
from pathlib import Path
from xml.etree import ElementTree
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from site_audit import audit

class TestCurriculum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters=json.loads((ROOT/'data/chapters.json').read_text(encoding='utf-8'))
        cls.sources={x['id']:x for x in json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))}
    def test_chapter_depth(self):
        self.assertGreaterEqual(len(self.chapters),40)
        self.assertGreaterEqual(sum(len(x['steps']) for x in self.chapters),160)
        for c in self.chapters:
            self.assertGreaterEqual(len(c['steps']),4)
            self.assertGreaterEqual(len(c['example']),18)
            self.assertGreaterEqual(len(c['outcome']),12)
            for s in c['steps']:
                for k in ('do','done','stuck'):
                    self.assertGreater(len(s[k]),10,f'{c["id"]} {k} too generic')
    def test_unique_slug_and_source_integrity(self):
        self.assertEqual(len({x['slug'] for x in self.chapters}),len(self.chapters))
        for c in self.chapters:
            self.assertTrue(c['sources'],c['title'])
            for item in c['sources']:self.assertIn(item,self.sources)
    def test_index_contains_real_links(self):
        page=(ROOT/'_site/index.html').read_text(encoding='utf-8')
        self.assertEqual(page.count('data-course data-stage='),len(self.chapters))
        self.assertIn('data-total="194"',page)
    def test_daily_plan_has_30_checks(self):
        page=(ROOT/'_site/plan.html').read_text(encoding='utf-8')
        self.assertEqual(page.count('data-day>'),30)
        self.assertEqual(page.count('data-task="day-'),30)
    def test_author_contact_and_website_are_visible_on_all_pages(self):
        pages=list((ROOT/'_site').rglob('*.html'))
        self.assertEqual(len(pages),63)
        for p in pages:
            content=p.read_text(encoding='utf-8')
            with self.subTest(page=str(p.relative_to(ROOT))):
                self.assertIn('https://metaver.vip/',content)
                self.assertIn('https://metaver.vip/services',content)
                self.assertIn('AIPMAndy',content)
                self.assertIn('data-copy-wechat',content)
                self.assertIn('个人微信：',content)
                contact='href="../contact.html"' if p.parent.name in ('lessons','sops') else 'href="contact.html"'
                self.assertIn(contact,content)
    def test_contact_page_is_discoverable(self):
        contact=(ROOT/'_site/contact.html').read_text(encoding='utf-8')
        self.assertIn('<h1>联系 AI 酋长 Andy</h1>',contact)
        self.assertIn('data-wechat="AIPMAndy"',contact)
        sitemap=(ROOT/'_site/sitemap.xml').read_text(encoding='utf-8')
        self.assertIn('https://aipmandy.github.io/seo-handbook/contact.html',sitemap)
    def test_homepage_author_ad_is_prominent(self):
        page=(ROOT/'_site/index.html').read_text(encoding='utf-8')
        self.assertLess(page.index('id="meet-andy"'),page.index('id="courses"'))
        self.assertIn('添加个人微信 · AIPMAndy',page)

    def test_no_misleading_robots(self):
        self.assertFalse((ROOT/'_site/robots.txt').exists())

class TestAuditFailures(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.site=Path(self.tmp.name)/'_site'
        shutil.copytree(ROOT/'_site',self.site)
    def tearDown(self):self.tmp.cleanup()
    def check_error_after_edit(self, old, new, file='index.html',expected=''):
        p=self.site/file
        src=p.read_text(encoding='utf-8')
        self.assertIn(old,src)
        p.write_text(src.replace(old,new,1),encoding='utf-8')
        errors,_,_=audit(self.site)
        self.assertTrue(any(expected in e for e in errors),errors)
    def test_clean_site(self):
        errors,warnings,count=audit(self.site)
        self.assertEqual(errors,[])
        self.assertEqual(count,63)
    def test_missing_page_found(self):
        dest=self.site/'plan.html'
        dest.unlink()
        errors,_,_=audit(self.site)
        self.assertTrue(any('broken internal href' in e for e in errors))
    def test_wrong_canonical(self):
        self.check_error_after_edit('https://aipmandy.github.io/seo-handbook/','https://bad.example/index.html',expected='canonical mismatch')
    def test_double_h1(self):
        self.check_error_after_edit('<main>','<main><h1>错误的额外标题</h1>',expected='exactly one H1')
    def test_jsonld_invalid(self):
        self.check_error_after_edit('"@context":"https://schema.org"','"@context":broken',expected='JSON-LD parse failed')
    def test_noindex_blocker(self):
        self.check_error_after_edit('content="index,follow,max-image-preview:large"','content="noindex,follow"',expected='accidental noindex')
    def test_sitemap_added_fake_url(self):
        p=self.site/'sitemap.xml'
        s=p.read_text(encoding='utf-8')
        s=s.replace('</urlset>','<url><loc>https://aipmandy.github.io/seo-handbook/fake.html</loc></url></urlset>')
        p.write_text(s,encoding='utf-8')
        errors,_,_=audit(self.site)
        self.assertTrue(any('Sitemap URL mismatch' in e for e in errors),errors)

if __name__=='__main__':unittest.main()
