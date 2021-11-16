from app.microservice_main.src.main import app
from app.microservice_payment.payment import app3
from app.microservice_stock.stock import app1
from app.microservice_user.user import app2

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    app1.run(host='0.0.0.0', port=5000)
    app2.run(host='0.0.0.0', port=5001)
    app3.run(host='0.0.0.0', port=5002)

