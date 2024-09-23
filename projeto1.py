import flet as ft
import mysql.connector

def executar_script_sql():
    cursor = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="acesso123",
            database="biblioteca",
            port="3306"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (titulo, autor, genero) VALUES ('Teste Book', 'Autor Exemplo', 'Ficção')")
        conn.commit()
        print("Registro inserido com sucesso na tabela 'books'!")
    except Exception as e:
        print(f"Erro ao conectar ou executar o script SQL: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada!")

def salvar_cadastro(e, nome_cadastro, senha_cadastro, repetir_senha, show_popup_cadastro_sucesso, show_popup_cadastro_erro):
    if senha_cadastro.value == repetir_senha.value:
        usuario = {
            "nome": nome_cadastro.value,
            "senha": senha_cadastro.value,
        }

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="biblioteca",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuario (nome, senha) VALUES (%s, %s)", (usuario["nome"], usuario["senha"]))
            conn.commit()
            show_popup_cadastro_sucesso()

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            show_popup_cadastro_erro()
        finally:
            cursor.close()
            conn.close()
    else:
        show_popup_cadastro_erro()

def main(page: ft.Page):
    global nome, senha, frame_cadastro

    executar_script_sql()

    def delete_frames():
        page.controls.clear()
        page.update()

    def show_popup_cadastro_sucesso():
        popup = ft.AlertDialog(
            title=ft.Text("Aviso"),
            content=ft.Text("Cadastro realizado com sucesso!"),
            actions=[ft.TextButton("OK", on_click=lambda e: (setattr(popup, "open", False), delete_frames()))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = popup
        popup.open = True
        page.update()

    def show_popup_cadastro_erro():
        popup = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text("As senhas não coincidem!"),
            actions=[ft.TextButton("OK", on_click=lambda e: setattr(page.dialog, "open", False))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = popup
        popup.open = True
        page.update()

    def show_popups(e):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="biblioteca",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE nome = %s", (nome.value,))
            result = cursor.fetchone()

            if result:
                popup = ft.AlertDialog(
                    title=ft.Text("Usuário Encontrado"),
                    content=ft.Text("Usuário já cadastrado!"),
                    actions=[ft.TextButton("OK", on_click=lambda e: (setattr(popup, "open", False), delete_frames()))],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                page.dialog = popup
                popup.open = True
            else:
                abrir_cadastro()

        except mysql.connector.Error as err:
            print(f"Erro ao verificar usuário: {err}")
        finally:
            cursor.close()
            conn.close()

        page.update()

    def abrir_cadastro():
        page.controls.clear()

        label_cadastro = ft.Text("Cadastro", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        nome_cadastro = ft.TextField(label="Nome")
        senha_cadastro = ft.TextField(label="Senha", password=True)
        repetir_senha = ft.TextField(label="Repetir Senha", password=True)

        botao_cadastrar = ft.ElevatedButton(text="Cadastrar", on_click=lambda e: salvar_cadastro(e, nome_cadastro, senha_cadastro, repetir_senha, show_popup_cadastro_sucesso, show_popup_cadastro_erro))

        frame_cadastro = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(label_cadastro, alignment=ft.alignment.center, bgcolor="#4D4D4D", padding=18),
                    ft.Container(nome_cadastro, alignment=ft.alignment.center),
                    ft.Container(senha_cadastro, alignment=ft.alignment.center),
                    ft.Container(repetir_senha, alignment=ft.alignment.center),
                    ft.Container(botao_cadastrar, alignment=ft.alignment.center)
                ]
            ),
            bgcolor="#696969",
            width=400,
            height=400,
            border_radius=10,
            alignment=ft.alignment.center,
            padding=20
        )

        page.add(frame_cadastro)
        page.update()

    page.title = "Supermercado"
    page.window.full_screen = True

    label = ft.Text("Biblioteca Acervo", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    label1 = ft.Text("Login")
    label2 = ft.Text("Nome")
    label3 = ft.Text("Senha")

    nome = ft.TextField(label="Nome")
    senha = ft.TextField(label="Senha", password=True)

    botao = ft.ElevatedButton(text="X", on_click=lambda e: page.window.destroy())
    botao1 = ft.ElevatedButton(text="Cadastrar", on_click=show_popups)

    frame = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(label, alignment=ft.alignment.center, bgcolor="#4D4D4D", padding=18),
                ft.Container(label1, alignment=ft.alignment.center),
                ft.Container(label2, alignment=ft.alignment.center),
                ft.Container(nome, alignment=ft.alignment.center),
                ft.Container(label3, alignment=ft.alignment.center),
                ft.Container(senha, alignment=ft.alignment.center),
                ft.Container(botao, alignment=ft.alignment.top_right),
                ft.Container(botao1, alignment=ft.alignment.center)
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
    page.update()

    titulo = ft.TextField(label="Título")
    autor = ft.TextField(label="Autor")
    genero = ft.TextField(label="Gênero")
    idioma = ft.TextField(label="Idioma")
    localizacao = ft.TextField(label="Localização")

    page.add(
        ft.Column(
            controls=[
                ft.Container(titulo, alignment=ft.alignment.center),
                ft.Container(autor, alignment=ft.alignment.center),
                ft.Container(genero, alignment=ft.alignment.center),
                ft.Container(idioma, alignment=ft.alignment.center),
                ft.Container(localizacao, alignment=ft.alignment.center)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()

ft.app(target=main)
