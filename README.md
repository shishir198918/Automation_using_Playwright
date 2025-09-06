# Automation Framework: Behave + Playwright + Allure

This project is an **automation framework** built using  
- Behave(https://behave.readthedocs.io/en/stable/) for BDD (Gherkin-style tests)  
- Playwright  
- Allure for reporting  

It covers automation for two modules of the application:  
- **HIM Dashboard**  
- **Login Page**  


##  Sample Feature File

```gherkin
Feature: Testing data validation

  Scenario: Testing default episodes presenting on HIM dashboard and validating UI with total number of episodes
    Given login into enviroment as per directed
    When Goto Him_dashboard where list of episode is shown
    Then Match value with UI to API

  Scenario Outline: Testing episodes presenting on HIM dashboard and validating UI with API
    Given Login into environment go to HIM dashboard
    When Into HIM dashboard go to <assign_coder> selecting
    Then validate data with API with element Total Episode, Uncoded, Unassigned and In progress

    Examples:
      | assign_coder |
      | sai          |
      | sagar        |
      | amrutha      |
```

---

---

## Project Structure

```
Tests/
│   .env                     # Environment configuration (Base URL, credentials, etc.)
│   requirements.txt         # Python dependencies
│
├── HIM_enviroment/          # Module: HIM Dashboard
│   ├── features/            # Feature files & step definitions
│   │   ├── HIM_dashborad.feature
│   │   ├── environment.py
│   │   └── steps/
│   │       ├── HIM_assignCoder.py
│   │       └── HIM_home_page.py
│   │
│   └── reports/
│       ├── allure-results/  # Raw Allure results
│       └── allure-reports/  # HTML Allure reports
│
└── login_Page/              # Module: Login Page
    ├── features/            # Feature files
    │   ├── him_dashboard.feature
    │   └── testing.py
    │
    ├── steps/               # Step definitions
    │   ├── test_login.py
    │   ├── test_blank_login.py
    │   └── flow.text
    │
    └── reports/
        ├── allure-results/
        └── allure-reports/
```

---



## Running Tests

Run all tests:
```bash
behave
```

Run tests for a specific module:
```bash
cd HIM_enviroment/features
behave

cd login_Page/features
behave
```

Run a single feature file:
```bash
behave HIM_enviroment/features/HIM_dashborad.feature
```

---

## Generating Reports (Allure)

After running tests, **Allure results** are generated in `reports/allure-results`.  
To view the report:

```bash
allure serve HIM_enviroment/reports/allure-results
```

or for Login Page:

```bash
allure serve login_Page/reports/allure-results
```

This will open an interactive **HTML dashboard** with trends, charts, and detailed execution history.

