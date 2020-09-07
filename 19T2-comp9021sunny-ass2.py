from collections import defaultdict

list_direction = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

#yuchen yang
def graph(a,graph_list,x,y):
    (x1, y1) = graph_list[-2]
    (x2, y2) = graph_list[-1]
    x3 = x1 - x2
    y3 = y1 - y2
    index = list_direction.index((x3,y3))
    if index == 7:
        index = -1
    new_list = list_direction[(index + 1):] + list_direction[:index + 2] #不要out of range
    find = 0
    for (x4, y4) in new_list:
        new_x = x2 + x4
        new_y = y2 + y4
        if new_x < 0 or new_x >= len(a):
            continue #return就结束了
        if new_y < 0 or new_y >= len(a[0]):
            continue
        if a[new_x][new_y] == 1:
            find = 1
            graph_list.append((new_x, new_y))
            break
    if graph_list.count((x,y))!=2 and find: #考虑（0，0）情况 所以要find
        graph(a,graph_list,x,y)
        
#yuchen yang
def area(list1):
    sum = 0
    for i in range(len(list1)):
        sum += (list1[i][0] * list1[i-1][1]) - (list1[i][1] * list1[i-1][0])
    return abs(sum/2)

#yuchen yang
def convex(list2):
    sum = 0
    for i in range(len(list2)):
        if list2[i] != list2[i-1]:
            sum += (list2[i] - list2[i-1]) % 8
    if sum == 8:
        return True
    else:
        return False

#yuchen yang
def invariant_rotations(list1, list2):
    temp=[]
    for i in range(len(list2)):
        if list2[i]!=list2[i]-1:
            temp.append(list1[i])
    mind_x = temp[0][0]+temp[len(temp)//2][0]
    mind_y = temp[0][1]+temp[len(temp)//2][1]
    if len(temp) % 2 == 1:
        return 1
    for i in range(len(temp)//2):
        if (temp[i][0] + temp[len(temp)//2+i][0]) == mind_x and mind_y == (temp[i][1]+temp[len(temp)//2+i][1]):
            if len(temp) % 4 == 0:
                for j in range(len(temp)//4):
                    if (mind_y+mind_x-temp[i][1],temp[i][0]-mind_x+mind_y) not in temp:
                        return 2
                return 4
            else:
                return 2
        else:
            return 1

#yuchen yang
def shexian(point,list1):
    x,y = point
    count = 0
    for i in range(len(list1)):
        if list1[i]!=list1[i-1]:
            x1,y1 = list1[i]
            x2,y2 = list1[i-1]
            if y <= min(y1,y2) or y > max(y1,y2):
                pass
            else:
                if x < ((x1-x2)*(y-y1)/(y1-y2)+x2):
                    count+=1
    return count%2

#yuchen yang
class PolygonError(Exception):
    def __init__(self,errormessage):
        #super(PolygonError,self).__init__()
        self.inform = errormessage

    def error(self):
        return self.inform

#yuchen yang
class Polygons:
    def __init__(self,file_name):
        self.data = []
        self.shape = defaultdict(list)
        with open(file_name) as file:
            new_file = file.read()
            new_file = new_file.replace(' ','')
            self.data = new_file.split()

    def analyse(self):
        a = self.data[:]
        #每行长度相等(2-50)
        #列（2-50)
        if not 2 <= len(a) <= 50:
            raise PolygonError('Incorrect input.')
        for i in range(len(a)):
            if len(a[i]) != len(a[i-1]):
                raise PolygonError('Incorrect input.')
            if not 2 <= len(a[i]) <= 50:
                raise PolygonError('Incorrect input.')
            b = []
            for j in a[i]:
                try:
                    j = int(j)
                    if j in range(2):
                        b.append(j)
                    else:
                        raise PolygonError('Incorrect input.')
                except ValueError:
                    raise PolygonError('Incorrect input.')
            a[i] = b

        color = 2
        for i in range(len(a)):
            for j in range(len(a[0])):
                graph_list = []
                shape = []
                if a[i][j] == 1:
                    graph_list.append((i-1, j))
                    graph_list.append((i,j))
                    graph(a,graph_list,i,j)

                if graph_list == []:
                    pass
                if len(graph_list) == 2:
                    raise PolygonError('Cannot get polygons as expected.')

                graph_list = graph_list[1:-1]
                if len(graph_list) == 2:
                    raise PolygonError('Cannot get polygons as expected.')

                k = 0
                while k < len(graph_list):
                    shape.append(graph_list[k])
                    if graph_list.count(graph_list[k]) == 2:
                        k = graph_list.index(graph_list[k],k+1)
                    k += 1

                if len(graph_list) == 1:
                    raise PolygonError('Cannot get polygons as expected.')

                for (m,n) in shape:
                    a[m][n] = color
                if shape:
                    self.shape[color-1].append(shape)
                    color += 1

        for m in self.shape:
            temp=[]
            for n in range(len(self.shape[m][0])):
                x = self.shape[m][0][n-1][0] - self.shape[m][0][n][0]
                y = self.shape[m][0][n-1][1] - self.shape[m][0][n][1]
                temp.append(list_direction.index((x,y)))
            self.shape[m].append(temp)
            count = 0
            for l in temp:
                if l%2 == 1:
                    count += 1
            self.shape[m].append((0.4*(len(temp)-count),count))
            self.shape[m].append(area(self.shape[m][0])*0.16)
            self.shape[m].append(convex(self.shape[m][1]))
            self.shape[m].append(invariant_rotations(self.shape[m][0],self.shape[m][1]))
            count=0
            for n in self.shape:
                if m!=n:
                   count += shexian(self.shape[m][0][0],self.shape[n][0])

            print(self.shape[m],count)




        #print(area(self.shape[1][0])*0.16)
        #print(convex(self.shape[1][1]))


    def display(self):
        pass


#yuchen yang
polys = Polygons('polys_4.txt')
polys.analyse()
#yuchen yang


