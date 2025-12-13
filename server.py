from sqlalchemy import text, create_engine, Column, String, Integer, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Relationship
import dotenv
import datetime
import os

dotenv.load_dotenv()
engine = create_engine(f"mysql+pymysql://{os.getenv("USER")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT")}", echo=True)
Base = declarative_base()
_Sessao = None

class ChamadoTI(Base):
    __tablename__ = "ChamadoTi"

    id = Column(Integer, primary_key=True, autoincrement=True)
    solicitante = Column(String(250), nullable=False)
    setor = Column(String(250), nullable=False)
    descricao_problema = Column(String(250), nullable=False)
    data_abertura = Column(DateTime, default=datetime.datetime.now)
    prioridade = Column(Enum('baixa', 'media', 'alta', 'critica', name='prioridade_enum'), default='baixa', nullable=False)
    status = Column(Enum('aberto', 'em andamento', 'resolvido', 'fechado', name='status_enum'), default='aberto', nullable=False)

    #criando a foreignKey no ORM
    TecnicoTI_id = Column(Integer, ForeignKey('TecnicoTI.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)

    TecnicoTI = Relationship('TecnicoTI',backref='chamados', lazy="subquery")

    @staticmethod
    def adicionarChamado(solicitante, setor, descricao_problema, prioridade, status):
        with _Sessao() as sessao:  # adicionar chamado
            chamado = ChamadoTI(
                solicitante = solicitante,
                setor = setor,
                descricao_problema = descricao_problema,
                prioridade = prioridade,
                status = status
            )
            sessao.add(chamado)
            sessao.commit()
            sessao.close()

    def listarChamados(self):  # listar chamados
        with _Sessao() as sessao:
            chamados = sessao.query(ChamadoTI).order_by(ChamadoTI.prioridade).all()
            for chamado in chamados:
                print(chamado.id, chamado.descricao_problema)

    @staticmethod
    def alterarStatus(id,  valor):
        with _Sessao() as sessao: #Alterar status chamado
            chamado = sessao.query(ChamadoTI).filter_by(id=id).first()
            chamado.status = valor
            sessao.commit()

    @staticmethod
    def atribuirChamado(id, tecnico):
            with _Sessao() as sessao:  # Atribuir chamado
                chamado = sessao.query(ChamadoTI).filter_by(id=id).first()
                chamado.TecnicoTI_id = tecnico
                sessao.commit()

    @staticmethod
    def desatribuirChamado(id):
        with _Sessao() as s: # Desatribuir chamado
            chamado = s.query(ChamadoTI).filter_by(id=id).first()
            if not chamado:
                return False

            chamado.TecnicoTI_id = None
            chamado.status = "aberto"
            s.commit()
            return True


class TecnicoTI(Base):
    __tablename__ = "TecnicoTI"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(250), nullable=False)
    turno = Column(Enum('manha', 'tarde', 'noite', 'madrugada', name='turno_enum'), default='manha', nullable=False)
    role = Column(Enum('admin', 'user', name='role_enum'), default='user', nullable=False)

    @staticmethod
    def criarTecnico(nome, turno, role='user'):
        with _Sessao() as sessao:  # adicionar tecnico 
            tecnico = TecnicoTI(
                nome=nome,
                turno=turno,
                role=role
            )
            sessao.add(tecnico)
            sessao.commit()
            sessao.close()
            return True
    
    @staticmethod
    def autenticar(nome, turno):
        with _Sessao() as sessao:
            tecnico = sessao.query(TecnicoTI).filter_by(nome=nome, turno=turno).first()

            if tecnico:
                return tecnico
            else:
                return None

def criar_banco():
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{os.getenv("DATABASE")}`"))
        print(f"Database '{os.getenv("DATABASE")}' verificado ou criado.")

def print_hi(name):
    print(f'Hi, {name}')

def existe_admin():
    with _Sessao() as sessao:
        admin_existente = sessao.query(TecnicoTI).filter_by(role="admin").first()
        if not admin_existente:
            novo_admin = TecnicoTI(
                nome="Admin",
                turno="manha",
                role="admin"
            )
            sessao.add(novo_admin)
            sessao.commit()
            print("Usuário administrador criado automaticamente.")

def menu():
    while True:
        print("\n=== MENU HELP DESK TI ===")
        print("1 - Criar técnico")
        print("2 - Criar chamado")
        print("3 - Listar chamados")
        print("4 - Alterar status de um chamado")
        print("5 - Atribuir chamado a um técnico")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do técnico: ")
            turno = input("Turno do técnico: ")
            TecnicoTI().criarTecnico(nome, turno)
            print("Técnico criado com sucesso!")

        elif opcao == "2":
            solicitante = input("Solicitante: ")
            setor = input("Setor: ")
            descricao = input("Descrição do problema: ")
            prioridade = input("Prioridade (Alta/Média/Baixa): ")
            status = input("Status inicial: ")

            ChamadoTI().adicionarChamado(
                solicitante, setor, descricao, prioridade, status
            )
            print("Chamado criado com sucesso!")

        elif opcao == "3":
            print("Lista de chamados:")
            ChamadoTI().listarChamados()

        elif opcao == "4":
            id_chamado = int(input("ID do chamado: "))
            novo_status = input("Novo status: ")
            ChamadoTI().alterarStatus(id_chamado, novo_status)
            print("Status alterado com sucesso!")

        elif opcao == "5":
            id_chamado = int(input("ID do chamado: "))
            id_tecnico = int(input("ID do técnico: "))
            ChamadoTI().atribuirChamado(id_chamado, id_tecnico)
            print("Chamado atribuído com sucesso!")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

def iniciar_servidor():
    global engine, Base, _Sessao
    criar_banco()
    engine = create_engine(f"mysql+pymysql://{os.getenv("USER")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DATABASE")}", echo=True)
    _Sessao = sessionmaker(engine)
    Base.metadata.create_all(engine)
    existe_admin()
    #menu()

if __name__ == '__main__':
    iniciar_servidor()


