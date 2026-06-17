# 🏦 TrustFlow: AI-Powered Loan Approval Predictor

TrustFlow is a complete, modern end-to-end Machine Learning web application designed to predict the likelihood of loan approvals based on historical applicant profiles. The system uses a **FastAPI backend** to serve predictions from a trained **Logistic Regression model** and a **Vite + React frontend** styled with a premium dark-themed dashboard using Indian Rupees (₹).

---

## 🎓 Developer Profile

* **Developer Name**: M. VENKATA RAMANA 
* **University**: Aditya University
* **Program**: Master of Computer Applications (MCA)
* **Academic Batch**: 2025-27
* **Student Roll Number / ID**: 25M11MC089

---

## 📋 1. Project Overview

### Problem Statement
In traditional banking systems, loan approval is a time-consuming, manual process that is prone to human error, cognitive bias, and operational delays. Financial institutions need an automated, data-driven system to perform preliminary credit risk assessment instantly, while providing explanation of the risk factors to bank officers and applicants.

### What TrustFlow Does
TrustFlow solves this problem by using an AI classification pipeline trained on historical loan data to evaluate applicant profiles in real-time. It predicts whether a loan should be approved or rejected, outputs a confidence probability score, and generates dynamic, feature-level risk explanations (e.g., impact of low credit history or debt load) to assist in transparent decision-making.

### Architecture Summary
TrustFlow employs a multi-tiered architecture:
1. **Frontend Layer**: React.js with custom modern HSL styling and Lucide icons.
2. **Backend API Layer**: FastAPI for high-throughput, low-latency endpoints, featuring an in-memory caching mechanism (mimicking Redis) to optimize redundant requests.
3. **Machine Learning Layer**: Scikit-learn preprocessing pipelines and a trained Logistic Regression model.
4. **Database Layer**: SQLAlchemy ORM storing logs and application audit trails in a portable SQLite database (`loans.db`).

---

## ⚡ 2. Key Features

| Feature Name | Category | Description |
|---|---|---|
| **Real-time Inference** | ML Core | Instantly predicts loan eligibility status (Approved/Rejected) upon profile submission. |
| **Probability Scoring** | ML Core | Calculates a confidence percentage score (0-100%) indicating approval likelihood. |
| **AI Explainability** | ML Core | Lists feature-level positive and negative risk factors (e.g., credit history status, debt ratio). |
| **Feature Engineering** | ML Pipeline | Auto-generates derived metrics: `Total_Income`, `Loan_to_Income_Ratio`, and `Income_Per_Dependent`. |
| **Median Imputation** | ML Pipeline | Robustly handles missing numerical values dynamically during pipeline execution. |
| **Categorical Imputation**| ML Pipeline | Replaces missing categorical values with the mode of the training population. |
| **Standard Scaling** | ML Pipeline | Normalizes numerical attributes to ensure distance-based models evaluate coefficients fairly. |
| **CORS Middleware** | Security | Configured with security-compliant cross-origin Resource sharing for smooth React interaction. |
| **Dashboard Metrics** | UI Dashboard | Renders total applications, average approval indices, average income, and loan size metrics. |
| **Applicant Form** | UI Form | Dynamic inputs with live type validation, dropdown configurations, and custom step validation. |
| **Currency Adaptation**| UI Layout | Displays all financial figures, metrics, forms, and results in Indian Rupees (₹). |
| **Historical Logs** | UI Logs | Table view showing the logged history of all assessed loans with outcome badges. |
| **Redis-like Caching** | Performance | In-memory lookup table preventing redundant processing of identical applicant structures. |
| **Swagger Docs** | Documentation | Interactive OpenAPI documentation automatically exposed at `/docs`. |
| **SQL Database Logs** | Storage | Persistent logging of inputs, predictions, engineered features, and timestamps in SQLite. |

---

## 💻 3. Tech Stack

### Frontend
* **Core Framework**: React.js (Vite template for fast builds and hot module reloading)
* **Styling**: Vanilla CSS with custom HSL variables, dark mode layout, and neon glowing borders
* **Icons**: Lucide React library

