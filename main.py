import FacetAndFuncs as faf
from pathlib import Path

if __name__ == '__main__':
    # получаем первоначальную информацию о многограннике из txt файла
    way = input("путь к файлу: ")
    with open(way, "r") as fle:
        lines = fle.read().splitlines()
    normals = [lines[1 + ind * 7] for ind in range(int((len(lines) - 2) / 7))]
    bunch_facets = faf.obtain_info(lines, normals)

    # теперь эти вершины сортируем, на выходе получается грань
    for i in range(len(bunch_facets)):
        faf.Facet.facets.append(faf.Facet(faf.sorting(bunch_facets[i])))

    # заполняем список соседей
    for i in range(len(faf.Facet.facets)):
        for j in range(len(faf.Facet.facets)):
            if i != j:
                faf.Facet.facets[i].add_neighbours(faf.Facet.facets[j])

    # ориентируем многогранник
    faf.orient(faf.Facet.facets)

    print(faf.Facet.all_vertexes)
    print(list(set(faf.Facet.all_vertexes)))
    # проверяем согласованность ориентаций
    if not faf.count_pairs(faf.Facet.facets):
        faf.Facet.set_OK()

    # содание файла и запись в него результатов
    qualities = "Результаты для " + way + ":" + "\n" + "Количество вершин: " + str(len(faf.Facet.facets[0].all_vertexes))
    qualities += "\n" + "Количество ребер: " + str(len(faf.Facet.facets[0].edges)) + "\n" + "Количество граней: "
    qualities += str(len(faf.Facet.facets)) + "\n" + "При этом:" + "\n" + faf.Facet.different_facets() + "\n" + "Ориентируемость: "
    if faf.Facet.OK:
        qualities += "ориентируем"
    else:
        qualities += "неориентируем"
    qualities += "\n" + "Эйлерова характеристика: " + str(faf.Facet.euler()) + "\n" + "Род: " + str(faf.Facet.rod()) + "\n"
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

