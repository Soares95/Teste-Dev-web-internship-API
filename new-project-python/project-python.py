from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import List, Optional


app = FastAPI()

DATABASE_URL = "postgresql+psycopg2://usuario:senha@localhost/empresa_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cnpj = Column(String, unique=True, index=True)
    endereco = Column(String, index=True)
    email = Column(String, index=True)
    telefone = Column(String, index=True)
    obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa")

class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacoes_acessorias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    periodicidade = Column(String, index=True)  # mensal, trimestral, anual
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    empresa = relationship("Empresa", back_populates="obrigacoes")

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(EmpresaBase):
    pass

class EmpresaOut(EmpresaBase):
    id: int
    obrigacoes: List['ObrigacaoAcessoriaOut'] = []

    class Config:
        orm_mode = True

class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str
    empresa_id: int

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass

class ObrigacaoAcessoriaUpdate(ObrigacaoAcessoriaBase):
    pass

class ObrigacaoAcessoriaOut(ObrigacaoAcessoriaBase):
    id: int

    class Config:
        orm_mode = True

EmpresaOut.update_forward_refs()

Base.metadata.create_all(bind=engine)

@app.post("/empresas/", response_model=EmpresaOut)
def create_empresa(empresa: EmpresaCreate):
    db = SessionLocal()
    db_empresa = Empresa(
        nome=empresa.nome,
        cnpj=empresa.cnpj,
        endereco=empresa.endereco,
        email=empresa.email,
        telefone=empresa.telefone
    )
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    db.close()
    return db_empresa

@app.get("/empresas/{empresa_id}", response_model=EmpresaOut)
def read_empresa(empresa_id: int):
    db = SessionLocal()
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    db.close()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

@app.put("/empresas/{empresa_id}", response_model=EmpresaOut)
def update_empresa(empresa_id: int, empresa: EmpresaUpdate):
    db = SessionLocal()
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    db_empresa.nome = empresa.nome
    db_empresa.cnpj = empresa.cnpj
    db_empresa.endereco = empresa.endereco
    db_empresa.email = empresa.email
    db_empresa.telefone = empresa.telefone
    db.commit()
    db.refresh(db_empresa)
    db.close()
    return db_empresa

@app.delete("/empresas/{empresa_id}")
def delete_empresa(empresa_id: int):
    db = SessionLocal()
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    db.delete(db_empresa)
    db.commit()
    db.close()
    return {"detail": "Empresa deletada com sucesso"}

@app.post("/obrigacoes/", response_model=ObrigacaoAcessoriaOut)
def create_obrigacao(obrigacao: ObrigacaoAcessoriaCreate):
    db = SessionLocal()
    db_obrigacao = ObrigacaoAcessoria(
        nome=obrigacao.nome,
        periodicidade=obrigacao.periodicidade,
        empresa_id=obrigacao.empresa_id
    )
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    db.close()
    return db_obrigacao

@app.get("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaOut)
def read_obrigacao(obrigacao_id: int):
    db = SessionLocal()
    obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    db.close()
    if obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")
    return obrigacao

@app.put("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaOut)
def update_obrigacao(obrigacao_id: int, obrigacao: ObrigacaoAcessoriaUpdate):
    db = SessionLocal()
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")
    db_obrigacao.nome = obrigacao.nome
    db_obrigacao.periodicidade = obrigacao.periodicidade
    db_obrigacao.empresa_id = obrigacao.empresa_id
    db.commit()
    db.refresh(db_obrigacao)
    db.close()
    return db_obrigacao

@app.delete("/obrigacoes/{obrigacao_id}")
def delete_obrigacao(obrigacao_id: int):
    db = SessionLocal()
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")
    db.delete(db_obrigacao)
    db.commit()
    db.close()
    return {"detail": "Obrigação acessória deletada com sucesso"}

