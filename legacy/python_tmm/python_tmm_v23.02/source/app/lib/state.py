
class MetaSingleton(type):
    _instances={}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractState(metaclass=MetaSingleton):
    def __init__(self):
        self.data = {}
        self.updateMethods = {}
        self.partialUpdateMethods = {}

    def use(self, key, init_value=[]):
        self.data[key] = init_value
        self.updateMethods[key] = {}
        self.partialUpdateMethods[key] = [{} for _ in init_value]

    def set(self, key, value, index=None):
        if index == None:
            self.data[key] = value
            self._update(key)
        else:
            self.data[key][index] = value
            self._update(key, index)

    def setPartial(self, key, index, value):
        self.set(key, value, index)

    def get(self, key, index=None):
        if index == None:
            return self.data[key]
        else:
            return self.data[key][index]

    def append(self, key, value, index):
        self.data[key].append(index, value)
        self.partialUpdateMethods[key].append(index, {})
        self._update(key)

    def insert(self, key, value, index):
        self.data[key].insert(index, value)
        self.partialUpdateMethods[key].insert(index, {})
        self._update(key)

    def delete(self, key, index):
        del self.data[key][index]
        del self.partialUpdateMethods[key][index]
        self._update(key)

    def bind(self, key, id, method, index=None):
        if index == None:
            self.updateMethods[key][id] = method
        else:
            self.partialUpdateMethods[key][index][id] = method
        self._update(key, index)
    
    def unbind(self, key, id):
        if id in self.updateMethods[key].keys():
            del self.updateMethods[key][id]
        for i, methods in enumerate(self.partialUpdateMethods[key]):
            if id in methods.keys():
                del self.partialUpdateMethods[key][i][id]
                print(id)
        print(self.partialUpdateMethods[key])
        self._update(key)

    def _update(self, key, index=None):
        if index == None:
            method_keys = list(self.updateMethods[key].keys())
            for id in method_keys:
                try:
                    method = self.updateMethods[key][id]
                    method(self.data[key])
                except RuntimeError:
                    del self.updateMethods[key][id]
            for i, methods in enumerate(self.partialUpdateMethods[key]):
                method_keys = list(methods.keys())
                for id in method_keys:
                    try:
                        method = methods[id]
                        method(self.data[key][i])
                    except RuntimeError:
                        del self.partialUpdateMethods[key][i][id]
        else:
            method_keys = list(self.partialUpdateMethods[key][index].keys())
            for id in method_keys:
                try:
                    method = self.partialUpdateMethods[key][index][id]
                    method(self.data[key][index])
                except RuntimeError:
                    del self.partialUpdateMethods[key][index][id]