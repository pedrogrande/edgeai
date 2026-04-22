import os
from dotenv import load_dotenv
load_dotenv()
uid = os.environ.get("AGENT_SPEC_USER_ID", "")
dsid = os.environ.get("AGENT_SPEC_DESIGN_SYSTEM_ID", "")
dburl = os.environ.get("SUPABASE_DB_URL", "")
results = []
results.append(f"USER_ID: {'SET (' + uid[:8] + '...)' if uid else 'NOT SET'}")
results.append(f"DS_ID: {'SET (' + dsid[:8] + '...)' if dsid else 'NOT SET'}")
results.append(f"DB_URL: {'SET (' + dburl[:50] + '...)' if dburl else 'NOT SET'}")
output = "\n".join(results)