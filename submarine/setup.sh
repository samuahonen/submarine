#!/bin/bash

# --- CONFIGURATION ---
SCRIPT_PATH="/home/samu/submarine/submarine/main.py"
SCRIPT_DIR="/home/samu/submarine/submarine"
SERVICE_NAME="submarine.service"
USERNAME="samu"

echo "--- Starting Submarine Setup ---"

# 1. Check if main.py exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: Could not find file at $SCRIPT_PATH"
    echo "Please check that the folder path is correct."
    exit 1
fi

# 2. Make executable
chmod +x "$SCRIPT_PATH"

# 3. Create the Systemd Service File
echo "📝 Updating service file..."

sudo bash -c "cat > /etc/systemd/system/$SERVICE_NAME <<EOF
[Unit]
Description=Submarine Python Startup Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_PATH
WorkingDirectory=$SCRIPT_DIR
StandardOutput=inherit
StandardError=inherit
User=$USERNAME

# --- RESTART SETTINGS ---
# Restart automatically if it crashes or exits
Restart=always
# Wait 5 seconds before restarting (prevents rapid looping)
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF"

# 4. Reload and Enable
echo "🔄 Reloading system daemon..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

# 5. Restart the service to apply changes
echo "🚀 Restarting the service with new settings..."
sudo systemctl restart $SERVICE_NAME

echo "--- Setup Complete! ---"
echo "Your script will now wait 5 seconds before restarting if it fails."
echo "Status:"
sudo systemctl status $SERVICE_NAME --no-pager