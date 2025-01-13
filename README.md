# E-Teams Auto Check 👨‍💻

A Python script for automatic check-in/out on E-Teams platform.可自动跳过中国节假日，自定义打卡位置。

## Features ✨

- Automatic daily check-in and check-out 🕒
- Random time variation (±5 minutes) to simulate human behavior 🎲
- Cron job scheduling for reliability ⚡

## Setup and Configuration 🛠️

1. Clone this repository
2. Install required dependencies
3. Configure your credentials
4. Set up cron jobs

## Cron Configuration ⏰

Follow these steps to set up automatic scheduling:

1. Open your crontab configuration:
   ```bash
   crontab -e
   ```

2. Add the following lines (adjust paths according to your setup):
   ```bash
   # Morning check-in (8:25 AM ± 5 minutes)
   25 8 * * * sleep $((RANDOM % 300)) && cd /path/to/project && python auto_checker.py >> /path/to/project/logs/auto_checker.log 2>&1
   
   # Evening check-out (6:10 PM ± 5 minutes)
   10 18 * * * sleep $((RANDOM % 300)) && cd /path/to/project && python auto_checker.py >> /path/to/project/logs/auto_checker.log 2>&1
   ```

4. Save and exit the editor
   - For vim: Press `ESC`, then type `:wq`
   - For nano: Press `Ctrl + X`, then `Y`, then `Enter`

5. Verify your cron jobs:
   ```bash
   crontab -l
   ```

The script will now run automatically at specified times.

Note: Ensure the path `/path/to/project` is replaced with your actual project directory path.

## Usage 📝

The script will automatically run at configured times:
- Morning: Around 8:25 AM (8:20 - 8:30)
- Evening: Around 6:10 PM (18:05 - 18:15)

## Note ⚠️
需要手动安装chinesecalender
   ```bash
   pip install chinesecalender
   ```

## Acknowledgements

This project is built upon the work of others:
- [Emo403/eteams_auto](https://github.com/Emo403/eteams_auto)

## License 📄

MIT License
