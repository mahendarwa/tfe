Missing User Activity Logs in Wiz Cloud Events – Azure

Hi Wiz Support Team,

We are experiencing an issue with Azure activity logs not appearing in Wiz Cloud Events.

Details:

Activity logs from Azure are being sent to Wiz through the configured connector.

However, in Wiz we only see events for service principals.

User activities (e.g., console logins, subscription selections, cluster access) are missing or very minimal.

For example, users like Vishal, Nilesh, and myself log into the Azure console frequently, but their activity is not visible in Wiz Cloud Events.

Only a few scattered user events (like Yogesh) show up, and even those are incomplete.

Impact:

Makes it difficult to track user-level activity for compliance and investigation.

Verified that the events are available in Azure activity logs and are also being sent to Splunk, but not showing correctly in Wiz.

Request:

Please investigate why Azure user activity logs are not being ingested or displayed in Wiz Cloud Events, while service principal activity is visible.
