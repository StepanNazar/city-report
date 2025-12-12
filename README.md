# City Report 🏙️

## Project Overview 🌟

City Report is a platform for reporting urban problems that are pinned on a map as geographic markers. Each report represents a problem attached to a location, allowing users to see where issues concentrate across the city. Reports can be viewed on a map as markers and explored in a feed that can be filtered by localities.

For each report, users may post solutions — either proposals for resolving the problem or testimony that it has been resolved. The author of a report can mark solutions as approved if they genuinely solved the problem or are being implemented.

<img width="1683" height="980" alt="зображення" src="https://github.com/user-attachments/assets/01284af0-2cb2-465d-9d3b-49790e6baf4e" />

<img width="515" height="1143" alt="зображення" src="https://github.com/user-attachments/assets/bf47b601-fe79-4d67-9603-d2b356ccb9f9" />

## Main features 🚀

- Pin posts(reports) on a map with geographic markers tied to specific locations.
- Browse a feed of posts (supports pagination).
- Filter posts by localities (cities, towns, villages).
- Create posts with text, location, and optional attached photos.
- Post solutions to reports, with optional photos.
- Post's authors can approve solutions that resolved the problem.
- Authors can edit or delete their own posts and solutions, including managing attached photos.
- Clickable photos open a photo viewer to browse images attached to a post.

## Authors ✍️

- Nazar Stepan
- Vasylyk Rostyslav

## Deployed demo 🌐

- https://city-report-17wv.onrender.com
- Note: The demo is hosted on a free tier; it may take ~1 minute to load on first access because the hosting spins down when idle. Also, images may not appear if the monthly free-tier CDN limit is reached.

## Technologies 💻

- **Frontend**: **Angular**
- **Geolocation**: **OpenStreetMap**
- **API Documentation**: **OpenAPI specification**
- **Backend**: Flask (Python) API
- **Database**: SQLite for development, PostgreSQL for production
- **Development Tools**:
  - Ruff & Pyright for Python linting/type checking
  - Commitizen for standardized commit messages
  - Pre-commit hooks for code quality

## Installation Guide (development) 🛠️

### Prerequisites

- Git
- Docker

or

- Git
- Python 3.12+
- Node.js 22.x+

### Quick Start with Docker 🐳

The easiest way to run the project locally for development is using Docker:

```bash
# Clone and enter the project
git clone https://github.com/StepanNazar/city-report.git
cd city-report

# Start all services with hot reload
docker compose -f docker-compose.dev.yml up --build
```

Access the app at:

- **Frontend**: http://localhost:4200
- **API**: http://localhost:5000

Features of Docker setup:

- ✅ Hot reload for both Angular and Flask
- ✅ SQLite for simplicity (PostgreSQL available as opt-in)
- ✅ Volume mounts for live code changes
- ✅ No local Python/Node.js installation required

### Manual Setup Instructions

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
