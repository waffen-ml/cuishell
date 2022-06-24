import os
from time import sleep
from string import punctuation


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def confirm(title):
    inp = input(f'{title} (y/n) ')
    return inp.lower() == 'y'


def _construct_title(s, alt=False):
    starting = '//' if alt else '#'
    ending = '' if s[-1] in punctuation else ':'
    return starting + ' ' + s + ending


def show_title(s, alt=False):
    title = _construct_title(s, alt=alt)
    print(title)


def prompt(title):
    show_title(title)
    return input('] ')


def prompts(*titles):
    inputs = []
    for title in titles:
        inp = prompt(title)
        inputs.append(inp)
    return inputs


def choice(options, title=None):
    if title is not None:
        show_title(title)
    if type(options) == list:
        for i, el in enumerate(options):
            print(f'{i + 1}. {el}')
        inp = input('] ')
        if not inp.isnumeric():
            return None
        idx = int(inp) - 1
        if not (0 <= idx < len(options)):
            return None
        return idx
    elif type(options) == dict:
        for key, el in options.items():
            print(f'{key}. {el}')
        inp = input('] ')
        if inp not in options:
            return None
        return inp
    else:
        return None


def alert(msg):
    time = min(0.075 * len(msg), 10)
    print(msg)
    sleep(time)


def launch_if_exists(obj):
    if obj is not None:
        obj()


def conseq_choice(options, title=None, default=None):
    if title is not None:
        show_title(title)
    if type(options) == list:
        base_list, conseqs = list(zip(*options))
        idx = choice(list(base_list))
        if idx is None:
            launch_if_exists(default)
            return
        conseqs[idx]()
    elif type(options) == dict:
        keys, rem = list(zip(*options.items()))
        vals, conseqs = list(zip(*rem))
        base_dict = dict(zip(keys, vals))
        ch = choice(base_dict)
        if ch is None:
            launch_if_exists(default)
            return
        conseq = conseqs[keys.index(ch)]
        conseq()
    else:
        launch_if_exists(default)
        return


def mixed_choice(options_l, options_d, title=None):
    if title is not None:
        show_title(title)
    for i, el in enumerate(options_l):
        print(f'{i + 1}. {el}')
    for key, el in options_d.items():
        print(f'{key}. {el}')
    inp = input('] ')
    
    if inp.isnumeric():
        idx = int(inp) - 1
        if not (0 <= idx < len(options_l)):
            return None
        return idx
    elif inp in options_d:
        return inp
    else:
        return None


def strweight(s):
    for ch in s:
        if ch not in [' ', '\n']:
            return True
    return False


class Scene:
    def __init__(self, title=None):
        self.title = title
    
    def main(self, *args, **kwargs):
        pass

    def start(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        self.start(*args, **kwargs)
        while True:
            clear()
            if self.title is not None:
                show_title(self.title, alt=True)
            if self.main(*args, **kwargs) == False:
                break


class App:
    def __init__(self, scenes, name):
        self.name = name
        self.scenes = scenes

    def __getitem__(self, name):
        return self.get_scene(name)

    def get_scene(self, name):
        return self.scenes[name]

    def launch_scene(self, name, *args, **kwargs):
        self.get_scene(name)(*args, **kwargs)

    def __call__(self, name, *args, **kwargs):
        self.launch_scene(name, *args, **kwargs)