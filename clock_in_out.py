import requests
from typing import Dict
import logging
import yaml
import os
from dataclasses import dataclass

@dataclass
class SessionInfo:
    jsessionid: str = ""
    tenantkey: str = ""
    uid: str = ""
    eteamsid: str = ""
    signature: str = ""
    timecard_status: str = ""
    message: str = ""

class ClockInSystem:
    def __init__(self):
        self.config = self._load_config()
        self.session = SessionInfo()
        self._configure_logging()

    def _load_config(self) -> Dict:
        """Load configuration from yaml file."""
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _configure_logging(self) -> None:
        """Configure logging settings."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def push_notification(self) -> None:
        """Push notification via Telegram."""
        if not self.session.message:
            return

        telegram_api = f"https://api.telegram.org/bot{self.config['telegram']['bot_token']}/sendMessage"
        params = {
            "chat_id": self.config['telegram']['chat_id'],
            "text": self.session.message,
        }
        
        try:
            response = requests.get(telegram_api, params=params)
            response.raise_for_status()
            logging.info("Telegram notification sent successfully✅")
        except requests.RequestException as e:
            logging.error(f"Failed to send Telegram notification: {e}")

    def login(self) -> None:
        """Login to the system."""
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) weapp/4.3.9/public//1.0/",
        }
        params = {
            "username": self.config['credentials']['username'],
            "password": self.config['credentials']['password'],
            "loginTyp": "app_account",
            "imei": "F1A480AB-1A98-44D2-8200-91220A4529F4",
            "version": "15.1.1",
            "secondImei": "",
            "adviceInfo": "iPhone",
        }

        try:
            response = requests.post(self.config['urls']['login'], headers=headers, params=params)
            response.raise_for_status()
            self._process_login_response(response.json())
            logging.info("Login successful✅")
        except requests.RequestException as e:
            logging.error(f"Login failed: {e}")
            raise

    def _process_login_response(self, result: Dict) -> None:
        """Process login response and update session info."""
        self.session.jsessionid = result.get("jsessionid", "")
        self.session.tenantkey = result.get("tenantkey", "")
        self.session.uid = result.get("uid", "")
        self.session.eteamsid = result.get("ETEAMSID", "")

    def get_signature(self) -> None:
        """Get signature for attendance."""
        headers = {
            "Cookie": f"ETEAMSID={self.session.eteamsid}",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) weapp/4.3.9/public//1.0/",
        }
        params = {
            "clientVersion": "4.0.216",
            "clientTag": "public",
            "clientPackage": "com.weaver.teams",
            "devType": "1"
        }

        try:
            response = requests.get(self.config['urls']['signature'], headers=headers, params=params)
            response.raise_for_status()
            self.session.signature = response.json().get("data", {}).get("signature", "")
            logging.info("Signature obtained successfully✅")
        except requests.RequestException as e:
            logging.error(f"Failed to get signature: {e}")
            raise

    def check_attendance(self) -> None:
        """Check attendance status."""
        headers = self._get_auth_headers()
        try:
            response = requests.get(self.config['urls']['check'], headers=headers)
            response.raise_for_status()
            self.session.timecard_status = response.json().get("data", {}).get("signStatus", "")
            logging.info(f"Attendance status: {self.session.timecard_status}")
        except requests.RequestException as e:
            logging.error(f"Failed to check attendance status: {e}")
            raise

    def clock_in_out(self) -> None:
        """Perform attendance check-in or check-out."""
        headers = self._get_auth_headers()
        payload = {
            "checkAddress": self.config['location']['check_address'],
            "latitude": self.config['location']['latitude'],
            "longitude": self.config['location']['longitude'],
            "type": self.session.timecard_status,
            "sign": self.session.signature,
            "userId": self.session.uid,
        }
        params = self._get_device_params()

        try:
            response = requests.post(self.config['urls']['attend'], headers=headers, json=payload, params=params)
            response.raise_for_status()
            self._process_attendance_response(response.json())
        except requests.RequestException as e:
            logging.error(f"Clock in/out failed: {e}")
            raise

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        return {
            "Cookie": f"ETEAMSID={self.session.eteamsid}; JSESSIONID={self.session.jsessionid}",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) weapp/4.3.9/public//1.0/",
        }

    def _get_device_params(self) -> Dict[str, str]:
        """Get device parameters."""
        return {
            "device": "Mobile",
            "engine": "WebKit",
            "browser": "Weapp",
            "os": "iOS",
            "osVersion": "15.1.1",
            "version": "4.3.9",
            "language": "zh_CN",
        }

    def _process_attendance_response(self, result: Dict) -> None:
        """Process attendance response and update message."""
        if result.get("status", False):
            action = "Clock in" if self.session.timecard_status == "CHECKIN" else "Clock out"
            self.session.message = f"{action} successful! ✅"
            logging.info(self.session.message)
        else:
            self.session.message = "Attendance operation failed!"
            logging.error(self.session.message)

    def execute(self) -> None:
        """Execute the clock in/out process."""
        try:
            self.login()
            self.get_signature()
            self.check_attendance()
            self.clock_in_out()
            self.push_notification()
        except Exception as e:
            logging.error(f"Process failed: {e}")
            raise

def main():
    """Main entry point."""
    try:
        clock_system = ClockInSystem()
        clock_system.execute()
    except Exception as e:
        logging.error(f"System error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
