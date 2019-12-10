from flask import Flask, jsonify, request, abort
from goodDAO import goodDAO

app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)

#@app.route('/')
#def index():
#    return "Hello, World!"

#curl "http://127.0.0.1:5000/goods"
@app.route('/goods')
def getAll():
    #print("in getall")
    results = goodDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/goods/2"
@app.route('/goods/<int:id>')
def findById(id):
    foundGood = goodDAO.findByID(id)

    return jsonify(foundGood)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Name\":\"hello\",\"Flavor\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/goods
@app.route('/goods', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    good = {
        "name": request.json['name'],
        "flavor": request.json['flavor'],
        "price": request.json['price'],
    }
    values =(good["name"],good["flavor"],good["price"])
    newId = goodDAO.create(values)
    good['id'] = newId
    return jsonify(good)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Name\":\"hello\",\"Flavor\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/books/1
@app.route('/goods/<int:id>', methods=['PUT'])
def update(id):
    foundGood = goodDAO.findByID(id)
    if not foundGood:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['price']) is not int:
        abort(400)

    if 'name' in reqJson:
        foundGood['name'] = reqJson['name']
    if 'flavor' in reqJson:
        foundGood['flavor'] = reqJson['flavor']
    if 'price' in reqJson:
        foundGood['price'] = reqJson['price']
    values = (foundGood['name'],foundGood['flavor'],foundGood['Price'],foundGood['id'])
    goodDAO.update(values)
    return jsonify(foundGood)
        

    

@app.route('/goods/<int:id>' , methods=['DELETE'])
def delete(id):
    goodDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)