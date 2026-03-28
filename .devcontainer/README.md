# PlanVenture Dev Container Setup

This directory contains configuration files for VS Code Dev Containers, which provides a consistent development environment for the PlanVenture project.

## Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Git

### Opening the Project in Dev Container

1. Clone the repository and open it in VS Code:
   ```bash
   git clone https://github.com/itech4real/planventure.git
   cd planventure
   code .
   ```

2. When prompted, click **"Reopen in Container"** or use the Command Palette (`Ctrl+Shift+P`) and search for **"Dev Containers: Reopen in Container"**

3. VS Code will build the Docker image and start the container (first time may take 2-3 minutes)

4. The post-create script will automatically install all dependencies

## Environment Details

### What's Included
- **Python 3.11** with pip, virtual environments, and development tools
- **Node.js LTS** with npm, yarn, and pnpm
- **PostgreSQL** database server (running in separate container)
- **Git** and **GitHub CLI** for version control
- **Development extensions** pre-installed in VS Code:
  - Python (Pylance, Debugpy, Ruff)
  - JavaScript/TypeScript (ESLint, Prettier)
  - Docker extension
  - GitHub Copilot

### Services

| Service | Port | Command |
|---------|------|---------|
| PlanVenture API | 5000 | `cd planventure-api && python app.py` |
| PlanVenture Web | 3000 | `cd planventure-web && npm run dev` |
| PostgreSQL | 5432 | Running in background |

## Running Services

### Start the API
```bash
cd planventure-api
python app.py
```
The API will be available at `http://localhost:5000`

### Start the Web App
```bash
cd planventure-web
npm run dev
```
The web app will be available at `http://localhost:3000`

### Run Tests
```bash
cd planventure-api
python -m pytest -v
```

### Database Access
PostgreSQL is running on `localhost:5432` with:
- Username: `postgres`
- Password: `postgres`
- Database: `postgres`

Use `psql` CLI or any PostgreSQL client to connect:
```bash
psql -h localhost -U postgres -d postgres
```

## Customization

### Adding More Extensions
Edit `.devcontainer/devcontainer.json` and add extension IDs to the `customizations.vscode.extensions` array, then rebuild the container:
```json
"extensions": [
  "ms-python.python",
  "your-new-extension-id"
]
```

### Installing Additional Packages
- For Python: `pip install package-name`
- For Node: `npm install package-name`

These will be available in the container but won't persist if the container is deleted unless added to `requirements.txt` or `package.json`.

### Modifying Base Image
To upgrade Python or Node versions, edit `.devcontainer/Dockerfile` and rebuild.

## Troubleshooting

### Container won't start
- Ensure Docker Desktop is running
- Try: `Dev Containers: Rebuild Container` (Ctrl+Shift+P)

### Extensions not showing up
- All extensions will be installed inside the container
- They won't appear in your local VS Code installation
- Reload the VS Code window to see them

### Port conflicts
- If ports 5000, 3000, or 5432 are already in use, modify `forwardPorts` in `devcontainer.json`

### Slow performance on Windows/Mac
- Dev Containers run best on Linux
- For Windows, use WSL2 backend in Docker Desktop
- Consider disabling antivirus/file scanning in docker directories

## Rebuilding the Container

If you modify the Dockerfile or devcontainer.json:
```
Ctrl+Shift+P → Dev Containers: Rebuild Container
```

## References
- [VS Code Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [Dev Container Specification](https://containers.dev/)
