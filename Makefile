
build:
	docker build --build-arg GH_TOKEN=${GH_TOKEN} --build-arg CARGO_REGISTRIES_LHAVA_DEV_TOKEN=${TOKEN} -t webhooks-server:latest .
