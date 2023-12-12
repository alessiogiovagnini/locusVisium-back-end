import pathlib

from src.endpoints import app
from src.mongoQuery import make_index

if __name__ == '__main__':
    port = 3000
    host = "0.0.0.0"
    make_index()  # even if the index already exist it won't create a new one, but if the value is different it will
    # trow and error
    if not pathlib.Path("data").is_dir():
        pathlib.Path("data").mkdir()
    app.run(port=port, host=host)

