start-dev:
	uvicorn taskon_main:app --host 0.0.0.0 --port 4034 --workers 1


start:
	nohup uvicorn taskon_main:app --host 0.0.0.0 --port 4034 --workers 1 >> taskon.log  2>&1 &
