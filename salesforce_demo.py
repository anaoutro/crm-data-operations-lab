import json
from pathlib import Path
p=Path(__file__).parent; rows=json.loads((p/'salesforce_opportunities.json').read_text()); out=[]
for r in rows:
    issues=[]
    if r['amount']<=0: issues.append('invalid_amount')
    if r['stage'] not in ('Closed Won','Closed Lost'):
        if r['days_idle']>14: issues.append('stale_opportunity')
        if not r['next_step'].strip(): issues.append('missing_next_step')
    out.append({'id':r['id'],'issues':issues,'review_priority':'high' if issues else 'normal'})
(p/'salesforce_result.json').write_text(json.dumps(out,indent=2))
print({'reviewed':len(out),'flagged':sum(bool(x['issues']) for x in out)})
