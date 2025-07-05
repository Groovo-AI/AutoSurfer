tree:
	tree -I "__pycache__/*|.venv"
dev:
	python runner.py
env:
	@echo "source .env"
	@cat .env
