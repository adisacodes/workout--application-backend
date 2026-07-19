from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


# ---------- Workouts ----------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify([{'id': w.id, 'date': str(w.date)} for w in workouts]), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify({'id': workout.id, 'date': str(workout.date)}), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    workout = Workout(
        date=data.get('date'),
        duration_minutes=data.get('duration_minutes'),
        notes=data.get('notes')
    )
    db.session.add(workout)
    db.session.commit()
    return jsonify({'id': workout.id}), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    db.session.delete(workout)
    db.session.commit()
    return jsonify({}), 204


# ---------- Exercises ----------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([{'id': e.id, 'name': e.name} for e in exercises]), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify({'id': exercise.id, 'name': exercise.name}), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    exercise = Exercise(
        name=data.get('name'),
        category=data.get('category'),
        equipment_needed=data.get('equipment_needed', False)
    )
    db.session.add(exercise)
    db.session.commit()
    return jsonify({'id': exercise.id}), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({}), 204


# ---------- Workout <-> Exercise linking ----------

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    if not workout or not exercise:
        return jsonify({'error': 'Workout or Exercise not found'}), 404

    data = request.get_json()
    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )
    db.session.add(workout_exercise)
    db.session.commit()
    return jsonify({'id': workout_exercise.id}), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)