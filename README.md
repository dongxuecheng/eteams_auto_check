# E-Teams Auto Check 👨‍💻

A Python script for automatic check-in/out on the E-Teams platform. Automatic daily check-in and check-out！
[中文](README_zh.md)

## Features ✨

- **Random time variation** (±5 minutes) to simulate human behavior 🎲
- **Cron job scheduling** for reliability ⚡
- **Holiday skipping**: Automatically skips Chinese holidays 🏖️
- **Customizable check-in locations** 📍
- **Telegram bot notifications** 📲


## Setup and Configuration on Your Server/VPS 🛠️

1. **Clone this repository**
   ```bash
   git clone -b vps-deploy https://github.com/dongxuecheng/eteams_auto_check.git
   ```

2. **Install required dependencies**
   ```bash
   cd eteams_auto_check
   apt install python3-venv
   apt install python3-pip
   python3 -m venv .venv  
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure your info in `config.yaml`**

4. **Set up cron jobs** ⏰
   - Set the system timezone to Shanghai
   ```bash
   timedatectl set-timezone Asia/Shanghai
   ```

5. **Run the `config_cron` script**
   ```bash
   chmod +x config_cron.sh && ./config_cron.sh /home/eteams_auto_check
   ```

## Usage 📝

The script will automatically run at the configured times:
- **Morning:** Around 8:20 AM (8:20 - 8:25)
- **Evening:** Around 6:10 PM (18:10 - 18:15)

## Acknowledgements 🙏

This project is built upon the work of others:
- [Emo403/eteams_auto](https://github.com/Emo403/eteams_auto)

## License 📄

This project is licensed under the MIT License.
