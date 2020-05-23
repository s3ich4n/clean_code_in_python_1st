import logging

logger = logging.getLogger(__name__)


class DescriptorClass:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        print("Call: %s.get__(%r %r)", self.__class__.__name__, instance, owner)
        return instance


class ClientClass:
    descriptor = DescriptorClass()
