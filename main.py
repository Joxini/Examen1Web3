# Call external libraries
import psycopg2
import locale
from flask import Flask, jsonify, abort, make_response, request
# Create default flask application
locale.setlocale(locale.LC_ALL, "es")
app = Flask(__name__)
# ================================================================
# D A T A A C C E S S C O D E
# ================================================================
# Function to execute data modification sentence
def execute(auxsql):
 data = None
 try:
     # Create data access object
     conex = psycopg2.connect(host='10.90.28.173',
     database='demo',
     user='postgres',
     password='utn')
     # Create local cursor to SQL executor
     cur = conex.cursor()
     # Execute SQL sentence
     cur.execute(auxsql)
     # Retrieve data if exists
     data = cur.fetchall()
     # close cursor
     cur.close()
 except (Exception, psycopg2.DatabaseError) as error:
    print(error)
 finally:
    if conex is not None:
        conex.close()
        print('Close connection.')
 # Return data
 return data
# ================================================================
# A P I R E S T F U L S E R V I C E
# ================================================================
# -----------------------------------------------------
# Error support section
# -----------------------------------------------------
@app.errorhandler(400)
def bad_request(error):
 return make_response(jsonify({'error': 'Bad request....!'}), 400)
@app.errorhandler(401)
def unauthorized(error):
 return make_response(jsonify({'error': 'Unauthorized....!'}), 401)
@app.errorhandler(403)
def forbiden(error):
 return make_response(jsonify({'error': 'Forbidden....!'}), 403)
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found....!'}), 404)

# Get Aircraft
@app.route('/airports/<string:lala>', methods=['GET'])
def get_aircraft(lala):
 resu = execute("select airport_code,airport_name,city,coordinates,timezone from airports_data")
 if resu != None:
     salida = {"status_code": 200,
     "status": "OK",
     "data":[]
    }
     for cod, nombre, ciudad, coor, timz in resu:
        salida["data"].append({
         "code": cod,
         "name": nombre[lala],
        "city": ciudad[lala],
            "coordinates":coor,
            "timezone":timz,
         })
 else:
    abort(404)
 return jsonify({'airPorts': salida}), 200

@app.route('/pasajeros', methods=['GET'])
def get_passenger():
    ress = execute('select t.passenger_id, t.passenger_name,t.contact_data,h.fare_conditions,f.flight_id,f.departure_airport, f.arrival_airport,f.actual_departure, f.actual_arrival  from ticket_flights h join tickets t on t.ticket_no = h.ticket_no join flights f on f.flight_id = h.flight_id LIMIT 100;')
    if ress !=None:
        salida = {"status_code": 200,
                  "status": "OK",
                  "data": []
                  }
        for id,nombre,info,cond,id2,ai1,ai2,hor1,hor2 in ress:
            salida["data"].append({
                "Passenger_ID":id,
                "Passenger_name":nombre,
                "Contac_Info":info,
                "Class":cond,
                "Fligths_ID":id2,
                "Airport_of_Departure":ai1,
                "Airport_of_Arrival":ai2,
                "Hour_of_Departure":hor1,
                "Hour_of_Arrival":hor2
            })
    else:
        abort(404)
    return jsonify({'pasajeros': salida}), 200

@app.route('/flight', methods=['GET'])
def get_flights():
    quer = execute('select f.flight_id,f.aircraft_code,(select count(seat_no) from seats where aircraft_code = f.aircraft_code), (select count(ticket_no) from ticket_flights where flight_id = f.flight_id) from flights f join ticket_flights t on t.flight_id = f.flight_id join aircrafts_data a on a.aircraft_code=f.aircraft_code group BY f.flight_id limit 100')
    if quer !=None:
        salida = {"status_code": 200,
                  "status": "OK",
                  "data": []
                  }
        for num,mod,asi,ocu in quer:
            salida["data"].append({
                "Flight_number" :num,
                "Plane_model" : mod,
                "Number_of_seats": asi,
                "Ocupied_seats": ocu
            })
    else:
            abort(404)
    return jsonify({'Flights': salida}), 200
# -----------------------------------------------------
# Create thread app
# -----------------------------------------------------
if __name__ == '__main__':
 app.run(host='10.90.30.24', port=5001, debug=True)