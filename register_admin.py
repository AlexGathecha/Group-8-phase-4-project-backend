from app import app, db
from app import Admin

def register_admin():
    with app.app_context():
        db.create_all()
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")
        admin = Admin(email=email, password=password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin {email} registered successfully.")

if __name__ == '__main__':
    register_admin()
