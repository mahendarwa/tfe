import os
from wizcli import WizClient

# Set environment variables first
os.environ['WIZ_CLIENT_ID'] = 'your_client_id_here'
os.environ['WIZ_CLIENT_SECRET'] = 'your_client_secret_here'

# Create client and connect
client = WizClient()

# Example: Get issues
issues = client.get_issues()
print(f"Found {len(issues)} issues")
