tree:
	tree -I "__pycache__/*|.venv"

dev:
	uv run python runner.py

env:
	@echo "source .venv/bin/activate"
	@echo "source .env"

test-browsers:
	uv run python -m examples.test_launch_browsers

test-memory:
	uv run python -m examples.test_agent_memory enabled

test-agents:
	uv run python -m examples.test_browser_agents

test-captcha:
	uv run python -m examples.test_captcha_detection 