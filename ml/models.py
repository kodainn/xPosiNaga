from transformers import pipeline, AutoModelForSequenceClassification, BertJapaneseTokenizer,BertTokenizer, BertForSequenceClassification

class Model:
    def __init__(self):
        model = AutoModelForSequenceClassification.from_pretrained('llm-book/bert-base-japanese-v3-wrime-sentiment') 
        tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
        self.classifier = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)
    
    def predict(self, text):
        return self.classifier(text)[0]['label']