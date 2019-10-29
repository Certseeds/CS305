from rdt import *
from DNSHeader import *
import time

questions_cache = []
response_cache = []

server_address = "127.0.0.1"
server_port = 54831
dns_address = "114.114.114.114"
dns_port = 53
Living_time = 600
server_Socket = socket(AF_INET, SOCK_DGRAM)
client_Socket = socket(AF_INET, SOCK_DGRAM)
server_Socket.bind((server_address, server_port))


def trans_bit_toint(int1, int2, value=8):
    return (int1 << value) + int2


def trans_int_toarray(value, length, max):
    willreturn = []
    for i in range(length):
        willreturn.insert(0, value % max)
        value = (value - value % max) // max
    return willreturn


class dns_H_Q(object):
    def __init__(self, bin):
        data = list(bin)
        self.hiddata = bin
        self.id = data[0:2]
        self.header = data[0:12]
        data[10:12] = [0, 0]
        domain_finish = data[12:].index(0) + 13
        self.question = data[12:domain_finish + 4]
        self.ques_domain = data[12:domain_finish]
        self.ques_type = data[domain_finish:domain_finish + 2]
        self.ques_class = data[domain_finish + 2:domain_finish + 4]
        self.re_question = bytes(data[0:domain_finish + 5])
        self.Answers = data[domain_finish + 4:]

    def get_header_question(self):
        willreturn = []
        willreturn += self.header
        willreturn += self.ques_domain
        willreturn += self.ques_type
        willreturn += self.ques_class
        return bytes(willreturn)


class dns_H_Q_A(object):

    def get_header_question_answers(self):
        willreturn = []
        willreturn += self.HQ.get_header_question()
        for i in range(self.answers_number):
            willreturn += self.ans_names[i]
            willreturn += self.ans_types[i]
            willreturn += self.ans_classes[i]
            willreturn += self.ans_ttls[i]
            willreturn += self.ans_rdlengths[i]
            willreturn += self.ans_rdatas[i]

        return bytes(willreturn)

    def __init__(self, response):
        self.HQ = dns_H_Q(response)
        self.answers_number = trans_bit_toint(self.HQ.header[6], self.HQ.header[7]) + trans_bit_toint(self.HQ.header[8], self.HQ.header[9])
        self.initime = time.time()
        self.ttl = []
        self.ans_names = []
        self.ans_types = []
        self.ans_classes = []
        self.ans_ttls = []
        self.ans_rdlengths = []
        self.ans_rdatas = []
        pointer = 0
        times = 0
        print(self.answers_number)
        print(self.HQ.hiddata)
        print(self.HQ.Answers)
        while pointer < len(self.HQ.Answers) and times < self.answers_number:
            times += 1
            # 192 = 0b11000000 = 128+64
            if self.HQ.Answers[pointer] == 192:
                pointer += 2
                ans_name = self.HQ.Answers[pointer:pointer + 2]
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
            self.ttl.insert(-1, (pointer, trans_bit_toint(trans_bit_toint(self.HQ.Answers[pointer], self.HQ.Answers[pointer + 1]),
                                                          trans_bit_toint(self.HQ.Answers[pointer + 2], self.HQ.Answers[pointer + 3]), 16)))
            pointer += 4
            ans_rdlength = self.HQ.Answers[pointer:pointer + 2]
            print(ans_rdlength)
            rd_length = trans_bit_toint(self.HQ.Answers[pointer], self.HQ.Answers[pointer + 1])
            pointer += 2
            ans_rdata = self.HQ.Answers[pointer:pointer + rd_length]
            pointer += rd_length
            self.ans_names.append(ans_name)
            self.ans_types.append(ans_type)
            self.ans_classes.append(ans_class)
            self.ans_ttls.append(ans_ttl)
            self.ans_rdlengths.append(ans_rdlength)
            self.ans_rdatas.append(ans_rdata)
            print("this is the pointer", pointer, " this is ANswers.length", len(self.HQ.Answers))


while True:
    message, clientAddress = server_Socket.recvfrom(2048)
    request = message
    delete_list = []
    for i in range(len(questions_cache)):
        for j in range(len(response_cache[i].ttl)):
            if time.time() - response_cache[i].initime > min(Living_time, response_cache[i].ttl[j][1]):
                delete_list.append(i)
                break
    delete_list.reverse()
    for i in delete_list:
        questions_cache.pop(i)
        response_cache.pop(i)

    print("----------------------------------")
    dns_request = dns_H_Q(request)
    # begin
    request_object = dns_H_Q(request)
    if request_object.question in questions_cache:
        print("in here")
        index_of_question = questions_cache.index(request_object.question)
        response_message_1 = response_cache[index_of_question].HQ.hiddata
        response_message_2 = list(response_message_1)
        response_message_2[0:2] = request_object.id
        response_message_1 = bytes(response_message_2)
        # 接下来check一下ttl是否有效,无效的话还得走一套流程
        need_change = False
        for i in response_cache[index_of_question].ttl:
            print(i[1])
            if time.time() - response_cache[index_of_question].initime > i[1]:
                need_change = True
        if need_change:
            print("it need change")
            questions_cache.pop(index_of_question)
            response_cache.pop(index_of_question)
            client_Socket.sendto(request_object.re_question, (dns_address, dns_port))
            receive, useless_address = client_Socket.recvfrom(2018)
            server_Socket.sendto(receive, clientAddress)
            receive_message = dns_H_Q_A(receive)
            questions_cache.append(request_object.question)
            response_cache.append(receive_message)
        else:
            print("change no need")
            for i in response_cache[index_of_question].ttl:
                print(len(response_message_2))
                # response_message_2[i[0]:(i[0] + 4)] = trans_int_toarray(i[1], 4, 2 ** 8)
                print(i[1] - round(time.time() - response_cache[index_of_question].initime))
            response_message_1 = bytes(response_message_2)
            server_Socket.sendto(response_message_1, clientAddress)
    else:
        print("in there ")
        client_Socket.sendto(request, (dns_address, dns_port))
        receive, useless_address = client_Socket.recvfrom(2018)
        print(receive)
        server_Socket.sendto(receive, clientAddress)
        # 另一方接收完了,这边要存储了
        receive_message = dns_H_Q_A(receive)
        questions_cache.append(request_object.question)
        response_cache.append(receive_message)

    # client_Socket.sendto(request, (dns_address, dns_port))
    # response, address = client_Socket.recvfrom(2018)
    # dns_response = dns_H_Q_A(request, response)
    # for i in dns_response.Ans:
    #      print(i)
    # print(response)
    # server_Socket.sendto(response, clientAddress)
