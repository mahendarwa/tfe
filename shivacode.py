detect-unauthorized-hostpath-access-except-o11y

===

/etc/**, /var/**, /root/**, /usr/**, /opt/**, /home/**, /tmp/**

===
^(?!/var/log/pods)(?!/var/lib/otelcol).*
