Act as a Senior Python Architect, Full Stack Developer, UI/UX Designer, and Streamlit Expert.

Develop a production-quality AI-powered application named "Wiz Vulnerability AI Agent" using Python and Streamlit.

The application will communicate with the Wiz GraphQL API using OAuth2 authentication and retrieve vulnerability findings based on user selections.

This is Phase-1 (MVP). Build the application for LOCAL DEVELOPMENT ONLY.

The application should look and behave like a modern enterprise web application rather than a default Streamlit application.

Use clean architecture, modular code, reusable components, proper logging, exception handling, SOLID principles, and enterprise coding standards.

==================================================
DEVELOPMENT ENVIRONMENT
==================================================

This version is ONLY for local development.

Do NOT generate:

• Dockerfile
• docker-compose.yml
• Linux deployment scripts
• Nginx configuration
• Kubernetes manifests
• CI/CD pipelines

The application should run locally using:

streamlit run app.py

==================================================
TECH STACK
==================================================

Frontend

• Streamlit
• Custom CSS
• HTML Components
• Streamlit Session State
• Plotly
• streamlit-aggrid

Backend

• Python 3.11
• Requests
• GraphQL
• Pandas
• dotenv
• Pydantic
• Logging

Authentication

OAuth2 Client Credentials

==================================================
PROJECT STRUCTURE
==================================================

wiz-agent/

app.py

config.py

requirements.txt

README.md

.env.example

assets/

    styles.css

    logo.png

backend/

    auth.py

    wiz_client.py

    graphql_queries.py

    vulnerability_service.py

    account_service.py

    charts.py

    export.py

utils/

    helpers.py

    logger.py

==================================================
GENERAL REQUIREMENTS
==================================================

Create a modern enterprise dashboard.

Hide Streamlit branding.

Hide Streamlit menu.

Hide footer.

Use custom CSS.

Professional spacing.

Rounded cards.

Glassmorphism.

Smooth animations.

Hover effects.

Responsive layout.

Professional typography.

Dark left sidebar.

White content area.

Enterprise blue theme.

The UI should resemble

• Wiz Console

• Microsoft Azure Portal

• AWS Console

• Datadog

• GitHub Enterprise

==================================================
APPLICATION HEADER
==================================================

Display

🛡️ Wiz Vulnerability AI Agent

Subtitle

Enterprise Vulnerability Intelligence Dashboard

Display

Current Date

Current Time

Tenant Name

Logged-in User

==================================================
WELCOME MESSAGE
==================================================

Display chatbot-style welcome.

Hello 👋

Welcome to Wiz Vulnerability AI Agent.

I can retrieve vulnerability findings directly from Wiz Cloud Security Platform.

Please select the vulnerability severity to begin.

==================================================
STEP 1
==================================================

DO NOT use Streamlit radio buttons.

Create four professional clickable cards.

Each card must contain

Large icon

Title

Short description

Rounded corners

Hover animation

Shadow

Selected border

Selected background

Check mark

Cards

🟥 Critical

Highest priority vulnerabilities

🟧 High

High-risk vulnerabilities

🟨 Medium

Medium-risk vulnerabilities

🟩 Low

Low-risk vulnerabilities

Only one card can be selected.

==================================================
STEP 2
==================================================

Display another row of professional cards.

🌍 All Accounts

Retrieve vulnerabilities from every cloud account.

☁ Specific Account

Retrieve vulnerabilities from one cloud account.

Only one selection allowed.

==================================================
STEP 3
==================================================

If the user selects

Specific Account

Call the Wiz API to retrieve available Cloud Accounts.

Populate a searchable dropdown.

Do NOT use manual text input.

==================================================
STEP 4
==================================================

Display output options as professional cards.

Allow multiple selections.

Cards

📋 Interactive Table

📊 Executive Dashboard

🥧 Pie Chart

📈 Bar Chart

📄 CSV Export

Selected cards should display

Blue border

Check icon

Light blue background

