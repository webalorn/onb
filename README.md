[![Build Status](https://travis-ci.org/webalorn/onb.svg?branch=master)](https://travis-ci.org/webalorn/onb)

# ONB - One dice Battles

**One dice Battles** is a **miniature wargame system** that aims to suport elaborate rules, but to be very **simple to play**, through the usage of pre-computed actions tests. Don't worry: you still have to roll a dice yourself, but **only one**. Creatures and entities are created inside the program, and the user can generate a simple 'action' card for each action and each pair of attacking creature / attacked creature. On this card is writed the dice player should roll and the bonus to apply. Then, when a player want to perform an attack, he only have to roll the dice, apply bonuses/maluses, and look in the game table of dammages how many damage he dealt to his opponent.

> *One dice to rule them all*

*Every game cards and tables should be printable in order to allow playing without any screen. Users should be able to choose their armies in the program, and/or create their own creatures, before printing all informations useful for the game, or use them directly in the program*

## Installation

#### Requirements

- python3
- pipenv
- postgreSQL
- [Local DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)

#### Install dependencies

- Install pipenv packages 
- Install PostgreSQL and create 'onb' user with 'onb' password, and databases 'onb_dev', 'onb_testing' and 'onb_production'

#### Environment variables:

(You can put them into '.env')
- DATABASE_URL
- JWT_SECRET_KEY
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

## Usage

You can run a script in the projet with:
```bash
./run.sh <script_name>
```
Scripts:

- main.py (default entry point)
- sqldb/generateDb.py

You can also run tests:
```bash
./runTests.sh
```

Or start the development server:
```base
./startDevApi.sh
```

For local development with 'dev', you must:
- Have a working postgresql server
- Create tables with `./run.sh sqldb/generateDb.sh`
- Launch a local instance of dynamoDB on port 8000 (with `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`)

### API

Development API can be accessed at `http://127.0.0.1:5000`

The API has a [swagger specification on swaggerhub](https://app.swaggerhub.com/apis/webalorn/onb)

## Code specifications

```
| engine
	| models
		| [Game models files]
	| generator
		| [Game models geneators]
| sqldb
	| models
		| [Website models]
| api
	| common
		| [Common API code]
	| ressources
		| [API endpoints]
| tests
	| [Test files, following the same organization as the global one]
```

Sql models for game objects are automaticly created
Game model name format: camelCase name, must end with 'model'.
Ex: **CreatureModel** ; **MyWeaponModel**

#### Game model class definitions: (engine/models)

```python3
class MyModelTypeModel(BaseGameModel):
	"""
	model identifier will be 'my_model_type'
	Any game models must inherit 'GameEntityModel'
	"""
	def getFields():
		"""
		Return all fields present in the model
		Fields are automaticly inherited
		
		Optional fields attributes:
		- default [default :None] defines the default field value
		- min [default: None] defines the minimum accepted value / minimum string size
		- max [default: None] defines the maximum accepted value / maximum string size
		- values [default: [] ] defines a list of accepted values (ignored if empty)
		- generated [default: False] Tell the value is generated, the users will be dissuaded to change it's value
		"""
		return {
			'my_int_field_name': IntField(),
			'my_bool_field_name': BoolField(),
			'my_string_field_name': StringField(),
			'my_float_field_name': FloatField(),
			
			'my_submodel_field': ClassField('model_identifier'),
			'my_list_field': ListField('stored_model_type_identifier'), # List of models (shortcut for below)
			'my_list_field': ListField(<field object>), # List of fields <field object>
			'my_int_list': ListField(IntField(min=3)), # Example of a list of int values
			
			'my_foreign_key_field': ForeignKeyField('modle_id'), # Store an id to reference a model stored in db
			'my_2nd_foreign_key_field': ForeignKeyField('modle_id', default='modle_id'), # Fill with a model
		}
	
	storable = True # [default=False] If the property is set to True, a new table will be created in the database in order to store this models. Otherwise, this model can still be stored in an other model's field
	exposedFields = ['<field_name>',' <field_name>'] # Fields that will be copied in the databse entry, in order to easily retrieve the model
	
```

Models tables can store the model and any model that inherit it
Model identifiers are created by taking the model class without the ending 'Model', and separating word with '_'. All letters are lowercase. For instance, **'MyVikingCharacterModel' **identifer will be **'my_viking_character'**

#### Code 

- Tabulations are used instead of spaces
- Names must be in camelCase format,
- Game models properties and sql model fields use lowercase letters and underscores
