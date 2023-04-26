from config_db import Parent,Child,session

class Crud():

    @staticmethod
    def cadastrar_parent():
        new_user=Parent(
            name="testuser"
        )
    
        new_user2=Parent(
          name="testuser2"
        )

        session.add_all([new_user, new_user2])
        session.commit()


    @staticmethod
    def cadastrar_child():
    
      parent1 = session.query(Parent).filter_by(id=1).one_or_none()      
      child = Child(
        name="Child 2",
        parent=parent1
      )

      session.add(child)
      session.commit()
      
      print(parent1.child)
      
    def deletar_parent():
      parent = session.query(Parent).filter_by(id=1).first()
      session.delete(parent)
      session.commit()
      
      print(parent)
      print(parent.child)
    
    def mostrar():
      print(f"Parent {session.query(Parent).all()}")
      print(f"Childre {session.query(Child).all()}")


