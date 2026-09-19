# gera clubes.json (força por banda em escala OVR) a partir do dataset do Fenômeno
import json, re
SRC = r"C:\Users\PC\Documents\FenomenoDOBR"
d = json.load(open(SRC + r"\dados_fenomeno_completo.json", encoding="utf-8"))
est = {str(e["tid"]): e for e in json.load(open(SRC + r"\estadios_fenomeno.json", encoding="utf-8"))}
TEC = {
  "GK": ["Reflexes","One on ones","Handling","Communication","Positioning"],
  "DC": ["Tackling","Marking","Positioning","Communication","Heading"],
  "Lateral": ["Tackling","Marking","Positioning","Communication","Crossing"],
  "MC": ["Creativity","Passing","First touch","Positioning","Long shots"],
  "Meia-Lateral": ["Creativity","Passing","First touch","Positioning","Crossing"],
  "FC": ["First touch","Positioning","Shooting","Dribbling","Heading"],
}
BANDA = {"GK":"GK","DC":"DF","Lateral":"DF","MC":"MF","Meia-Lateral":"MF","FC":"FW"}
def tier(div):
    if "Campeonato Brasileiro - " in div and "Divis" not in div.split(" - ")[-1]: return 3
    s = div.split(" - ")[-1]
    if s.startswith("Campeonato") : return 3
    if " B" in s and "C" not in s.split()[-1][0:1]: pass
    m = re.search(r"\b([BC])(\d)\b", s)
    if m: return 2 if m.group(1)=="B" else 1
    return 3
clubes = {}
for t in d["times"]:
    div = t["divisao"].replace("\ufffd","o")
    s = div.split(" - ")[-1]
    m = re.search(r"\b([BC])(\d)\b", s)
    tr = (2 if m.group(1)=="B" else 1) if m else 3
    e = est.get(str(t["id"]), {})
    grupo = (m.group(1)+m.group(2)) if m else "CB"
    clubes[t["id"]] = {"id": t["id"], "nome": t["nome"], "tier": tr, "grupo": grupo, "liga": ("Brasileirão" if tr==3 else ("Série B" if tr==2 else "Série C")) , "estadio": e.get("estadio",""), "cap": e.get("capacidade",0), "band": {"GK":[], "DF":[], "MF":[], "FW":[]}, "vals": {}}
for j in d["jogadores"]:
    c = clubes.get(j["idTime"])
    if not c: continue
    best = 0; bb = None
    for pos, nv in j["posicoes"].items():
        if pos in TEC and nv in ("Natural","Competent"):
            ops = sum(j["atributos"].get(a,0) for a in TEC[pos])
            if ops > best: best, bb = ops, BANDA[pos]
    if bb: c["band"][bb].append(round(best*0.4))
out = []
for c in clubes.values():
    row = {"id": c["id"], "nome": c["nome"], "tier": c["tier"], "grupo": c["grupo"], "liga": c["liga"], "estadio": c["estadio"], "cap": c["cap"]}
    for b, v in c["band"].items():
        v = sorted(v, reverse=True)[:4]
        row[b] = round(sum(v)/len(v)) if v else 60
    out.append(row)
json.dump(out, open("clubes.json","w",encoding="utf-8"), ensure_ascii=False)
import collections
print(len(out), collections.Counter(c["tier"] for c in out))
for t in (1,2,3):
    xs=[ (c["GK"]+c["DF"]+c["MF"]+c["FW"])/4 for c in out if c["tier"]==t]
    print(t, round(min(xs)), round(sum(xs)/len(xs)), round(max(xs)))
