from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)
englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(englishBot)
trainer.train("chatterbot.corpus.english") 

@app.route("/")
def index():
    return render_template(".//templae//index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(englishBot.get_response(userText))
if __name__ == "__main__":
    app.run()