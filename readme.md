BSD Monitor - Snowflake Feeds Monitoring
Overview
The BSD Monitor is a Python-based monitoring system designed to track and validate Snowflake table loads. It checks data feeds against predefined thresholds, logs potential issues, and alerts users when anomalies occur. The system is configured dynamically, allowing easy modifications for different feeds.

Key Functionalities
1. Connecting to Snowflake
The monitor retrieves Snowflake credentials using HiPam and establishes a connection to execute queries.
2. Query Execution
Runs predefined SQL queries in Snowflake to extract feed data and validate it against expected values.
3. Threshold Validation
Compares query results with predefined thresholds to ensure data availability, freshness, and integrity.
4. Generating Alerts
Creates ITO (Infrastructure Technology Operations) alerts for feeds that fail validation and logs them for further analysis.
5. Email Reporting
Generates detailed email reports summarizing feed health and sends them to configured recipients.
6. Scheduled Monitoring
Supports interval-based and daily scheduled checks to continuously validate feed data.
7. Dynamic Configuration
Uses external configuration files to define monitored feeds, thresholds, and scheduling, enabling easy modification.
8. Lookback Handling
Supports lookback periods to check feeds that load previous day’s data, ensuring accurate validation.
9. Frequency-Based Checks
Allows users to specify data check frequency using time intervals, ensuring timely detection of anomalies.
10. Logging and Debugging
Maintains detailed logs for both application and ITO alerts to track failures and execution history.

How to Use the BSD Monitor
	1. Configure Email Groups and Thresholds
Update configurations in bsd/config/sql_config_<env>.py for email recipients and threshold values.
	2. Run One-Time Report
Execute python bsd_monitor.py to check today’s data.
	3. Run Periodic Checks
Use python bsd_monitor.py -loop <XX> to check every XX minutes.
	4. Schedule Daily Reports
Use python bsd_monitor.py -daily "<HHMM>" to generate reports at a specific military time.
	5. Run Multiple Reports Per Day
Use python bsd_monitor.py -daily <HHMM> <HHMM> to send reports at multiple times a day.
	6. Combine Interval and Daily Checks
Example: python bsd_monitor.py -loop 30 -daily 0915 runs every 30 minutes and sends a report at 9:15 AM daily.

Enhancements and Requirements
	• Implement a configuration format similar to Aries-Common for defining Snowflake table names, lookback periods, and frequency of checks.
	• Ensure that new feeds can be added dynamically through configuration.
	• Generate SQL queries dynamically based on configuration settings.
	• Monitor feeds for Start-of-Day (SOD), Intraday, and End-of-Day (EOD) slices.
	• Utilize the tables ARIP.FICC.BUSINESS_DATE and ARIP.NSCC.BUSINESS_DATE for business date validation.

Conclusion
The BSD Monitor is a scalable and configurable solution for tracking Snowflake data feeds. It ensures data integrity by performing scheduled validations, generating alerts, and automating reporting, helping to proactively identify and resolve feed-related issues.
![Uploading image.png…]()
