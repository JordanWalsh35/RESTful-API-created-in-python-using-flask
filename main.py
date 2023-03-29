from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
# db.create_all()


# Define the Car model for the database
class CarModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	brand = db.Column(db.String(50), nullable=False)
	model = db.Column(db.String(50), nullable=False)
	year = db.Column(db.Integer, nullable=False)
	bhp = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Car(brand = {self.brand}, model = {self.model}, year = {self.year}, bhp = {self.bhp})"



post_args = reqparse.RequestParser()
post_args.add_argument("brand", type=str, required=True, help="Brand of the car is required")
post_args.add_argument("model", type=str, required=True, help="Model of the car is required")
post_args.add_argument("year", type=int, required=True, help="Year of the car is required")
post_args.add_argument("bhp", type=int, required=True, help="BHP of the car is required")

patch_args = reqparse.RequestParser()
patch_args.add_argument("brand", type=str, help="Brand of the car")
patch_args.add_argument("model", type=str, help="Model of the car")
patch_args.add_argument("year", type=int, help="Year of the car")
patch_args.add_argument("bhp", type=int, help="BHP of the car")


resource_fields = {
	'id': fields.Integer,
	'brand': fields.String,
	'model': fields.String,
	'year': fields.Integer,
	'bhp': fields.Integer
}


# Here we define our endpoints for our Car class
class Car(Resource):
	@marshal_with(resource_fields)
	def get(self, car_id):
		result = CarModel.query.filter_by(id=car_id).first()
		if not result:
			abort(404, message="Could not find a car with that ID. Please try again.")
		return result
	

	@marshal_with(resource_fields)
	def post(self, car_id):
		args = post_args.parse_args()
		result = CarModel.query.filter_by(id=car_id).first()
		if result:
			abort(409, message="This ID is already taken!")

		car = CarModel(id=car_id, brand=args['brand'], model=args['model'], year=args['year'], bhp=args['bhp'])
		db.session.add(car)
		db.session.commit()
		return car, 201
	

	@marshal_with(resource_fields)
	def patch(self, car_id):
		args = patch_args.parse_args()
		result = CarModel.query.filter_by(id=car_id).first()
		if not result:
			abort(404, message="Car does not exist, cannot update.")

		if args['brand']:
			result.brand = args['brand']
		if args['model']:
			result.model = args['model']
		if args['year']:
			result.year = args['year']
		if args['bhp']:
			result.bhp = args['bhp']
		
		db.session.commit()
		return result
	
	
	@marshal_with(resource_fields)
	def put(self, car_id):
		args = patch_args.parse_args()
		result = CarModel.query.filter_by(id=car_id).first()
		if not result :
			abort(404, message="Car does not exist, cannot update.")
		
		if args['brand'] and args['model'] and args['year'] and args['bhp']:
			result.brand = args['brand']
			result.model = args['model']
			result.year = args['year']
			result.bhp = args['bhp']
		else:
			abort(404, message="Put needs all arguments in order to update.")
		
		db.session.commit()
		return result


	@marshal_with(resource_fields)
	def delete(self, car_id):
		result = CarModel.query.filter_by(id=car_id).first()
		if not result:
			abort(404, message="There isn't a car with that ID available. Please try again.")
		db.session.delete(result)
		db.session.commit()
		return '', 204



# Define a new class for retrieving all Cars
class Cars(Resource):
	@marshal_with(resource_fields)
	def get(self):
		results = CarModel.query.all()
		if not results:
			abort(404, message="There are no cars in this database!")
		return results


api.add_resource(Car, "/car/<int:car_id>")
api.add_resource(Cars, "/cars/")


if __name__ == "__main__":
	app.run(debug=True)