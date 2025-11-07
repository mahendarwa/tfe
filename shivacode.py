Namespace	Path	Expected Behavior
o11y-collectors	/var/log/pods (read)	No alert
o11y-collectors	/var/lib/otelcol (read/write)	No alert
o11y-collectors	/etc or other dirs	Alert
default / others	Any hostPath	Blocked or Alert


Create test pods in o11y-collectors (for allowed paths /var/log/pods, /var/lib/otelcol) and in another namespace (for blocked paths like /etc) to verify alert behavior.
