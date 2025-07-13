import sys

# Este bloco tenta importar de várias formas, cobre rodar como módulo ou script direto
try:
    from agent import chat
except ModuleNotFoundError:
    try:
        from src.agent import chat
    except ModuleNotFoundError:
        # Se estiver rodando como pacote relativo
        from .agent import chat

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or input("Pergunta: ")
    resposta = chat(question)
    print(resposta)
