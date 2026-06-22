from fastapi import FastAPI
# 1. ADICIONE ESSA LINHA DE IMPORTAÇÃO:
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 2. ADICIONE TODO ESSE BLOCO AQUI EMBAIXO:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que o Live Server acesse a API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Abaixo daqui continua o resto do seu código normal (@app.get, @app.post, etc...)

# Conexão com Banco de Dados SQLite
def conectar_banco():
    conexao = sqlite3.connect("estoque.db")
    conexao.row_factory = sqlite3.Row
    return conexao

# Criação da tabela com suporte a Categorias e Estoque Mínimo
def inicializar_banco():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            estoque_minimo INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

inicializar_banco()

class ProdutoSchema(BaseModel):
    nome: str
    categoria: str
    quantidade: int
    preco: float
    estoque_minimo: int

@app.get("/api/produtos")
def listar_produtos():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return produtos

@app.post("/api/produtos")
def adicionar_produto(produto: ProdutoSchema):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, categoria, quantidade, preco, estoque_minimo)
        VALUES (?, ?, ?, ?, ?)
    """, (produto.nome, produto.categoria, produto.quantidade, produto.preco, produto.estoque_minimo))
    conn.commit()
    conn.close()
    return {"status": "sucesso", "mensagem": "Produto registrado no banco de dados."}

@app.delete("/api/produtos/{produto_id}")
def deletar_produto(produto_id: int):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()
    return {"status": "sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)