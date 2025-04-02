pytest --collect-only -q | grep "::" | awk -F"::" '{print $1}' | sort | uniq | wc -l
