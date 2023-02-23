class Logic:
    floor : int = lambda self, x : int(x)
    nroot : float = lambda self, n , x : x ** (1 / n)
    reverse : str = lambda self, s : s[:: -1]
    valid_anagram : bool = lambda self, str1, str2 : sorted(str1) == sorted(str2)
    sort : list = lambda self, strArr : sorted(strArr)
    def __init__(self):
        self.hashmap = {
            "floor": self.floor,
            "nroot": self.nroot,
            "reverse": self.reverse,
            "validAnagram": self.valid_anagram,
            "sort": self.sort
        }

    def parse_request(self, request):
        func = self.hashmap[request["method"]]
        param_list = request["params"]
        param_types_list = request["param_types"]
        parsed_param_list = []

        # Define a dictionary to map parameter types to conversion functions
        type_map = {
            "int": int,
            "float": float,
            "list[str]": lambda x: x,
            "str": str
        }

        for i, param_type in enumerate(param_types_list):
            if param_type not in type_map:
                print(f"{param_type} is not a supported type.")
                exit()
            parsed_param_list.append(type_map[param_type](param_list[i]))

        if len(parsed_param_list) != len(func.__code__.co_varnames) - 1:
            print("Invalid number of arguments.")
            exit()

        return func(*parsed_param_list)



