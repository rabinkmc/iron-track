# iron-track/Makefile

.PHONY: build clean deploy

REMOTE_ALIAS=iron
REMOTE_PATH=/home/ubuntu/iron-track/

deploy: build
	scp dist.zip $(REMOTE_ALIAS):$(REMOTE_PATH)
	ssh $(REMOTE_ALIAS) "cd $(REMOTE_PATH) && unzip -o dist.zip && rm dist.zip"

build:
	# VITE_API_URL="https://iron.rabindhamala.com.np/api"
	sed -i 's|VITE_API_URL=.*|VITE_API_URL="https://iron.rabindhamala.com.np/api"|' .env
	npm run build
	sed -i /preload/d dist/index.html
	zip -r dist.zip dist/
	
dev:
	# VITE_API_URL="http://localhost:8000/api"
	# VITE_API_URL="https://iron.rabindhamala.com.np/api"
	sed -i 's|VITE_API_URL=.*|VITE_API_URL="http://localhost:8000/api"|' .env
	npm run dev

	

# Clean frontend build (if using dist/)
clean:
	rm -rf dist
	rm -rf dist.zip
