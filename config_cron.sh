#!/bin/bash

# Project configuration
PROJECT_PATH="/home/eteams_auto_check"  # Change to your project path
VENV_PATH="${PROJECT_PATH}/.venv"
LOG_PATH="${PROJECT_PATH}/logs"

# Check if project directory exists
if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project directory not found at $PROJECT_PATH"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p "$LOG_PATH"

# Build cron configuration with virtual environment activation
CRON_CONFIG=$(cat << EOF
# Morning check-in (8:25 AM)
TZ=Asia/Shanghai 25 8 * * * cd "${PROJECT_PATH}" && ${VENV_PATH}/bin/python3 auto_checker.py >> "${LOG_PATH}/auto_checker.log" 2>&1

# Evening check-out (6:10 PM)
TZ=Asia/Shanghai 10 18 * * * cd "${PROJECT_PATH}" && ${VENV_PATH}/bin/python3 auto_checker.py >> "${LOG_PATH}/auto_checker.log" 2>&1
EOF
)

# Backup existing crontab
crontab -l > "${PROJECT_PATH}/crontab.backup" 2>/dev/null

# Update crontab with new configuration
(crontab -l 2>/dev/null; echo "$CRON_CONFIG") | crontab -

echo "Cron configuration updated successfully!"
echo "Backup of previous configuration saved to: ${PROJECT_PATH}/crontab.backup"

# Display current crontab
echo -e "\nCurrent crontab configuration:"
crontab -l
