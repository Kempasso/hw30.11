import re

from flask import Flask, request, jsonify

app: Flask = Flask(__name__)


class Controller:
    @staticmethod
    def map(data, parameter: str) -> list[str]:
        return list(map(lambda x: x.split()[int(parameter)].replace('\"', ""), data))

    @staticmethod
    def filter(data, parameter: str) -> list[str]:
        return list(filter(lambda string: parameter in string, data))

    @staticmethod
    def unique(data, parameter: str) -> list[str]:
        return list(set(data))

    @staticmethod
    def sort(data, parameter: str) -> list[str]:
        return sorted(data, reverse=True if parameter == 'desk' else False)

    @staticmethod
    def limit(data, parameter: int) -> list[str]:
        return data[:int(parameter)]

    @staticmethod
    def regex(data, parameter: str) -> list[str]:
        pattern = re.compile(f'{parameter}')
        return [i for i in data if re.match(pattern, i)]
#_io.TextIOWrapper

@app.route('/perform_query', methods=['POST'])
def foo():
    data = dict(request.form)
    filename = data['filename']
    with open(f'data/{filename}') as file:
        file_data = file
        print(type(file_data))
        first_result = getattr(Controller, data['cmd1'])(file_data, data["value1"])
        if not data.get('cmd2', None):
            return jsonify(first_result)
        result2 = getattr(Controller, data['cmd2'])(first_result, data["value2"])
        return jsonify(result2)


if __name__ == "__main__":
    app.run()
