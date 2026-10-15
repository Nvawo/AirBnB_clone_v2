#!/usr/bin/env bash
# Sets up a web server for the deployment of web_static

# Install Nginx if it is not already installed
if ! command -v nginx > /dev/null 2>&1; then
    apt-get update -y
    apt-get install -y nginx
fi

# Create the required folders (-p skips ones that already exist)
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file to test the Nginx configuration
cat > /data/web_static/releases/test/index.html << 'EOF'
<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>
EOF

# Recreate the symbolic link every time the script runs
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to the ubuntu user and group, recursively
chown -R ubuntu:ubuntu /data/

# Serve /data/web_static/current/ at /hbnb_static (only add it once)
CONF="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" "$CONF"; then
    sed -i '/server_name _;/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' "$CONF"
fi

# Restart Nginx to apply the changes
service nginx restart

exit 0
