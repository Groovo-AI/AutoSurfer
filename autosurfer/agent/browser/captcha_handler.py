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
        # Cache for recent captcha checks
        self._last_checked_url: str = ""
        self._last_checked_result: Optional[CaptchaInfo] = None
        # Note: we no longer use a time-based cache; we only re-scan when the URL changes.

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
        """Return False if captcha found; otherwise True. Skip repeated scans on same URL within 10 s."""
        current_url = self.page.url

        # Skip if we've already scanned this URL in the current session
        if current_url == self._last_checked_url:
            logger.debug(
                "Skipping captcha scan: URL unchanged since last check")
            return self._last_checked_result is None

        # URL changed → perform a fresh scan and update cache metadata
        self._last_checked_url = current_url

        captcha_info = self.detect_captcha()
        self._last_checked_result = captcha_info

        if captcha_info:
            logger.error(f"🔒 CAPTCHA DETECTED: {captcha_info.type}")
            logger.error("Task cannot continue due to captcha presence.")
            logger.error(
                "Future implementation will stream screen to user for manual solving.")
            return False

        return True

    def invalidate_cache(self):
        """Clear the cached URL so the next call will perform a fresh scan."""
        self._last_checked_url = ""
