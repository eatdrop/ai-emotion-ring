"""
RingHealth 鍚庣API鏈嶅姟
鍩轰簬Flask鐨凴ESTful API - 闆嗘垚鎯呯华绠楁硶寮曟搸
"""

import os
import sys
import json
import time
import logging
from datetime import datetime, timedelta

# 纭繚椤圭洰璺緞鍙闂?
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, g
from flask_cors import CORS
import jwt

from config import (
    HOST, PORT, DEBUG,
    JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS,
    EMOTION_ENGINE_DIR, CORS_ORIGINS, LOG_LEVEL, LOG_FILE
)

# ==================== 鏃ュ織閰嶇疆 ====================
os.makedirs(os.path.join(os.path.dirname(LOG_FILE)), exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ringhealth')

# ==================== Flask搴旂敤鍒濆鍖?====================
app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS if CORS_ORIGINS != '*' else None)
if CORS_ORIGINS == '*':
    # 鍏佽鎵€鏈夋潵婧愶紙寮€鍙戠幆澧冿級
    from flask_cors import cross_origin
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-Requested-With'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        return response

# ==================== 鏁版嵁瀛樺偍(鏀寔MySQL鍜孞SON鍙屾ā寮? ====================
STORAGE_MODE = os.environ.get('STORAGE', 'json')  # json 鎴?mysql
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# JSON鏂囦欢璺緞
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
DEVICES_FILE = os.path.join(DATA_DIR, 'devices.json')
BIOMETRIC_FILE = os.path.join(DATA_DIR, 'biometric_raw_data.json')
EMOTION_RESULTS_FILE = os.path.join(DATA_DIR, 'emotion_results.json')
USER_PROFILES_FILE = os.path.join(DATA_DIR, 'user_profiles.json')

def _load_json(path, default=None):
    """瀹夊叏鍔犺浇JSON鏂囦欢"""
    if default is None:
        default = [] if not path.endswith('.json') else {}
    if not os.path.exists(path):
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f'鍔犺浇JSON澶辫触 {path}: {e}')
        return default

