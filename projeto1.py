import ttkbootstrap as ttk
from tkinter import StringVar
import psycopg2

app = ttk.Window(themename="superhero")
app.title("Supermercado")
app.geometry("400x300")

script_sql = '''create table books (
  id bigint primary key generated always as identity,
  title text not null,
  author text not null,
  genre text,
  language text,
  location text
);

create table readers (
  id bigint primary key generated always as identity,
  name text not null,
  email text unique,
  registration_date date default current_date
);

create table loans (
  id bigint primary key generated always as identity,
  book_id bigint references books (id),
  reader_id bigint references readers (id),
  loan_date date default current_date,
  return_date date
);

drop table if exists books cascade;

drop table if exists readers cascade;

drop table if exists loans cascade;

create table dimensao_acervo (
  id bigint primary key generated always as identity,
  titulo text not null,
  genero text,
  categoria text,
  idioma text,
  localizacao text
);

create table fato_genero (
  id bigint primary key generated always as identity,
  genero text not null
);

create table fato_idioma (
  id bigint primary key generated always as identity,
  idioma text not null
);

create table fato_categoria (
  id bigint primary key generated always as identity,
  categoria text not null
);

create table fato_veiculo_itinerante (
  id bigint primary key generated always as identity,
  localizacao text not null
);

alter table fato_genero
add constraint unique_genero unique (genero);

alter table dimensao_acervo
add constraint fk_genero foreign key (genero) references fato_genero (genero);

alter table fato_idioma
add constraint unique_idioma unique (idioma);

alter table fato_categoria
add constraint unique_categoria unique (categoria);

alter table fato_veiculo_itinerante
add constraint unique_localizacao unique (localizacao);

alter table dimensao_acervo
add constraint fk_idioma foreign key (idioma) references fato_idioma (idioma);

alter table dimensao_acervo
add constraint fk_categoria foreign key (categoria) references fato_categoria (categoria);

alter table dimensao_acervo
add constraint fk_localizacao foreign key (localizacao) references fato_veiculo_itinerante (localizacao);

alter table fato_categoria
rename column id to id_categoria;

alter table fato_genero
rename column id to id_genero;

alter table fato_idioma
rename column id to id_idioma;

alter table fato_veiculo_itinerante
rename column id to id_veiculo;

alter table dimensao_acervo
rename column id to id_acervo;

create table exemplares (
  id_exemplar bigint primary key generated always as identity,
  id_acervo bigint not null,
  estado text,
  data_aquisicao date,
  codigo_barras text unique,
  foreign key (id_acervo) references dimensao_acervo (id_acervo)
);

create table leitores (
  id_leitor bigint primary key generated always as identity,
  nome text not null,
  email text unique,
  telefone text
);

create table emprestimos (
  id_emprestimo bigint primary key generated always as identity,
  id_leitor bigint not null,
  id_exemplar bigint not null,
  data_emprestimo date not null,
  data_devolucao date,
  foreign key (id_leitor) references leitores (id_leitor),
  foreign key (id_exemplar) references exemplares (id_exemplar)
);'''


label = ttk.Label(app, text="Biblioteca Acervo", font=('Helvetica', 14, 'bold'), foreground="white", background="#4D4D4D")
label.place(x= 120, y= 10)

label1 = ttk.Label(app, text="loguin")
label1.place(x= 180, y=40)

label2 = ttk.Label(app, text="Nome")
label2.place(x= 180, y=70)

entry = ttk.Entry(app)
entry.place(x=135, y= 95)

label3 = ttk.Label(app, text="Senha")
label3.place(x= 180, y=160)

entry = ttk.Entry(app)
entry.place(x=135, y= 180)
app.mainloop()