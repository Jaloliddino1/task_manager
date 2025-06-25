import datetime

import jwt

from U2_rest.settings import SECRET_KEY


access_secret = SECRET_KEY
refresh_secret = SECRET_KEY


def create_token(user_id):
    access_payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }
    refresh_payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }

    access = jwt.encode(access_payload, access_secret, algorithm='HS256')
    refresh = jwt.encode(refresh_payload, refresh_secret, algorithm='HS256')

    return {'access': access,
            'refresh': refresh}


def verify_token(token, secret, type='access'):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        if payload['type'] != type:
            return None
        if payload.get('exp') < datetime.datetime.utcnow().timestamp():
            raise jwt.ExpiredSignatureError('expired')
        return payload
    except jwt.ExpiredSignatureError:
        return 'Token Expired'
    except jwt.InvalidTokenError:
        return 'Invalid Token'


def refresh_token(refresh_token):
    payload = verify_token(refresh_token, refresh_secret, type='refresh')

    if not isinstance(payload, dict):
        return {"error": payload}

    access_payload = {
        'user_id': payload['user_id'],
        'type': 'access',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }
    access = jwt.encode(access_payload, access_secret, algorithm='HS256')
    return {'access': access}


