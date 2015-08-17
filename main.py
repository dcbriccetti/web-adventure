from flask import Flask, render_template, redirect, session
from invitem import InvItem
from place import Place

STARTING_PLACE_INDEX = 0
app = Flask(__name__)

@app.route("/")
def index():
    session['placeIndex'] = STARTING_PLACE_INDEX
    session['inventory'] = []
    return redirect(places[STARTING_PLACE_INDEX].path)

@app.route("/<newPath>")
def showPlace(newPath):
    placeIndex = session.get('placeIndex', STARTING_PLACE_INDEX)
    place = places[placeIndex]
    newDest = placesByPath.get(newPath)
    if newDest in transitions[place]:
        place = newDest
        session['placeIndex'] = places.index(place)
    carryingItems = [itemsByShortName[shortName] for shortName in session['inventory']]
    availableItems = [item for item in place.items if item.shortName not in session['inventory']]
    availableItems.sort(key=lambda i: i.title)
    return render_template("advent.html", place=place, destinations=transitions[place],
        carryingItems=carryingItems, availableItems=availableItems)

@app.route("/getItem/<item>")
def getItem(item):
    place = places[session['placeIndex']]
    inv = session['inventory']
    if item not in inv:
        inv.append(item)
    return redirect(place.path)

paint = InvItem('paint', 'White spray paint')
invItems = (paint,)
itemsByShortName = {i.shortName: i for i in invItems}

pumpkin = Place('pumpkin', 'Arduino-Powered Pumpkin',
    audio='135498__compusician__halloween-003-wav-120b.wav', items=(paint,))
monster = Place('monster', 'Flying Spaghetti Monster')
camera  = Place('camera',  'Government Spy Camera')
trail   = Place('trail',   'Mountain Bike Trail')

places = (pumpkin, monster, camera, trail)
placesByPath = {p.path: p for p in places}

transitions = {
    pumpkin: (monster,),
    monster: (pumpkin, camera),
    camera : (monster, trail),
    trail  : (camera,),
}

app.secret_key = 'the dog flies at noon'
app.run(debug=True)
