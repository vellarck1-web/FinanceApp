from database import (
    criar_tabelas,
    criar_usuario
)

criar_tabelas()

criar_usuario(
    "João Admin",
    "admin@admin.com",
    "89986176"
)

print("Usuário criado com sucesso!")