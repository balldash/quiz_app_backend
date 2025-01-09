from flask import Blueprint, request, jsonify
from ..models import Question, Quiz, db

question_bp = Blueprint('questions', __name__)


# Get all questions
@question_bp.route('/questions', methods=['GET'])
def get_questions():
    # Pagination parameters
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Filtering parameters
    quiz_id = request.args.get('quiz_id', type=int)

    # Query base
    query = Question.query

    # Apply filtering
    if quiz_id:
        query = query.filter_by(quiz_id=quiz_id)

    # Apply pagination
    paginated_questions = query.paginate(page=page, per_page=per_page,
                                         error_out=False)

    # Build response
    return jsonify({
        "questions":
        [question.to_dict() for question in paginated_questions.items],
        "total": paginated_questions.total,
        "page": paginated_questions.page,
        "per_page": paginated_questions.per_page,
        "pages": paginated_questions.pages
    }), 200


# Get a single question by ID
@question_bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    return jsonify(question.to_dict()), 200


# Create a new question
@question_bp.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json()
    try:
        # Validate quiz_id
        quiz = Quiz.query.get(data['quiz_id'])
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404

        # Create the question
        new_question = Question(
            text=data['text'],
            correct_answer=data['correct_answer'],
            quiz_id=data['quiz_id']
        )
        db.session.add(new_question)
        db.session.commit()

        return jsonify({
            "message": "Question created successfully",
            "data": new_question.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500


# Update a question
@question_bp.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    data = request.get_json()
    try:
        question.text = data.get('text', question.text)
        question.correct_answer = data.get(
            'correct_answer', question.correct_answer)

        db.session.commit()
        return jsonify({
            "message": "Question updated successfully",
            "data": question.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500


# Delete a question
@question_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    try:
        db.session.delete(question)
        db.session.commit()
        return jsonify({"message": "Question deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500
