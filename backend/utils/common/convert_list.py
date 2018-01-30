def split_list(list, num=50):
    splited_list = [list[x:x + num] for x in range(0, len(list), num)]
    return splited_list