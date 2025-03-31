query_type = sys.argv[1] if len(sys.argv) > 1 else "list_tables"
server = sys.argv[2] if len(sys.argv) > 2 else "HSTNCMSRDIQA02.healthspring.inside"
database = sys.argv[3] if len(sys.argv) > 3 else "Staging"
