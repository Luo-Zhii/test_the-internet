# Tạo thư mục venv ngay trong source
python -m venv venv

# Kích hoạt môi trường ảo cho zsh
source venv/bin/activate

pip install -r requirements.txt

# Run 1 
python3 [file]

# Run sync 
pytest tests/ -n auto --html=report.html --self-contained-html

# Run async 
python3 run_fast.py