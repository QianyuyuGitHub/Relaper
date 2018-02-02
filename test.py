

class magicMethod(object):

    def __init__(self, age=18, gender='female'):
        self.age = age
        self.gender = gender

    def listout(self):
        print('The age of mine is:', self.age)
        print('The gender of mine is:', self.gender)

yoyo = magicMethod(20, 'male')
yoyo.listout()
zhang = magicMethod()
zhang.listout()
