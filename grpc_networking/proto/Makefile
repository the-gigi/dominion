*.py: *.proto
	poetry run python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. dominion.proto