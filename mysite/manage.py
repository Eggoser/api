from app import create_app, db
from config import DefaultConfig
from tests import MyTest
import warnings
import sys

warnings.filterwarnings("ignore")

app = create_app(DefaultConfig)


if len(sys.argv) > 1 and sys.argv[1] == "runtest":
    test = MyTest(app.test_client())
    test.run()
else:
    if __name__ == '__main__':
        app.run(debug=True, host="0.0.0.0", port=8080)