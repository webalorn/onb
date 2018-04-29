from werkzeug.routing import BaseConverter
from sqldb.models.gameobject import sqlModels
from api.common.errors import NotFoundError
import onb

class ModelConverter(BaseConverter):
	def to_python(self, value):
		if value in sqlModels:
			return sqlModels[value]
		raise NotFoundError

	def to_url(self, value):
		return value.modelClass

url_converters = {
	'model': ModelConverter,
}