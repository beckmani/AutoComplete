import os
import time
from flask import Flask, request, g
from auto_complete import Autocomplete
from stats import StatsServer


class AutoCompleteServer:
    '''
        Class for AutoComplete Server
    '''
    def __init__(self):
        self.ac = Autocomplete('dictionary.txt')  # ./dictionary_less_than_6.txt
        self.stats_server = StatsServer()
        self.stats_server.update_word_count(self.ac.get_stats()['wordCount'])

    def search(self, prefix):
        start = time.time()
        words = self.ac.search(prefix)
        end = time.time()
        diff = int(round((end - start) * 1000))
        self.update_stats(diff)
        return {'words': words}

    def get_statistics(self):
        return self.stats_server.get_stats()

    def update_stats(self, duration):
        self.stats_server.update_request_stats(duration)

app = Flask(__name__)
ac_server = AutoCompleteServer()


@app.route("/statistics")
def get_statistics():
    return ac_server.get_statistics()


@app.route("/dictionary")
def get_words():
    prefix = request.args.get('prefix', default='*', type=str)
    return ac_server.search(prefix.strip("'"))


#@app.before_request
#def before_request():
#    g.start = time.time()


#@app.after_request
#def after_request(response):
#    diff = int(round((time.time() - g.start) * 1000))
#    if ((response.response) and
#        (200 <= response.status_code < 300) and
#        (response.content_type.startswith('application/json'))):
#        ac_server.update_stats(diff)
#    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
