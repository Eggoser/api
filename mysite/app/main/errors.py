from . import main


@main.app_errorhandler(404)
def two(e):
	return "Not Found 404", 404

@main.app_errorhandler(500)
def one(e):
	return "Interal Server Error", 500

@main.app_errorhandler(400)
def three(e):
	return "Bad request 400", 400

@main.app_errorhandler(405)
def four(e):
	return "Method Not Allowed 405", 405

	