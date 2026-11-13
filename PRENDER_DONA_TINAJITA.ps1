cd "C:\Users\Ana Madeline\Desktop\DonaTinajitaIA"
python .\HAIOS_Gateway_Revocacion_Simulacro.py
uvicorn app.main:app --reload --port 8000