### Backend
* **Web Framework**: FastAPI (Uvicorn ASGI web server)
* **Database**: SQLite (SQLAlchemy ORM layer for portability)
* **ML Packages**: Scikit-Learn, Pandas, Numpy, Joblib

### Tooling & Development
* **Environment**: Python 3.14+
* **Package Managers**: pip, npm

---

## 📂 4. Project Structure

An annotated look at the workspace repository:

```text
LOAN APPROVAL PREDICTOR/
│
├── data/
│   └── train_u6lujuX_CVtuZ9i (1).csv   # Raw Kaggle Loan Dataset
│
├── ml/
│   └── train.py                        # Preprocessing, Feature Engineering & Model Training
│
├── backend/
│   ├── database.py                     # SQLAlchemy database configuration and engine
│   ├── models.py                       # SQLAlchemy ORM Database Models
│   ├── schemas.py                      # Pydantic Schemas for validation and serialization
│   └── main.py                         # FastAPI App, prediction caching, & explainability logic
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                     # Main Dashboard React component
│   │   ├── index.css                   # Custom global CSS (Dark mode variables & styling)
│   │   ├── App.css                     # Cleared CSS config to prevent styling conflicts
│   │   └── main.jsx                    # React startup entry point
│   ├── index.html                      # HTML root with SEO metadata and Google Fonts
│   └── package.json                    # Node dependencies (React, Lucide icons, Vite)
│
├── models/
│   ├── best_model.joblib               # Serialized ML Pipeline (scaler + model)
│   └── feature_meta.joblib             # Feature metadata
│
└── README.md                           # Developer & Intern Documentation
```

---

## 🗄️ 5. Database Schema

The SQLite database (`loans.db`) uses the following schema for tracking applications:

### Table: `loan_applications`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | Primary Key, Autoincrement | Unique identifier for each evaluation log. |
| `gender` | VARCHAR | Nullable | Applicant gender (Male/Female). |
| `married` | VARCHAR | Nullable | Marital status (Yes/No). |
| `dependents` | INTEGER | Default: 0 | Number of dependents (0, 1, 2, 3+). |
| `education` | VARCHAR | Not Null | Education level (Graduate/Not Graduate). |
| `self_employed` | VARCHAR | Nullable | Self-employment status (Yes/No). |
| `applicant_income`| FLOAT | Not Null | Monthly income of main applicant. |
| `coapplicant_income`| FLOAT | Not Null | Monthly income of co-applicant. |
| `loan_amount` | FLOAT | Nullable | Loan request size (in thousands). |
| `loan_amount_term`| FLOAT | Nullable | Term of the loan in months. |
| `credit_history` | FLOAT | Nullable | Credit standard meeting flag (1.0 or 0.0). |
| `property_area` | VARCHAR | Not Null | Location zone (Urban/Semiurban/Rural). |
| `total_income` | FLOAT | Nullable | Derived total combined income. |
| `loan_to_income_ratio`| FLOAT | Nullable | Derived loan repayment leverage ratio. |
| `income_per_dependent`| FLOAT | Nullable | Derived disposable household income index. |
| `prediction` | INTEGER | Not Null | Classification outcome (1 = Approved, 0 = Rejected). |
| `probability` | FLOAT | Not Null | Model probability of approval (0.0 to 1.0). |
| `status` | VARCHAR | Not Null | Text status ("Approved" or "Rejected"). |
| `applied_at` | DATETIME | Default: CURRENT_TIMESTAMP | Timestamp of when application was submitted. |

---

## 🎨 6. Architecture Diagram

Below is the execution flow map:

```text
  [Browser Client] 
         │ 
         │ HTTP POST/GET Requests (Port 5173)
         ▼
  [FastAPI Backend Server] (Port 8000)
    │     │
    │     ├─► [In-Memory Cache] (Quick checks for duplicate submissions)
    │     │
    │     ├─► [Joblib Pipeline] (Loads ML scaler + Logistic Regression)
    │     │
    ▼     ▼
  [SQLAlchemy ORM] ──► [SQLite DB] (loans.db table writes and read queries)
```

---

## 🔄 7. Application Workflow

