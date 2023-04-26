import os
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

conn = 'sqlite:///'+os.path.join(BASE_DIR, 'blog.db')

engine = create_engine(conn, echo=True)

Base = declarative_base()

class Parent(Base):
    __tablename__="parents"
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(40), nullable=False)
    child = relationship('Child', back_populates="parent", uselist=False, cascade="all, delete")
       
    def __repr__(self):
        return f"<Parent {self.name}>"
    
    
class Child(Base):
    __tablename__="children"
    id = Column(Integer(), primary_key=True)
    name = Column(String(200), nullable=False)
    parent_id = Column(Integer(), ForeignKey('parents.id', ondelete="CASCADE"))
    parent = relationship("Parent", back_populates="child")
    
    def __repr__(self):
        return f"<Child {self.name}>"    
    

session = sessionmaker()(bind=engine)

"""
        Você pode entender o atributo backref como sendo um atributo na tabela que 
        você especificou como a outra parte do relacionamento, no seu caso é a tabela Child.
        Se torna muito útil na hora de fazer querys no relacionamento, pois a partir dessa declaração, 
        você poderá fazer uma query como Child.parents, para saber quais usuários estão associados a um determinado Child.
        Note que esse relacionamento pode ser feito em qualquer uma das duas tabelas, 
        vai depender apenas do que faz mais sentido para o seu caso de uso. 
        Caso você queira fazer a query inversa, (Parents.child), 
        para saber quais usuários estão associados a um determinado elemento, 
        basta adicionar o mesmo tipo de atributo na tabela Instrumento:
"""

"""
Um exemplo no stackoverflow informando o que é backref

Pergunta:
Alguém pode explicar os conceitos dessas duas ideias e como 
elas se relacionam com a criação de relacionamentos entre tabelas? 
Eu realmente não consigo encontrar nada que explique isso claramente
e a documentação parece ter muito jargão para entender em conceitos fáceis.
Por exemplo, neste exemplo de relacionamento um para muitos na documentação:

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="children")
    
    Resposta: 
    
backref é um atalho para configurar ambos parent.childrene child.parent relationships
em um local apenas na classe pai ou filha (não em ambas). Ou seja, ao invés de ter

children = relationship("Child", back_populates="parent")  # on the parent class

e

parent = relationship("Parent", back_populates="children")  # on the child class
você só precisa de um desses:

children = relationship("Child", backref="parent")  # only on the parent class

ou

parent = relationship("Parent", backref="children") 

# only on the child class
children = relationship("Child", backref="parent")criará o .parentrelacionamento na 
classe filha automaticamente. Por outro lado, se você usar, back_populatesdeverá criar 
explicitamente os relationships nas classes pai e filho.

Por que o relacionamento () vai dentro da classe pai enquanto o ForeignKey vai dentro da classe filha?

Como eu disse acima, se você usar back_populates, ele precisa ir para as classes pai e filho
. Se você usar backref, ele precisa ir em apenas um deles.
ForeignKeyprecisa ir para a classe filha, não importa onde seja relationshipcolocado,
este é um conceito fundamental de bancos de dados relacionais.

E o que ter back_populates faz exatamente um com o outro?

back_populatesinforma cada relacionamento sobre o outro, para que sejam mantidos em sincronia. Por exemplo se você fizer

p1 = Parent()
c1 = Child()
p1.children.append(c1)
print(p1.children)  # will print a list of Child instances with one element: c1
print(c1.parent)  # will print Parent instance: p1
Como você pode ver, p1foi definido como pai c1mesmo quando você não o definiu explicitamente.

Ter a colocação de qual classe a função de relacionamento () existe é importante?

Isso só se aplica a backref, e não, você pode colocar o relacionamento na classe pai
( children = relationship("Child", backref="parent")) ou na classe filha ( parent = relationship("Parent", backref="children"))
e ter exatamente o mesmo efeito

"""