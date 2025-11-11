import json
import time
from urllib import request, parse

# Endpoints da API pública para teste
USERS_API = "https://jsonplaceholder.typicode.com/users"
POSTS_API = "https://jsonplaceholder.typicode.com/posts"


# ==========================================
# Função HTTP GET sem bibliotecas externas
# ==========================================
def http_get(url, params=None, timeout=10):
    """Realiza requisição GET usando apenas urllib."""
    try:
        if params:
            query = parse.urlencode(params)
            full_url = f"{url}?{query}"
        else:
            full_url = url

        req = request.Request(full_url, headers={"User-Agent": "api-validator-no-requests/1.0"})
        with request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            raw = resp.read().decode("utf-8")

            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = raw

            return status, data

    except Exception as e:
        print(f"⚠ Erro ao conectar: {e}")
        return None, None


# ==========================================
# Funções das APIs
# ==========================================
def buscar_usuario(user_id):
    print(f"\n🔍 Buscando usuário {user_id}...")
    time.sleep(0.6)

    status, data = http_get(f"{USERS_API}/{user_id}")
    if status == 200:
        return data

    print("❌ Usuário não encontrado.")
    return None


def buscar_posts(user_id):
    print(f"\n📝 Buscando posts do usuário {user_id}...")
    time.sleep(0.6)

    status, data = http_get(POSTS_API, params={"userId": user_id})
    if status == 200:
        return data if isinstance(data, list) else []

    print("❌ Erro ao buscar posts.")
    return []


def validar(user_id):
    usuario = buscar_usuario(user_id)
    posts = buscar_posts(user_id)

    if not usuario:
        print("\n❌ Integração cancelada: usuário não existe.")
        return

    print(f"\n👤 Usuário: {usuario.get('name')}")
    print(f"📧 Email:   {usuario.get('email')}")
    print(f"🌍 Cidade:  {usuario.get('address', {}).get('city', 'N/A')}")

    if posts:
        print(f"\n📌 Este usuário possui {len(posts)} post(s). Exemplos:")
        for p in posts[:3]:
            print(f"   - {p.get('title')}")
        print("\n✔ Integração concluída com sucesso!")
    else:
        print("\n⚠ Este usuário não possui posts.")


# ==========================================
# Menu interativo
# ==========================================
def menu():
    print("="*65)
    print("PROJETO DE VALIDAÇÃO ENTRE APIs")
    print("="*65)
    print("\nFunciona 100% sem bibliotecas externas.\n")

    while True:
        try:
            entrada = input("Digite o ID do usuário (1–10) ou 'sair': ").strip()

            if entrada.lower() in ("sair", "exit", "q"):
                print("\n👋 Encerrando o programa...")
                break

            user_id = int(entrada)
            validar(user_id)

        except ValueError:
            print("⚠ Digite um número válido ou 'sair'.")
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrompido pelo usuário.")
            break


if __name__ == "__main__":
    menu()