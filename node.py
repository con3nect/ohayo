from utils import *
from interact import interact
from glossary import glossary
from answer import solution, node_return
import json

law_glossary = glossary('名词解释库.xlsx')

class node:

    def __init__(self, definiton):
        self.assistant_link = []
        self.assistant = []
        self.function = []
        self.return_true = True
        self.solution_true = None
        self.return_false = False
        self.solution_false = None
        self.already_run = False
        self.allow_forget = True
        self.identification = None

        self.name = definiton['name'] #函数名称
        self.type = definiton['type'] #节点类型

        if 'return_true' in definiton:
            self.return_true = definiton['return_true']

        if 'solution_true' in definiton:
            val = definiton['solution_true']
            self.solution_true = solution(val[0], val[1], val[2])

        if 'return_false' in definiton:
            self.return_false = definiton['return_false']

        if 'solution_false' in definiton:
            val = definiton['solution_false']
            self.solution_false = solution(val[0], val[1], val[2])

        if 'format' in definiton:
            self.format = definiton['format']

        if 'ask_more' in definiton:
            self.ask_more = definiton['ask_more']

        if 'assistant' in definiton:
            self.assistant = definiton['assistant']

        if 'assistant_link' in definiton:
            self.assistant_link = definiton['assistant_link']

        if 'identification' in definiton:
            self.identification = definiton['identification']

        if 'why' in definiton:
            self.why = definiton['why']

        if 'pre_query' in definiton:
            self.pre_query = definiton['pre_query']

        if 'prework' in definiton:
            self.prework = definiton['prework']

        if 'require' in definiton:
            self.require = definiton['require']

        if 'cmp_rule' in definiton:
            self.cmp_rule = definiton['cmp_rule']

        if 'answer_false' in definiton:
            self.answer_false = definiton['answer_false']

        if 'pattern' in definiton:
            self.pattern = definiton['pattern']

        if 'function' in definiton:
            self.function = definiton['function']

    def execute(self, background):
        print(self.name)
        self.json['attrs']['fill'] = 'lightgreen'
        return_value = None
        if self.type == 'query':
            return_value = self.query(background)
        if self.type == 'leaf':
            return_value = self.leaf(background)
        if self.type == 'mid':
            return_value = self.mid(background)
        if self.type == 'extract':
            return_value = self.entity_extract(background)
        if self.type == 'output':
            return_value = self.output(background)

        if self.json['attrs']['fill'] == 'lightgreen':
            self.json['attrs']['fill'] = 'green'
        return return_value

    #输出函数
    def output(self, background):
        if hasattr(self, "prework"):
            prework_return = self.prework.execute(background)
            answer = prework_return.output_solution(background, self.format)
            #print(answer)
            return answer

    def get_assistant_content(self):
        assistant_link_content = law_glossary.get_definition(self.assistant_link)
        for single_assistant in self.assistant:
            assistant_link_content.append(interact_prompt(single_assistant))
        return assistant_link_content

    def mid(self, background):
        if hasattr(self, "prework"):
            prework_return = self.prework.execute(background)
            if not prework_return.return_tag:
                self.json['attrs']['fill'] = 'red'
                return prework_return #不存在prework_return 字段

        all_return = node_return()
        pattern = ['AND', 'OR', 'ALL'].index(self.pattern)
        for func in self.function:
            func_return = func.execute(background)
            if func_return.return_tag == True:
                all_return = all_return | func_return
            if func_return.return_tag == False:
                all_return = all_return & func_return
            if func_return.return_tag == pattern:
                break

        if all_return.return_tag:
            all_return = all_return & node_return(self.return_true, self.solution_true, None)
        else:
            self.json['attrs']['fill'] = 'red'
            all_return = all_return & node_return(self.return_false, self.solution_false, None)
        return all_return

    def entity_extract(self, background):
        extract_keys = self.identification
        if hasattr(self, "prework"):
            prework_return = self.prework.execute(background)
            prework_return.court_extract(background, assistant_link_content= self.get_assistant_content())
            return prework_return

    def query(self, background):
        def supplement(background, user_inputs, question):
            if user_inputs == []:
                return background
            user_inputs = [background] + user_inputs
            user_inputs = ['A:' + user_input for user_input in user_inputs]
            prompt = ('\nB:' + question + '\n').join(user_inputs)
            task = '请基于A说的话，和B的提问，把A说的所有信息放进一句话中，并保留原本的人称，要求在A说的第一句话上面做少量的修改即可。\n我强调一次，请你不要写B干了什么，B说的话是辅助你完善A说的话的。'
            prompt = prompt + '\n' + task
            print(prompt)
            penalty = {"33":-100}
            return interact(prompt, penalty)
        assistant_link_content = self.get_assistant_content()
        identification = '请你提取出：' + ','.join(self.identification) + '，以json格式输出，无法提取或推断出的字段请填写null'
        identification_content = interact_prompt('有背景:' + background + '\n' + identification, role='user')

        user_inputs = []
        user_supplements = []
        while True:
            prompt = assistant_link_content + user_supplements + [identification_content]
            print(prompt)
            answer = interact(prompt)
            #print(answer)
            try:
                answer = answer.split('{', 1)[-1].rsplit('}', 1)[0]
                answer = json.loads('{' + answer + '}')
                for key,value in answer.items():
                    if value == None or value == '':
                        raise KeyError("Can't load value:", key)
                break
            except:
                print(self.ask_more)
                more_background = input()
                user_inputs.append(more_background)
                user_supply = '对于问题:' + self.ask_more + "用户补充:" + more_background
                more_background = interact_prompt(user_supply, 'user')
                user_supplements.append(more_background)

        new_background = supplement(background, user_inputs, self.ask_more)
        print(new_background)
        return self.return_true

    def leaf(self, background):
        assistant_link_content = self.get_assistant_content()
        identification =  self.identification + '请回答True或False'
        identification_content = interact_prompt('有背景:' + background + '\n' + identification, role='user')

        prompt = assistant_link_content + [identification_content]
        print(prompt)
        answer = interact(prompt)
        print(answer)
        if answer.find('True')!=-1:
            return node_return(self.return_true, self.solution_true, None)
        else:
            self.json['attrs']['fill'] = 'red'
            return node_return(self.return_false, self.solution_false, None)