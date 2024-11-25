import jwt
import logging

# Clave secreta para firmar el token (debería ser guardada de forma segura, nunca en código plano)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Función para generar un token JWT sin expiración
def generate_token(user_id, role="user"):
    """
    Genera un token JWT para un usuario con el ID y rol proporcionados.
    Este token no tendrá fecha de expiración (exp) por lo que nunca expirará.
    """
    try:
        # Payload del token, que incluye user_id y rol del usuario
        payload = {
            "user_id": user_id,
            "role": role,
            # No se agrega la fecha de expiración (exp), el token nunca expirará
        }

        # Generar el token
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        logging.error(f"Error generating token: {e}")
        raise

# Función para verificar un token JWT
def verify_token(token):
    """
    Verifica si el token JWT es válido y devuelve los datos del payload.
    Este método NO verifica la expiración del token.
    """
    try:
        # Decodifica el JWT, sin verificar la expiración (exp)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})

        # Validar que el token contiene los campos requeridos
        user_id = decoded.get("user_id")
        role = decoded.get("role")
        
        if not user_id or not role:
            raise ValueError("Invalid token: Missing user_id or role")

        return decoded  # Retorna el payload del token (user_id, role)
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    except Exception as e:
        logging.error(f"Error verifying token: {e}")
        raise ValueError("Invalid token")
