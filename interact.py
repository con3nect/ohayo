import random

#__sk_list = ['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', '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', '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', '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']
__sk_list = ['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']

def interact(prompt, penalty = {}):
    import openai
    openai.api_key = random.choice(__sk_list)
    if isinstance(prompt, list):
        messages = prompt
    else:
        messages = [{"role": "user", "content": prompt}]

    out = ''
    for message in messages:
        if message['role'] == 'assistant':
            out = out + '有知识：' + message['content'] + '\n'
        else:
            out = out + message['content'] + '\n'
    #print(out)

    while True:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=messages,
                logit_bias = penalty,
                temperature=0
            )
            break
        except:
            from time import sleep
            sleep(0.2)

    answer = completion.choices[0].message['content']
    return answer

def embedding(text):
    import openai
    openai.api_key = random.choice(__sk_list)
    completion = openai.Embedding.create(
      model="text-embedding-ada-002",
      input=text
    )
    return completion['data'][0]['embedding']
