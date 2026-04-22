import os
from dotenv import load_dotenv
load_dotenv()
uid = os.environ.get("AGENT_SPEC_USER_ID", "NOT_SET")
dsid = os.environ.get("AGENT_SPEC_DESIGN_SYSTEM_ID", "NOT_SET")
db = os.environ.get("SUPABASE_DB_URL", "NOT_SET")
print(f"USER_ID: '{uid}'")
print(f"DESIGN_SYSTEM: '{dsid}'") 
print(f"DB_URL: '{db[:50]}...'")