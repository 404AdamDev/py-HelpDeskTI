from sqlalchemy import create_engine, Column, String, Integer, DateTime,Text, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Relationship
import datetime

engine = create_engine("mysql+pymysql://root:86856772*@localhost:3306/helpDeskTI", echo=True)

Base = declarative_base()
_Sessao = sessionmaker(engine)

class ChamadoTI(Base):
    __tablename__ = "ChamadoTi"

    id = Column(Integer, primary_key=True, autoincrement=True)
    solicitante = Column(String(250), nullable=False)
    setor = Column(String(250), nullable=False, unique=True)
    descricao_problema = Column(String(250), nullable=False)
    data_abertura = Column(DateTime, nullable=False, default= datetime.datetime.now())
    prioridade = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)

    #criando a foreignKey no ORM
    TecnicoTI_id = Column(Integer, ForeignKey('TecnicoTI.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    TecnicoTI = Relationship('TecnicoTI',backref='chamados', lazy="subquery")

    def adicionarChamado(self, solicitante, setor, descricao_problema, prioridade, status):
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

    def alterarStatus(self, id,  valor):
        with _Sessao() as sessao: #Alterar status chamado
            chamado = sessao.query(ChamadoTI).filter_by(id=id).first()
            chamado.status = valor
            sessao.commit()

    def atribuirChamado(self, id, tecnico):
            with _Sessao() as sessao:  # Atribuir chamado
                chamado = sessao.query(ChamadoTI).filter_by(id=id).first()
                chamado.TecnicoTI_id = tecnico
                sessao.commit()

class TecnicoTI(Base):
    __tablename__ = "TecnicoTI"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(250), nullable=False)
    turno = Column(String(250), nullable=False, unique=True)

    def criarTecnico(self, nome, turno):
        with _Sessao() as sessao:  # adicionar tecnico
            tecnico = TecnicoTI(
                nome=nome,
                turno=turno
            )
            sessao.add(tecnico)
            sessao.commit()
            sessao.close()


def print_hi(name):
    print(f'Hi, {name}')

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

if __name__ == '__main__':
    menu()

