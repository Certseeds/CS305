from socket import *
import time
'''
首先,本次出现的 八位数组 能够被写为 [0-f][0-f]的形式,每个字符[0-f]可被转写为[0-1]*4,所以八位数组可以被转写为[0-1]*8,而二进制流中的最小单位就是八位数组:[0-f][0-f]

'''
questions_cache = []
response_cache = []

server_address = ("127.0.0.1", 54321)
dns_address = ("114.114.114.114", 53)
Living_time = 600
server_socket = socket(AF_INET, SOCK_DGRAM)
dns_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(server_address)


def trans_bit_toint(int1, int2, value=8):
    return (int1 << value) + int2


def trans_int_tobit(value):
    willreturn = []
    for i in range(4):
        willreturn.insert(0, value % 256)
        value = value // 256
    return willreturn


class dns_H_Q(object):
    def __init__(self, bin):
        '''
        其中Header部分的长度是固定的,但是其他的长度都是不定的,需要对二进制串进行处理,再从中得出信息
        Part A:
        形式为  {Number (几个八位数组表示的字符) } * n +00,表示xxx.xxx.xxx.xxx + 一个终结提示符
        Part B,Part C:两个八位数组代码 * 2,一i个代表查询类型,另一个表示查询的类
        所以,首要问题是从中判断Part A,然后part b,c就顺理成章了,这里面直接寻找终结提示符:"00"就可
        :param bin: 传入的byte流,将被拆成小块
        '''
        data = list(bin)
        # self.hiddata = bin
        self.id = data[0:2]
        self.header = data[0:12]
        data[10:12] = [0, 0]
        domain_finish = data[12:].index(0) + 13
        self.question = data[12:domain_finish + 4]
        self.ques_domain = data[12:domain_finish]
        self.ques_type = data[domain_finish:domain_finish + 2]
        self.ques_class = data[domain_finish + 2:domain_finish + 4]
        self.re_question = bytes(data[0:domain_finish + 4])
        self.Answers = data[domain_finish + 4:]

    def get_header_question(self):
        '''
        :return: header_question部分,[]形式
        '''
        willreturn = []
        willreturn += self.id
        willreturn += self.header[2:12]
        willreturn += self.ques_domain
        willreturn += self.ques_type
        willreturn += self.ques_class

        return willreturn


