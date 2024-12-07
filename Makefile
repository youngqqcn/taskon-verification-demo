start-dev:
	uvicorn taskon_main:app --host 0.0.0.0 --port 4034 --workers 1


start:
	nohup uvicorn taskon_main:app --host 0.0.0.0 --port 4034 --workers 1 >> taskon.log  2>&1 &


stop:
	ps aux | grep taskon_main | grep -v grep | awk '{print $$2}' | xargs kill