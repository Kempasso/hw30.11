from flask import Flask, request, jsonify

app = Flask(__name__)


class Controller:
    @classmethod
    def map(cls, data, parameter):
        return list(map(lambda x: x.split()[int(parameter)].replace('\"', ""), data))

    @classmethod
    def filter(cls, data, parameter):
        return list(filter(lambda string: parameter in string, data))

    @classmethod
    def unique(cls, data, parameter):
        return list(set(data))

    @classmethod
    def sort(cls, data, parameter):
        return sorted(data, reverse=True if parameter == 'desk' else False)

    @classmethod
    def limit(cls, data, parameter):
        return data[:int(parameter)]


@app.route('/perform_query', methods=['POST'])
def foo():
    data = request.get_json()
    filename = data['filename']
    with open(f'data/{filename}') as file:
        file_data = file
        first_result = getattr(Controller, data['cmd1'])(file_data, data["value1"])
        if not data.get('cmd2', None):
            return jsonify(first_result)
        result2 = getattr(Controller, data['cmd2'])(first_result, data["value2"])
        return jsonify(result2)


app.run()
