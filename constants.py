import os
from dotenv import load_dotenv

APP_ROOT = os.path.dirname(__file__)
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path, override=True)

# launch mod (실계좌: REAL, 모의: DEMO)
MOD = os.getenv('MOD', 'DEMO')

LOGIN_ID = os.getenv(MOD + '_ID')
PASSWORD = os.getenv(MOD + '_PASS')

# option code
OPTION_EXPIRATION_YEAR_CODE = {
    2021: 'R',
    2022: 'S',
    2023: 'T',
    2024: 'V',
    2025: 'W',
    2026: 6,
    2027: 7,
    2028: 8,
    2029: 9,
    2030: 0,
    2031: 1,
    2032: 2,
    2033: 3,
    2034: 4,
    2035: 5
}
