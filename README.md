<h1 align="center">AI-Powered Hiring & Assessment Platform</h1>

<p align="center">
<em>An advanced, multi-agent system for automating and enhancing the recruitment process.</em>
</p>

## Overview

This project is a comprehensive, AI-driven platform designed to revolutionize the technical recruitment lifecycle. It leverages multiple specialized AI agents to automate the creation of realistic candidate profiles, generate unique and role-specific technical assessments, analyze market trends, and evaluate candidates for behavioral and cultural fit.

The system is composed of a powerful Python backend that orchestrates the AI agents and a modern React frontend that provides an intuitive interface for recruiters. Recruiters can specify a job role and the number of candidates, and the platform will generate detailed PDF reports for each, complete with a unique assessment designed to prevent plagiarism and accurately gauge a candidate's skills.

---

## Features

- Realistic Candidate Profile Generation: Automatically creates detailed and lifelike candidate profiles using Faker, including work experience, skills, education, and even a simulated LinkedIn bio.

- Unique, AI-Generated Assessments: Utilizes Google Gemini to generate a unique set of three problems for each candidate based on the target job role: one difficult project-based task, one medium problem-solving challenge, and one hard system design question. This ensures no two candidates receive the same assessment.

- Behavioral & Cultural Fit Analysis: An AI agent analyzes a candidate's qualitative data (like a LinkedIn bio) to identify keywords and themes related to collaboration, problem-solving, and communication, providing insights into their soft skills without demographic bias.

- Market Intelligence & Sourcing Optimizer: Another AI agent analyzes simulated market data to identify talent trends, compensation benchmarks, and optimal sourcing channels for various job roles, generating a summary report with actionable recommendations.

- Comprehensive PDF Reporting: Generates professional, multi-page PDF reports for each candidate, detailing their profile, the unique assessment questions, and the behavioral analysis.

- Web-Based User Interface: A clean frontend built with React and Material-UI allows recruiters to easily configure and trigger the generation process, view market analysis, and download the generated reports individually or as a single .zip file.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React, Vite, Material-UI (MUI), Axios |
| **Backend** | Python, FastAPI |
| **AI & LLM** | Google Gemini |
| **Data Generation** | Faker |
| **PDF Generation** | ReportLab |

---

## 🛠 Installation & Setup

### 1) Clone the Repository

```bash
git clone https://github.com/Mit-Gandhi/AI-Hiring-Task.git
cd AI-Hiring-Task
```
### 2) Navigate to backend folder

```bash
cd backend
```

### 3) Install Dependencies

```bash
pip install -r requirements.txt
```

### 4) Run backend

```bash
python api_server.py
```

### 6) Navigate to frontend folder

```bash
cd frontend
```

### 7) Install dependencies

```bash
npm install
```

### 8) Run frontend

```bash
npm run dev
```
