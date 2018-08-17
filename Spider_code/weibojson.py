import json as js
import codecs

file = "./json/data.json"
output = "data3out.json"
with open(file, 'r', encoding="utf8") as f:
    data = js.load(f)
    statuses = data['statuses']
    f.close()

print("Number of weibo: ", len(statuses))

timeline = {}
for x in statuses:
    if x['created_at'] in timeline:
        timeline[x['created_at']] += 1
    else:
        timeline.setdefault(x['created_at'], 1)

with open(output, 'a') as out:
    js.dump(timeline, out, ensure_ascii=False)
    out.write('\n')
