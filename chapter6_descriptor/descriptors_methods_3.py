class ProtectedAttribute:
    """
    User 의 descriptor

    email 값에 대해서는 이런식으로 빡세게 처리해줄 수 있다.

    """
    def __init__(self, requires_role=None) -> None:
        self.permission_required = requires_role
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __set__(self, user, value):
        if value is None:
            raise ValueError(f"{self._name}을(를) None으로 설정할 수 없음.")
        user.__dict__[self._name] = value

    def __delete__(self, user):
        """ 객체 삭제를 수행할 때는 이쪽 로직을 탄다.

        설계시 email이 None인 값에 대해서는 잘못된 값으로 '간주'하도록 로직을 잘 작성해야한다.
        아예 그런값을 허락하지 않도록 방어적으로 짤 필요가 있다.
        :param user:
        :return:
        """
        if self.permission_required in user.permissions:
            user.__dict__[self._name] = None
        else:
            raise ValueError(
                f"{user!s} 사용자는 {self.permission_required} 권한이 없음."
            )


class User:
    """ Admin 권한을 가진 사용자만 이메일 주소를 삭제할 수 있음
    """
    email = ProtectedAttribute(requires_role="admin")

    def __init__(self, username: str, email: str, permission_list: list = None) -> None:
        """

        __init__은 저 값들이 들어오기를 기대하고 작성되어있다.
        "해당값을 넣지 않으면 안된다." 라고 기대하고있다.

        따라서 실제 로직에서는 이를 해결하기위한 방어로직을 작성해야 할 것이다.
        :param username:
        :param email:
        :param permission_list:
        """
        self.username = username
        self.email = email
        self.permissions = permission_list or []

    def __str__(self):
        return self.username


if __name__ == "__main__":
    admin = User("root", "root@d.com", ["admin"])
    user = User("user", "user1@d.com", ["email", "helpdesk"])

    print(admin.email)
    del admin.email
    print(admin.email is None)

    print(user.email)

    # 아래 로직은 에러가 발생한다. 필요시 주석 해제하고 쫓아가서 확인할 것
    user.email = None
    del user.email
