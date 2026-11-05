import csv,tempfile,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from gsc_opportunities import parse_ctr,analyze

class TestGSC(unittest.TestCase):
  def test_percent(self):
    self.assertAlmostEqual(parse_ctr('3.5%'),.035)
    self.assertAlmostEqual(parse_ctr('0.035'),.035)
    with self.assertRaises(ValueError):parse_ctr('35')
  def test_gsc_en_export(self):
    with tempfile.TemporaryDirectory() as t:
      p=Path(t)/'gsc.csv'
      p.write_text('Top queries,Clicks,Impressions,CTR,Position\nseo tutorial,20,1000,2%,8.5\nseo test,2,20,10%,5\n',encoding='utf-8')
      result=analyze(str(p))
      self.assertEqual(len(result),1)
      self.assertEqual(result[0][1],'seo tutorial')
      self.assertAlmostEqual(result[0][4],0.02)
  def test_gsc_cn_export(self):
    with tempfile.TemporaryDirectory() as t:
      p=Path(t)/'gsc-cn.csv'
      p.write_text('查询,点击次数,展示次数,点击率,平均排名\nSEO课程,3,300,1%,7.5\n',encoding='utf-8-sig')
      result=analyze(str(p))
      self.assertEqual(result[0][3],300)
      self.assertEqual(result[0][1],'SEO课程')
if __name__=='__main__':unittest.main()
