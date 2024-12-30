

class File:

    def read(self, name, path, mode='a+'):
        file_path = path + name
        file = open(file_path, 'a+')
        return file.read()

    def write(self, content, name, path="", mode='w'):
        file_path = path + name
        file = open(file_path, mode)
        file.write(content)
        file.close()
