from .errors import NotFoundError
import onb

def NotFoundFunction():
	raise NotFoundError

def require_anonymous_enabled(fct):
	if onb.conf.anonymousLogin:
		return fct
	else:
		return NotFoundFunction

def require_search_enabled(fct):
	if onb.conf.searchEnabled:
		return fct
	else:
		return NotFoundFunction