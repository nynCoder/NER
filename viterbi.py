'''viterbi算法
参考链接：https://www.zhihu.com/question/20136144?sort=created，结合图解和代码，就清晰了'''


# state 存放隐藏序列，sunny 0 rainy 1
# obser 存放观测序列  0 1 2 对应 walk shop clean
# start_p 是初始概率，0元素对应sunny的初始概率 1元素对应rainy的概率
# transition_p 转移概率矩阵 2*2 行为初始状态  列为新状态
# emission_p 发射概率矩阵 2*3 行为隐藏状态  列为可观测状态

# 迭代过程，每次只需要记录第t个时间点 每个节点的最大概率即可，后续计算时直接使用前序节点的最大概率即可
def compute(obser, state, start_p, transition_p, emission_p):
    # max_p 记录每个时间点每个状态的最大概率，i行j列，（i,j）记录第i个时间点 j隐藏状态的最大概率
    max_p = [[0 for col in range(len(state))] for row in range(len(obser))]
    # path 记录max_p 对应概率处的路径 i 行 j列 （i,j）记录第i个时间点 j隐藏状态最大概率的情况下 其前驱状态
    path = [[0 for col in range(len(state))] for row in range(len(obser))]
    # 初始状态(1状态)
    for i in range(len(state)):
        # max_p[0][i]表示初始状态第i个隐藏状态的最大概率
        # 概率 = start_p[i] * emission_p [state[i]][obser[0]]
        max_p[0][i] = start_p[i] * emission_p[state[i]][obser[0]]
        path[0][i] = i
    # 后续循环状态(2-t状态)
    # 此时max_p 中已记录第一个状态的两个隐藏状态概率
    for i in range(1, len(obser)):  # 循环t-1次，初始已计算
        max_item = [0 for i in range(len(state))]  # 存储当前层每个状态的最大概率时的那个前驱状态
        # 跟全连接层的差不多
        for j in range(len(state)):  # 遍历计算当前层状态每个隐藏状态的概率
            item = [0 for i in state]  # 临时变量，存储当前层该状态下每个前驱状态的概率
            for k in range(len(state)):  # 再次循环，这里是选定当前层的状态时的前驱状态为各种状态的概率
                p = max_p[i - 1][k] * emission_p[state[j]][obser[i]] * transition_p[state[k]][state[j]]
                # k即代表前驱状态 k或state[k]均为前驱状态
                item[state[k]] = p
            # 设置概率记录为最大情况
            max_item[state[j]] = max(item)
            # 记录最大情况路径(下面语句的作用：当前时刻下第j个状态概率最大时，记录其前驱节点)
            # item.index(max(item))寻找item的最大值索引，因item记录各种前驱情况的概率
            path[i][state[j]] = item.index(max(item))
        # 将单个状态的结果加入总列表max_p
        max_p[i] = max_item
    # newpath记录最后路径
    newpath = []
    # 判断最后一个时刻哪个状态的概率最大
    p = max_p[len(obser) - 1].index(max(max_p[len(obser) - 1]))
    newpath.append(p)
    # 从最后一个状态开始倒着寻找前驱节点
    for i in range(len(obser) - 1, 0, -1):
        newpath.append(path[i][p])
        p = path[i][p]
    newpath.reverse()
    return newpath


if __name__ == '__main__':
    #   隐状态
    hidden_state = ['rainy', 'sunny']
    #   观测序列
    obsevition = ['walk', 'shop', 'clean']
    state_s = [0, 1]
    obser = [0, 1, 2]
    #   初始状态，测试集中，0.6概率观测序列以sunny开始
    start_probability = [0.6, 0.4]
    #   转移概率，0.7：sunny下一天sunny的概率
    transititon_probability = [[0.7, 0.3], [0.4, 0.6]]
    #   发射概率，0.4：sunny在0.4概率下为shop
    emission_probability = [[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]]
    result = compute(obser, state_s, start_probability, transititon_probability, emission_probability)
    for k in range(len(result)):
        print(hidden_state[int(result[k])])
