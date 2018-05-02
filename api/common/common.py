from .errors import NotFoundError
import onb

def require_anonymous_enabled(fct):
	if onb.conf.anonymousLogin:
		return fct
	else:
		raise NotFoundError

def require_search_enabled(fct):
	if onb.conf.searchEnabled:
		return fct
	else:
		raise NotFoundError