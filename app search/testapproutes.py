from flask import Flask

app = Flask(__name__)

# Define functions associated with routes
def function1():
    return "Function 1 called."

def function2():
    return "Function 2 called."

# Define 10 routes with associated functions
@app.route('/route1')
def route1():
    return function1()

@app.route('/route1/alt')
def route1_alt():
    return function2()

@app.route('/route2')
def route2():
    return function1()

@app.route('/route2/alt')
def route2_alt():
    return function2()

@app.route('/route3')
def route3():
    return function1()

@app.route('/route3/alt')
def route3_alt():
    return function2()

@app.route('/route4')
def route4():
    return function1()

@app.route('/route4/alt')
def route4_alt():
    return function2()

@app.route('/route5')
def route5():
    return function1()

@app.route('/route5/alt')
def route5_alt():
    return function2()

if __name__ == '__main__':
    app.run(debug=True)
