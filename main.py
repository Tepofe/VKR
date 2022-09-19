import header as hd
from pathlib import Path

if __name__ == '__main__':
    # получаем первоначальную информацию о многограннике из txt файла
    way = input("путь к файлу: ")
    with open(way, "r") as fle:
        lines = fle.read().splitlines()
    normals = [lines[1 + ind * 7] for ind in range(int((len(lines) - 2) / 7))]
    bunch_facets = hd.obtain_info(lines, normals)

    # теперь эти вершины сортируем, на выходе получается грань
    for i in range(len(bunch_facets)):
        hd.Facet.facets.append(hd.Facet(hd.sorting(bunch_facets[i])))

    # заполняем список соседей
    for i in range(len(hd.Facet.facets)):
        for j in range(len(hd.Facet.facets)):
            if i != j:
                hd.Facet.facets[i].add_neighbours(hd.Facet.facets[j])

    # ориентируем многогранник
    hd.orient(hd.Facet.facets)

    print(hd.Facet.all_vertexes)
    print(list(set(hd.Facet.all_vertexes)))
    # проверяем согласованность ориентаций
    if not hd.count_pairs(hd.Facet.facets):
        hd.Facet.set_OK()

    # содание файла и запись в него результатов
    qualities = "Результаты для " + way + ":" + "\n" + "Количество вершин: " + str(len(hd.Facet.facets[0].all_vertexes))
    qualities += "\n" + "Количество ребер: " + str(len(hd.Facet.facets[0].edges)) + "\n" + "Количество граней: "
    qualities += str(len(hd.Facet.facets)) + "\n" + "При этом:" + "\n" + hd.Facet.different_facets() + "\n" + "Ориентируемость: "
    if hd.Facet.OK:
        qualities += "ориентируем"
    else:
        qualities += "неориентируем"
    qualities += "\n" + "Эйлерова характеристика: " + str(hd.Facet.euler()) + "\n" + "Род: " + str(hd.Facet.rod()) + "\n"
    print(qualities)
    save = input("желаете ли сохранить результаты? (y/n) ")
    if save != 'n':
        res_way = input("путь к каталогу сохранения: ")
        if res_way != '':
            way = "Result of " + Path(way).stem
            result = open(res_way + "\\" + way + ".txt", "a+")
        else:
            result = open(way[:len(way)-4] + " Results" + ".txt", "a+")
        result.write(qualities)
        result.close()

