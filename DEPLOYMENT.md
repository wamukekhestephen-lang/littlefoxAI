# DigitalOcean Deployment Guide

## Option 1: DigitalOcean App Platform (Recommended - Easiest)

### Prerequisites
- DigitalOcean account
- GitHub repository with your code
- Docker Hub account (optional)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create App Platform**
   - Go to DigitalOcean Dashboard
   - Click "Apps" → "Create App"
   - Select GitHub as source
   - Connect your repository
   - Select the repo and branch (main)

3. **Configure the App**
   - Component Type: Docker
   - Dockerfile path: `./Dockerfile`
   - HTTP Port: `8080`
   - Environment variables:
     ```
     FLASK_ENV=production
     FLASK_DEBUG=0
     OLLAMA_HOST=http://localhost:11434
     ```

4. **Set Resources**
   - Basic plan: $12/month for single container
   - Or go higher for better performance

5. **Deploy**
   - Review settings
   - Click "Create Resources"
   - Wait for deployment (5-10 minutes)

---

## Option 2: Droplet + Docker Compose (More Control)

### Prerequisites
- DigitalOcean account
- SSH key pair
- Docker installed

### Steps

1. **Create Droplet**
   - Size: 2GB RAM / 1 CPU minimum ($6/month)
   - Image: Ubuntu 22.04 LTS
   - Add SSH keys
   - Choose region nearest to you

2. **SSH into Droplet**
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Install Docker & Docker Compose**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   chmod +x /usr/local/bin/docker-compose
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

5. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   nano .env
   ```

6. **Update Secrets**
   - Generate secure password for PostgreSQL
   - Generate secret key for Flask
   - Update DATABASE_URL

7. **Start Services**
   ```bash
   docker-compose up -d
   ```

8. **Setup Reverse Proxy (Nginx)**
   ```bash
   apt-get update
   apt-get install -y nginx
   ```

   Create `/etc/nginx/sites-available/ai-assistant`:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:8080;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Enable and start:
   ```bash
   ln -s /etc/nginx/sites-available/ai-assistant /etc/nginx/sites-enabled/
   nginx -t
   systemctl restart nginx
   ```

9. **Setup SSL (Let's Encrypt)**
   ```bash
   apt-get install -y certbot python3-certbot-nginx
   certbot --nginx -d your_domain.com
   ```

10. **Monitor Logs**
    ```bash
    docker-compose logs -f web
    docker-compose logs -f ollama
    ```

---

## Option 3: Droplet + Manual Setup

Less recommended but possible if you prefer not to use Docker.

### Steps
1. Create Droplet (Ubuntu 22.04)
2. Install Python 3.11+
3. Install system dependencies
4. Install requirements: `pip install -r requirements.txt`
5. Use Gunicorn for production: `pip install gunicorn`
6. Setup Nginx as reverse proxy
7. Use systemd service file for auto-restart
8. Setup monitoring and backups

---

## Post-Deployment Checklist

- [ ] Test application at your domain
- [ ] Configure HTTPS/SSL certificate
- [ ] Setup database backups
- [ ] Configure monitoring (DigitalOcean Monitoring)
- [ ] Setup automatic updates
- [ ] Configure firewalls/security groups
- [ ] Test Ollama model loading
- [ ] Verify knowledge base imports
- [ ] Setup logging and error tracking
- [ ] Configure domain DNS
- [ ] Test all main features (chat, search, etc.)

---

## Cost Estimates

### App Platform
- Basic: $12/month
- Starter: $25/month
- Professional: $50+/month

### Droplet + Docker
- Minimum: $4-6/month (1GB RAM)
- Recommended: $12-18/month (2-4GB RAM)
- With database: +$15/month

---

## Troubleshooting

### Container won't start
```bash
docker-compose logs web
```

### Port already in use
```bash
# Change port in docker-compose.yml or stop conflicting service
lsof -i :8080
```

### Ollama not responding
```bash
docker-compose logs ollama
# Ensure ollama service is healthy
docker-compose ps
```

### Database connection errors
- Verify DATABASE_URL in .env
- Check PostgreSQL container is running
- Ensure password is correct

### Out of disk space
```bash
docker system prune -a
df -h
```

---

## Scaling Tips

1. **Load Balancing**: Use DigitalOcean Load Balancer ($10/month)
2. **CDN**: DigitalOcean Spaces for static files ($5/month)
3. **Database**: Managed PostgreSQL ($15+/month)
4. **Monitoring**: Datadog or New Relic integration
5. **Auto-scaling**: App Platform auto-scales with CPU/memory

---

## Security Considerations

1. **Environment Variables**: Never commit secrets, use .env
2. **Firewall Rules**: Restrict access to required ports only
3. **HTTPS**: Always use SSL/TLS certificates
4. **Database**: Use strong passwords, consider encryption
5. **Updates**: Keep Docker images and packages updated
6. **Backups**: Regular database and file backups
7. **Monitoring**: Setup alerts for errors and downtime

---

## Next Steps

1. Choose deployment option (App Platform recommended for simplicity)
2. Follow steps for your chosen option
3. Test deployment thoroughly
4. Setup monitoring and backups
5. Configure custom domain
6. Monitor costs and scale as needed

For questions or issues, refer to:
- DigitalOcean Docs: https://docs.digitalocean.com
- Docker Docs: https://docs.docker.com
- Flask Docs: https://flask.palletsprojects.com
