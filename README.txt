sudo apt install python3.8 python3.8-venv
cd "путь к папке проекта"
python3.8 -m venv env
pip install -r requirements.txt
. env/bin/activate
python main.py