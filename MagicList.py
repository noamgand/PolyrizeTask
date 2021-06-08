from dataclasses import dataclass

@dataclass
class Person:
    age: int = 1

class MagicList(list):
    def __init__(self, **kwargs):
        if len(kwargs) == 1:
            age = kwargs.get('cls_type').age
            super().append(Person(age))
        else:
            super().__init__(range(1))

    def __setitem__(self, key, value):
        MagicListLen = self.__len__()
        if key > MagicListLen-1:
            i = MagicListLen-1
            for i in range(i, key):
                self.append('0')
        super(MagicList, self).__setitem__(key, value)


def main():
    a = MagicList()
    a[0] = 5
    print(a)

    print("-----support in assigned types-----")
    b = MagicList(cls_type=Person)
    b[0].age = 5
    print(b)


main();


