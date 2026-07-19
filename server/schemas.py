from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()


class ExerciseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    category = fields.String(required=True)
    equipment_needed = fields.Boolean()

    class Meta:
        fields = ('id', 'name', 'category', 'equipment_needed')


class WorkoutExerciseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer()
    sets = fields.Integer()
    duration_seconds = fields.Integer()
    exercise = fields.Nested(ExerciseSchema, only=('id', 'name', 'category'))

    class Meta:
        fields = ('id', 'workout_id', 'exercise_id', 'reps', 'sets', 'duration_seconds', 'exercise')


class WorkoutSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer()
    notes = fields.String()
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, exclude=('workout_id',))

    class Meta:
        fields = ('id', 'date', 'duration_minutes', 'notes', 'workout_exercises')


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()