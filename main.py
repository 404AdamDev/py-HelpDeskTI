from sqlalchemy import create_engine, Column, String, Integer, DateTime,Text, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Relationship
import datetime

engine = create_engine("mysql+pymysql://root:senha@localhost:3306/helpDeskTI", echo=True)

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

    TecnicoTI = Relationship('usuarios',backref='tarefas', lazy="subquery")

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
            chamado = sessao.query(ChamadoTI).filter_by(id).first()
            chamado.status = valor
            sessao.commit()

    def atribuirChamado(self, id, tecnico):
            with _Sessao() as sessao:  # Atribuir chamado
                chamado = sessao.query(ChamadoTI).filter_by(id).first()
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


if __name__ == '__main__':
    print_hi('PyCharm')

