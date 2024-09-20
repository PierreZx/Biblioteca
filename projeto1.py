import flet as ft
import mysql.connector

# Ajuste no script SQL com o uso de AUTO_INCREMENT no MySQL
script_sql = '''
CREATE TABLE books (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  genre TEXT,
  language TEXT,
  location TEXT
);

CREATE TABLE readers (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  registration_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE loans (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  book_id BIGINT,
  reader_id BIGINT,
  loan_date DATE DEFAULT CURRENT_DATE,
  return_date DATE,
  FOREIGN KEY (book_id) REFERENCES books(id),
  FOREIGN KEY (reader_id) REFERENCES readers(id)
);

-- O restante do seu script segue da mesma forma...
'''
def executar_script_sql():
    try:
        # Conectar ao banco de dados MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="1009061",
            password="acesso123",
            database="biblioteca",
            port="3306"
        )
        
        cursor = conn.cursor()

        # Dividir o script SQL em comandos individuais e executar um por um
        for statement in script_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)

        conn.commit()
        print("Script SQL executado com sucesso!")
        
        # Teste: Inserir um registro na tabela "books" para verificar a conexão
        cursor.execute("INSERT INTO books (title, author, genre) VALUES ('Teste Book', 'Autor Exemplo', 'Ficção')")
        conn.commit()
        print("Registro inserido com sucesso na tabela 'books'!")

    except Exception as e:
        print(f"Erro ao conectar ou executar o script SQL: {e}")
    
    finally:
        cursor.close()
        conn.close()
def main(page: ft.Page):
    page.title = "Supermercado"
    page.window_full_screen = True

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    label = ft.Text("Biblioteca Acervo", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    label1 = ft.Text("Login")
    label2 = ft.Text("Nome")
    label3 = ft.Text("Senha")

    nome = ft.TextField(label="Nome")
    senha = ft.TextField(label="Senha", password=True)
    
    def on_button_click(e):
        print("botão clicado")
        page.window_destroy() 

    botao = ft.ElevatedButton(text="X", on_click=on_button_click)
    botao1 = ft.ElevatedButton(text="Cadastrar")

    frame = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(label, alignment=ft.alignment.center, bgcolor="#4D4D4D", padding=18),
                ft.Container(label1, alignment=ft.alignment.center),
                ft.Container(label2, alignment=ft.alignment.center),
                ft.Container(nome, alignment=ft.alignment.center),
                ft.Container(label3, alignment=ft.alignment.center),
                ft.Container(senha, alignment=ft.alignment.center),
                ft.Container(botao, alignment=ft.alignment.top_right)
            ]
        ),
        bgcolor="#696969",
        width=400,
        height=400,
        border_radius=10,
        alignment=ft.alignment.center,
        padding=20
    )

    page.add(frame)

ft.app(target=main)
