class HelperValue(OwnedObject, TableModel):
	""" Helper values are the values a field can take """
	value = TextField()
	field_name = TextField()
	description = TextField(default="")