class dns_H_Q_A(object):

    def get_header_question_answers(self):
        '''
        :return: 一个byte流,其中由这个responsex的各个部分组合而成
        '''
        willreturn = []
        willreturn += self.HQ.get_header_question()
        print(willreturn)
        for i in range(0, self.answers_number, 1):
            willreturn += self.ans_names[i]
            willreturn += self.ans_types[i]
            willreturn += self.ans_classes[i]
            willreturn += self.ans_ttls[i]
            willreturn += self.ans_rdlengths[i]
            willreturn += self.ans_rdatas[i]
            print(willreturn)
        return bytes(willreturn)

    def __init__(self, response):
        '''
        首先呢,为了信息压缩,使用指针的方式来重复利用域名,
        Name部分有两种可能,一是两个八位数组,其中第一个八位数组的前两个value == 11
        第二个是传统的{Number (几个八位数组表示的字符) } * n +00.
        Type,class仍为两个八位数组
        TTL:四个八位数组,代表时间煎个
        RDLENGTH:预示接下来的RDATA长度,两个八位数组.
        RDATA:RDLENGTH个八位数组,其中的具体表现形式,还可以为嵌套的方式,即其中的最后一部分被表示为指针.
        '''
        self.HQ = dns_H_Q(response)
        self.answers_number = trans_bit_toint(self.HQ.header[6], self.HQ.header[7]) + trans_bit_toint(self.HQ.header[8], self.HQ.header[9])
        self.initime = int(time.time())
        self.ttl = []
        self.ans_names = []
        self.ans_types = []
        self.ans_classes = []
        self.ans_ttls = []
        self.ans_rdlengths = []
        self.ans_rdatas = []
        pointer = 0
        times = 0
        while pointer < len(self.HQ.Answers) and times < self.answers_number:
            times += 1
            # 192 = 0b11000000 = 128+64
            if self.HQ.Answers[pointer] == 192:
                ans_name = self.HQ.Answers[pointer:pointer + 2]
                pointer += 2
            else:
                namelength = self.HQ.Answers[pointer:].index(0)
                ans_name = self.HQ.Answers[pointer:pointer + namelength]
                pointer += namelength
                pointer += 1
            ans_type = self.HQ.Answers[pointer:pointer + 2]
            pointer += 2
            ans_class = self.HQ.Answers[pointer:pointer + 2]
            pointer += 2
            ans_ttl = self.HQ.Answers[pointer:pointer + 4]
            self.ttl.append((pointer, trans_bit_toint(trans_bit_toint(self.HQ.Answers[pointer], self.HQ.Answers[pointer + 1]),
                                                      trans_bit_toint(self.HQ.Answers[pointer + 2], self.HQ.Answers[pointer + 3]), 16)))
            pointer += 4
            ans_rdlength = self.HQ.Answers[pointer:pointer + 2]
            rd_length = trans_bit_toint(self.HQ.Answers[pointer], self.HQ.Answers[pointer + 1])
            pointer += 2
            ans_rdata = self.HQ.Answers[pointer:pointer + rd_length]
            pointer += rd_length
            print("this is the ans_name", ans_name)
            self.ans_names.append(ans_name)
            self.ans_types.append(ans_type)
            self.ans_classes.append(ans_class)
            self.ans_ttls.append(ans_ttl)
            self.ans_rdlengths.append(ans_rdlength)
            self.ans_rdatas.append(ans_rdata)
            print("this is the pointer", pointer, " this is ANswers.length", len(self.HQ.Answers))


while True:
    request, request_address = server_socket.recvfrom(2048)
    request_object = dns_H_Q(request)
    delete_list = []
    for i in range(len(questions_cache)):
        for j in range(len(response_cache[i].ttl)):
            # 剔除cache中过期的
            if time.time() - response_cache[i].initime > min(Living_time, response_cache[i].ttl[j][1]):
                delete_list.append(i)
                break
    delete_list.reverse()
    # 反向pop,防止乱序
    for i in delete_list:
        questions_cache.pop(i)
        response_cache.pop(i)
    # 判断question是否被client提出过
    if request_object.question in questions_cache:
        print("in here")
        index_of = questions_cache.index(request_object.question)
        response_cache[index_of].HQ.id = request_object.id
        need_change = False
        for i in response_cache[index_of].ttl:
            if time.time() - response_cache[index_of].initime > i[1]:
                need_change = True
        if need_change:
            print("it need change")
            questions_cache.pop(index_of)
            response_cache.pop(index_of)
            dns_socket.sendto(request_object.re_question, dns_address)
            response, useless_address = dns_socket.recvfrom(1145)
            server_socket.sendto(response, request_address)
            response_object = dns_H_Q_A(response)
            questions_cache.append(request_object.question)
            response_cache.append(response_object)
        else:
            print("change no need")
            for i in range(len(response_cache[index_of].ttl)):
                print(response_cache[index_of].ttl[i][1], " is the ttl")
                # 更新ttl
                return_ttl = response_cache[index_of].ttl[i][1] - (int(time.time()) - response_cache[index_of].initime)
                response_cache[index_of].ans_ttls[i] = trans_int_tobit(return_ttl)
            # 生成byte流
            response_bytes = response_cache[index_of].get_header_question_answers()
            # 传回发送的那边
            server_socket.sendto(response_bytes, request_address)

    else:
        # 需要刷新的这部分和上面那部分是同用的,都是先向dns_socket
        print("it first accept")
        dns_socket.sendto(request_object.re_question, dns_address)
        response, useless_address = dns_socket.recvfrom(1145)
        server_socket.sendto(response, request_address)
        # 另一方接收完了,这边要存储了
        response_object = dns_H_Q_A(response)
        questions_cache.append(request_object.question)
        response_cache.append(response_object)