def _save_json(path, data):
    """瀹夊叏鍐欏叆JSON鏂囦欢"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    except IOError as e:
        logger.error(f'鍐欏叆JSON澶辫触 {path}: {e}')
        raise

def _generate_id(prefix=''):
    """鐢熸垚鍞竴ID"""
    return prefix + str(int(time.time() * 1000))[-8:]

# ==================== 鎯呯华绠楁硶寮曟搸鍔犺浇 ====================
emotion_model = None
scaler = None
user_baselines = {}
user_profiles = {}

def load_emotion_engine():
    """鍔犺浇鎯呯华璇嗗埆妯″瀷鍜岃祫婧?""
    global emotion_model, scaler, user_baselines, user_profiles
    
    engine_dir = EMOTION_ENGINE_DIR
    
    # 灏濊瘯浠巖inghealth-emotion-main鐩綍鍔犺浇
    possible_dirs = [
        engine_dir,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ringhealth-emotion-main'),
        r'e:\ringhealth-emotion-main'
    ]
    
    for d in possible_dirs:
        model_path = os.path.join(d, 'models', 'emotion_model.pkl')
        scaler_path = os.path.join(d, 'models', 'scaler.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                import pickle
                with open(model_path, 'rb') as f:
                    emotion_model = pickle.load(f)
                with open(scaler_path, 'rb') as f:
                    scaler = pickle.load(f)
                
                logger.info(f'鎯呯华妯″瀷宸插姞杞? {d}')
                
                baseline_path = os.path.join(d, 'data', 'user_baselines.json')
                if os.path.exists(baseline_path):
                    with open(baseline_path, 'r', encoding='utf-8') as f:
                        user_baselines = json.load(f)
                
                profile_path = os.path.join(d, 'data', 'user_profiles.json')
                if os.path.exists(profile_path):
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        user_profiles = json.load(f)
                        
                break
            except Exception as e:
                logger.warning(f'灏濊瘯浠巤d}鍔犺浇妯″瀷澶辫触: {e}')
    
    if emotion_model is None:
        logger.warning('鏈壘鍒版儏缁ā鍨嬶紝棰勬祴鍔熻兘灏嗕笉鍙敤')


# ==================== JWT璁よ瘉瑁呴グ鍣?====================
def token_required(f):
    """JWT Token楠岃瘉涓棿浠?""
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': '缂哄皯璁よ瘉Token'}), 401
        
        token = auth_header[7:]
        
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            g.user_id = payload.get('user_id')
            g.user_info = payload
            
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'Token宸茶繃鏈燂紝璇烽噸鏂扮櫥褰?}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': '鏃犳晥鐨凾oken'}), 401
        
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated


# ==================== API璺敱 ====================

@app.route('/health', methods=['GET'])
def health_check():
    """鍋ュ悍妫€鏌?""
    return jsonify({
        'status': 'ok',
        'service': 'RingHealth API Server v1.0.0',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': emotion_model is not None,
        'storage_mode': STORAGE_MODE
    })


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
# 璁よ瘉妯″潡 /api/v1/auth/
# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """鐢ㄦ埛鐧诲綍"""
    data = request.get_json()
    
    phone = (data or {}).get('phone', '').strip()
    password = (data or {}).get('password', '')
    
    if not phone or len(phone) < 11:
        return jsonify({'success': False, 'error': '璇疯緭鍏ユ纭殑鎵嬫満鍙?}), 400
    
    users = _load_json(USERS_FILE, {})
    
    user = None
    for uid, u in users.items():
        if u.get('phone') == phone:
            user = u
            break
    
    if not user:
        return jsonify({'success': False, 'error': '璇ユ墜鏈哄彿鏈敞鍐?}), 404
    
    # 瀵嗙爜楠岃瘉锛堢敓浜х幆澧冨簲浣跨敤bcrypt绛夊姞瀵嗭級
    if user.get('password') != password:
        return jsonify({'success': False, 'error': '瀵嗙爜閿欒'}), 401
    
    # 鐢熸垚JWT Token
    token_payload = {
        'user_id': uid,
        'phone': phone,
        'nickname': user.get('nickname'),
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    return jsonify({
        'success': True,
        'token': token,
        'data': {
            'user_id': uid,
            'nickname': user.get('nickname'),
            'phone': phone,
            'gender': user.get('gender'),
            'age': user.get('age'),
            'weight_kg': user.get('weight_kg'),
            'created_at': user.get('created_at')
        }
    })


@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    """鐢ㄦ埛娉ㄥ唽"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': '缂哄皯璇锋眰浣?}), 400
    
    phone = data.get('phone', '').strip()
    password = data.get('password', '').strip()
    confirm_password = (data.get('confirmPassword') or data.get('confirm_password') or '').strip()
    
    # 楠岃瘉
    errors = []
    if len(phone) != 11 or not phone.isdigit():
        errors.append('鎵嬫満鍙锋牸寮忎笉姝ｇ‘')
    if len(password) < 6:
        errors.append('瀵嗙爜鑷冲皯6浣?)
    # 濡傛灉鍓嶇鍙戜簡纭瀵嗙爜鎵嶆牎楠岋紝鍚﹀垯璺宠繃锛堝墠绔凡鍋氳繃楠岃瘉锛?
    if confirm_password and password != confirm_password:
        errors.append('涓ゆ瀵嗙爜涓嶄竴鑷?)
    
    if errors:
        return jsonify({'success': False, 'error': '; '.join(errors)}), 400
    
    users = _load_json(USERS_FILE, {})
    
    # 妫€鏌ユ槸鍚﹀凡娉ㄥ唽
    for uid, u in users.items():
        if u.get('phone') == phone:
            return jsonify({'success': False, 'error': '璇ユ墜鏈哄彿宸叉敞鍐?}), 409
    
    # 鍒涘缓鐢ㄦ埛
    user_id = _generate_id('U')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    user_data = {
        'user_id': user_id,
        'phone': phone,
        'password': password,  # 鐢熶骇鐜搴攈ash
        'nickname': data.get('nickname', f'鐢ㄦ埛{phone[-4:]}'),
        'gender': data.get('gender', 1),
        'age': int(data['age']) if data.get('age') else None,
        'weight_kg': float(data['weight_kg']) if data.get('weight_kg') else None,
        'height_cm': float(data.get('height_cm')) if data.get('height_cm') else None,
        'created_at': now,
        'updated_at': now
    }
    
    users[user_id] = user_data
    _save_json(USERS_FILE, users)
    
    # 鍚屾椂鍒涘缓鐢诲儚璁板綍
    profiles = _load_json(USER_PROFILES_FILE, {})
    profiles[user_id] = {
        'user_id': user_id,
        'phone': phone,
        'gender': user_data['gender'],
        'age': user_data['age'],
        'weight_kg': user_data['weight_kg'],
        'height_cm': user_data.get('height_cm'),
        'created_at': now
    }
    _save_json(USER_PROFILES_FILE, profiles)
    
    # 鍚屾鍒板唴瀛樹腑鐨勭敤鎴风敾鍍忥紙渚涙儏缁畻娉曚娇鐢級
    global user_profiles
    user_profiles[user_id] = {
        'gender': user_data.get('gender', 1),
        'age': user_data.get('age', 22),
        'weight_kg': user_data.get('weight_kg', 65)
    }
    
    # 鑷姩鐧诲綍杩斿洖Token
    token_payload = {
        'user_id': user_id,
        'phone': phone,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    return jsonify({
        'success': True,
        'token': token,
        'data': {
            'user_id': user_id,
            'nickname': user_data['nickname']
        },
        'message': '娉ㄥ唽鎴愬姛'
    })


@app.route('/api/v1/auth/verify', methods=['GET'])
@token_required
def verify_token():
    """楠岃瘉Token鏈夋晥鎬?""
    return jsonify({
        'success': True,
        'data': {'user_id': g.user_id, 'valid': True}
    })


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
# 鐢ㄦ埛绠＄悊 /api/v1/user/
# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@app.route('/api/v1/user/me', methods=['GET'])
@token_required
def get_current_user():
    """鑾峰彇褰撳墠鐢ㄦ埛淇℃伅"""
    users = _load_json(USERS_FILE, {})
    user = users.get(g.user_id)
    
    if not user:
        return jsonify({'success': False, 'error': '鐢ㄦ埛涓嶅瓨鍦?}), 404
    
    # 杩斿洖鏁忔劅瀛楁鑴辨晱鐨勬暟鎹?
    safe_user = {k: v for k, v in user.items() if k != 'password'}
    return jsonify({
        'success': True,
        'data': safe_user
    })


@app.route('/api/v1/user/profile/<user_id>', methods=['PUT'])
@token_required
def update_profile(user_id):
    """鏇存柊鐢ㄦ埛鐢诲儚"""
    if g.user_id != user_id and g.user_info.get('role') != 'admin':
        return jsonify({'success': False, 'error': '鏃犳潈鎿嶄綔'}), 403
    
    data = request.get_json(silent=True) or {}
    
    users = _load_json(USERS_FILE, {})
    if user_id not in users:
        return jsonify({'success': False, 'error': '鐢ㄦ埛涓嶅瓨鍦?}), 404
    
    # 鏇存柊鍏佽鐨勫瓧娈?
    updatable_fields = ['nickname', 'gender', 'age', 'weight_kg', 'height_cm', 'avatar']
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for field in updatable_fields:
        if field in data:
            val = data[field]
            if field == 'gender': 
                val = int(val) if val is not None else None
            elif field == 'age':
                val = int(val) if val else None
            elif field in ('weight_kg', 'height_cm'):
                val = float(val) if val else None
            
            users[user_id][field] = val
    
    users[user_id]['updated_at'] = now
    _save_json(USERS_FILE, users)
    
    # 鍚屾鏇存柊鐢诲儚琛?
    profiles = _load_json(USER_PROFILES_FILE, {})
    if user_id in profiles:
        for field in ['gender', 'age', 'weight_kg', 'height_cm']:
            if field in data:
                profiles[user_id][field] = data[field]
        profiles[user_id]['updated_at'] = now
        _save_json(USER_PROFILES_FILE, profiles)
    
    # 鏇存柊鍐呭瓨涓殑鐢ㄦ埛鐢诲儚
    global user_profiles
    user_profiles[user_id] = {
        'gender': users[user_id].get('gender', 1),
        'age': users[user_id].get('age', 22),
        'weight_kg': users[user_id].get('weight_kg', 65)
    }
    
    return jsonify({
        'success': True,
        'data': users[user_id],
        'message': '鏇存柊鎴愬姛'
    })


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
# 鐢熺墿鐗瑰緛鏁版嵁 /api/v1/biometric
# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@app.route('/api/v1/biometric', methods=['POST'])
@token_required
def upload_biometric():
    """
    涓婁紶鐢熺墿鐗瑰緛鏁版嵁 鈫?娓呮礂 鈫?瀛樺偍 鈫?鎯呯华鍒嗘瀽 鈫?杩斿洖缁撴灉
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '缂哄皯璇锋眰浣?}), 400
    
    # 鏁版嵁娓呮礂
    cleaned, errors = clean_biometric_data(data)
    
    # 鍏抽敭瀛楁楠岃瘉
    critical_errors = [e for e in errors if any(kw in e for kw in ['user_id', 'heart_rate', 'device_id'])]
    
    if critical_errors or not cleaned.get('user_id') or cleaned.get('heart_rate') is None:
        return jsonify({
            'success': False,
            'error': '鍏抽敭鏁版嵁缂哄け鎴栨棤鏁?,
            'cleaning_errors': errors
        }), 400
    
    # 鍐欏叆瀛樺偍
    record_id = _generate_id('R')
    cleaned['id'] = record_id
    cleaned['exec_status'] = '0'
    cleaned['created_at'] = datetime.now().isoformat()
    
    records = _load_json(BIOMETRIC_FILE, [])
    records.append(cleaned)
    _save_json(BIOMETRIC_FILE, records)
    
    # 鎵ц鎯呯华鍒嗘瀽
    result = analyze_emotion_for_record(cleaned)
    
    if result:
        # 瀛樺偍鎯呯华缁撴灉
        emotions = _load_json(EMOTION_RESULTS_FILE, [])
        emotions.append(result)
        _save_json(EMOTION_RESULTS_FILE, emotions)
        
        # 鏍囪宸插垎鏋?
        for r in records:
            if r.get('id') == record_id:
                r['exec_status'] = '1'
        _save_json(BIOMETRIC_FILE, records)
        
        extra = {}
        try:
            extra = json.loads(result.get('extra_result', '{}'))
        except:
            pass
        
        return jsonify({
            'success': True,
            'data': {
                'record_id': record_id,
                'emotion_label': result.get('emotion_label'),
                'emotion_score': result.get('emotion_score'),
                'probabilities': extra.get('probabilities'),
                'analyzed_at': result.get('analyzed_at')
            },
            'warnings': errors if errors else None
        })
    else:
        return jsonify({
            'success': True,
            'data': {
                'record_id': record_id,
                'emotion_label': None,
                'emotion_score': None,
                'note': '妯″瀷鏈姞杞斤紝鏁版嵁宸蹭繚瀛樹絾鏈垎鏋?
            },
            'warnings': ['妯″瀷鏈姞杞斤紝鎯呯华鍒嗘瀽鏆備笉鍙敤'],
            'cleaning_errors': errors
        })


@app.route('/api/v1/latest/<user_id>', methods=['GET'])
@token_required
def get_latest(user_id):
    """鑾峰彇鐢ㄦ埛鏈€鏂版暟鎹拰鎯呯华缁撴灉"""
    records = _load_json(BIOMETRIC_FILE, [])
    results = _load_json(EMOTION_RESULTS_FILE, [])
    
    user_records = [r for r in records if str(r.get('user_id')) == str(user_id)]
    user_records.sort(key=lambda x: x.get('collected_at', ''), reverse=True)
    
    biometric = user_records[0] if user_records else None
    
    user_results = [r for r in results if str(r.get('user_id')) == str(user_id)]
    user_results.sort(key=lambda x: x.get('analyzed_at', ''), reverse=True)
    emotion_result = user_results[0] if user_results else None
    
    if not biometric and not emotion_result:
        return jsonify({
            'success': False,
            'error': f'鏈壘鍒扮敤鎴?{user_id} 鐨勬暟鎹?
        }), 404
    
    return jsonify({
        'success': True,
        'data': {
            'biometric': biometric,
            'emotion_result': emotion_result
        }
    })


@app.route('/api/v1/history/<user_id>', methods=['GET'])
@token_required
def get_history(user_id):
    """鑾峰彇鐢ㄦ埛鍘嗗彶璁板綍"""
    params = request.args
    page = int(params.get('page', 1))
    limit = min(int(params.get('limit', 50)), 200)
    start_date = params.get('start_date')
    end_date = params.get('end_date')
    
    records = _load_json(BIOMETRIC_FILE, [])
    results = _load_json(EMOTION_RESULTS_FILE, [])
    
    # 杩囨护鐢ㄦ埛
    user_records = [
        r for r in records 
        if str(r.get('user_id')) == str(user_id)
    ]
    
    # 鏃ユ湡杩囨护
    if start_date:
        user_records = [r for r in user_records if str(r.get('collected_at', '')) >= start_date]
    if end_date:
        user_records = [r for r in user_records if str(r.get('collected_at', '')) <= end_date + ' 23:59:59']
    
    # 鎺掑簭锛堟渶鏂扮殑鍦ㄥ墠锛?
    user_records.sort(key=lambda x: x.get('collected_at', ''), reverse=True)
    
    # 鍒嗛〉
    total = len(user_records)
    start_idx = (page - 1) * limit
    paged = user_records[start_idx:start_idx + limit]
    
    # 鍚堝苟鎯呯华缁撴灉
    emotion_map = {}
    for er in results:
        if str(er.get('raw_data_id')):
            emotion_map[str(er.get('raw_data_id'))] = er
    
    enriched_data = []
    for r in paged:
        record_copy = dict(r)
        rid = str(r.get('id'))
        if rid in emotion_map:
            er = emotion_map[rid]
            record_copy['emotion_label'] = er.get('emotion_label')
            record_copy['emotion_score'] = er.get('emotion_score')
        enriched_data.append(record_copy)
    
    return jsonify({
        'success': True,
        'data': enriched_data,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit if total > 0 else 0
        }
    })


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
# 鎯呯华棰勬祴鎺ュ彛 /api/v1/predict
# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@app.route('/api/v1/predict', methods=['POST'])
@token_required
def predict_emotion():
    """鍗曟潯鎯呯华棰勬祴锛堣交閲忕骇锛?""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '缂哄皯璇锋眰浣?}), 400
    
    user_id = str(data.get('user_id', ''))
    heart_rate = data.get('heart_rate')
    timestamp = data.get('timestamp')
    
    if not user_id or heart_rate is None:
        return jsonify({'success': False, 'error': '缂哄皯蹇呰鍙傛暟'}), 400
    
    heart_rate = int(heart_rate)
    
    # 鐗瑰緛鎻愬彇 + 棰勬祴
    feature_vector, user_info = extract_features(
        user_id, heart_rate, timestamp,
        data.get('gender'), data.get('age'), data.get('weight_kg')
    )
    
    label, label_name, probabilities, score = run_prediction(feature_vector)
    
    if label is None:
        return jsonify({'success': False, 'error': '妯″瀷鏈姞杞?}), 500
    
    feature_names = [
        'age', 'gender', 'weight_kg', 'heart_rate',
        'hr_baseline_deviation', 'hr_zscore', 'hr_ratio',
        'hour_sin', 'hour_cos', 'is_night', 'hrv_proxy'
    ]
    
    extra = {
        'feature_vector': dict(zip(feature_names, feature_vector)),
        'probabilities': {
            'calm': round(probabilities[0], 4),
            'anxious': round(probabilities[1], 4),
            'excited': round(probabilities[2], 4)
        } if probabilities else {},
        'user_info': user_info
    }
    
    return jsonify({
        'success': True,
        'data': {
            'raw_data_id': None,
            'user_id': user_id,
            'analyzed_at': timestamp or datetime.now().isoformat(),
            'emotion_label': label_name,
            'emotion_score': score,
            'extra_result': json.dumps(extra, ensure_ascii=False)
        }
    })


@app.route('/api/v1/batch_predict', methods=['POST'])
@token_required
def batch_predict():
    """鎵归噺鎯呯华棰勬祴"""
    data = request.get_json()
    records = (data or {}).get('records', [])
    
    if not records:
        return jsonify({'success': False, 'error': '缂哄皯records鍙傛暟'}), 400
    
    results = []
    for rec in records:
        uid = str(rec.get('user_id', ''))
        hr = rec.get('heart_rate')
        ts = rec.get('timestamp')
        
        if not uid or hr is None:
            results.append({'user_id': uid, 'error': '缂哄皯蹇呰瀛楁'})
            continue
        
        feature_vector, user_info = extract_features(uid, int(hr), ts)
        label, label_name, probs, score = run_prediction(feature_vector)
        
        results.append({
            'user_id': uid,
            'heart_rate': hr,
            'emotion_label': label_name,
            'emotion_score': score,
            'probabilities': {
                'calm': round(probs[0], 4) if probs else None,
                'anxious': round(probs[1], 4) if probs else None,
                'excited': round(probs[2], 4) if probs else None
            }
        })
    
    return jsonify({
        'success': True,
        'count': len(results),
        'data': results
    })


@app.route('/api/v1/baseline/<user_id>', methods=['GET'])
@token_required
def get_baseline(user_id):
    """鑾峰彇鐢ㄦ埛蹇冪巼鍩虹嚎淇℃伅"""
    baseline = user_baselines.get(str(user_id), {})
    profile = user_profiles.get(str(user_id), {})
    
    return jsonify({
        'success': True,
        'data': {
            'user_id': str(user_id),
            'baseline_hr_mean': baseline.get('mean'),
            'baseline_hr_std': baseline.get('std'),
            'baseline_hr_median': baseline.get('median'),
            'data_count': baseline.get('count', 0),
            'gender': profile.get('gender'),
            'age': profile.get('age'),
            'weight_kg': profile.get('weight_kg')
        }
    })


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
# 璁惧绠＄悊 /api/v1/device/
# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@app.route('/api/v1/device/bind', methods=['POST'])
@token_required
def bind_device():
    """缁戝畾璁惧锛堟敮鎸?ble_address 鐢ㄤ簬鑷姩閲嶈繛锛?""
    data = request.get_json() or {}
    
    device_id = data.get('device_id', '').strip()
    device_name = data.get('device_name', 'RingHealth Ring')
    ble_address = data.get('ble_address', '').strip()  # BLE MAC鍦板潃锛岀敤浜庤嚜鍔ㄩ噸杩?
    
    if not device_id:
        return jsonify({'success': False, 'error': '缂哄皯璁惧ID'}), 400
    
    devices = _load_json(DEVICES_FILE, [])
    
    # 妫€鏌ユ槸鍚﹀凡缁戝畾
    existing = next((d for d in devices if d.get('device_id') == device_id), None)
    
    now = datetime.now().isoformat()
    
    if existing:
        existing['user_id'] = g.user_id
        existing['device_name'] = device_name
        existing['is_active'] = True
        existing['bound_at'] = now
        existing['last_seen'] = now
        if ble_address:
            existing['ble_address'] = ble_address
    else:
        devices.append({
            'id': _generate_id('D'),
            'device_id': device_id,
            'device_name': device_name,
            'device_type': 'ring',
            'user_id': g.user_id,
            'ble_address': ble_address or '',
            'is_active': True,
            'is_online': True,
            'bound_at': now,
            'last_seen': now
        })
    
    _save_json(DEVICES_FILE, devices)
    
    return jsonify({
        'success': True,
        'data': {'device_id': device_id, 'status': 'bound'},
        'message': '璁惧缁戝畾鎴愬姛'
    })


@app.route('/api/v1/device/last/<user_id>', methods=['GET'])
@token_required
def get_last_device(user_id):
    """鑾峰彇鐢ㄦ埛鏈€鍚庤繛鎺ョ殑娲昏穬璁惧锛堢敤浜庤嚜鍔ㄩ噸杩烇級"""
    devices = _load_json(DEVICES_FILE, [])
    active = [d for d in devices if d.get('user_id') == user_id and d.get('is_active') == True]
    
    if not active:
        return jsonify({
            'success': False,
            'error': '璇ョ敤鎴锋殏鏃犵粦瀹氳澶?,
            'data': None
        }), 404
    
    # 鎸?last_seen 鎺掑簭锛岃繑鍥炴渶杩戜娇鐢ㄧ殑璁惧
    active.sort(key=lambda d: d.get('last_seen', ''), reverse=True)
    device = active[0]
    
    return jsonify({
        'success': True,
        'data': {
            'device_id': device.get('device_id'),
            'device_name': device.get('device_name', 'RingHealth Ring'),
            'ble_address': device.get('ble_address', ''),
            'last_seen': device.get('last_seen')
        }
    })


@app.route('/api/v1/device/list/<user_id>', methods=['GET'])
@token_required
def list_devices(user_id):
    """鑾峰彇鐢ㄦ埛璁惧鍒楄〃"""
    devices = _load_json(DEVICES_FILE, [])
    user_devices = [d for d in devices if d.get('user_id') == user_id]
    
    return jsonify({
        'success': True,
        'data': user_devices,
        'count': len(user_devices)
    })


@app.route('/api/v1/device/unbind', methods=['POST'])
@token_required
def unbind_device():
    """瑙ｇ粦璁惧"""
    data = request.get_json() or {}
    device_id = data.get('device_id', '').strip()
    
    if not device_id:
        return jsonify({'success': False, 'error': '缂哄皯璁惧ID'}), 400
    
    devices = _load_json(DEVICES_FILE, [])
    updated = []
    
    for d in devices:
        if d.get('device_id') == device_id:
            d['is_active'] = False
            d['unbound_at'] = datetime.now().isoformat()
        updated.append(d)
    
    _save_json(DEVICES_FILE, updated)
    
    return jsonify({
        'success': True,
        'message': '璁惧宸茶В缁?
    })


@app.route('/api/v1/device/heartbeat', methods=['POST'])
@token_required
def device_heartbeat():
    """璁惧蹇冭烦/鍦ㄧ嚎鐘舵€佹洿鏂帮紙杩炴帴鎴愬姛鍚庤皟鐢紝鏇存柊 last_seen + ble_address锛?""
    data = request.get_json() or {}
    device_id = data.get('device_id', '').strip()
    ble_address = data.get('ble_address', '').strip()
    
    if not device_id:
        return jsonify({'success': False, 'error': '缂哄皯璁惧ID'}), 400
    
    devices = _load_json(DEVICES_FILE, [])
    now = datetime.now().isoformat()
    
    for d in devices:
        if d.get('device_id') == device_id:
            d['last_seen'] = now
            d['is_online'] = True
            if ble_address:
                d['ble_address'] = ble_address
            break
    
    _save_json(DEVICES_FILE, devices)
    
    return jsonify({'success': True, 'message': 'ok'})


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
# 缁熻姒傝 /api/v1/stats
# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@app.route('/api/v1/stats', methods=['GET'])
def stats_overview():
    """绯荤粺缁熻姒傝"""
    records = _load_json(BIOMETRIC_FILE, [])
    results = _load_json(EMOTION_RESULTS_FILE, [])
    users = _load_json(USERS_FILE, {})
    devices = _load_json(DEVICES_FILE, [])
    
    # 缁熻鐢ㄦ埛鏁?
    total_users = len(users)
    
    # 缁熻璁板綍鏁?
    total_records = len(records)
    analyzed_count = sum(1 for r in records if r.get('exec_status') == '1')
    
    # 鎯呯华鍒嗗竷
    emotion_dist = {'calm': 0, 'anxious': 0, 'excited': 0}
    for r in results:
        label = r.get('emotion_label', 'calm')
        if label in emotion_dist:
            emotion_dist[label] += 1
    
    # 鏈€杩?4灏忔椂璁板綍
    since_24h = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    last_24h = sum(1 for r in records if str(r.get('collected_at', '')) >= since_24h)
    
    # 鍦ㄧ嚎璁惧鏁?
    online_devices = sum(1 for d in devices if d.get('is_online') and d.get('is_active'))
    
    return jsonify({
        'success': True,
        'data': {
            'total_users': total_users,
            'total_records': total_records,
            'total_analyzed': analyzed_count,
            'total_pending': total_records - analyzed_count,
            'emotion_distribution': emotion_dist,
            'last_24h_records': last_24h,
            'online_devices': online_devices,
            'total_devices': len(devices),
            'storage_backend': STORAGE_MODE,
            'model_loaded': emotion_model is not None
        }
    })


# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
# 鍚庡彴绠＄悊鎺ュ彛 /api/v1/admin/
# 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@app.route('/api/v1/admin/users', methods=['GET'])
def admin_list_users():
    """绠＄悊鍛橈細鑾峰彇鎵€鏈夌敤鎴峰垪琛?""
    users = _load_json(USERS_FILE, {})
    
    user_list = []
    for uid, u in users.items():
        safe_u = {k: v for k, v in u.items() if k != 'password'}
        safe_u['_id'] = uid
        user_list.append(safe_u)
    
    # 鍒嗛〉
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 20)), 100)
    keyword = request.args.get('keyword', '')
    
    if keyword:
        user_list = [
            u for u in user_list 
            if keyword.lower() in (u.get('nickname','').lower()) 
            or keyword in u.get('phone','')
        ]
    
    total = len(user_list)
    start = (page - 1) * limit
    paged = user_list[start:start+limit]
    
    return jsonify({
        'success': True,
        'data': paged,
        'pagination': {'total': total, 'page': page, 'pages': (total+limit-1)//limit}
    })


@app.route('/api/v1/admin/emotions', methods=['GET'])
def admin_emotion_stats():
    """绠＄悊鍛橈細鎯呯华缁熻鎶ヨ〃"""
    results = _load_json(EMOTION_RESULTS_FILE, [])
    
    # 鎸夊ぉ缁熻
    daily_stats = {}
    for r in results:
        date_str = str(r.get('analyzed_at', ''))[:10]
        if date_str:
            if date_str not in daily_stats:
                daily_stats[date_str] = {'calm': 0, 'anxious': 0, 'excited': 0}
            
            label = r.get('emotion_label', 'calm')
            if label in daily_stats[date_str]:
                daily_stats[date_str][label] += 1
    
    # 鎺掑簭
    sorted_daily = sorted(daily_stats.items(), key=lambda x: x[0], reverse=True)[:30]
    
    # 鐢ㄦ埛鎯呯华鎺掕
    user_emotion_counts = {}
    for r in results:
        uid = str(r.get('user_id', ''))
        if uid not in user_emotion_counts:
            user_emotion_counts[uid] = {'calm': 0, 'anxious': 0, 'excited': 0}
        label = r.get('emotion_label', 'calm')
        if label in user_emotion_counts[uid]:
            user_emotion_counts[uid][label] += 1
    
    top_users = sorted(
        [{'user_id': k, **v} for k, v in user_emotion_counts.items()],
        key=lambda x: sum(v for k,v in x.items() if k != 'user_id'),
        reverse=True
    )[:10]
    
    return jsonify({
        'success': True,
        'data': {
            'daily_trend': sorted_daily,
            'top_users_by_emotion': top_users,
            'total_analyses': len(results)
        }
    })


# 鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲
# 鏍稿績涓氬姟鍑芥暟
# 鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲

def clean_biometric_data(data):
    """娓呮礂鍓嶇鍙戞潵鐨勭敓鐗╃壒寰佹暟鎹紝杩斿洖(cleaned_dict, errors_list)"""
    errors = []
    
    user_id = str(data.get('user_id', '')).strip()
    if not user_id:
        errors.append('user_id 涓嶈兘涓虹┖')
    
    hr_raw = data.get('heart_rate')
    if hr_raw is None:
        errors.append('heart_rate 涓嶈兘涓虹┖')
        heart_rate = None
    else:
        try:
            heart_rate = int(float(hr_raw))
            if heart_rate < 30 or heart_rate > 220:
                errors.append(f'heart_rate {heart_rate} 瓒呭嚭鏈夋晥鑼冨洿 [30-220]')
        except (ValueError, TypeError):
            errors.append(f'heart_rate "{hr_raw}" 涓嶆槸鏈夋晥鏁板€?)
            heart_rate = None
    
    device_id = str(data.get('device_id', '')).strip()
    if not device_id:
        errors.append('device_id 涓嶈兘涓虹┖')
    
    device_type = str(data.get('device_type', 'ring')).strip().lower()
    if device_type not in ('ring', 'bracelet'):
        errors.append(f'device_type "{device_type}" 鏃犳晥')
        device_type = 'ring'
    
    collected_at = data.get('collected_at', '').strip()
    if not collected_at:
        collected_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    weight_kg = data.get('weight_kg')
    gender = data.get('gender')
    age = data.get('age')
    
    return {
        'user_id': user_id,
        'heart_rate': heart_rate,
        'device_id': device_id,
        'device_type': device_type,
        'collected_at': collected_at,
        'weight_kg': float(weight_kg) if weight_kg else None,
        'gender': int(gender) if gender is not None else None,
        'age': int(age) if age else None,
        'remark': data.get('remark')
    }, errors


def extract_features(user_id, heart_rate, timestamp=None, gender=None, age=None, weight_kg=None):
    """涓哄崟鏉￠娴嬭姹傛彁鍙?1缁寸壒寰佸悜閲?""
    import math
    
    # 鑾峰彇鐢ㄦ埛鐢诲儚
    profile = user_profiles.get(str(user_id), {})
    
    if gender is None:
        gender = profile.get('gender', 1)
    if age is None:
        age = profile.get('age', 22)
    if weight_kg is None:
        weight_kg = profile.get('weight_kg', 65)
    
    # 鏃堕棿鐗瑰緛
    if timestamp:
        try:
            dt = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00').split('+')[0])
        except ValueError:
            dt = datetime.now()
    else:
        dt = datetime.now()
    
    hour = dt.hour
    minute = dt.minute
    hour_decimal = hour + minute / 60.0
    hour_sin = math.sin(2 * math.pi * hour_decimal / 24.0)
    hour_cos = math.cos(2 * math.pi * hour_decimal / 24.0)
    is_night = 1 if (hour >= 0 and hour < 5) or (hour >= 23) else 0
    
    # 鍩虹嚎鐗瑰緛
    baseline = user_baselines.get(str(user_id), {})
    base_mean = baseline.get('mean', 70)
    base_std = baseline.get('std', 10)
    base_median = baseline.get('median', 70)
    
    hr_deviation = heart_rate - base_mean
    hr_zscore = hr_deviation / base_std if base_std > 0 else 0
    hr_ratio = heart_rate / base_median if base_median > 0 else 1.0
    hrv_proxy = baseline.get('std', 5) * 0.3
    
    feature_vector = [
        float(age), float(gender), float(weight_kg), float(heart_rate),
        round(hr_deviation, 1), round(hr_zscore, 3), round(hr_ratio, 3),
        round(hour_sin, 4), round(hour_cos, 4), float(is_night),
        round(hrv_proxy, 2)
    ]
    
    user_info = {
        'age': age, 'gender': gender, 'weight_kg': weight_kg,
        'baseline_mean': base_mean, 'baseline_std': base_std
    }
    
    return feature_vector, user_info


def run_prediction(feature_vector):
    """杩愯鎯呯华棰勬祴妯″瀷"""
    if emotion_model is None or scaler is None:
        return None, None, None, None
    
    import numpy as np
    
    X = np.array([feature_vector])
    X_scaled = scaler.transform(X)
    
    probs = emotion_model.predict_proba(X_scaled)[0]
    label = int(emotion_model.predict(X_scaled)[0])
    
    labels_map = ['calm', 'anxious', 'excited']
    label_name = labels_map[label]
    
    if label == 0:
        score = round((1 - probs[0]) * 0.3, 3)
    else:
        score = round(probs[label] * 0.7 + 0.3, 3)
    
    return label, label_name, probs.tolist(), score


def analyze_emotion_for_record(record):
    """瀵瑰崟鏉¤褰曡繘琛屽畬鏁存儏缁垎鏋?""
    user_id = str(record.get('user_id', ''))
    heart_rate = int(record.get('heart_rate', 0))
    
    gender = record.get('gender')
    age = record.get('age')
    weight_kg = record.get('weight_kg')
    
    if isinstance(gender, str):
        gm = {'M': 1, 'F': 0, 'O': 2, '鐢?: 1, '濂?: 0}
        gender = gm.get(gender.upper(), 1)
    
    collected_at = record.get('collected_at')
    
    feature_vector, user_info = extract_features(
        user_id, heart_rate, collected_at, gender, age, weight_kg
    )
    
    label, label_name, probabilities, score = run_prediction(feature_vector)
    
    if label is None:
        return None
    
    feature_names = [
        'age', 'gender', 'weight_kg', 'heart_rate',
        'hr_baseline_deviation', 'hr_zscore', 'hr_ratio',
        'hour_sin', 'hour_cos', 'is_night', 'hrv_proxy'
    ]
    
    extra_result = json.dumps({
        'feature_vector': dict(zip(feature_names, feature_vector)),
        'probabilities': {
            'calm': round(probabilities[0], 4),
            'anxious': round(probabilities[1], 4),
            'excited': round(probabilities[2], 4)
        },
        'user_info': user_info
    }, ensure_ascii=False)
    
    return {
        'raw_data_id': record.get('id'),
        'user_id': user_id,
        'analyzed_at': collected_at or datetime.now().isoformat(),
        'emotion_label': label_name,
        'emotion_score': score,
        'extra_result': extra_result
    }


# 鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲
# 鍚姩鍏ュ彛
# 鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲

if __name__ == '__main__':
    print('=' * 60)
    print('  [RingHealth] RingHealth API Server v1.0.0')
    print('  鏄熸灑鏅鸿兘鍋ュ悍鎸囩幆 - 鍚庣鏈嶅姟')
    print('=' * 60)
    
    # 鍔犺浇鎯呯华寮曟搸
    load_emotion_engine()
    
    if emotion_model:
        print(f'\n  [OK] 鎯呯华妯″瀷宸插姞杞?(RandomForest)')
        print(f'  [OK] 鐢ㄦ埛鍩虹嚎: {len(user_baselines)} 浜?)
        print(f'  [OK] 鐢ㄦ埛鐢诲儚: {len(user_profiles)} 浜?)
    else:
        print('\n  [!] 鎯呯华妯″瀷鏈姞杞?(棰勬祴鍔熻兘涓嶅彲鐢?')
        print(f'     鎼滅储璺緞: {EMOTION_ENGINE_DIR}')
    
    print(f'\n  [>>] 鏈嶅姟鍦板潃: http://{HOST}:{PORT}')
    print(f'  [DB] 瀛樺偍妯″紡: {STORAGE_MODE.upper()}')
    print(f'  [--] 璋冭瘯妯″紡: {DEBUG}')
    print('\n  API绔偣:')
    print('    GET  /health              - 鍋ュ悍妫€鏌?)
    print('    POST /api/v1/auth/login   - 鐧诲綍')
    print('    POST /api/v1/auth/register - 娉ㄥ唽')
    print('    POST /api/v1/biometric   - 涓婁紶蹇冪巼鏁版嵁')
    print('    POST /api/v1/predict     - 鎯呯华棰勬祴')
    print('    GET  /api/v1/latest/<uid> - 鏈€鏂版暟鎹?)
    print('    GET  /api/v1/history/<uid> - 鍘嗗彶璁板綍')
    print('    GET  /api/v1/stats        - 缁熻姒傝')
    print('    POST /api/v1/device/bind  - 缁戝畾璁惧')
    print('')
    print('=' * 60)
    
    app.run(host=HOST, port=PORT, debug=DEBUG)

