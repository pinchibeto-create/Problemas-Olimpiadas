#!/usr/bin/env python3
"""Build a static website and a SQLite database from the versioned SQL source."""
import json
import sqlite3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with sqlite3.connect(":memory:") as db:
    db.executescript((ROOT / "database/banco_sqlite.sql").read_text(encoding="utf-8"))
    db.row_factory = sqlite3.Row
    assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert not db.execute("PRAGMA foreign_key_check").fetchall()
    def table(name, order):
        return [dict(r) for r in db.execute(f"SELECT * FROM {name} ORDER BY {order}")]
    c = table("contenidos", "id")
    a = table("pdas", "id")
    p = table("problemas", "id")
    l = table("problema_pda", "pda_id, problema_id")
    ps = {x["problema_id"] for x in l}
    aps = {x["pda_id"] for x in l}
    dup = int(db.execute("SELECT valor FROM metadatos WHERE clave='duplicados_excluidos'").fetchone()[0])
    counts = dict(contenidos=len(c), pdas=len(a), clasificados=sum(x["contenido_id"] is not None for x in p), sin_clasificar=sum(x["contenido_id"] is None for x in p), total=len(p), duplicados_excluidos=dup, vinculos=len(l), prioritarios=sum(x["nivel"]=="Prioritaria" for x in l), tematicos=sum(x["nivel"]=="Temática" for x in l), problemas_con_sugerencia=len(ps), problemas_solo_contenido=sum(x["contenido_id"] is not None and x["id"] not in ps for x in p), pdas_sin_sugerencia=len(a)-len(aps), figuras_marcadas=sum(x["figura"]=="Marcada en original" for x in p), alertas_visuales=sum(x["figura"]=="Revisar referencia visual" for x in p))
    assert counts["clasificados"] + counts["sin_clasificar"] == counts["total"]
    data = dict(contenidos=c,pdas=a,problemas=p,vinculos=l,resumen=counts)
    target = ROOT / "database/banco.sqlite"
    tmp = target.with_suffix(".sqlite.tmp")
    with sqlite3.connect(tmp) as dest:
        db.backup(dest)
    tmp.replace(target)
serialized = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
template = (ROOT / "src/index.template.html").read_text(encoding="utf-8")
assert template.count("__BANCO_JSON__") == 1
public = ROOT / "public"
public.mkdir(exist_ok=True)
(public / "index.html").write_text(template.replace("__BANCO_JSON__", serialized), encoding="utf-8")
print(json.dumps(counts, ensure_ascii=False))
