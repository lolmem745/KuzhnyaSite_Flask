from app import create_app

def test_db_url():
    app = create_app()
    with app.app_context():
        print("Current SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])

if __name__ == "__main__":
    test_db_url()
