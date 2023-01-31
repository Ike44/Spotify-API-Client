import os
from dotenv import load_dotenv

load_dotenv()
aabc = os.environ.get('CLIENT_ID')
print(aabc)