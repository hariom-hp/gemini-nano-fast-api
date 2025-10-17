# Makefile for managing both Python FastAPI and Go Gin APIs

.PHONY: help python-install python-run go-install go-build go-run go-clean test-health test-single test-multiple clean all

help:
	@echo "Available commands:"
	@echo ""
	@echo "Python FastAPI:"
	@echo "  make python-install    - Install Python dependencies"
	@echo "  make python-run        - Run Python FastAPI server"
	@echo ""
	@echo "Go Gin:"
	@echo "  make go-install        - Install Go dependencies"
	@echo "  make go-build          - Build Go binary"
	@echo "  make go-run            - Run Go Gin server"
	@echo "  make go-clean          - Clean Go build artifacts"
	@echo ""
	@echo "Testing:"
	@echo "  make test-health       - Test health endpoint"
	@echo "  make test-single       - Test single image endpoint (requires test.jpg)"
	@echo "  make test-multiple     - Test multiple images endpoint (requires test1.jpg, test2.jpg)"
	@echo ""
	@echo "Other:"
	@echo "  make clean             - Clean all build artifacts"
	@echo "  make all               - Install and build everything"

# Python FastAPI commands
python-install:
	@echo "Installing Python dependencies..."
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Python dependencies installed"

python-run:
	@echo "Starting Python FastAPI server..."
	. venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Go Gin commands
go-install:
	@echo "Installing Go dependencies..."
	cd go_api && go mod download
	@echo "✅ Go dependencies installed"

go-build:
	@echo "Building Go application..."
	cd go_api && go build -o server main.go
	@echo "✅ Go binary built: go_api/server"

go-run: go-build
	@echo "Starting Go Gin server..."
	cd go_api && ./server

go-clean:
	@echo "Cleaning Go build artifacts..."
	rm -f go_api/server
	@echo "✅ Cleaned"

# Testing commands
test-health:
	@echo "Testing health endpoint..."
	@curl -s http://localhost:8000/health | jq '.'

test-single:
	@echo "Testing single image endpoint..."
	@if [ ! -f test.jpg ]; then \
		echo "❌ Error: test.jpg not found"; \
		exit 1; \
	fi
	@curl -X POST "http://localhost:8000/edit-image" \
		-F "file=@test.jpg" \
		-F "prompt=Make it colorful" \
		--output result_single.png
	@echo "✅ Result saved to result_single.png"

test-multiple:
	@echo "Testing multiple images endpoint..."
	@if [ ! -f test1.jpg ] || [ ! -f test2.jpg ]; then \
		echo "❌ Error: test1.jpg or test2.jpg not found"; \
		exit 1; \
	fi
	@curl -X POST "http://localhost:8000/edit-multiple-images" \
		-F "files=@test1.jpg" \
		-F "files=@test2.jpg" \
		-F "prompt=Combine these images" \
		--output result_multiple.png
	@echo "✅ Result saved to result_multiple.png"

# Cleanup
clean: go-clean
	@echo "Cleaning all build artifacts..."
	rm -rf __pycache__
	rm -f result_*.png
	@echo "✅ All cleaned"

# Install everything
all: python-install go-install go-build
	@echo "✅ Everything installed and built!"
	@echo ""
	@echo "To run Python FastAPI: make python-run"
	@echo "To run Go Gin:         make go-run"
