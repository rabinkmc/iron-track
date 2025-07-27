# iron-track/Makefile

.PHONY: build clean deploy

REMOTE_ALIAS=iron
REMOTE_PATH=/home/ubuntu/iron-track/

deploy: build
	scp dist.zip $(REMOTE_ALIAS):$(REMOTE_PATH)

build:
	npm run build
	sed -i /preload/d dist/index.html
	zip -r dist.zip dist/
	

# Clean frontend build (if using dist/)
clean:
	rm -rf dist
	[[-f dist.zip]] && rm dist.zip
