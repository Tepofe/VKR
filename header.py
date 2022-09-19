class Facet:
    all_vertexes = []  # список всех вершин многогранника
    edges = []  # список всех ребер многогранника
    facets = []  # список всех граней многогранника
    OK = False  # атрибут, отвечающий за ориентируемость (начальное значение False - неориентируем)
    euler_val = -1  # значение эйлеровой характеристики многогранника
    rod_val = -1  # з

    def __init__(self, vertexes: list):  #
        self.vertexes = vertexes  #
        self.wasOKed = False  #
        self.start = False
        self.neighbours = []  #
        self.numb_of_edges = len(self.vertexes)  #
        self.wasreversed = False  #
        for i in range(self.numb_of_edges):  #
            if self.vertexes[i] not in self.all_vertexes:  #
                self.all_vertexes.append(self.vertexes[i])  #

    @classmethod
    def different_facets(cls):
        evry_edg = []
        info_of_edg = ""
        for i in range(len(Facet.facets)):
            evry_edg.append(Facet.facets[i].numb_of_edges)
        diff_edg = list(set(evry_edg))
        for i in range(len(diff_edg)):
            info_of_edg += "Количество " + str(diff_edg[i]) + "-угольных граней: " + str(evry_edg.count(diff_edg[i])) + "\n"
        return info_of_edg

    @classmethod
    def set_OK(cls):
        Facet.OK = True

    @classmethod
    def euler(cls):
        Facet.euler_val = len(Facet.all_vertexes) - len(Facet.edges) + len(Facet.facets)
        return Facet.euler_val

    @classmethod
    def rod(cls):
        if Facet.OK:
            Facet.rod_val = 1 - (Facet.euler()/2)
        else:
            Facet.rod_val = 2 - Facet.euler()
        return int(Facet.rod_val)

    def reverse(self):
        self.vertexes.reverse()
        if self.wasreversed:
            self.wasreversed = False
        else:
            self.wasreversed = True
        for i in range(len(self.neighbours)):
            self.neighbours[i][1], self.neighbours[i][2] = self.neighbours[i][2], self.neighbours[i][1]

    def is_neighbour(self, n_inq):
        if self.vertexes[0] in n_inq.vertexes and self.vertexes[- 1] in n_inq.vertexes:
            ind_first = n_inq.vertexes.index(self.vertexes[0])
            ind_last = n_inq.vertexes.index(self.vertexes[- 1])
            if self.vertexes[0] + " ; " + self.vertexes[- 1] not in self.edges and self.vertexes[- 1] + " ; " + self.vertexes[0] not in self.edges:
                self.edges.append(self.vertexes[0] + " ; " + self.vertexes[- 1])
            return ['0', ind_first, ind_last]
        else:
            for ind in range(len(self.vertexes) - 1):
                if self.vertexes[ind] in n_inq.vertexes and self.vertexes[ind + 1] in n_inq.vertexes:
                    ind_i = n_inq.vertexes.index(self.vertexes[ind])
                    ind_next = n_inq.vertexes.index(self.vertexes[ind + 1])
                    if self.vertexes[ind] + " ; " + self.vertexes[ind + 1] not in self.edges and self.vertexes[
                        ind + 1] + " ; " + self.vertexes[ind] not in self.edges:
                        self.edges.append(self.vertexes[ind] + " ; " + self.vertexes[ind + 1])
                    return ['n', ind_i, ind_next]

    def add_neighbours(self, pair):
        a = self.is_neighbour(pair)
        if a is not None:
            self.neighbours.append([pair, a[1], a[2], a[0]])

    def is_OK(self, pair):  # pair - элемент списка соседей self
        if pair[3] == 'n':
            if pair[1] == 0 and pair[2] == pair[0].numb_of_edges - 1:
                return None
            elif pair[1] < pair[2]:
                return False
            elif pair[2] == 0 and pair[1] == pair[0].numb_of_edges - 1:
                return False
        elif pair[3] == '0':
            if pair[2] == 0 and pair[1] == pair[0].numb_of_edges - 1:
                return None
            elif pair[1] > pair[2]:
                return False
            elif pair[1] == 0 and pair[2] == pair[0].numb_of_edges - 1:
                return False

    def check_nbrs(self, nghbr):
        for i in range(len(self.neighbours)):
            if self.neighbours[i][0] == nghbr:
                return i
        return -1


