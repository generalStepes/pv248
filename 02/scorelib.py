def load(filename):
    printList = []
    for line in open(filename, 'r', encoding="utf8"):
        splitLine = (line.split(":"))
        try:
            splitLine[1] = (splitLine[1].strip())
        except:
            continue
        if splitLine[0] == "Print Number":
            object = Print(splitLine[1])
            print (object.print_id)


class Print:
    def __init__(self, print_id, edition, partiture):
        self.print_id = print_id
        self.edition = edition
        self.partiture = partiture
