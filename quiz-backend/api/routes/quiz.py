from flask import Blueprint, request, jsonify
from ..models import Quiz, Question, db

quiz_bp = Blueprint('quizzes', __name__)


# Get all quizzes
@quiz_bp.route('/quizzes', methods=['GET'])
def get_quizzes():
    # Pagination parameters
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Query and paginate quizzes
    paginated_quizzes = Quiz.query.paginate(page=page, per_page=per_page,
                                            error_out=False)

    # Build response
    return jsonify({
        "quizzes": [quiz.to_dict() for quiz in paginated_quizzes.items],
        "total": paginated_quizzes.total,
        "page": paginated_quizzes.page,
        "per_page": paginated_quizzes.per_page,
        "pages": paginated_quizzes.pages
    }), 200


# Get a single quiz by ID
@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404
    return jsonify(quiz.to_dict()), 200


# Create a new quiz
@quiz_bp.route('/quizzes', methods=['POST'])
def create_quiz():
    data = request.get_json()
    try:
        # Create the quiz
        new_quiz = Quiz(
            title=data['title']
        )
        db.session.add(new_quiz)

        # Add questions if provided
        if 'questions' in data:
            for question_data in data['questions']:
                new_question = Question(
                    text=question_data['text'],
                    correct_answer=question_data['correct_answer'],
                    quiz=new_quiz
                )
                db.session.add(new_question)

        db.session.commit()
        return jsonify({
            "message": "Quiz created successfully",
            "data": new_quiz.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500


# Update a quiz
@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    data = request.get_json()
    try:
        quiz.title = data.get('title', quiz.title)

        # Update questions if provided
        if 'questions' in data:
            for question_data in data['questions']:
                question = Question.query.get(question_data['id'])
                if question:
                    question.text = question_data.get('text', question.text)
                    question.correct_answer = question_data.get(
                        'correct_answer', question.correct_answer)

        db.session.commit()
        return jsonify({
            "message": "Quiz updated successfully",
            "data": quiz.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500


# Delete a quiz
@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404
    try:
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({"message": "Quiz deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500
