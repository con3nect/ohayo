# -*- coding: utf-8 -*-

#用于存储解决方案
#比如要去被告住所地和侵权行为地解决，是xx类型的纠纷，适用法条为xxxxx
class solution:

    def __init__(self, court_list=None, case_type='', law_list=None):
        if law_list is None:
            law_list = []
        else:
            if isinstance(law_list, str):
                law_list = [law_list]

        if court_list is None:
            court_list = []
        else:
            if isinstance(court_list, str):
                court_list = [court_list]

        self.court_list = court_list
        self.case_type = case_type
        self.law_list = law_list

    def __repr__(self):
        return f"court_list={self.court_list},case_type={self.case_type},law_list={self.law_list}"

    def __add__(self, other):
        answer = solution()
        answer.court_list = list(set(self.court_list + other.court_list))
        if self.case_type:
            answer.case_type = self.case_type
        else:
            answer.case_type = other.case_type
        answer.law_list = list(set(self.law_list + other.law_list))
        return answer

    def court_extract(self, background, user_supplements = [], assistant_link_content = []):
        from interact import interact
        from utils import interact_prompt
        import json
        identification = '请你提取出：' + ','.join(self.court_list) + '，以json格式输出，无法提取或推断出的字段请填写null'
        identification_content = interact_prompt('有背景:' + background + '\n' + identification, role='user')
        prompt = assistant_link_content + user_supplements + [identification_content]
        answer = interact(prompt)
        print(answer)
        answer = answer.split('{', 1)[-1].rsplit('}', 1)[0]
        answer = json.loads('{' + answer + '}')
        for i in range(len(self.court_list)):
            court = self.court_list[i]
            if court in answer:
                if isinstance(answer[court], str) and answer[court].find('无法')!=-1:
                    answer[court] = None
                if isinstance(answer[court], str) and answer[court].find('null')!=-1:
                    answer[court] = None

                self.court_list[i] = (court, answer[court])
            else:
                self.court_list[i] = (court, None)
        print(self.court_list)

    def output_solution_raw(self):
        def pad(court):
            if isinstance(court, str):
                court = (court, None)
            if isinstance(court, tuple):
                if court[1] == None:
                    return court[0] + '(无法确定)'
                return court[0] + '(' + court[1] + '人民法院)'
        start = '分析如下:\n'
        case_type = f'这是一个{self.case_type}' if self.case_type else None
        court_list = '可以在' + ','.join([pad(court) for court in self.court_list]) + '起诉' if self.court_list else None
        law_text = '\n'.join(self.law_list)
        law_recommend = f'相关法条如下:\n{law_text}' if law_text else None
        prompt_list = filter(None, [case_type, court_list, law_recommend])
        prompt = start + ','.join(prompt_list)
        return prompt

    def output_solution(self, background, format):
        #from interact import interact
        #background = '已知:' + background
        statement = self.output_solution_raw()
        #prompt = '\n'.join([background, statement, format])
        #answer = interact(prompt)
        return statement

class node_return:
    def __init__(self, return_tag=False, return_solution=None, return_background =''):
        if return_solution is None:
            return_solution = []
        self.return_tag = return_tag
        self.return_solution = return_solution
        self.return_background = return_background

    def __repr__(self):
        return f"node_return(return_tag={self.return_tag} ,return_solution={self.return_solution} background={self.return_background})"

    def __and__(self, other):
        if other == None:
            return self
        if self == None:
            return other
        if not isinstance(other.return_solution, list):
            other.return_solution = [other.return_solution]
        return_tag = self.return_tag or other.return_tag

        if self.return_solution and other.return_solution:
            return_solution = [single_solution + other.return_solution[0] for single_solution in self.return_solution]
        else:
            if self.return_solution:
                return_solution = self.return_solution
            else:
                return_solution = other.return_solution

        return_background = self.return_background if self.return_background else other.return_background
        return node_return(return_tag, return_solution, return_background)

    def __or__(self, other):
        if other == None:
            return self
        if self == None:
            return other
        if not isinstance(other.return_solution, list):
            other.return_solution = [other.return_solution]
        return_tag = self.return_tag or other.return_tag
        return_solution = self.return_solution + other.return_solution
        return_background = self.return_background if self.return_background else other.return_background
        return node_return(return_tag, return_solution, return_background)

    def court_extract(self, background, user_supplements = [], assistant_link_content = []):
        def supplement(background, dialogues):
            from interact import interact
            if dialogues == []:
                return background
            dialogues = ['A:' + background] + ['\nB:' + dialogue[0] + '\nA:' + dialogue[1] for dialogue in dialogues]
            prompt = ''.join(dialogues)
            task = '请基于A说的话，和B的提问，把A说的所有信息放进一句话中，并保留原本的人称，要求在A说的第一句话上面做少量的修改即可。\n我强调一次，请你不要写B干了什么，B说的话是辅助你完善A说的话的。'
            prompt = prompt + '\n' + task
            #print(prompt)
            penalty = {"33":-100}
            return interact(prompt, penalty)

        init_user_supplements = list(user_supplements)
        init_assistant_link_content = list(assistant_link_content)
        for i in range(len(self.return_solution)):
            user_supplements = list(init_user_supplements)
            assistant_link_content = list(init_assistant_link_content)
            dialogues = []

            init_court_list = list(self.return_solution[i].court_list)
            while True:
                self.return_solution[i].court_list = list(init_court_list)
                from utils import identify_null, interact_prompt
                self.return_solution[i].court_extract(background, user_supplements, assistant_link_content)
                #null_list = identify_null(self.return_solution[i].court_list)

                break
                #if null_list:
                #    ask_more = '为了更好地帮助你解决问题，需要您补充:' + ','.join(null_list) + '，以便我们更好地判断'
                #else:
                #    break

                print(ask_more + '\n如果你想跳过，请输入"跳过"')
                more_background = input()

                if more_background == '跳过':
                    break

                dialogues.append((ask_more, more_background))
                user_supply = '对于问题:' + ask_more + "。用户补充:" + more_background
                more_background = interact_prompt(user_supply, 'user')
                user_supplements.append(more_background)

                new_background = supplement(background, dialogues)
                print(new_background)
                background = new_background
                dialogues = []

        self.return_background = background

    def output_solution(self, background, format):
        answers = []
        for single_solution in self.return_solution:
            answer = single_solution.output_solution(background, format)
            print(answer)
            answers.append(answer)
        return answers

#a = solution([('信息设备所在地', '广州市天河区'), '被侵权人住所地'], '信息网络侵权纠纷', ['《中华人民共和国民事诉讼法》第二十九条规定：因侵权行为提起的诉讼，由侵权行为地或者被告住所地人民法院管辖。', '《中华人民共和国民事诉讼法司法解释》第二十五条规定：信息网络侵权行为实施地包括实施被诉侵权行为的计算机等信息设备所在地，侵权结果发生地包括被侵权人住所地。'])
#b = solution(court_list=[('被告住所地', '广州市白云区')])
#a = solution( None, '信息网络侵权纠纷', None)
#b = a + b
#print(b.output_solution())