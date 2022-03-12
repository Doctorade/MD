class Note:
    def __init__(self, timeStamp, score, energy, combo):
        self.timeStamp = timeStamp # 对应与时间戳列表中的索引，类型为TimeStamp索引
        self.score = score # 类型为整数
        self.energy = energy # 类型为整数
        self.feverWindow = FeverWindow()
        self.combo = combo

class FeverWindow:
    'f积攒能量和持续结束的n总和，包含积攒能量的n所在t、持续结束n所在t、开启的n所在t、分数总增值'
    def __init__(self):
        self.start = -1 # 窗口起始点，类型为note索引
        self.open = -1 # 开启f点，只是指向时间戳的位置，意思是f包含了这个note，类型为note索引
        self.extraScore = 0 # 增益总分，类型为整数

class TimeStamp:
    '每个时间单位有一个时间戳，这个时间戳记录了当前位置有什么类型的n以及以此为终点之前的最优解是什么，包含n的分值、能量、时间位置、以及最优解的窗口、最优解增益的总和'
    def __init__(self):
        self.note = -1 # 对应与note列表中的索引，-1代表没有note，类型为note索引
        self.finalWindows = [] # 类型为FeverWindow的列表
        self.maxExtraScore = 0 # 类型为整数

def Caculate(feverReduceTime):
    # 最开始计算出单位时间的个数
    bpm = 98
    T = 5 / bpm # 取这个值作单位时间可以使得间隔为整数个单位时间，例如十六分为3个单位时间，二十四分为2个
    FT = int(5.1 / T) - feverReduceTime # 一个fever当作5100ms
    time = 96  # 曲目单位s
    timeStampNum = int(time / T)

    # 读取谱面，构建note列表
    chart = [0, 200, 2, 1,
             6, 200, 2, 2,
             12, 200, 2, 3,
             15, 200, 2, 4,
             21, 200, 2, 5,
             24, 200, 2, 6,
             30, 200, 2, 7,
             36, 200, 2, 8,
             48, 400, 4, 9,
             84, 400, 4, 11,
             96, 400, 4, 13,
             108, 200, 2, 15,
             132, 200, 2, 16,
             144, 400, 4, 17,
             180, 200, 2, 19,
             192, 0, 4, 20,
             240, 300, 2, 21,
             288, 200, 2, 22,
             300, 200, 2, 23,
             312, 200, 2, 24,
             324, 200, 2, 25,
             336, 200, 2, 26,
             384, 200, 2, 27,
             396, 200, 2, 28,
             408, 200, 2, 29,
             420, 200, 2, 30,
             432, 200, 2, 31,
             444, 200, 2, 32,
             450, 200, 2, 33,
             456, 200, 2, 34,
             468, 200, 2, 35,
             480, 200, 2, 36,
             492, 200, 2, 37,
             498, 200, 2, 38,
             504, 200, 2, 39,
             516, 200, 2, 40,
             528, 200, 2, 41,
             540, 200, 2, 42,
             546, 200, 2, 43,
             552, 200, 2, 44,
             564, 200, 2, 45,
             576, 200, 2, 46,
             588, 400, 4, 47,
             600, 400, 4, 49,
             612, 400, 4, 51,
             624, 400, 4, 53,
             636, 200, 2, 55,
             642, 200, 2, 56,
             648, 200, 2, 57,
             660, 200, 2, 58,
             672, 200, 2, 59,
             684, 200, 2, 60,
             690, 200, 2, 61,
             696, 200, 2, 62,
             708, 200, 2, 63,
             720, 200, 2, 64,
             732, 200, 2, 65,
             738, 200, 2, 66,
             744, 200, 2, 67,
             756, 200, 2, 68,
             768, 200, 2, 69,
             780, 400, 4, 70,
             792, 400, 4, 72,
             804, 400, 4, 74,
             816, 500, 4, 76,
             822, 300, 2, 78,
             828, 300, 2, 79,
             834, 300, 2, 80,
             840, 300, 2, 81,
             846, 300, 2, 82,
             852, 300, 2, 83,
             858, 300, 2, 84,
             864, 300, 2, 85,
             870, 300, 2, 86,
             876, 300, 2, 87,
             882, 300, 2, 88,
             888, 300, 2, 89,
             894, 300, 2, 90,
             900, 300, 2, 91,
             906, 300, 2, 92,
             912, 300, 2, 93,
             918, 300, 2, 94,
             924, 300, 2, 95,
             930, 300, 2, 96,
             936, 300, 2, 97,
             942, 300, 2, 98,
             948, 300, 2, 99,
             954, 300, 2, 100,
             960, 300, 2, 101,
             966, 300, 2, 102,
             972, 300, 2, 103,
             978, 300, 2, 104,
             984, 300, 2, 105,
             990, 300, 2, 106,
             996, 300, 2, 107,
             1008, 200, 2, 108,
             1020, 400, 4, 109,
             1032, 400, 4, 111,
             1044, 400, 4, 113,
             1056, 500, 4, 115,
             1062, 300, 2, 117,
             1068, 300, 2, 118,
             1074, 300, 2, 119,
             1080, 300, 2, 120,
             1086, 300, 2, 121,
             1092, 300, 2, 122,
             1098, 300, 2, 123,
             1104, 400, 4, 124,
             1140, 400, 4, 126,
             1152, 0, 4, 128,
             1212, 300, 2, 129,
             1236, 300, 2, 130,
             1242, 300, 2, 131,
             1248, 200, 2, 132,
             1260, 400, 4, 133,
             1272, 400, 4, 135,
             1284, 500, 4, 137,
             1290, 300, 2, 139,
             1296, 200, 2, 140,
             1332, 400, 4, 141,
             1344, 400, 4, 143,
             1362, 500, 4, 145,
             1368, 200, 2, 147,
             1377, 400, 4, 148,
             1386, 500, 4, 150,
             1392, 300, 2, 152,
             1398, 300, 2, 153,
             1404, 200, 2, 154,
             1434, 500, 4, 155,
             1440, 200, 2, 157,
             1458, 400, 4, 158,
             1476, 500, 4, 160,
             1488, 0, 4, 162,
             1500, 0, 4, 163, ]  # 谱面应该具有四个属性，依次为在时间轴上的位置（第一个note出现为0时间），分数能量，暂时默认谱面位置处理为了单位时间的时间戳

    # 处理时间位置
    notes = []
    for i in range(0, len(chart), 4):
        notes.append(Note(chart[i], chart[i + 1], chart[i + 2], chart[i + 3]))

    # for note in notes:
    #     print(note.timeStamp, end=", ")
    #     print(note.score, end=", ")
    #     print(note.energy, end=", ")
    #     print(note.combo, end=", ")
    #     print()

    # 将时间戳分配好其他置为0
    timeStamps = []
    for i in range(timeStampNum):
        timeStamps.append(TimeStamp())

    # 根据note列表将时间戳列表数据补全
    for i in range(len(notes)):
        timeStamps[notes[i].timeStamp].note = i
    # for timeStamp in timeStamps:
    #     print(timeStamp.note)

    # 计算所有窗口，同时给出第一个窗口的终点
    startTimeStamp = -1  # 第一个窗口终点的时间戳，类型为时间戳索引
    cantFever = False
    for i in range(len(notes)):
        # 首先找到开F的点
        initalEnergy = 0
        j = i
        while initalEnergy < 120:
            initalEnergy += notes[j].energy
            if j + 1 >= len(notes):  # 超出note数组说明不足以创建一个窗口，上一个已经是最后一个了
                print(initalEnergy, i, j)
                cantFever = True
                break
            j += 1
        if cantFever:
            break
        openNote = j  # 开启f的点
        # 下面找到F结束的点，将这个窗口存入那个点中
        temFT = FT
        temExtraScore = notes[openNote].score * 0.5
        while 1:  # 判断的是当前j指向note的下一个是否能装进f
            if j + 1 >= len(notes):  # 如果是最后一个note那就直接将这个最后的当作f生效的最后一个
                cantFever = True
                break
            temFT -= notes[j + 1].timeStamp - notes[j].timeStamp
            if temFT < 0:
                break
            temExtraScore += notes[j + 1].score * 0.5
            j += 1
        # 将这个窗口赋给结尾，也就是F生效的最后一个note
        if notes[j].feverWindow.start != 0:  # 会有冲突的原因是可能有的正好取到120有的大于了120
            if notes[j].feverWindow.extraScore < temExtraScore:
                notes[j].feverWindow.open = openNote
                notes[j].feverWindow.start = i
                notes[j].feverWindow.extraScore = temExtraScore
    # for note in notes:
    #     print(note.feverWindow.start)

    # 找到第一个窗口，将对应窗口终点时间戳的最优解赋为这个窗口
    for note in notes:
        if note.feverWindow.start != -1:
            startTimeStamp = note.timeStamp + 1  # 此时j指向的是最后一个生效的note，所以要从下一个时间作为开始
            timeStamps[note.timeStamp].finalWindows.append(note.feverWindow)
            timeStamps[note.timeStamp].maxExtraScore = note.feverWindow.extraScore
            # print(timeStamps[note.timeStamp].note)
            break

    # 上面计算得出的起点note所在时间戳作为起点，依次往后索引，如果时间戳上没有note，将上一个时间戳的最优解和最高增益填入这个时间戳
    # 如果遇到时间戳上有note则假设将当前窗口装入，向前找到这个窗口的起点，起点前一个时间戳的增值总和加上当前窗口的总和如果大于当前时间戳的前一个的增值总和
    # 则将当前时间戳最优解等同于起点前一个时间戳的最优解并将当前窗口加入，不大于则等效于没有note
    for i in range(startTimeStamp, len(timeStamps)):
        if timeStamps[i].note == -1:
            timeStamps[i].maxExtraScore = timeStamps[i - 1].maxExtraScore
            timeStamps[i].finalWindows = timeStamps[i - 1].finalWindows
        elif notes[timeStamps[i].note].feverWindow.start != -1:
            if timeStamps[notes[notes[timeStamps[i].note].feverWindow.start].timeStamp].maxExtraScore + notes[
                timeStamps[i].note].feverWindow.extraScore > timeStamps[i - 1].maxExtraScore:
                timeStamps[i].maxExtraScore = timeStamps[notes[
                    notes[timeStamps[i].note].feverWindow.start].timeStamp].maxExtraScore + notes[
                                                  timeStamps[i].note].feverWindow.extraScore
                timeStamps[i].finalWindows = timeStamps[
                    notes[notes[timeStamps[i].note].feverWindow.start].timeStamp].finalWindows
                timeStamps[i].finalWindows.append(notes[timeStamps[i].note].feverWindow)
            else:
                timeStamps[i].maxExtraScore = timeStamps[i - 1].maxExtraScore
                timeStamps[i].finalWindows = timeStamps[i - 1].finalWindows

    # for timeStamp in timeStamps:
    #     if timeStamp.maxExtraScore != 0:
    #         print(timeStamp.maxExtraScore)

    for note in timeStamps[timeStampNum - 1].finalWindows:  # 最后一个时间戳上的就是最终解
        print(notes[note.open].combo, end="  ")

Caculate(6)