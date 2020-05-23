class Validation:

    def __init__(self, validation_function, error_msg: str):
        self.validation_function = validation_function
        self.error_msg = error_msg

    def __call__(self, value):
        """ callable 객체를 만들기 위함.

        객체에는 상태가 있기 때문에 함수 호출 사이에 정보를 저장할 수 있다.
        따라서 Validation 객체를 파라미터가 있는 함수처럼 쓰기위해 정의.

        cf.
        !r 은 이련 개념이다.
        repr() 을 call 했다고 생각하면 됨. 다시말해 repr(value)
        https://www.python.org/dev/peps/pep-0498/#s-r-and-a-are-redundant

        :param value:
        :return:
        """
        if not self.validation_function(value):
            raise ValueError(f"{value!r} {self.error_msg}")


class Field:
    """
    Descriptor 클래스.

    Descriptor protocol 을 따르는 magic methods 를 구현한다.
    """

    def __init__(self, *validations):
        """
        validator 로 처리할 메소드를 iterable values 형태로 받는다.

        :param validations:
        """
        self._name = None
        self.validations = validations

    def __set_name__(self, owner, name):
        """ descriptor 이름을 설정해주는 magic method

        NEW in Python 3.6!

        :param owner: descriptor 를 소유한 클래스
        :param name: descriptor 의 이름
        :return:
        """
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def validate(self, value):
        """ 값 검증 로직


        :param value:
        :return:
        """
        for validation in self.validations:
            validation(value)

    def __set__(self, instance, value):
        """ descriptor 를 거치고 instance 가 가리키는 _name 값에 value 를 할당하기 위해 쓴다.

        @property.setter 를 대신한다.

        :param instance: descriptor 로 점검하기 위한 도메인 추상화 객체
        :param value: descriptor 로 점검하기 위해 넣은 값
        :return:
        """
        self.validate(value)
        instance.__dict__[self._name] = value


class ClientClass:
    """
    Descriptor 구현체의 기능을 활용할 도메인 추상화 객체.

    Class attribute 로 descriptor 를 갖는다.

    cf. isinstance()는 x 값이 <iterables> 의 인스턴스인지 묻는 함수다.
    """
    descriptor = Field(
        Validation(lambda x: isinstance(x, (int, float)), "는 숫자가 아님."),
        Validation(lambda x: x >= 0, "는 0보다 작음"),
    )


if __name__ == "__main__":
    """
    client 라는 객체는 ClientClass 클래스의 객체다. 이는 Field 라는 디스크립터를 가지고있다.
    디스크립터는 이름을 descriptor 라고 붙여놨으며, 값 검증은 __get__에서 이루어진다.
    __get__은 validate() 을 수행하는데, 둘다 패스하면 ClientClass._name 에 값을 넣는다.

    그래서 print(client.descriptor) 를 하면 42를 리턴하는 것이다.  
    """

    client = ClientClass()
    client.descriptor = 42
    print(client.descriptor)

    # 아래 두 값은 에러가 난다. validate 과정을 디버그하며 쫓아가볼 것
    client.descriptor = -42
    # client.descriptor = "invalid value"
