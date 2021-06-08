from sanic import Sanic, Blueprint
from sanic.response import text, json
from sanic_jwt import Initialize, exceptions, protected, inject_user


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "name": self.username,
            "password": self.password
        }


users_list = [User("Noam", "123"), User("Gali", "abc")]
username_table = {u.username: u for u in users_list}


async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password")

    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found")

    if password != user.password:
        raise exceptions.AuthenticationFailed("password is incorrect")

    return user

app = Sanic("myapp")
Initialize(app, authenticate=authenticate)

output_data = {}


class InputData(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            self.name: self.value
        }


@app.route("normalized_data", methods=["POST"])
#@inject_user()
#@protected()
async def normalized_data(request):
    try:
        list_data = request.json
        value_string = ""
        for item in list_data:
            for field in item.keys():
                if "Val" in field:
                    value_string = field
            output_data[item["name"]] = item[value_string]

        return json(output_data, status=201)

    except Exception as error:
        print(error)
        return json({"message": "output creation failed"}, status=500)


app.run(host="0.0.0.0", port=8000)