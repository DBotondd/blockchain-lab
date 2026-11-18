from pathlib import Path
import csv,statistics as s,json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

root=Path(__file__).resolve().parent
src=root/'pow_200.csv'
out=root/'kepek'
out.mkdir(exist_ok=True)
rows=[]
with open(src,encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f)
  assert reader.fieldnames==['nehezseg','ismetles','probalkozasok','futasido_ms']
  for item in reader:
    rows.append({'nehezseg':int(item['nehezseg']),'ismetles':int(item['ismetles']),'probalkozasok':int(item['probalkozasok']),'futasido_ms':float(item['futasido_ms'])})
assert len(rows)==200
sums={}
for d in range(1,5):
 drows=[x for x in rows if x['nehezseg']==d]
 assert len(drows)==50 and sorted(x['ismetles'] for x in drows)==list(range(1,51))
 vals=[x['probalkozasok'] for x in drows]; ms=[x['futasido_ms'] for x in drows]
 assert all(v>0 for v in vals) and all(v>=0 for v in ms)
 quart=s.quantiles(vals,n=4,method='inclusive')
 sums[d]={'n':len(vals),'mean':s.mean(vals),'median':s.median(vals),'std':s.stdev(vals),'min':min(vals),'max':max(vals), 'q1':quart[0], 'q3':quart[2], 'time_mean':s.mean(ms),'time_median':s.median(ms),'time_std':s.stdev(ms),'time_min':min(ms),'time_max':max(ms),'expected_mean':16**d, 'ratio':s.mean(vals)/16**d, 'total_attempts':sum(vals)}
json.dump({'source':src.name,'rows':len(rows),'stats':sums},(root/'pow_200_statisztika.json').open('w',encoding='utf-8'),ensure_ascii=False,indent=2)

plt.rcParams.update({'font.size':11,'axes.titlesize':14,'axes.labelsize':11,'figure.dpi':140,'savefig.dpi':180})
D=list(sums)
pos=list(range(1,5))
fig,ax=plt.subplots(figsize=(8.2,4.9))
ax.plot(D,[sums[d]['mean'] for d in D],marker='o',lw=2,label='Mért átlag (50 futás / szint)')
ax.plot(D,[16**d for d in D],marker='s',ls='--',lw=1.7,label='Elméleti várható érték ($16^d$)')
ax.set_xticks(D); ax.set_yscale('log'); ax.set_ylim(8,160000)
ax.set_xlabel('Nehézségi szint (kezdő hexadecimális nullák)')
ax.set_ylabel('Átlagos próbálkozásszám (logaritmikus skála)')
ax.set_title('PoW: mért és elméleti átlagos próbálkozásszám')
ax.legend();ax.grid(True,alpha=.24,which='both');fig.tight_layout();fig.savefig(out/'pow200_atlag_elmelet.png');plt.close(fig)

fig,ax=plt.subplots(figsize=(8.2,4.9))
seq=[[x['probalkozasok'] for x in rows if x['nehezseg']==d] for d in D]
ax.boxplot(seq,tick_labels=[str(x) for x in D],showmeans=True, meanprops={'marker':'D','markersize':5})
ax.set_yscale('log');ax.set_xlabel('Nehézségi szint');ax.set_ylabel('Próbálkozások száma (logaritmikus skála)')
ax.set_title('PoW: próbálkozásszámok eloszlása (50 mérés / szint)')
ax.grid(True,which='both',alpha=.23,axis='y');fig.tight_layout();fig.savefig(out/'pow200_eloszlas_boxplot.png');plt.close(fig)

fig,ax=plt.subplots(figsize=(8.2,4.9))
for d in D:
 ss=[x for x in rows if x['nehezseg']==d]
 ax.scatter([x['probalkozasok'] for x in ss],[x['futasido_ms'] for x in ss],label=f'{d}. szint',alpha=.73,s=23)
ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel('Próbálkozások száma (log)');ax.set_ylabel('Mért bányászati idő (ms, log)')
ax.set_title('PoW: keresési munka és futásidő kapcsolata')
ax.legend(title='Nehézség');ax.grid(True,which='both',alpha=.2)
fig.tight_layout();fig.savefig(out/'pow200_probalkozas_ido.png');plt.close(fig)

print(json.dumps({'total':len(rows),'stats':sums},ensure_ascii=False,indent=2))
