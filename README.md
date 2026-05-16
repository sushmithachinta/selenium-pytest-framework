# selenium-pytest-framework

> Production-ready Selenium WebDriver + PyTest automation framework using Page Object Model, built against [The Internet](https://the-internet.herokuapp.com) — a free public website for automation practice.

---

## 📁 Project Structure

```
selenium-pytest-framework/
├── .github/
│   └── workflows/
│       └── test-pipeline.yml       # GitHub Actions CI (smoke + regression)
├── pages/
│   ├── base_page.py                # Base class — all shared WebDriver actions
│   ├── login_page.py               # Login page object
│   ├── dropdown_page.py            # Dropdown page object
│   ├── checkboxes_page.py          # Checkboxes page object
│   ├── alerts_page.py              # JS Alerts page object
│   └── drag_drop_page.py           # Drag & Drop page object
├── tests/
│   ├── conftest.py                 # Fixtures, WebDriver setup, auto-screenshot
│   ├── test_login.py               # 10 login scenarios (smoke + parametrized)
│   ├── test_dropdown.py            # 9 dropdown scenarios
│   ├── test_checkboxes.py          # 8 checkbox scenarios
│   ├── test_alerts.py              # 7 alert scenarios (parametrized)
│   └── test_drag_drop.py           # 5 drag & drop scenarios
├── utils/
│   ├── config.py                   # .env config loader
│   ├── driver_factory.py           # Chrome / Firefox / Edge setup
│   └── logger.py                   # Centralized logging to file + console
├── reports/                        # Auto-generated (gitignored)
│   └── screenshots/                # Auto-captured on failure
├── .env                            # Environment variables
├── .gitignore
├── pytest.ini                      # Pytest config, markers, report path
├── requirements.txt
└── README.md
```

---

## ✨ Features

| Feature | Details |
|---|---|
| Page Object Model | Clean separation — tests never touch locators directly |
| Cross-browser | Chrome · Firefox · Edge via webdriver-manager |
| Parallel execution | `pytest-xdist` — run with `-n 4` |
| Auto-screenshot | Captured automatically on any test failure |
| HTML reports | Generated at `reports/report.html` after every run |
| Centralized logging | Console + file log at `reports/test_run.log` |
| Markers | `smoke` · `regression` · `login` · `dropdown` · `checkbox` · `alert` · `drag_drop` |
| GitHub Actions CI | Smoke → Regression → Upload artifacts |
| Parametrized tests | Multiple data sets in single test functions |

---

## 🚀 Setup & Run

### 1. Clone & install
```bash
git clone https://github.com/Sushmithachinta/selenium-pytest-framework.git
cd selenium-pytest-framework
pip install -r requirements.txt
```

### 2. Run all tests (headless Chrome)
```bash
pytest --headless
```

### 3. Run only smoke tests
```bash
pytest -m smoke --headless -v
```

### 4. Run in parallel (4 workers)
```bash
pytest -n 4 --headless
```

### 5. Run specific test file
```bash
pytest tests/test_login.py -v --headless
```

### 6. Run with Firefox
```bash
pytest --browser=firefox --headless
```

### 7. Generate HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

---

## 🧪 Test Coverage

| Module | Tests | Markers |
|---|---|---|
| Login | 10 | smoke, login |
| Dropdown | 9 | regression, dropdown |
| Checkboxes | 8 | regression, checkbox |
| Alerts | 7 | regression, alert |
| Drag & Drop | 5 | regression, drag_drop |
| **Total** | **39** | |

---

## 🌐 Test Site

All tests run against **[The Internet by Herokuapp](https://the-internet.herokuapp.com)** — a free, publicly available website built specifically for automation practice. No account needed.

---

## 📊 CI Pipeline

Every push to `main` or `develop` triggers:
1. **Smoke tests** — fast gate (~2 min)
2. **Full regression** — parallel execution (if smoke passes)
3. **Artifact upload** — HTML reports + failure screenshots

---

*Built to demonstrate Google-aligned test engineering standards: framework ownership, test plan coverage, failure analysis, and CI/CD integration.*