==================================================
FETCH BUTTON
==================================================

Create one large enterprise button.

🔍 Fetch Vulnerabilities

Properties

Blue gradient

Rounded corners

White text

Full width

Hover animation

Loading spinner

Disabled until all mandatory selections are completed.

==================================================
APPLICATION FLOW
==================================================

User opens application

↓

Select Severity

↓

Select Scope

↓

(Optional) Select Account

↓

Select Output

↓

Click Fetch Vulnerabilities

↓

Authenticate using OAuth2

↓

Generate Access Token

↓

Generate GraphQL Query

↓

Execute GraphQL API

↓

Receive JSON

↓

Convert to Pandas DataFrame

↓

Display Results

==================================================
GRAPHQL
==================================================

Generate GraphQL dynamically.

Severity must be selected dynamically.

Support

Critical

High

Medium

Low

If

All Accounts

Do not include account filter.

If

Specific Account

Include selected account filter.

GraphQL query builder should be reusable.

==================================================
DISPLAY TABLE
==================================================

Display results using AgGrid.

Columns

Asset Name

Cloud Provider

Cloud Account

Subscription

Project

Region

Severity

Status

CVE

Vendor Severity

CVSS Score

Exploit Available

Fix Available

Operating System

Resource Type

Resource Name

First Seen

Last Seen

Owner

Business Unit

Recommendation

Enable

Pagination

Sorting

Filtering

Column Resize

Search

Export

==================================================
EXECUTIVE DASHBOARD
==================================================

Display KPI Cards

Total Vulnerabilities

Critical

High

Medium

Low

Open

Resolved

Generate charts

Severity Distribution

Top Vulnerable Accounts

Top Vulnerable Regions

Cloud Provider Distribution

Top Assets

Top CVEs

Use Plotly.

==================================================
EXPORT
==================================================

Support

CSV Export

==================================================
CHAT HISTORY
==================================================

Maintain conversation using Streamlit Session State.

Example

User

Critical

Agent

Retrieved 184 Critical vulnerabilities.

Retain previous searches.

==================================================
TOP STATUS BAR
==================================================

Display

Execution Time

API Response Time

Records Returned

API Connection Status

Refresh Button

==================================================
LOADING EXPERIENCE
==================================================

Display loading spinner with messages.

Authenticating...

Generating GraphQL Query...

Connecting to Wiz...

Retrieving Vulnerabilities...

Processing Results...

Generating Dashboard...

==================================================
ERROR HANDLING
==================================================

Handle gracefully

Authentication Failed

Connection Timeout

GraphQL Error

Invalid Account

No Vulnerabilities Found

Display professional notification cards.

==================================================
LOGGING
==================================================

Log

Authentication

API Calls

Execution Time

Errors

User Selections

==================================================
CONFIGURATION
==================================================

Read all values from .env

WIZ_CLIENT_ID

WIZ_CLIENT_SECRET

WIZ_AUTH_URL

WIZ_GRAPHQL_URL

Never hardcode credentials.

==================================================
CODE QUALITY
==================================================

Use

Type Hints

Docstrings

Pydantic Models

Reusable Functions

SOLID Principles

Layered Architecture

No duplicate code.

Separate UI from business logic.

==================================================
README
==================================================

Generate README.md including

Project Overview

Folder Structure

Prerequisites

Python Version

Virtual Environment Setup

Installing Requirements

Creating .env

Running the Application

Project Architecture

Troubleshooting

==================================================
FINAL EXPECTATION
==================================================

Generate the COMPLETE project with all Python files, CSS files, backend modules, authentication module, GraphQL query builder, chart utilities, export utilities, configuration files, README, and requirements.txt.

Do NOT leave TODO comments.

Do NOT generate placeholder code.

Generate production-ready, clean, modular, and fully functional code.

The application should look like an enterprise security dashboard instead of a default Streamlit application.

The UI should feel similar to the Wiz Console, Microsoft Azure Portal, or Datadog.
