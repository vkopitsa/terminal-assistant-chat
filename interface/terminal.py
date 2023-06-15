from interface import Interface


class Terminal(Interface):
    def __init__(self, provider):
        self.provider = provider

    def run(self):
        while True:
            user_input = input("# ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            msg = self.provider.process_msg(user_input)

            print(f"{msg}\n")
