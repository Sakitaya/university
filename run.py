from app.microservice_main.src.main import app
from app.microservice_stock.stock import app1
from app.microservice_user.user import app2

if __name__ == "__main__":
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    app1.run(host='0.0.0.0')

if __name__ == "__main__":
    app2.run(host='0.0.0.0')