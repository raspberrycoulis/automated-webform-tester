# Webform Submission Tester

This Python script automates the testing of a webform that includes a Google reCAPTCHA v3 verification step. It simulates realistic user behaviour, detects submission success or failure, and sends a Microsoft Teams webhook alert if the submission fails due to reCAPTCHA issues.

---

## Features

- Simulates human form filling with random mouse movement and delays
- Handles Google reCAPTCHA v3 (token generation via `grecaptcha.execute`)
- Detects submission status via URL pattern
- Sends a Microsoft Teams webhook alert on failure

---

## Requirements

- Python 3.8 or later
- [Playwright for Python](https://playwright.dev/python/docs/intro)
- Google Chrome or Chromium browser

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/raspberrycoulis/automated-webform-tester.git
automated-webform-tester
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
playwright install
```

3. **Set up environment variables**

```env
WEBFORM_URL=https://www.example.com/form-page
WEBHOOK_URL=https://your-teams-webhook-url
RECAPTCHA_SITE_KEY=your-site-key-from-google
```

## Usage

Run the script with:

```bash
python3 automated-webform-tester.py
```

This will launch a browser window, simulate a user completing the form and then report the result via the console and output any failures via a Teams webhook.

### Submission detection

✅ Success: URL will contain ?data={"sid":...}
❌ Failure: URL will contain ?data={"error":"Token did not pass Google reCAPTCHA verification."}


## Notes
* This script is intended for internal testing of webform functionality and CAPTCHA handling.
* It does not bypass or solve CAPTCHAs; it works only with reCAPTCHA v3 via token simulation.
* Ensure you have appropriate permissions and usage rights when running against live environments.

⸻

## License

MIT License. See LICENSE for details.
