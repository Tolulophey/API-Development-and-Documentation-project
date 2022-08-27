import os
from flask import Flask, request, abort, jsonify
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # CORS(app, resources={r"*/api/*": {origins: '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    # CORS Headers
    @app.after_request
    def after_request(response):
        # response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, PUT, PATCH, POST, DELETE, OPTIONS")
        return response

    # Endpoints

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def show_categories():
        data = {}
        try:
            categories = Category.query.order_by(Category.id).all()
            for category in categories:
                data[category.id] = category.type

            return jsonify({
                "categories": data
            })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions")
    def show_questions():
        data = {}
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.order_by(Category.id).all()
        for category in categories:
            data[category.id] = category.type
        if len(current_questions) == 0:
            abort(404)
        return jsonify(
            {
                "questions": current_questions,
                "totalQuestions": len(selection),
                "categories": data,
                "currentCategory": data[current_questions[0]['category']]
            }
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": question.id
                }
            )
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions", methods=['POST'])
    def add_or_search_question():
        body = request.get_json()

        question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)
        search = body.get("searchTerm", None)
        data = {}
        try:
            if search:
                categories = Category.query.order_by(Category.id).all()
                for category in categories:
                    data[category.id] = category.type
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search)))
                current_questions = paginate_questions(request, selection)
                if current_questions == []:
                    return jsonify(
                        {
                            "questions": current_questions,
                            "totalQuestions": len(selection.all()),
                        }
                    )
                else:
                    return jsonify(
                        {
                            "questions": current_questions,
                            "totalQuestions": len(selection.all()),
                            "currentCategory": data[current_questions[0]['category']]
                        }
                    )
            else:
                question = Question(
                    question=question, answer=answer, category=category, difficulty=difficulty)
                question.insert()
                return jsonify(
                    {
                        "success": True,
                        "created": question.id
                    }
                )
        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def get_category_questions(category_id):
        try:
            selection = Question.query.filter(
                Question.category == category_id).all()
            current_questions = paginate_questions(request, selection)
            category = Category.query.get(category_id)
            return jsonify(
                {
                    "questions": current_questions,
                    "totalQuestions": len(selection),
                    "currentCategory": category.type
                }
            )
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=['POST'])
    def create_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        category_type = body.get('quiz_category', None)
        data = {}
        try:
            
            if category_type == 'click':
                questions = Question.query.all()
            else:
                categories = Category.query.order_by(Category.id).all()
                for category in categories:
                    data[category.type] = category.id
                category_id = data[category_type]
                questions = Question.query.filter(Question.category == category_id).all()
            questions_id = [question.id for question in questions]
            unique_id = [id for id in questions_id if id not in previous_questions]
            if len(unique_id) == 0:
                return jsonify({})
            random_id = random.choice(unique_id)
            random_question = Question.query.filter(
                Question.id == random_id).one_or_none()
            
            return jsonify({
                'question': random_question.format()
            })
        except:
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
                "success": False,
                "error": 400,
                "message": "bad request",
                }), 400)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found",
                }), 404)

    @app.errorhandler(405)
    def not_allowed(error):
        return (jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed",
                }), 405)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable",
                }), 422)

    @app.errorhandler(500)
    def unprocessable(error):
        return (jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error",
                }), 500)
    return app
