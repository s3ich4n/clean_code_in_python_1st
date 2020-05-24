class DataDescriptor:

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return 42

    def __set__(self, instance, value):
        print(f"{instance} 값을 {value} 값으로 설정.")
        instance.__dict__["descriptor"] = value


class ClientClass:
    descriptor = DataDescriptor()
