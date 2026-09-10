import json
from datetime import datetime
def run():
 while True:
  with open("config.json") as f: c=json.load(f)
  print(f"\n--- {c["project_name"]} ---")
  for i,a in enumerate(c["agents"]):
   m=a["performance_metrics"]
   print(f"{i+1}. {a["id"]}: {m["win_rate"]*100}% ({m["matches_analyzed"]})")
  print("3. Exit")
  ch=input("Choice: ").strip()
  if ch=="3": break
  try:
   idx=int(ch)-1
   ag=c["agents"][idx]
   w=input("Win? (y/n): ").strip().lower()=="y"
   met=ag["performance_metrics"]
   tot=met["matches_analyzed"]+1
   wins=met["win_rate"]*met["matches_analyzed"]+(1 if w else 0)
   met["matches_analyzed"]=tot
   met["win_rate"]=round(wins/tot,4)
   c.setdefault("audit_logs",[]).append({"time":datetime.now().isoformat(),"agent":ag["id"]})
   with open("config.json","w") as f: json.dump(c,f,indent=2)
   print("Updated!")
  except: print("Error")
if __name__=="__main__": run()
