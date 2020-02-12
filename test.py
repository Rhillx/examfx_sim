import random
import json

with open('qna.json') as f:
    data = json.load(f)


q = 'When an insured makes truthful statements on the application for insurance and pays the required premium, it is known as which of the following?'
p = 'How are you?'
x = data.get(p)

if data.get(p) == None:
    print(True)
else:
    print(False)