A step-by-step walkthrough of the user interface flow:
1. **Explore Metrics**: On loading the page, the top dashboard displays real-time statistics (total applicants, approval indices, and average income/loan amounts).
2. **Select Assessment Form**: Under the "New Assessment" tab, input fields are set with default test values (₹5,000 income, ₹120,000 loan amount).
3. **Verify Loan Approval**: Clicking "Verify Loan Approval" sends a POST request. The page displays:
   - **Approval Decision**: A green "PRE-APPROVED" or red "REJECTED" badge.
   - **Meter Gauge**: Showing the exact probability score (e.g., 91% approval score).
4. **Inspect AI Explanations**: View the breakdown of risk factors (e.g., why semiurban location helped or how credit guideline failures impacted the decision).
5. **View History & Audit Trail**: Switch to the "History & Logs" tab to view a tabular history of all processed evaluations.

---

## 📊 8. Entity Relationship Diagram (ERD)

Since the app logs evaluations linearly, the SQLite model contains a single logs table which holds all transactional properties:

```text
┌──────────────────────────────────────────────┐
│              loan_applications               │
├──────────────────────────────────────────────┤
│ id (PK)            : INTEGER                 │
│ gender             : VARCHAR                 │
│ married            : VARCHAR                 │
│ dependents         : INTEGER                 │
│ education          : VARCHAR                 │
│ self_employed      : VARCHAR                 │
│ applicant_income   : FLOAT                   │
│ coapplicant_income : FLOAT                   │
│ loan_amount        : FLOAT                   │
│ loan_amount_term   : FLOAT                   │
│ credit_history     : FLOAT                   │
│ property_area      : VARCHAR                 │
│ total_income       : FLOAT                   │
│ loan_to_income_ratio: FLOAT                  │
│ income_per_dependent: FLOAT                  │
│ prediction         : INTEGER                 │
│ probability        : FLOAT                   │
│ status             : VARCHAR                 │
│ applied_at         : DATETIME                │
└──────────────────────────────────────────────┘
```

---

## 🌐 9. REST API Flow & Reference

### Endpoints Grouped by Domain:

```text
├── Prediction Domain
│   └── POST /api/predict       - Processes applicant profile, runs model, caches, and stores result
│
├── Insights & Explanation Domain
│   └── GET /api/explain/{id}   - Calculates mathematical contribution of features for given ID
│
└── Audit & Metrics Domain
    ├── GET /api/stats          - Fetches aggregated averages and rates for dashboard cards
    └── GET /api/history        - Retrieves historical log of last 50 assessments
```

### Full API Reference:

| Method | Path | Request Body | Response JSON | Description |
|---|---|---|---|---|
| **POST** | `/api/predict` | `LoanApplicationCreate` | `LoanApplicationResponse` | Runs prediction, caches parameters, writes to SQLite, and returns outcome. |
| **GET** | `/api/explain/{id}`| None | `{status, probability, explanations: [...]}` | Retrieves feature impact details for a specific evaluation log. |
| **GET** | `/api/stats` | None | `DashboardStats` | Returns total apps, approval rate, approved/rejected count, average income, average loan size. |
| **GET** | `/api/history` | None | `List[LoanApplicationResponse]` | Returns last 50 evaluation logs sorted by timestamp. |

---

## 📨 10. Data Flow Sequence

### Scenario A: Add Application
```text
Browser Client            FastAPI Server            SQLite Database
     │                           │                         │
     │─── POST /api/predict ────►│                         │
     │    (Applicant parameters) │                         │
     │                           │─── Write application ──►│
     │                           │    record               │
     │                           │◄── Confirm write ───────│
     │◄── Return classification ─│                         │
     │    & status               │                         │
```

### Scenario B: Caching Lifecycle
```text
Browser Client            FastAPI Server            In-Memory Cache
     │                           │                         │
     │─── POST /api/predict ────►│                         │
     │                           │─── Check cache ────────►│
     │                           │◄── Found matching record│
     │◄── Return cached result ──│                         │
```

---

## ⚠️ 11. Risk Alert Logic

