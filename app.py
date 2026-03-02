import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    is_prod = os.environ.get('FLASK_ENV') == 'production'
    app.run(debug=not is_prod)
