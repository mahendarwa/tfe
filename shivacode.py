pytest --collect-only -q | grep "::" | cut -d"::" -f1 | sort | uniq | wc -l
