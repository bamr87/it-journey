#!/bin/bash
# Installs apache and a custom homepage
sudo su -
apt update
apt -y install apache2
cat <<EOF > /var/www/html/index.html
<html><body><h1>Hello World</h1>
<p>This page was created from a start up script.</p>
</body></html>
EOF'
