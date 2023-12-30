from flask import jsonify


class ErrorHandler:
    def __init__(self, app):
        self.app = app

        # Register error handlers
        self.app.register_error_handler(400, self.handle_bad_request)
        self.app.register_error_handler(500, self.handle_server_error)

    def handle_bad_request(self, error):
        response = jsonify({'error': 'Bad Request', 'message': str(error)})
        response.status_code = 400
        return response

    def handle_server_error(self, error):
        response = jsonify({'error': 'Server Error', 'message': str(error)})
        response.status_code = 500
        return response