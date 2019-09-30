import os
import mimetypes


def test_fun():
    os.chdir("test_dir")


def test_fun_2():
    os.chdir("..")


print(b'HEAD' in (b'GET', b'HEAD'))
list = os.listdir()
for i in list:
    i = i
    print(i)
print(list[0][1:])
print(os.path.isfile("/file2.py"[1:]))
print(os.path.isdir("test_dir"))
for i in os.listdir():
    print(1)
    print(i)
print('ok')
string = "this is a test{}".format("hanpi")
print(string)
i = "tesingadhasdkj"
print("<a href=\"{}\">{}/</a><br>".format(i, i))
test_3 = "<a href=\"{}\">{}/</a><br>".format(i, i).encode('utf-8')
test_4 = b'<a href="tesingadhasdkj">tesingadhasdkj/</a><br>'
print(test_3)
print(test_4)
print(test_3 == test_4)

list = os.listdir()
for i in list:
    print(i)
test_fun()
list = os.listdir()
for i in list:
    print(i)
test_fun_2()
list = os.listdir()
for i in list:
    print(i)
print(os.path.isdir("test_dir/test_dir_2"))
print(os.path.isfile("test_dir/test"))
file = open("test_dir/test")
print(file.read())
file.close()
print(mimetypes.guess_type("a.txt")[0])
