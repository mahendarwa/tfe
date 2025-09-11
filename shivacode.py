Wiz Malware Incident – Timeline (EST)

Sep 9, 2025 – 10:27 AM EST
CSS initiated email notifying SOC/CSIRT about Wiz alert: VM/Serverless infected with high/critical severity malware.

Sep 9, 2025 – 12:50 PM EST
Response team confirmed remediation actions started; both hosts flagged for cleanup.

Sep 9, 2025 – 10:17 PM EST
Udai Varshney asked if the impacted VDI could be replaced with a new one.

Sep 9, 2025 – 10:18 PM EST
Scott Mundy responded that replacement process had already begun.

Sep 9, 2025 – 10:19 PM EST
Kitch Kelly requested Greg’s team to initiate rebuild for VM PAC4VDIPPS05609.

Sep 9, 2025 – 11:53 PM EST
Satish Chandramohan reported detection of additional malicious files from a new Wiz scan. Suggested pulling the VDI offline and coordinating next steps.

Sep 10, 2025 – 12:28 AM EST
Kitch Kelly confirmed Wiz was no longer detecting malicious versions; Adobe “*.Generic” files were not security concerns.

Sep 10, 2025 – 2:35 AM EST
Satish reported both VDIs still showing Adobe ARM related files; opened a support case with Wiz.

Sep 10, 2025 – 6:24 PM EST
Satish: CSIRT cleanup done but subsequent scan still showing files → initiated manual scan next morning.

Sep 10, 2025 – 10:08 PM EST
Mahendar confirmed manual scan run, but malicious files still visible. Recommended additional checks and VM restart to clear cache.

Sep 10, 2025 – 10:16 PM EST
Udai followed up again: “Is it possible to replace this VDI with a new one?”

Sep 10, 2025 – 10:18 PM EST
Scott Mundy: “We have already begun that process.”

Sep 11, 2025 – 8:20 AM EST
Greg Pirtz confirmed new VM build request; old VM to be set for deletion.

Sep 11, 2025 – 5:41 PM EST
Mahendar reported another manual scan → successful, but files still present; VM was active, not powered off.

Sep 11, 2025 – 6:06 PM EST
Jonathan Senko confirmed VM PAC4VDIPPS05609 placed in maintenance mode, powered off, pending deletion; new VM PAC4VDIPPS06574 assigned.
