# HTTPS Deployment Configuration

To deploy the Django application securely using HTTPS, the following steps are required:

## 1. Obtain SSL/TLS Certificates
Use one of the following:
- Let's Encrypt (free)
- Commercial SSL provider
- Self-signed certificate for testing

Example (Let's Encrypt with Certbot):

sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com


## 2. Configure Nginx for HTTPS
Example configuration:

server {
listen 443 ssl;
server_name yourdomain.com;

ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";

location / {
proxy_pass http://127.0.0.1:8000;
}
}

server {
listen 80;
server_name yourdomain.com;
return 301 https://$host$request_uri;
}


## 3. Django Settings
The following settings enforce HTTPS:

- SECURE_SSL_REDIRECT = True
- SECURE_HSTS_SECONDS = 31536000
- SECURE_HSTS_INCLUDE_SUBDOMAINS = True
- SECURE_HSTS_PRELOAD = True
- SESSION_COOKIE_SECURE = True
- CSRF_COOKIE_SECURE = True
