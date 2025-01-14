# E-Teams 自动签到 👨‍💻

一个用于在 E-Teams 平台上自动签到/签退的 Python 脚本。每天自动签到和签退！
[English](README.md)

## 功能 ✨

- **随机时间变化**（±5 分钟）模拟人类行为 🎲
- **Cron 任务调度** 可靠性高 ⚡
- **节假日跳过**：自动跳过中国节假日 🏖️
- **可自定义签到地点** 📍
- **Telegram 机器人通知** 📲

## 在您的服务器/VPS 上进行设置和配置 🛠️

1. **克隆此仓库**
    ```bash
    git clone -b vps-deploy https://github.com/dongxuecheng/eteams_auto_check.git
    ```

2. **安装所需依赖**
    ```bash
    cd eteams_auto_check
    apt install python3-venv
    apt install python3-pip
    python3 -m venv .venv  
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. **在 `config.yaml` 中配置您的信息**

4. **设置 cron 任务** ⏰
    - 将系统时区设置为上海
    ```bash
    timedatectl set-timezone Asia/Shanghai
    ```

5. **运行 `config_cron` 脚本**
    ```bash
    chmod +x config_cron.sh && ./config_cron.sh /home/eteams_auto_check
    ```

## 使用 📝

脚本将在配置的时间自动运行：
- **早上：** 大约 8:20 AM（8:20 - 8:25）
- **晚上：** 大约 6:10 PM（18:10 - 18:15）

## 致谢 🙏

此项目基于他人的工作：
- [Emo403/eteams_auto](https://github.com/Emo403/eteams_auto)

## 许可证 📄

此项目采用 MIT 许可证。
