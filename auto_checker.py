import datetime
import pytz
import chinese_calendar
import requests
import logging
import yaml
import os
import random
import time
from dataclasses import dataclass
from clock_in_out import ClockInSystem

@dataclass
class HolidayStatus:
    """Store holiday check results"""
    date: datetime.date
    is_holiday: bool
    holiday_name: str

class HolidayChecker:
    """Check holiday status and manage clock-in process"""
    
    def __init__(self):
        self.config = self._load_config()
        self.telegram_api = f"https://api.telegram.org/bot{self.config['telegram']['bot_token']}/sendMessage"
        self.chat_id = self.config['telegram']['chat_id']
        self._configure_logging()

    def _load_config(self) -> dict:
        """Load configuration from yaml file"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            raise

    def _configure_logging(self) -> None:
        """Configure logging settings"""
        if not os.path.exists('logs'):
            os.makedirs('logs')

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/auto_checker.log'),
                logging.StreamHandler()
            ]
        )

    def get_holiday_status(self) -> HolidayStatus:
        """Check if current day is a holiday in China"""
        cn_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        is_holiday, holiday_name = chinese_calendar.get_holiday_detail(cn_time.date())
        
        return HolidayStatus(
            date=cn_time.date(),
            is_holiday=is_holiday,
            holiday_name=holiday_name or "Working day"
        )

    def send_notification(self, message: str) -> None:
        """Send notification via Telegram"""
        try:
            response = requests.post(
                self.telegram_api,
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to send Telegram notification: {e}")

    def process_attendance(self) -> None:
        """Check holiday status and process attendance if needed"""
        status = self.get_holiday_status()
        
        if status.is_holiday:
            message = (
                f"📅 Date: {status.date}\n"
                f"🏖 Holiday: {status.holiday_name}\n"
                "✨ No attendance needed today!"
            )
            logging.info(f"Holiday detected: {status.holiday_name}")
        else:
            try:
                delay = random.randint(0, 300)  # 0-300s random delay
                time.sleep(delay)

                now = datetime.datetime.now()
                logging.info(f"[{now}] Starting attendance, delayed by {delay} seconds...")

                clock_system = ClockInSystem()
                clock_system.execute()
                message = (
                    f"📅 Date: {status.date}\n"
                    "💼 Working day\n"
                    "✅ Attendance processed successfully!"
                )
                logging.info("Attendance processed successfully✅")
            except Exception as e:
                message = (
                    f"📅 Date: {status.date}\n"
                    "💼 Working day\n"
                    f"❌ Attendance failed: {str(e)}"
                )
                logging.error(f"Attendance processing failed: {e}")
        
        self.send_notification(message)

def main():
    """Main entry point"""
    try:
        checker = HolidayChecker()
        checker.process_attendance()
    except Exception as e:
        logging.error(f"System error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
