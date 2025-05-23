#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Modified from : https://github.com/geekan/MetaGPT/blob/main/metagpt/config.py
"""
import os
import openai

import yaml

from .const import PROJECT_ROOT
from .logs import logger
from .utils.singleton import Singleton
from .tools import SearchEngineType, WebBrowserEngineType


class NotConfiguredException(Exception):
    """Exception raised for errors in the configuration.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="The required configuration is not set"):
        self.message = message
        super().__init__(self.message)


class Config(metaclass=Singleton):
    """
    常规使用方法：
    config = Config("config.yaml")
    secret_key = config.get_key("MY_SECRET_KEY")
    print("Secret key:", secret_key)
    """

    _instance = None
    key_yaml_file = PROJECT_ROOT / "config/config.yaml"
    default_yaml_file = PROJECT_ROOT / "config/config.yaml"

    def __init__(self, yaml_file=default_yaml_file):
        self._configs = {}
        self._init_with_config_files_and_env(self._configs, yaml_file)
        logger.info("Config loading done.")
        self.global_proxy = self._get("GLOBAL_PROXY")
        self.openai_api_key = self._get("OPENAI_API_KEY")
        # if not self.openai_api_key or "YOUR_API_KEY" == self.openai_api_key:
        #     raise NotConfiguredException("Set OPENAI_API_KEY first")

        self.openai_api_base = self._get("OPENAI_API_BASE")
        self.openai_proxy = self._get("OPENAI_PROXY")
        # if not self.openai_api_base or "YOUR_API_BASE" == self.openai_api_base:
        #     openai_proxy = self._get("OPENAI_PROXY") or self.global_proxy
        #     if openai_proxy:
        #         openai.proxy = openai_proxy
        #     else:
        #         logger.info("Set OPENAI_API_BASE in case of network issues")
        self.openai_api_type = self._get("OPENAI_API_TYPE")
        self.openai_api_version = self._get("OPENAI_API_VERSION")
        self.openai_api_rpm = self._get("RPM", 3)
        self.openai_api_model = self._get("OPENAI_API_MODEL", "gpt-4")
        self.max_tokens_rsp = self._get("MAX_TOKENS", 2048)
        self.deployment_id = self._get("DEPLOYMENT_ID")

        self.claude_api_key = self._get('Anthropic_API_KEY')
        self.serpapi_api_key = self._get("SERPAPI_API_KEY")
        self.serper_api_key = self._get("SERPER_API_KEY")
        self.google_api_key = self._get("GOOGLE_API_KEY")
        self.google_cse_id = self._get("GOOGLE_CSE_ID")
        self.search_engine = self._get("SEARCH_ENGINE", SearchEngineType.SERPAPI_GOOGLE)

        self.web_browser_engine = WebBrowserEngineType(self._get("WEB_BROWSER_ENGINE", "playwright"))
        self.playwright_browser_type = self._get("PLAYWRIGHT_BROWSER_TYPE", "chromium")
        self.selenium_browser_type = self._get("SELENIUM_BROWSER_TYPE", "chrome")

        self.long_term_memory = self._get('LONG_TERM_MEMORY', False)
        if self.long_term_memory:
            logger.warning("LONG_TERM_MEMORY is True")
        self.max_budget = self._get("MAX_BUDGET", 10.0)
        self.total_cost = 0.0

    def _init_with_config_files_and_env(self, configs: dict, yaml_file):
        """从config/config.yaml / config/config.yaml / env三处按优先级递减加载"""
        configs.update(os.environ)

        for _yaml_file in [yaml_file, self.key_yaml_file]:
            if not _yaml_file.exists():
                continue

            # 加载本地 YAML 文件
            with open(_yaml_file, "r", encoding="utf-8") as file:
                yaml_data = yaml.safe_load(file)
                if not yaml_data:
                    continue
                os.environ.update({k: v for k, v in yaml_data.items() if isinstance(v, str)})
                configs.update(yaml_data)

    def _get(self, *args, **kwargs):
        return self._configs.get(*args, **kwargs)

    def get(self, key, *args, **kwargs):
        """从config/config.yaml / config/config.yaml / env三处找值，找不到报错"""
        value = self._get(key, *args, **kwargs)
        if value is None:
            raise ValueError(f"Key '{key}' not found in environment variables or in the YAML file")
        return value


CONFIG = Config()
