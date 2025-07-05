from autosurfer.logger import logger
from playwright.sync_api import Page
import time
from typing import Optional
from dataclasses import dataclass


@dataclass
class CaptchaInfo:
    type: str  # 'recaptcha', 'hcaptcha', 'image', 'text', 'checkbox'
    confidence: float
    selectors: list


class CaptchaHandler:
    def __init__(self, page: Page):
        self.page = page

        # Common captcha selectors for detection only
        self.captcha_selectors = {
            'recaptcha': [
                'iframe[src*="recaptcha"]',
                '.g-recaptcha',
                '#recaptcha',
                '[data-sitekey]',
                'iframe[title*="recaptcha"]'
            ],
            'hcaptcha': [
                'iframe[src*="hcaptcha"]',
                '.h-captcha',
                '#hcaptcha',
                'iframe[title*="hCaptcha"]'
            ],
            'image_captcha': [
                'img[src*="captcha"]',
                '.captcha-image',
                '#captcha-image',
                'img[alt*="captcha"]'
            ],
            'text_captcha': [
                'input[name*="captcha"]',
                '.captcha-input',
                '#captcha-input',
                'input[placeholder*="captcha"]'
            ],
            'checkbox_captcha': [
                'input[type="checkbox"][name*="captcha"]',
                '.captcha-checkbox',
                '#captcha-checkbox'
            ]
        }

    def detect_captcha(self) -> Optional[CaptchaInfo]:
        """Detect if there's a captcha on the current page"""
        logger.info("Scanning for captcha elements...")

        # Check for various captcha types
        for captcha_type, selectors in self.captcha_selectors.items():
            for selector in selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    if elements:
                        logger.info(
                            f"Detected {captcha_type} captcha with selector: {selector}")
                        return CaptchaInfo(
                            type=captcha_type,
                            confidence=0.9,
                            selectors=[selector]
                        )
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue

        # Check for captcha-related text in page content
        page_text = self.page.content().lower()
        captcha_indicators = [
            'captcha', 'recaptcha', 'hcaptcha', 'verify you are human',
            'prove you are not a robot', 'security check', 'verification'
        ]

        for indicator in captcha_indicators:
            if indicator in page_text:
                logger.info(f"Detected captcha indicator: {indicator}")
                return CaptchaInfo(
                    type='unknown',
                    confidence=0.7,
                    selectors=[],
                )

        return None

    def handle_captcha_detection(self) -> bool:
        """Handle captcha detection - just detect and exit"""
        captcha_info = self.detect_captcha()

        if captcha_info:
            logger.error(f"🔒 CAPTCHA DETECTED: {captcha_info.type}")
            logger.error("Task cannot continue due to captcha presence.")
            logger.error(
                "Future implementation will stream screen to user for manual solving.")
            return False

        return True
