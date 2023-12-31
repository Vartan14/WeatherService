from handlers.error_handler import ErrorHandler


class FlaskAppWrapper:
    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)
        self.error_handler = ErrorHandler(app)

    def configs(self, **configs):
        for config, value in configs.items():
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None, *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)
