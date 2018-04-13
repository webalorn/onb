class UserAlreadyExistsError(Exception):
	pass

class ResourceDoesNotExist(Exception):
	pass

class UserAuthError(Exception):
	pass

class NotFoundError(Exception):
	pass

class BadRequestError(Exception):
	pass

errors = {
	'UserAlreadyExistsError': {
		'message': "A user with that username already exists",
		'status': 409,
	},
	'ResourceDoesNotExist': {
		'message': "A resource with that ID does not exists",
		'status': 404,
	},
	'UserAuthError': {
		'message': "Auth failed",
		'status': 400,
	},
	'NotFoundError': {
		'message': "Ressource not found",
		'status': 404,
	},
	'BadRequestError': {
		'message': "Bad request",
		'status': 400,
	},
}