# City Report 🏙️

## Project Overview 🌟

City Report is an interactive platform that allows users to report and discuss various urban issues and improvement proposals. Users can create posts representing problems or suggestions, engage in discussions through comments and reactions, and collaboratively propose solutions. All reports are visualized on a map as markers, enabling intuitive exploration of issues across the city and fostering informed community participation. The system also incorporates moderation tools and AI-assisted suggestions to enhance content quality and community engagement.

Users can:

- Create posts about urban problems or improvement suggestions 📝
- Engage in discussions through comments and reactions 💬
- Collaboratively propose solutions 🤝
- Explore issues across the city using an interactive map interface 🗺️

## Concept Visualization 🎨

<img width="1177" height="678" alt="Screenshot 2025-10-06 at 22-06-44 City Report Concept" src="https://github.com/user-attachments/assets/c1980dbc-3426-453c-a610-b3a192ec1050" />

```
+---------------------------------------+
|           CITY REPORT APP             |
+---------------------------------------+
|                                       |
|  +------+                +--------+   |
|  | Menu |                | User   |   |
|  +------+                +--------+   |
|                                       |
|  +-------------------------------+    |
|  |                               |    |
|  |        INTERACTIVE MAP        |    |
|  |     (With issue markers)      |    |
|  |                               |    |
|  +-------------------------------+    |
|                                       |
|  +-------------------------------+    |
|  |       ISSUE FEED/LIST         |    |
|  | +---------------------------+ |    |
|  | | Issue 1                   | |    |
|  | | [Comments] [Solutions]    | |    |
|  | +---------------------------+ |    |
|  |                               |    |
|  | +---------------------------+ |    |
|  | | Issue 2                   | |    |
|  | | [Comments] [Solutions]    | |    |
|  | +---------------------------+ |    |
|  +-------------------------------+    |
|                                       |
+---------------------------------------+
```

## Technologies 💻

- **Backend**: Flask (Python) API
- **Frontend**: Angular
- **Database**: SQLite for development, PostgreSQL for production
- **API Documentation**: OpenAPI specification
- **Development Tools**:
  - Ruff & Pyright for Python linting/type checking
  - Commitizen for standardized commit messages
  - Pre-commit hooks for code quality

## Installation Guide 🛠️

### Prerequisites

- Python 3.12+
- Node.js 22.x+
- Git

### Setup Instructions

#### 1. Clone the repository

```bash
git clone https://github.com/StepanNazar/city-report.git
cd city-report
git checkout dev
```

#### 2. Backend Setup (Flask API)

```bash
cd api
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt

# Setup pre-commit hooks
pre-commit install
```

#### 3. Frontend Setup (Angular)

```bash
cd ../angular-app

# Install dependencies
npm install
# or with Yarn
yarn install

# Setup Angular CLI globally if you don't have it
npm install -g @angular/cli
# or with Yarn
yarn global add @angular/cli
```

## Scripts Documentation 📜

The project contains two separate `package.json` files (root and angular-app) each with their own scripts.

### Root Directory Scripts

```bash
# Start Angular frontend
npm run start-angular
# or with Yarn
yarn start-angular
# Alternatively, you can use 'npm start' or 'yarn start' to run the Angular frontend:
npm start
# or with Yarn
yarn start

# Start the Flask API backend
npm run start-api
# or with Yarn
yarn start-api

# Start a mock API using Prism
npm run start-mock-api
# or with Yarn
yarn start-mock-api

# Update OpenAPI specification (generated from Flask code)
npm run update-spec
# or with Yarn
yarn update-spec
```

### Angular App Directory Scripts (cd angular-app)

```bash
# Start Angular development server
npm run start
# or with Yarn
yarn start

# Start Flask API. Start mock API, Update OpenAPI specification are same as in root

# Build the Angular app
npm run build
# or with Yarn
yarn build

# Run tests for Angular components
npm run test
# or with Yarn
yarn test

# Build in watch mode
npm run watch
# or with Yarn
yarn watch
```
