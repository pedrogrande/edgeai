import os
import psycopg
import psycopg.rows
from dotenv import load_dotenv
load_dotenv()

db_url = os.environ.get("SUPABASE_DB_URL", "")
output_lines = []
with psycopg.connect(db_url, row_factory=psycopg.rows.dict_row) as conn:
    rows = conn.execute(
        "SELECT id, name, created_by FROM public.design_system LIMIT 5"
    ).fetchall()
    for r in rows:
        output_lines.append(f"DS: {r['id']} name={r['name']} created_by={r['created_by']}")

    specs = conn.execute(
        "SELECT id, agent_name, created_by FROM public.agent_spec LIMIT 5"
    ).fetchall()
    for s in specs:
        output_lines.append(f"Spec: {s['id']} name={s['agent_name']} created_by={s['created_by']}")

result = "\n".join(output_lines)