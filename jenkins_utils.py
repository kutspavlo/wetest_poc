import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[UDT-Utils] %(message)s')
logger = logging.getLogger(__name__)


class UDTConfig:
    def __init__(self):
        self._data = self._load_and_clean_config()

    def _load_and_clean_config(self):
        """ Load configuration from environment variable path, read JSON, then delete the file """
        config_path = os.environ.get('UDT_CONFIG_PATH')

        if not config_path:
            old_config = os.environ.get('UDT_CONFIG')
            if old_config:
                return json.loads(old_config)
            raise ValueError("Error: 'UDT_CONFIG_PATH' environment variable is missing.")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Error: Config file not found at: {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Config loaded from {config_path}")
        except Exception as e:
            logger.error(f"Failed to parse config file: {e}")
            raise

        # Delete the file immediately after reading
        try:
            os.remove(config_path)
        except Exception:
            pass

        return data

    def get_host(self):
        return self._data.get('host', 'udt.wetest.net')

    def get_remote_executor_url(self):
        host = self.get_host()
        if not host.startswith("http"):
            return f"https://{host}/wd/hub"
        return f"{host}/wd/hub"

    def get_desired_capabilities(self, name):
        """
        Assemble parameters
        """
        target = self._data.get('target', {})
        auth = self._data.get('auth', {})

        # 1. Basic authentication Caps
        caps = {
            "udt:host": self.get_host(),
            "udt:userId": auth.get('userId'),
            "udt:userKey": auth.get('userKey'),
            "udt:projectId": target.get('projectId'),
            "udt:projectToken": target.get('projectToken'),
            "automationName": target.get('automationName'),  # Universal
            # Custom job name
            "udt:jobName": name
        }

        # Handle deviceId
        device_id = target.get('deviceId')
        if device_id:
            caps["udt:deviceId"] = int(device_id) if str(device_id).isdigit() else device_id

        # Handle appId
        app_id = target.get('appId')
        if app_id:
            caps["udt:appId"] = int(app_id) if str(app_id).isdigit() else app_id

        # --- 2. Key routing logic ---
        # Java plugin passes three platform types: Android, iOS
        config_platform = target.get('platform', '')
        # For each platform, the Java plugin will pass a modeType field, indicating whether it's native or web
        mode_type = target.get('modeType', 'native')

        if config_platform == 'WEB':
            # === Web mode processing ===
            # In Web mode, Appium's platformName must be 'Android' or 'iOS' (from Java's platformName field)
            real_platform = target.get('platformName')  # Corresponds to Java: builder.getWebPlatformName()
            caps["platformName"] = real_platform

            # Browser configuration
            caps["browserName"] = target.get('browserName')  # Chrome or Safari

            # iOS Web special handling
            if real_platform and real_platform.lower() == 'ios':
                caps["udid"] = target.get('udid')
                caps["webDriverAgentUrl"] = "UdtWebDriverAgentUrl"  # Fixed placeholder
                # caps["udt:needResign"] = False # Web testing usually doesn't require resigning

        caps["platformName"] = config_platform

        if config_platform.lower() == 'android':
            if mode_type == 'native':
                if target.get('appPackage'):
                    caps["appPackage"] = target.get('appPackage')
                if target.get('appActivity'):
                    caps["appActivity"] = target.get('appActivity')
            else:
                # Browser configuration
                caps["browserName"] = target.get('browserName')  # Chrome or Safari

        elif config_platform.lower() == 'ios':
            if mode_type == 'native':
                if target.get('udid'):
                    caps["udid"] = target.get('udid')
                if target.get('bundleId'):
                    caps["bundleId"] = target.get('bundleId')
                if target.get('wdaUrl'):
                    caps["webDriverAgentUrl"] = target.get('wdaUrl')
                if 'needResign' in target:  # Resign parameter
                    caps["udt:needResign"] = target.get('needResign')
            else:
                # Browser configuration
                caps["browserName"] = target.get('browserName')  # Chrome or Safari
                caps["udid"] = target.get('udid')
                caps["webDriverAgentUrl"] = "UdtWebDriverAgentUrl"  # Fixed placeholder
                # caps["udt:needResign"] = False # Web testing usually doesn't require resigning
        return caps
