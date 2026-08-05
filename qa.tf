The VM Vulnerability Search page is already working.

Do NOT change the existing search functionality.

After the user searches a VM and the vulnerability results are displayed, add a new section below the existing results called

"AI Recommendation"

This section should help the end user understand the vulnerability and take action.

Use the same Material UI theme as the existing application.

Create a clean card with the following layout.

------------------------------------------------

AI Recommendation

Policy Name

Display the Wiz policy name that flagged this VM.

Severity

Critical / High / Medium

Why is this vulnerability flagged?

Display a short 2-3 line explanation describing why this policy is violated.

Example:

"This VM is running an unsupported OpenSSL version that contains known security vulnerabilities."

Business Impact

Display a short explanation of the security impact.

Example

"This vulnerability could allow attackers to exploit the server if left unpatched."

------------------------------------------------

Actions

Create three buttons.

1.

View Remediation Steps

When clicked, expand a collapsible section below the button.

Display numbered remediation steps.

Example

1. Login to the VM.

2. Update the vulnerable package.

3. Restart the required service.

4. Run vulnerability scan again.

5. Verify the issue is resolved.

Initially use placeholder text.

Later this will come from FastAPI.

------------------------------------------------

2.

Raise Exception

Display a button.

On click open the configured Exception Request URL in a new browser tab.

The URL should be configurable through a constant or environment variable.

Do not hardcode the URL inside the component.

------------------------------------------------

3.

Open in Wiz

Display a button that opens the Wiz resource page in a new tab.

The Wiz URL should be passed from the backend.

------------------------------------------------

UI Requirements

Use Material UI Card.

Use Material UI Accordion for remediation steps.

Use Material UI Buttons.

Keep spacing consistent with the rest of the application.

Do not add charts.

Do not add tables.

Do not redesign the existing page.

Simply append this new AI Recommendation card below the search results.

Structure the component so the remediation text, policy name, business impact and URLs can later be populated from FastAPI APIs.
