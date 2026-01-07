from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Inicializa o hasher
ph = PasswordHasher()

def gerar_hash_senha(senha: str) -> str:
    """
    Gera o hash usando Argon2. Não tem limite de 72 bytes.
    """
    return ph.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Verifica se a senha coincide com o hash.
    """
    try:
        return ph.verify(hash_senha, senha)
    except VerifyMismatchError:
        return False