---
title: "Host Django on Raspberry Pi: A Complete Guide"
description: ""
date: 2025-02-05T21:01:31.550Z
preview: ""
tags: []
categories: []
sub-title: null
excerpt: null
snippet: null
author: ""
layout: null
keywords: {}
lastmod: 2025-02-05T21:08:47.736Z
permalink: null
attachments: ""
---

Below is a detailed, step-by-step guide to hosting your Django project on a Raspberry Pi behind Cloudflare Tunnel. The end result will be a secure HTTPS connection to your Raspberry Pi’s Django application using your own domain name, without having to open ports on your home router.

---

## Overview of the Process

1. **Obtain a Domain** and **Add It to Cloudflare**  
2. **Prepare the Raspberry Pi** (update system, install Python dependencies, set up Django)  
3. **Install and Configure Cloudflare Tunnel (`cloudflared`)** on the Pi  
4. **Configure Your Tunnel** to point your domain to the local Django server port  
5. **Test and Verify** everything works under `https://yourdomain.com`

---

## 1. Set Up Your Domain on Cloudflare

### 1.1 Obtain a Domain Name
- Purchase a domain from a registrar (e.g., Namecheap, Google Domains, etc.) if you don’t already have one.

### 1.2 Create a Cloudflare Account and Add Your Domain
1. Go to [https://dash.cloudflare.com/](https://dash.cloudflare.com/) and sign up or log in.  
2. Click **Add a Site**.  
3. Enter your domain name (e.g., `example.com`) and select a free plan (or paid if you prefer).  
4. Cloudflare will scan existing DNS records (you can review or adjust these later).  
5. You’ll be prompted to change your domain’s nameservers to Cloudflare’s nameservers.  
   - Log in to your domain registrar, find the DNS or Nameservers settings, and update them to the nameservers shown by Cloudflare.
6. Wait for Cloudflare to confirm your domain is active (this can take from a few minutes up to 24 hours, but usually it’s quick).

Once your domain is **active** in Cloudflare, you will manage its DNS from the Cloudflare dashboard.

---

## 2. Prepare Your Raspberry Pi

### 2.1 Update and Install System Packages

1. **SSH into your Raspberry Pi** or connect via a monitor/keyboard.  
2. Update the system:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```
3. (Optional) Install some useful packages:
   ```bash
   sudo apt install -y python3 python3-pip python3-venv git
   ```

### 2.2 Set Up Your Django Project

Assuming you already have a Django project, do something like:

1. Clone the barodybroject repository onto the Pi:
   ```bash
   git clone https://github.com/bamr87/github/barodybroject.git
   cd barodybroject
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt  # or manually: django gunicorn, etc.
   ```
3. Run migrations and test the development server locally:
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```
4. If you see the Django welcome page on `http://<Pi-IP>:8000`, you’re good. **Stop** the dev server (Ctrl + C).

### 2.3 (Optional) Use Gunicorn/Uvicorn in Production Mode

For a more robust setup, you can run Django via [Gunicorn](https://gunicorn.org/) or [Uvicorn](https://www.uvicorn.org/). For instance:
```bash
gunicorn --bind 127.0.0.1:8000 barodybroject.wsgi
```
- This will bind your app to localhost:8000.  
- You can set this up as a systemd service so it starts automatically, or just run it in a screen/tmux session for testing.

---

## 3. Install and Configure `cloudflared` on Raspberry Pi

Cloudflare Tunnel works by installing a small daemon (`cloudflared`) on your Raspberry Pi that creates an outbound-only connection to Cloudflare’s network. Then, Cloudflare routes inbound traffic (from the public internet) over that tunnel to your Pi.

### 3.1 Install `cloudflared`

#### Option A: Install Using the Official Cloudflare .deb Package

1. Download and add the Cloudflare GPG key:
   ```bash
   curl -L https://pkg.cloudflare.com/cloudflare-main.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloudflare-main.gpg
   ```
2. Add the Cloudflare apt repository:
   ```bash
   echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] http://pkg.cloudflare.com/ jammy main" | sudo tee /etc/apt/sources.list.d/cloudflare.list
   ```
   *(Note: Replace `jammy` with your actual OS codename if necessary. Raspberry Pi OS is often based on `bullseye` or `buster`, so verify which repository is appropriate. More info here: [Cloudflare Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/).)*

3. Update and install:
   ```bash
   sudo apt update
   sudo apt install cloudflared
   ```

#### Option B: Install via Manually Downloading Binary (If APT not supported)
- Go to the [Cloudflare GitHub Releases](https://github.com/cloudflare/cloudflared/releases) page, download the latest ARM .deb or tarball for Raspberry Pi, and install it manually:
  ```bash
  wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm.deb
  sudo dpkg -i cloudflared-linux-arm.deb
  ```
*(Instructions vary, but typically it’s straightforward to install.)*

### 3.2 Authenticate `cloudflared`

1. Log in to Cloudflare from the Pi:
   ```bash
   cloudflared tunnel login
   ```
2. This command will print a URL. Copy it, open it in your browser (where you’re logged in to Cloudflare), and **authorize** `cloudflared`.  
3. Once authorized, return to your Pi terminal.

---

## 4. Create and Configure a Named Tunnel

### 4.1 Create the Tunnel

1. Create a new tunnel (give it a name):
   ```bash
   cloudflared tunnel create my-django-tunnel
   ```
2. This stores a credentials JSON file to your system, typically at:
   ```
   /home/pi/.cloudflared/<TUNNEL_ID>.json
   ```
   or `/etc/cloudflared/<TUNNEL_ID>.json`.

### 4.2 Configure the Tunnel to Point to Django

Create (or edit) a config file for this tunnel. For example:
```bash
sudo nano /etc/cloudflared/config.yml
```
*(Location can vary; just be consistent. Many users keep it in `/home/pi/.cloudflared/`.)*

Put something like this in `config.yml`:

```yaml
tunnel: <TUNNEL_ID_FROM_ABOVE>
credentials-file: /etc/cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
```

Explanation:

- **tunnel**: The unique tunnel ID you generated.
- **credentials-file**: Path to the JSON credentials from step 4.1.
- **ingress** rules:
  - First rule: direct requests for `yourdomain.com` to `http://localhost:8000` (where Gunicorn or Django dev server is running).
  - Second rule: a “catch-all” for anything else that returns a 404.

### 4.3 Route Your Domain to the Tunnel

1. You can do this either from the Cloudflare web dashboard or from the command line.  
2. **From command line**:
   ```bash
   cloudflared tunnel route dns my-django-tunnel yourdomain.com
   ```
   This will automatically create a DNS record (CNAME) in Cloudflare linking `yourdomain.com` to the tunnel.

### 4.4 Start the Tunnel

```bash
sudo cloudflared tunnel run my-django-tunnel
```
or  
```bash
sudo cloudflared tunnel run --config /etc/cloudflared/config.yml
```

#### (Optional) Run as a Systemd Service
To ensure Cloudflare Tunnel starts at boot, you can enable the service:

```bash
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

Now your Pi will automatically connect to Cloudflare on reboot.

---

## 5. Configure Cloudflare SSL/TLS Settings

Log in to your Cloudflare dashboard and do the following:

1. Go to **SSL/TLS** → **Overview** for your domain.  
2. Choose the encryption mode:
   - **Flexible**: Encrypts traffic between the browser and Cloudflare, but unencrypted between Cloudflare and your Pi. This is easiest if you don’t have an SSL certificate installed locally.  
   - **Full** (strict recommended if you can manage local certificates): End-to-end encryption. Requires you to have a certificate on the Pi or use an origin cert from Cloudflare.  

For quick setups, **Flexible** is fine. If you want truly secure end-to-end, switch to “Full (strict)” once you’ve installed an SSL cert on your Pi (you can use Cloudflare Origin Certificates, for example).

---

## 6. Test Your Setup

1. Ensure your Django application is running locally on `localhost:8000` (e.g., `gunicorn your_django_project.wsgi:application --bind 127.0.0.1:8000`).  
2. Ensure `cloudflared` tunnel is running:
   ```bash
   sudo systemctl status cloudflared
   ```
   or if running manually, confirm it’s showing “Connected to Cloudflare.”
3. In a web browser, go to **`https://yourdomain.com`**.
4. You should see your Django app!  

If everything is working, you have a secure, globally accessible site:

- Browsers show HTTPS lock icon (if Cloudflare SSL settings are correct).  
- Your Pi’s public IP remains hidden (no open ports, no direct exposure).  

---

## 7. Additional Best Practices

1. **Set Django’s `ALLOWED_HOSTS`**  
   - In the settings file (located at src/barodybroject/settings.py), add your domain (e.g., "yourdomain.com") along with "localhost" and "127.0.0.1":
     ```python
     ALLOWED_HOSTS = ["yourdomain.com", "localhost", "127.0.0.1"]
     ```
2. **Run in Production Mode**  
   - Use Gunicorn (or Uvicorn) + a process manager (systemd) or Docker.  
3. **Secure Your Pi**  
   - Disable password SSH login, use SSH keys.  
   - Keep software updated (`sudo apt update && sudo apt upgrade`).  
4. **Logging and Metrics**  
   - Check Cloudflare’s dashboard for requests, error logs, etc.  
   - Check `cloudflared` logs on the Pi: `journalctl -u cloudflared -f`.  
5. **Use a Reverse Proxy Locally (Optional)**  
   - Some prefer Nginx or Caddy on the Pi to handle advanced logic (e.g., multiple apps). You can still have your local proxy listen on `localhost:8000` or `localhost:8080`, and `cloudflared` forwards traffic to that port.

---

# Final Summary

**Cloudflare Tunnel** is one of the easiest and most secure ways to host your Django app on a Raspberry Pi from home without exposing ports or dealing with dynamic IP headaches. In a nutshell:

1. **Set up your domain on Cloudflare** (and make sure DNS is managed by Cloudflare).  
2. **Install and authenticate `cloudflared`** on the Pi.  
3. **Run your Django application** on a local port (e.g., `127.0.0.1:8000`).  
4. **Create a named tunnel** and configure Cloudflare to forward requests from `yourdomain.com` to `localhost:8000`.  
5. **Browse to `https://yourdomain.com`** and enjoy your publicly accessible, SSL-protected Django site with minimal fuss and maximum security.