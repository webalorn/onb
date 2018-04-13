import onb, types

def api_route(self, *args, **kwargs):
	def wrapper(cls):
		self.add_resource(cls, *args, **kwargs)
		return cls
	return wrapper

onb.api.route = types.MethodType(api_route, onb.api)