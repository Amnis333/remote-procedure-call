class Logic:
    floor : int = lambda self, x : int(x)
    nroot : float = lambda self, n , x : x ** (1 / n)
    reverse : str = lambda self, s : s[:: -1]
    valid_anagram : bool = lambda self, str1, str2 : sorted(str1) == sorted(str2)
    sort : list[str] = lambda self, strArr : sorted(strArr)
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

        for param_i in range(len(param_types_list)):
            if param_types_list[param_i] == "int":
                parsed_param_list.append(int(param_list[param_i]))
            elif param_types_list[param_i] == "float":
                parsed_param_list.append(float(param_list[param_i]))
            elif param_types_list[param_i] == "list[str]":
                parsed_param_list.append(param_list)
            elif param_types_list[param_i] == "str":
                parsed_param_list.append(param_list[param_i])
            else:
                print(f'{param_types_list[param_i]} is not supported type.')
                exit()
        
        if len(parsed_param_list) == 1:
            return func(parsed_param_list[0])
        elif len(parsed_param_list) == 2:
            return func(parsed_param_list[0], parsed_param_list[1])
        else:
            print("Too many arguments are given.")
            exit()


