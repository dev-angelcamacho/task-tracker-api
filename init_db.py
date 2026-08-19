from database import SessionLocal
import models
import security

def create_admin():
    db = SessionLocal()
    admin_email = "angelcamachotoro@gmail.com"
    
    # Verifica si el admin ya existe para evitar duplicados
    user = db.query(models.UserModel).filter(models.UserModel.email == admin_email).first()
    if not user:
        hashed_password = security.hash_password("dev123")
        admin_user = models.UserModel(
            email=admin_email,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ Usuario Administrador creado exitosamente.")
    else:
        print("ℹ️ El usuario Administrador ya existe.")
    db.close()

if __name__ == "__main__":
    create_admin()