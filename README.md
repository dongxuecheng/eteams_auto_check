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

运行config_cron脚本
```bash
chmod +x config_cron.sh && ./config_cron.sh
```

运行test.sh脚本
```bash
chmod +x test.sh && ./test.sh
```

## Usage 📝

The script will automatically run at configured times:
- Morning: Around 8:25 AM (8:20 - 8:30)
- Evening: Around 6:10 PM (18:05 - 18:15)

## Note ⚠️
修改config.yaml中的内容
   ```bash
   apt install python3-venv
   apt install python3-pip
   python3 -m venv .venv  # 在当前目录下创建名为 .venv 的虚拟环境，.venv 是常见的虚拟环境目录名
   source .venv/bin/activate  # 或 .venv\Scripts\activate 在 Windows 上
   #激活虚拟环境后，安装如下内容
   pip install -r requirements.txt
   ```

## Acknowledgements

This project is built upon the work of others:
- [Emo403/eteams_auto](https://github.com/Emo403/eteams_auto)

## License 📄

MIT License
