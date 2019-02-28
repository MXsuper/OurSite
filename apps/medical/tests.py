from django.test import TestCase

# Create your tests here.
class MyTest():
    name = "666666"
    seven = "fdafafa"

my_test = MyTest()

my_test.temp = 77777
print(my_test.temp)

del my_test.temp
print(my_test.temp)