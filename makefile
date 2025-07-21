tree:
	tree -I "__pycache__/*|.venv"

dev:
	python runner.py

env:
	@echo "source .venv/bin/activate"
	@echo "source .env"

test-browsers:
	python -m examples.test_launch_browsers

test-memory:
	python -m examples.test_agent_memory enabled

test-agents:
	python -m examples.test_browser_agents

test-captcha:
	python -m examples.test_captcha_detection 

test-scroll:
	python -m examples.test_scroll_action

test-loop-detection:
	python -m examples.test_loop_detection 