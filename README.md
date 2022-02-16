# wallart_backend_v1

python3 -m venv wallart-env
source wallart-env/bin/activate
pip3 install fastapi 
pip3 install uvicorn
uvicorn main:app --reload
pip3 install -r requirements.txt