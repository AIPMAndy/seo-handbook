#!/usr/bin/env python3
"""Summarize Google Search Console CSV exports, without inventing traffic estimates."""
import argparse,csv,re,sys
from pathlib import Path

def parse_number(x):
    x=str(x or '').strip().replace(',','')
    if not x:return 0.0
    return float(x)

def parse_ctr(x):
    x=str(x or '').strip()
    if x.endswith('%'):return float(x[:-1].replace(',',''))/100
    n=parse_number(x)
    if not 0<=n<=1:raise ValueError('CTR 无 % 标记时必须是 0 到 1 的小数；输入如 12.3%')
    return n

def pick(row,aliases):
    data={k.strip().casefold():v for k,v in row.items() if k}
    for a in aliases:
        if a.casefold() in data:return data[a.casefold()]
    return None

def analyze(path,min_impressions=100):
    results=[]
    with open(path,encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames:raise ValueError('CSV 无表头')
        for num,row in enumerate(reader,2):
            query=pick(row,['Top queries','Query','Queries','查询','热门查询','热门搜索查询','最热门的查询'])
            page=pick(row,['Top pages','Page','Pages','网页','页面','热门网页','最热门的网页'])
            label=query or page
            if not label:raise ValueError('未找到“查询/页面”列，确认导出的是 GSC 查询或网页报表')
            try:
                clicks=parse_number(pick(row,['Clicks','点击次数','点击量','点击']))
                impressions=parse_number(pick(row,['Impressions','展示次数','展示量','展示']))
                ctr=parse_ctr(pick(row,['CTR','点击率','平均点击率']))
                pos=parse_number(pick(row,['Position','Average position','平均排名','平均排名位置','排名']))
            except (ValueError,TypeError) as e:raise ValueError(f'第 {num} 行指标解析失败：{e}') from e
            if impressions<min_impressions:continue
            # Ranking is NOT an estimated volume or an SEO guaranteed opportunity.
            # The heuristic merely prefers rows with more observations and lower CTR.
            priority=impressions*(1-ctr)
            results.append((priority,label,int(clicks),int(impressions),ctr,pos))
    return sorted(results,reverse=True)

def main(argv=None):
    ap=argparse.ArgumentParser(description='从 GSC 导出的查询/页面 CSV 列出值得人工核查的行')
    ap.add_argument('csv',help='Search Console 查询或网页报表 CSV')
    ap.add_argument('--min-impressions',type=int,default=100,help='最低展示次数，默认 100')
    ap.add_argument('--top',type=int,default=20,help='输出条数')
    args=ap.parse_args(argv)
    try:res=analyze(args.csv,args.min_impressions)
    except (ValueError,OSError) as e:print('错误：',e,file=sys.stderr);return 2
    print('说明：按展示×(1-CTR)做待核查排序；不是“损失点击数”或实际商业价值。必须手动核对搜索意图、排名、品牌属性和页面质量。')
    print('查询/网页\t点击\t展示\tCTR\t平均排名\t观察优先值')
    for score,label,clicks,imp,ctr,pos in res[:args.top]:
        print(f'{label}\t{clicks}\t{imp}\t{ctr:.1%}\t{pos:.1f}\t{score:.0f}')
    if not res:print('没有满足展示阈值的数据；可降低阈值或积累更多样本。')
    return 0
if __name__=='__main__':sys.exit(main())
