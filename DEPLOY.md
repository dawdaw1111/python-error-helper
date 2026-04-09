# Deployment Guide

This project is ready for a single Linux cloud server deployment with Docker Compose.

## What gets deployed

- `frontend`: Vue app built into static files and served by Nginx
- `backend`: FastAPI app
- `backend/data`: persistent SQLite storage mounted from the host

The frontend proxies `/api/*` and `/health` to the backend, so users only need one public port.

## Server requirements

- Ubuntu 22.04+ or another modern Linux distribution
- Docker Engine
- Docker Compose plugin
- Port `80` open in the server firewall / security group

## Files to prepare on the server

1. Copy the repository to the server.
2. In the project root, create `.env` from `.env.server.example`.

Example:

```bash
cp .env.server.example .env
```

Update at least these values:

```env
APP_PORT=80
VITE_API_BASE_URL=/api
PYERR_DATABASE_URL=sqlite:////app/data/pyerr.db
PYERR_CORS_ORIGINS=https://your-domain.com,http://your-server-ip
PYERR_ADMIN_USERNAME=admin
PYERR_ADMIN_PASSWORD=change-this-password
PYERR_TOKEN_SECRET=change-this-secret
PYERR_TOKEN_EXPIRE_SECONDS=86400
```

## Deploy

Run from the project root:

```bash
docker compose up -d --build
```

## Verify

```bash
docker compose ps
curl http://127.0.0.1/health
```

If the service is public, open:

```text
http://your-server-ip
```

## Useful operations

View logs:

```bash
docker compose logs -f
```

Restart:

```bash
docker compose restart
```

Stop:

```bash
docker compose down
```

Update after code changes:

```bash
git pull
docker compose up -d --build
```

## Notes

- SQLite data is stored on the host in `backend/data`.
- The backend is protected by admin login for `/api/admin/*`.
- If you want HTTPS, put Cloudflare, Nginx Proxy Manager, Caddy, or another TLS terminator in front of port `80`.
