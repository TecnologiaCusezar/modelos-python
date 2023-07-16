class Coefficient:
    __name: str = None
    __variable: str = None
    __value: float = None
    __p_value: float = None

    def __init__(self, name: str, value: float, variable: str = None, p_value: float = None) -> None:
        self.__name = name
        self.__value = value
        self.__variable = variable or 'B_' + name.lower()
        self.__p_value = p_value

    def __dict__(self) -> str:
        return {
            "name": self.__name,
            "variable": self.__variable,
            "value": self.__value,
            "p-value": self.__p_value,
        }
