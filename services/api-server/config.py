"""
RingHealth 鍚庣鏈嶅姟閰嶇疆
"""
import os

# 鍩虹璺緞
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================== 鏈嶅姟鍣?====================
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

# ==================== 鏁版嵁搴?MySQL) ====================
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'ringhealth')

# ==================== JWT璁よ瘉 ====================
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24 * 7  # 7澶?

# ==================== 鎯呯华绠楁硶寮曟搸 ====================
EMOTION_ENGINE_DIR = os.environ.get(
    'EMOTION_ENGINE_DIR',
    os.path.join(BASE_DIR, '..', 'ringhealth-emotion-main') if os.path.exists(os.path.join(BASE_DIR, '..', 'ringhealth-emotion-main')) 
    else os.path.join(BASE_DIR, 'emotion_engine')
)

EMOTION_MODEL_PATH = os.path.join(EMOTION_ENGINE_DIR, 'models', 'emotion_model.pkl')
EMOTION_SCALER_PATH = os.path.join(EMOTION_ENGINE_DIR, 'models', 'scaler.pkl')
EMOTION_BASELINE_PATH = os.path.join(EMOTION_ENGINE_DIR, 'data', 'user_baselines.json')

# ==================== CORS ====================
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

# ==================== 鏃ュ織 ====================
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')

