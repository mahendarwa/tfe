- "*"                             # Wildcard host (Non-Compliant)
- "/"                             # Root host without namespace
- "other-namespace/service"       # Different namespace
- "example.com"                   # diff domain 
======
metadata:
  name: compliant-gateway
  namespace: test-namespace
spec:
  servers:
  - hosts:
    - "test-namespace/app-service"   # Starts with namespace
    - "test-namespace/web-service"   # Starts with namespace