In `/api/explain/{id}`, the application flags risk metrics:
* **Credit History failure**: If `credit_history == 0.0`, a critical risk alert is appended (score impact of `-0.9`), stating the applicant does not meet core bank credit guidelines.
* **High Debt-to-Income**: If the ratio of loan to income exceeds 300% (the monthly loan obligation is too high relative to earnings), a warning is appended (score impact `-0.6`), cautioning against over-leveraging.
* **Disposable Income Pressure**: If the monthly income per dependent is under ₹1,500, a negative flag (score impact `-0.3`) is added, indicating budget constraints.

---

## 📱 12. Application Screens
1. **Assessment Workspace**: Contains form inputs organized in a sleek 2-column layout. Form submissions show real-time progress indicators.
2. **Assessment Results Card**: Shows a pre-approval rating percentage meter along with high-impact color statuses (Emerald for approval, Crimson for rejection).
3. **AI Explanations Card**: Renders color-coded blocks explaining feature impacts.
4. **History Log Center**: Shows logged evaluations in tabular format, complete with formatted dates and outcome tags.

---

## 🚀 13. Getting Started

Choose one of these launching methods:

### Option A: PowerShell Launcher (Recommended)
Open PowerShell in the project directory and run:
```powershell
# Start Backend
python ml/train.py
Start-Process python -ArgumentList "-m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

# Start Frontend
cd frontend
npm install
npm run dev
```

### Option B: Command Prompt (CMD) Launcher
Open two CMD windows:
* **Window 1 (Backend)**:
  ```cmd
  python ml/train.py
  python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
  ```
* **Window 2 (Frontend)**:
  ```cmd
  cd frontend
  npm install
  npm run dev
  ```

### Option C: Manual Launch
1. Run `python ml/train.py` to train the model.
2. Run `python -m uvicorn backend.main:app` to start the backend.
3. Open a browser to `http://localhost:5173/` after starting Vite via `npm run dev` in the frontend directory.

---

## 🗃️ 14. Seed Data

Example evaluation records compiled in the system:

| Gender | Married | Dependents | Education | Self-Employed | Income (₹) | Loan Amount (₹) | Credit History | Expected Outcome |
|---|---|---|---|---|---|---|---|---|
| Male | Yes | 0 | Graduate | No | 5,849 | 120,000 | Meets Guidelines | Approved |
| Male | Yes | 1 | Graduate | No | 4,583 | 128,000 | Meets Guidelines | Approved |
| Male | Yes | 0 | Graduate | Yes | 3,000 | 66,000 | Meets Guidelines | Approved |
| Male | Yes | 3+ | Graduate | No | 5,516 | 495,000 | Does Not Meet | Rejected |
| Female| No | 0 | Graduate | Yes | 4,583 | 133,000 | Does Not Meet | Rejected |

---

## 📝 15. Development Notes & Future Enhancements

### Key Design Decisions
1. **Scikit-Learn Preprocessing Pipelines**: Wrapping both imputation and encoding in a single `ColumnTransformer` pipeline guarantees that new input data undergoes identical transformations, avoiding manual data manipulation bugs.
2. **In-Memory Cache over Redis**: Using an in-memory dictionary avoids local dependency installation issues for users, keeping the application portable.
3. **Decoupled Architecture**: Standardized REST payloads make the frontend independent of the ML model used behind the scenes.
4. **Logistic Regression Selection**: Chosen for its high interpretability, enabling clear explanation of weights and coefficients.
5. **SQLite Database**: SQLite database files compile locally and require zero backend service setups, keeping the setup lightweight.
6. **Robust Validation**: Enforces rigorous type compliance through Pydantic data schemas.
7. **Premium Styling Variable system**: CSS HSL variables support easy theme styling changes.

### Future Enhancements
* **SHAP Explainability Integration**: Use SHAP values directly in the backend for deeper ML insights.
* **Auto-Retraining Pipeline**: Implement cron jobs to retrain the model daily as new records are stored in `loans.db`.
* **Multilingual Frontend**: Support local Indian languages (Hindi, Telugu, Tamil, etc.).
#   L o a n - A p p r o v a l - P r e d i c t o r  
 