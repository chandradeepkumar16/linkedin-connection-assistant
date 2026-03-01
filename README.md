# LinkedIn Connection Request Automation

Automates sending connection requests to 2nd and 3rd degree connections
from a specific company.

## ⚠️ CRITICAL WARNINGS

**This tool is for educational purposes only.** - Automated activity
violates LinkedIn's Terms of Service - LinkedIn has **weekly limits**
(\~100 connection requests/week for free accounts) - Exceeding limits
will result in **account restrictions** or **permanent ban** - Use at
your own risk - Start with VERY LOW numbers (5-10 requests max per day)

## Features

✅ Automatically logs into LinkedIn\
✅ Searches for people from a specific company\
✅ Filters to 2nd & 3rd connections (not already connected)\
✅ Clicks "Connect" button for each person\
✅ Handles "Send without a note" vs direct send\
✅ Skips people already connected or pending\
✅ Automatically moves to next page when current page is done\
✅ Stops after reaching target number of requests

## How It Works

    1. Login to LinkedIn
    2. Search for people from company (e.g., "Google")
    3. On each page:
       ├─ Find all people (2nd & 3rd connections)
       ├─ For each person:
       │  ├─ Check if already connected → Skip
       │  ├─ Click "Connect" button
       │  ├─ If modal appears → Click "Send without a note"
       │  └─ Wait 3-6 seconds
       └─ Move to next page
    4. Stop when target number reached

## Installation

### Step 1: Install Dependencies

``` bash
pip install -r requirements.txt
```

### Step 2: Configure Settings

Open `linkedin_connect_automation.py` and modify:

``` python
LINKEDIN_EMAIL = "your_email@example.com"
LINKEDIN_PASSWORD = "your_password"
COMPANY_NAME = "Google"
MAX_REQUESTS = 10
```

## Usage

### Run the script:

``` bash
python linkedin_connect_automation.py
```

### What happens:

1.  Browser opens and logs into LinkedIn
2.  Searches for people from specified company
3.  Goes through search results page by page
4.  Sends connection requests (without notes)
5.  Skips already connected or pending requests
6.  Moves to next page automatically
7.  Stops after reaching your target number

## Configuration Options

### COMPANY_NAME

Examples: - "Google" - "Microsoft" - "Amazon" - "Tesla"

### MAX_REQUESTS

**VERY IMPORTANT**: Start small! - First time: 5-10 max - Daily limit:
20-30 max recommended - Weekly limit: \~100/week for free accounts -
Monthly: 200-400 generally safe

## Safety Features

-   Skips 1st connections
-   Skips pending requests
-   Human-like delays (3-6 seconds)
-   Auto-pagination
-   Request counter limit

## LinkedIn Limits (Important!)

  Account Type      Weekly Limit     Daily Recommended
  ----------------- ---------------- -------------------
  Free Account      \~100 requests   15-20 max
  Premium Account   \~200 requests   30-40 max
  Sales Navigator   Higher           50+ possible

## Best Practices

1.  Start Small
2.  Don't Run Daily
3.  Monitor Your Account
4.  Be Strategic
5.  Mix with Manual Activity

## Troubleshooting

### Connect button not found

-   Already connected
-   Requests disabled
-   UI changed

### Account restricted

-   Sent too many requests
-   Wait 1-2 weeks
-   Reduce MAX_REQUESTS

### No people found

-   Check company spelling
-   Try common company
-   Search may be blocked

## Warning Signs to Stop

-   LinkedIn warnings
-   Frequent CAPTCHA
-   Unusual activity notifications
-   Temporary restrictions
-   Low acceptance rate (\<20%)

## Code Structure

    linkedin_connect_automation.py
    ├── LinkedInConnectBot class
    │   ├── setup_driver()
    │   ├── login()
    │   ├── search_company_people()
    │   ├── get_people_on_current_page()
    │   ├── send_connection_request()
    │   ├── go_to_next_page()
    │   └── run_automation()
    └── main()

## Ethical Use

-   Connect with relevant professionals
-   Avoid spam behavior
-   Respect platform limits
-   Build genuine relationships

## Legal Disclaimer

-   Violates LinkedIn Terms of Service
-   May result in account termination
-   Provided "as-is"
-   Use at your own risk

------------------------------------------------------------------------

**Remember**: Real networking beats automation. Use responsibly.
