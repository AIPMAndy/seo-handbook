#!/usr/bin/env python3
"""Compare two *same-scope* GSC query/page CSV exports; cannot attribute causality.
No dependencies. Does not upload user data. CSV rows are exported for manual audit.
"""
from __future__ import annotations
import argparse,csv,sys
from pathlib import Path
from gsc_opportunities import parse_number, parse_ctr, pick

QUERY=['Top queries','Query','Queries','查询','热门查询','热门搜索查询','最热门的查询']
PAGE=['Top pages','Page','Pages','网页','页面','热门网页','最热门的网页']
CLICK=['Clicks','点击次数','点击量','点击']
IMP=['Impressions','展示次数','展示量','展示']
CTR=['CTR','点击率','平均点击率']
POS=['Position','Average position','平均排名','平均排名位置','排名']

def load_file(path):
    data={}
    with open(path,encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames:raise ValueError(f'{path}: 空表或缺表头')
        names={x.strip().casefold() for x in reader.fieldnames if x}
        mode='query' if names & {x.casefold() for x in QUERY} else ('page' if names & {x.casefold() for x in PAGE} else None)
        if not mode:raise ValueError(f'{path}: 没有查询或页面列')
        for rownum,row in enumerate(reader,2):
            label=pick(row, QUERY if mode=='query' else PAGE)
            if not label:continue
            label=label.strip()
            if label in data:raise ValueError(f'{path}: 第 {rownum} 行重复标签 {label[:60]}；需先按相同维度导出，不能重复拼接')
            try:
                c=pick(row,CLICK);i=pick(row,IMP);ctr=pick(row,CTR);pos=pick(row,POS)
                if any(x is None or not str(x).strip() for x in (c,i,ctr,pos)):raise ValueError('缺少或留空点击、展示、CTR 或平均排名数值（不能把未知当成 0）')
                values=(parse_number(c),parse_number(i),parse_ctr(ctr),parse_number(pos))
                if any(x<0 for x in values):raise ValueError('指标不能为负')
            except (ValueError,TypeError) as e:raise ValueError(f'{path} 第 {rownum} 行指标错误：{e}') from e
            data[label]={'clicks':values[0],'impressions':values[1],'ctr':values[2],'position':values[3]}
    return mode,data

def compare(before,after,min_impressions=10):
    t1,a=load_file(before);t2,b=load_file(after)
    if t1!=t2:raise ValueError('两次导出必须同为查询报表或同为页面报表')
    rows=[]
    for label in a.keys()|b.keys():
        old=a.get(label,{'clicks':0,'impressions':0,'ctr':0,'position':None})
        new=b.get(label,{'clicks':0,'impressions':0,'ctr':0,'position':None})
        if max(old['impressions'],new['impressions'])<min_impressions:continue
        rows.append({'type':t1,'label':label,'old_clicks':old['clicks'],'new_clicks':new['clicks'],
           'delta_clicks':new['clicks']-old['clicks'],'old_impressions':old['impressions'],'new_impressions':new['impressions'],
           'delta_impressions':new['impressions']-old['impressions'],'old_ctr':old['ctr'],'new_ctr':new['ctr'],
           'old_position':old['position'],'new_position':new['position'],
           'status':'新增于后期导出' if label not in a else '后期导出未出现' if label not in b else '两期都有'})
    return sorted(rows,key=lambda x:(x['delta_clicks'],x['delta_impressions'],x['label']))

def main(argv=None):
    parser=argparse.ArgumentParser(description='同口径对比两期 Search Console 查询/页面 CSV，列出数据变化，不能证明因果')
    parser.add_argument('before');parser.add_argument('after')
    parser.add_argument('--min-impressions',type=int,default=10)
    parser.add_argument('--output',default='gsc-compare.csv')
    args=parser.parse_args(argv)
    try:
        if args.min_impressions<0:raise ValueError('展示阈值不能为负')
        rows=compare(args.before,args.after,args.min_impressions)
        columns=['type','label','status','old_clicks','new_clicks','delta_clicks','old_impressions','new_impressions','delta_impressions','old_ctr','new_ctr','old_position','new_position']
        with open(args.output,'w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader()
            for row in rows:
                row=row.copy()
                # Prevent spreadsheet formula execution on CSV import for uncontrolled query names.
                if row['label'].lstrip().startswith(('=','+','-','@')):row['label']="'"+row['label']
                writer.writerow(row)
    except (OSError,ValueError) as e:
        print('无法比较：',e,file=sys.stderr);return 2
    print(f'共 {len(rows)} 行 | 输出 {args.output}')
    print('提醒：两期必须相同网站/搜索类型/国家/设备/时长。GSC 部分查询因隐私未展示，合计不一定等于总量。变化不是优化带来的因果证明。')
    return 0
if __name__=='__main__':sys.exit(main())
