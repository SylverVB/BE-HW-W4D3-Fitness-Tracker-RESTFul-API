# Lesson 2: Assignment | Building RESTFul APIs

# 1. Managing a Fitness Center Database

# Objective:
# The aim of this assignment is to develop a Flask application to manage a fitness center's database, focusing 
# on interacting with the Members and WorkoutSessions tables. This will enhance your skills in building RESTful 
# APIs using Flask, handling database operations, and implementing CRUD functionalities.

# Task 1: Setting Up the Flask Environment and Database Connection

# Create a new Flask project and set up a virtual environment.
# Install necessary packages like Flask, Flask-Marshmallow, and MySQL connector.
# Establish a connection to your MySQL database.
# Use the Members and WorkoutSessions tables used on previous Lessons

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error
from datetime import date, time, timedelta

app = Flask(__name__)
app.json.sort_keys = False

ma = Marshmallow(app)


class MemberSchema(ma.Schema): 
    member_id = fields.Int(dump_only=True)
    name = fields.String(required=True) 
    email = fields.String(required=True)
    phone = fields.String(required=True)
    credit_card = fields.String(required=True)

    class Meta:
        fields = ("member_id", "name", "email", "phone_number", "credit_card")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

db_name = "fitness_tracker"
user = "root"
password = "your_password"
host = "localhost"

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )
       
        if conn.is_connected():
            print("Connected to db successfully (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
            return conn
        
    except Error as e:
        print(f"Error: {e}")
        return None
    

# Task 2: Implementing CRUD Operations for Members

# Create Flask routes to add, retrieve, update, and delete members from the Members table.
# Use appropriate HTTP methods: POST for adding, GET for retrieving, PUT for updating, and DELETE for deleting members.
# Ensure to handle any errors and return appropriate responses.
# using flask's dynamic routing to receive parameters through the url

@app.route('/members', methods=["POST"])
def add_member():

    try:
        member_data = member_schema.load(request.json)
        print(member_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    name = member_data['name']
    email = member_data['email']
    phone = member_data['phone_number']
    credit_card = member_data['credit_card']
    
    new_member = (name, email, phone, credit_card)
    print(new_member)
    
    query = "INSERT INTO Members (name, email, phone_number, credit_card) VALUES (%s, %s, %s, %s)"
 
    cursor.execute(query, new_member)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "New member was added successfully"}), 201

    
@app.route("/members", methods=["GET"])
def get_members():
   
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    
        query = "SELECT * FROM Members"
        cursor.execute(query)
        members = cursor.fetchall()
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return members_schema.jsonify(members)


@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try: 
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        name = member_data['name']
        email = member_data['email']
        phone = member_data['phone_number']
        credit_card = member_data['credit_card']

        query = "UPDATE Members SET name = %s, email = %s, phone_number = %s, credit_card = %s WHERE member_id = %s"
        updated_customer = (name, email, phone, credit_card, id)
        cursor.execute(query, updated_customer)
        conn.commit()

        return jsonify({"message": "Member details updated successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500 
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        member_to_remove = (id,)

        query = "SELECT * FROM Members WHERE member_id = %s"
        cursor.execute(query, member_to_remove)
        customer = cursor.fetchone()
        
        if not customer:
            return jsonify({"message": "Customer not found"}), 404

    
        query = "SELECT * FROM Workouts WHERE member_id = %s"
        cursor.execute(query, member_to_remove)
        workouts = cursor.fetchall()
        if workouts:
            return jsonify({"message": "Member has associated workout sessions, cannot delete"}), 400 
       
        query = "DELETE FROM Members WHERE member_id = %s"
        cursor.execute(query, member_to_remove)
        conn.commit()

        return jsonify({"message": "Member Removed Successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# Task 3: Managing Workout Sessions

# Develop routes to schedule, update, and view workout sessions.
# Implement a route to retrieve all workout sessions for a specific member.
# Expected Outcome:
# A comprehensive set of endpoints for scheduling and viewing workout sessions, 
# with the ability to retrieve detailed information about each session.
            
        
class WorkoutSessionSchema(ma.Schema):
    workout_id = fields.Int(dump_only=True) 
    session = fields.String(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    member_id = fields.Int(required=True)

    class Meta:
        fields = ("workout_id", "session", "date", "time", "member_id") 

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True) 

@app.route('/workouts', methods=["POST"])
def add_session():

    workout_session_data = workout_session_schema.load(request.json)
    print(workout_session_data)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    session = workout_session_data['session']
    date = workout_session_data['date']
    time = workout_session_data['time']
    member_id = workout_session_data['member_id']
 
    new_session = (session, date, time, member_id)
    print(new_session)
 
    query = "INSERT INTO Workouts (session, date, time, member_id) VALUES (%s, %s, %s, %s)"
 
    cursor.execute(query, new_session) 
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "New session was added successfully"}), 201


@app.route("/workouts/<int:workout_id>", methods=["PUT"])
def update_workout(workout_id):
    try:
        workout_session_data = workout_session_schema.load(request.json)
    
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database Connection Failed"}), 500
    
    try:
        cursor = conn.cursor()
        
        session = workout_session_data['session']
        date = workout_session_data['date']
        time = workout_session_data['time']
        member_id = workout_session_data['member_id']

        query = "UPDATE Workouts SET session = %s, date = %s, time = %s, member_id = %s WHERE workout_id = %s"
        updated_session = (session, date, time, member_id, workout_id)
        cursor.execute(query, updated_session)
        conn.commit()
        
        return jsonify({"message": "Workout session was updated successfully"}), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()


@app.route("/workouts", methods=["GET"])
def view_sessions():
  
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Workouts"
        cursor.execute(query)

        workouts = cursor.fetchall()
        print("Fetched workouts data:", workouts)

        # Convert datetime.timedelta to datetime.time
        for workout in workouts:
            if isinstance(workout['time'], timedelta):
                total_seconds = int(workout['time'].total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                workout['time'] = time(hour=hours, minute=minutes, second=seconds)

    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return workout_sessions_schema.jsonify(workouts)


@app.route("/workouts/member/<int:member_id>", methods=["GET"])
def view_sessions_by_member_id(member_id):
  
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    
        query = "SELECT * FROM Workouts WHERE member_id = %s"
        cursor.execute(query, (member_id,))
    
        workouts = cursor.fetchall()

        for workout in workouts:
            if isinstance(workout['time'], timedelta):
                total_seconds = int(workout['time'].total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                workout['time'] = time(hour=hours, minute=minutes, second=seconds)

    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return workout_sessions_schema.jsonify(workouts)

@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database Connection Failed"}), 500
    
    try:
        cursor = conn.cursor()
        
        # Checking if the workout session exists
        cursor.execute("SELECT * FROM Workouts WHERE workout_id = %s", (workout_id,))
        workout = cursor.fetchone()
        if not workout:
            return jsonify({"error": "Workout session not found"}), 404
        
        # Deleting the workout session
        cursor.execute("DELETE FROM Workouts WHERE workout_id = %s", (workout_id,))
        conn.commit()
        
        return jsonify({"message": "Workout session was deleted successfully"}), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True) 