import flet as ft
import mysql.connector

def main(page: ft.Page):
    global nome, senha, frame_cadastro

    def on_send_click(e):
        if radio_group.value == 'Leitor':
            Leitor_page()
        elif radio_group.value == 'Autor':
            page_normal()

    def salvar_cadastro(e, nome_cadastro, senha_cadastro, repetir_senha):
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
                page.update()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                show_popup_cadastro_erro()
            finally:
                cursor.close()
                conn.close()
        else:
            show_popup_cadastro_erro()

    def show_popup_cadastro_sucesso():
        popup = ft.AlertDialog(
            title=ft.Text("Aviso"),
            content=ft.Text("Cadastro realizado com sucesso!"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: (fechar_popup()))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        def fechar_popup():
            popup.open = False
            page.update()
        
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

    def senha_existe():
        popup = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text("Já existe um usuário com essa senha, tente outra senha!"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def delete_frames():
        page.controls.clear()
        page.update()

    def show_popups(e):
        print("Tentando fazer login...")
        print(f"Nome: {nome.value}, Senha: {senha.value}")

        if not radio_group.value:
            show_popup_radio_nao_selecionado()
            return

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

                on_send_click(e)
                show_popup_login_sucesso()
            else:
                show_popup_usuario_nao_encontrado()

        except mysql.connector.Error as err:
            print(f"Erro ao verificar usuário: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_popup_radio_nao_selecionado():
            popup = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text("Por favor, selecione um tipo de usuário (Leitor ou Autor)!"),
                actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
                actions_alignment=ft.MainAxisAlignment.END
            )

            def fechar_popup():
                popup.open = False
                page.update()

            page.dialog = popup
            popup.open = True
            page.update()

    def show_popup_login_sucesso():
        popup = ft.AlertDialog(
            title=ft.Text("Login Sucesso"),
            content=ft.Text("Login realizado com sucesso!"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def voltar_para_login():
        delete_frames()
        page.add(main_container)
        page.update()
    def abrir_cadastro():
        page.controls.clear()

        label_cadastro = ft.Text("Cadastro", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        nome_cadastro = ft.TextField(label="Nome")
        senha_cadastro = ft.TextField(label="Senha", password=True)
        repetir_senha = ft.TextField(label="Repetir Senha", password=True)

        def v_senha_existe(e):
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="biblioteca",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT senha FROM usuario")
                result = cursor.fetchall()

                for resultado in result:
                    if resultado[0] == senha_cadastro.value:
                        senha_existe()
                        return

                salvar_cadastro(e, nome_cadastro, senha_cadastro, repetir_senha)

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                show_popup_cadastro_erro()
            finally:
                cursor.close()
                conn.close()

        botao_cadastrar = ft.ElevatedButton(text="Cadastrar", on_click=lambda e: v_senha_existe(e))
    
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
            controls=[frame_container],
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

    def handle_login_click(e):
        show_popups(e)
        on_send_click(e)

    botao = ft.ElevatedButton(text="X", on_click=lambda e: page.window.destroy())
    botao1 = ft.ElevatedButton(text="Entrar", on_click= handle_login_click)
    botao2 = ft.ElevatedButton(text="Cadastrar", on_click=lambda e: abrir_cadastro())

    radio_group = ft.RadioGroup(
        value='Leitor',
        content=ft.Column(
            controls=[
                ft.Radio(value="Leitor", label="Leitor"),
                ft.Radio(value='Autor', label='Autor')
            ]
        )
    )

    frame = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(label, alignment=ft.alignment.center, bgcolor="#4D4D4D"),
                ft.Container(label1, alignment=ft.alignment.center),
                ft.Container(label2, alignment=ft.alignment.center),
                ft.Container(nome, alignment=ft.alignment.center),
                ft.Container(label3, alignment=ft.alignment.center),
                ft.Container(senha, alignment=ft.alignment.center),
                ft.Container(botao1, alignment=ft.alignment.center),
                ft.Container(label4, alignment=ft.alignment.center),
                ft.Container(botao2, alignment=ft.alignment.center),
                ft.Container(radio_group, alignment=ft.alignment.center)
            ]
        ),
        bgcolor="#696969",
        width=400,
        height=500,
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
    def verifica_livro_existente(titulo, autor):
        cursor = None
        existe = False
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
                "SELECT COUNT(*) FROM books WHERE titulo = %s AND autor = %s",
                (titulo, autor)
            )
            count = cursor.fetchone()[0]
            existe = count > 0
        except Exception as e:
            print(f"Erro ao verificar livro existente: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return existe
    
    def show_popup_livro_existente():
        popup = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text("O livro já está registrado!"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def page_normal():
        titulo = ft.TextField(label="Título")
        autor = ft.TextField(label="Autor")
        genero = ft.TextField(label="Gênero")
        idioma = ft.TextField(label="Idioma")
        localizacao = ft.TextField(label="Localização")
        button3 = ft.TextButton(text="Cadastrar livro", on_click=lambda e: executar_script_sql_r(titulo, autor, genero, idioma, localizacao))

        frame_livro = ft.Container(
            content=ft.Column(
                controls=[
                    titulo,
                    autor,
                    genero,
                    idioma,
                    localizacao,
                    button3
                ]
            ),
            bgcolor="#696969",
            width=400,
            height=400,
            border_radius=10,
            alignment=ft.alignment.center,
            padding=20
        )

        page.controls.clear()
        page.add(
            ft.Container(
                content=frame_livro,
                alignment=ft.alignment.center
            )
        )
        page.update()

        def executar_script_sql_r(titulo, autor, genero, idioma, localizacao):
            tit = titulo.value
            aut = autor.value
            gen = genero.value
            idi = idioma.value
            loc = localizacao.value
            if verifica_livro_existente(tit, aut):
                show_popup_livro_existente()
                return

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

        print(f"Livro: {titulo.value}, Autor: {autor.value}, Gênero: {genero.value}, Idioma: {idioma.value}, Localização: {localizacao.value}")
    def Leitor_page():

        page.controls.clear()

        titulo = ft.TextField(label="Título")
        autor = ft.TextField(label="Autor")
        button3 = ft.TextButton(text="Buscar Livro", on_click=lambda e: buscar_livro(titulo.value, autor.value))

        frame_livro = ft.Container(
            content=ft.Column(
                controls=[
                    titulo,
                    autor,
                    button3
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
        content=frame_livro,
        alignment=ft.alignment.center,
        padding=20)

        main_container = ft.Column(
        controls=[
            frame_container
        ],
        alignment=ft.MainAxisAlignment.START,
    )

        page.add(main_container)
        page.update()

    def buscar_livro(titulo, autor):

        if not verifica_livro_existente(titulo, autor):
            show_popup_livro_nao_encontrado()
        else:

            pass

    def show_popup_livro_nao_encontrado():
        popup = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text("Não há livros registrados no momento!"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

ft.app(target=main)