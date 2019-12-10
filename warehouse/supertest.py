class Person(object):
    def __init__(self):
        print("wo yao hao hao xue xi")

    def  study(self , v1):
        print("wo yao xue hao yu yan")

class Man(Person):

    def __init__(self):
        print("wo shi nan ren wo yao hao hao xue xi")

    def study(self,v1):
        super().study(v1)