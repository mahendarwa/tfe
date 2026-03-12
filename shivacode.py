MITRE ATT&CK Cloud Matrix
This framework is designed specifically for cloud environments and maps attack techniques related to platforms such as AWS, Azure, GCP, SaaS applications, and Identity Providers. It focuses on cloud control-plane activities such as IAM misuse, cloud service discovery, and access to cloud storage or services, making it directly relevant for cloud security monitoring in Wiz.
Reference: https://attack.mitre.org/matrices/enterprise/cloud/

MITRE ATT&CK Enterprise Matrix
This framework covers a broader enterprise environment, including endpoints, operating systems (Windows, Linux, macOS), networks, containers, and cloud. It is typically used for enterprise security monitoring where both on-premise infrastructure and cloud workloads are involved.
Reference: https://attack.mitre.org/matrices/enterprise/

Conclusion
The Cloud Matrix is derived from the Enterprise Matrix, but it includes only the techniques relevant to cloud platforms. Techniques related to endpoints or traditional on-prem infrastructure are excluded, which is why some categories have fewer techniques compared to the Enterprise Matrix. Since our focus is primarily cloud infrastructure, the MITRE ATT&CK Cloud Matrix provides the most relevant coverage for our cloud security use case in Wiz.
