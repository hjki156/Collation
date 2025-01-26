import Flask from flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world';


def main():

	return

if __name__ == '__main__':
    app.run(port=2013)
