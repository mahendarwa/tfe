Thanks, Raul. So just to confirm — any files inside subfolders under /var/<folder> or /etc/<folder> will not be monitored by Runtime FIM because recursive monitoring is not supported. Only top-level files are monitored. Please confirm.


Feature	Supported?	Notes
Monitor exact file	✔ Yes	e.g., /etc/passwd
Monitor all files directly in a folder	✔ Yes	e.g., everything immediately inside /etc/
Monitor nested subfolders	❌ No	/etc/ssl/certs/* won't work
