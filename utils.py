def interact_prompt(content, role='assistant'):
    return {"role": role, "content": content}

def answer_merge(answer, add):
    def merge_sub(a,b):
        if a is None:
            return b
        if b is None:
            return a

        if isinstance(a, str) and isinstance(b, str):
            return [a, b]

        if isinstance(a, str) and isinstance(b, list):
            return [a] + b

        if isinstance(a, list) and isinstance(b, str):
            return a + [b]

        if isinstance(a, list) and isinstance(b, list):
            return a + b

    answer[0] = answer[0] or add[0]
    for i in range(1,4):
        answer[i] = merge_sub(answer[i], add[i])

def identify_null(court_list):
    null_list = []
    for court in court_list:
        if court[1] == None:
            null_list.append(court[0])
    return null_list