def obtain_info(all_l, list_norm):  # функция, с помощью которой мы объединяем все вершины каждой грани
    bunch = []
    face = [all_l[i] for i in range(3, 6)]
    for ind in range(1, len(list_norm)):
        if list_norm[ind] != list_norm[ind - 1]:
            bunch.append(face)
            face = []
        elif all_l[(ind - 1) * 7 + 3] != all_l[ind * 7 + 3]:
            bunch.append(face)
            face = []
        face.append(all_l[ind * 7 + 3])
        face.append(all_l[ind * 7 + 4])
        face.append(all_l[ind * 7 + 5])
    bunch.append(face)
    for i in range(len(bunch)):
        for j in range(len(bunch[i])):
            bunch[i][j] = bunch[i][j].replace('        vertex ', '')
            bunch[i][j] = bunch[i][j].replace('-0.00', '0.00')
    return bunch


def sorting(coord):  # функция для упорядочивания вершин одной грани
    result = [coord[0]]
    leng = len(coord) / 3
    for i in range(1, len(coord)):
        if coord.count(coord[i]) == 1:
            result.append(coord[i])
            if coord[i - 1] != coord[0]:
                result.append(coord[i - 1])
                del coord[i - 1:i + 1]
            else:
                result.append(coord[i + 1])
                del coord[i:i + 2]
            break
    while len(coord) != leng:
        for i in range(1, len(coord)):
            if coord[i] == result[len(result) - 1]:
                if coord[i - 1] != coord[0]:
                    result.append(coord[i - 1])
                    del coord[i - 1:i + 1]
                else:
                    result.append(coord[i + 1])
                    del coord[i:i + 2]
                break
    return result


def orient(input_vertex):  # функция согласования ориентаций
    for i in range(len(input_vertex)):
        if i == 0:
            input_vertex[i].wasOKed = True
            input_vertex[i].start = True
        if not input_vertex[i].wasOKed:
            input_vertex[i].start = True
            for j in range(i):
                res = input_vertex[i].check_nbrs(input_vertex[j])
                if res != -1:
                    if input_vertex[i].neighbours[res][0].wasreversed:
                        input_vertex[i].neighbours[res][1], input_vertex[i].neighbours[res][2] = input_vertex[i].neighbours[res][2], input_vertex[i].neighbours[res][1]
                    if input_vertex[i].is_OK(input_vertex[i].neighbours[res]) is not None:
                        input_vertex[i].reverse()
                    input_vertex[i].wasOKed = True
                    break
        for j in range(i + 1, len(input_vertex)):
            res = input_vertex[i].check_nbrs(input_vertex[j])
            if res != -1:
                if input_vertex[i].is_OK(input_vertex[i].neighbours[res]) is not None:
                    input_vertex[j].reverse()
                input_vertex[j].wasOKed = True
                input_vertex[j], input_vertex[i + 1] = input_vertex[i + 1], input_vertex[j]
                break


def count_pairs(ver):  # функция проверки согласованности ориентаций на смежных гранях
    errs = False
    for m in range(len(ver)):
        for j in range(m+1, len(ver)):
            # if ver[m].start or ver[j].start:
            chk = ver[m].is_neighbour(ver[j])
            if chk is not None:
                nb = [ver[j], chk[1], chk[2], chk[0]]
                if ver[m].is_OK(nb) is not None:
                    # errs += a + ', ' + str(m) + ', ' + str(j) + '; '
                    errs = True
    return errs
