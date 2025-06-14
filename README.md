
cd /home
source myenv/bin/activate

pip install requests
pip install Faker
pip install names

cd scam-form-filler
nohup python3 cyrpto_scam.py > output.log 2>&1 &
