import flet as ft
import mysql.connector


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

    def delete_frames():
        page.controls.clear()
        page.update()

    def show_popup_cadastro_sucesso():
        popup = ft.AlertDialog(
            title=ft.Text("Aviso"),
            content=ft.Text("Cadastro realizado com sucesso!"),
            actions=[ft.TextButton("OK", on_click=lambda e: (setattr(popup, "open", False), delete_frames(), page_normal()))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = popup
        popup.open = True
        page.update()

    def show_popup_cadastro_erro():
        popup = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text("As senhas não coincidem!"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )
        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def show_popups(e):
        print("Tentando fazer login...")
        print(f"Nome: {nome.value}, Senha: {senha.value}")  
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="biblioteca",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE nome = %s AND senha = %s", (nome.value, senha.value))

            result = cursor.fetchall()
            print(f"Resultado da consulta: {result}")  

            if result:
                popup = ft.AlertDialog(
                    title=ft.Text("Usuário Encontrado"),
                    content=ft.Text("Login realizado!"),
                    actions=[ft.TextButton("OK", on_click=lambda e: (setattr(popup, "open", False), delete_frames(), page_normal()))],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                page.dialog = popup
                popup.open = True
                page.update()
            else:
                show_popup_usuario_nao_encontrado()

        except mysql.connector.Error as err:
            print(f"Erro ao verificar usuário: {err}")  
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

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
                    ft.Container(botao_cadastrar, alignment=ft.alignment.center),
                ]
            ),
            bgcolor="#696969",
            width=400,
            height=400,
            border_radius=10,
            alignment=ft.alignment.center,
            padding=20
        )
        frame_container = ft.Container(
        content=frame_cadastro,
        alignment=ft.alignment.center,
        padding=115
    )
        main_container = ft.Column(
        controls=[
        frame_container
        ],
        alignment=ft.MainAxisAlignment.START,
    )
        page.add(main_container)
        page.update()

    page.title = "Supermercado"
    page.window.full_screen = True

    label = ft.Text("Biblioteca Acervo", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    label1 = ft.Text("Login")
    label2 = ft.Text("Nome")
    label3 = ft.Text("Senha")
    label4 = ft.Text("Não tem uma conta?")

    nome = ft.TextField(label="Nome")
    senha = ft.TextField(label="Senha", password=True)

    botao = ft.ElevatedButton(text="X", on_click=lambda e: page.window.destroy())
    botao1 = ft.ElevatedButton(text="Entrar", on_click=show_popups)
    botao2 = ft.ElevatedButton(text="Cadastrar", on_click= lambda e: abrir_cadastro())

    frame = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(label, alignment=ft.alignment.center, bgcolor="#4D4D4D", padding=10),
                ft.Container(label1, alignment=ft.alignment.center),
                ft.Container(label2, alignment=ft.alignment.center),
                ft.Container(nome, alignment=ft.alignment.center),
                ft.Container(label3, alignment=ft.alignment.center),
                ft.Container(senha, alignment=ft.alignment.center),
                ft.Container(botao1, alignment=ft.alignment.center),
                ft.Container(label4, alignment=ft.alignment.center),
                ft.Container(botao2, alignment=ft.alignment.center)
            ]
        ),
        bgcolor="#696969",
        width=400,
        height=400,
        border_radius=10,
        alignment=ft.alignment.center,
        padding=20
    )
    def show_popup_usuario_nao_encontrado():
        popup = ft.AlertDialog(
            title=ft.Text("Usuário Não Encontrado"),
            content=ft.Text("O usuário não foi encontrado. Deseja se cadastrar?"),
            actions=[
                ft.TextButton("Cadastrar", on_click=lambda e: (setattr(popup, "open", False), abrir_cadastro())),
                ft.TextButton("Cancelar", on_click=lambda e: fechar_popup())
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        def fechar_popup():
            popup.open = False
            page.update()
            
        page.dialog = popup
        popup.open = True
        page.update()

    frame_container = ft.Container(
        content=frame,
        alignment=ft.alignment.center,
        padding=20
    )

    button_container = ft.Container(
        content=botao,
        alignment=ft.alignment.top_right,
        padding=20
    )


    main_container = ft.Column(
        controls=[
            button_container,
            frame_container
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    page.add(main_container)

    page.update()
    def page_normal():
        titulo = ft.TextField(label="Título")
        autor = ft.TextField(label="Autor")
        genero = ft.TextField(label="Gênero")
        idioma = ft.TextField(label="Idioma")
        localizacao = ft.TextField(label="Localização")
        button3 = ft.TextButton(text="Cadastrar livro", on_click=lambda e: executar_script_sql_r(titulo, autor, genero, idioma, localizacao))

        def executar_script_sql_r(titulo, autor, genero, idioma, localizacao):
            tit = titulo.value
            aut = autor.value
            gen = genero.value
            idi = idioma.value
            loc = localizacao.value

            livro = {
                "titulo": tit,
                "Autor": aut,
                "Genero": gen,
                "Idioma": idi,
                "loc": loc
            }

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
                cursor.execute(
                    "INSERT INTO books (titulo, autor, genero, idioma, localizacao) VALUES (%s, %s, %s, %s, %s)",
                    (livro["titulo"], livro["Autor"], livro["Genero"], livro["Idioma"], livro["loc"])
                )
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

        page.add(
            ft.Column(
                controls=[
                    ft.Container(titulo, alignment=ft.alignment.center),
                    ft.Container(autor, alignment=ft.alignment.center),
                    ft.Container(genero, alignment=ft.alignment.center),
                    ft.Container(idioma, alignment=ft.alignment.center),
                    ft.Container(localizacao, alignment=ft.alignment.center),
                    ft.Container(botao, alignment=ft.alignment.top_right),
                    ft.Container(button3, alignment=ft.alignment.center)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

ft.app(target=main)
