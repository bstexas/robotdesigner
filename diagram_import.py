import xmltodict


def find_path(graph, start, end, path=None):
    if path is None:
        path = []
    # https://www.python.org/doc/essays/graphs/
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None

def is_arrow(cell): 
    return "arrow" in cell.get("@style", "").lower()

def is_curved(cell):
    return "curved=1" in cell.get("@style", "")


def main():
    xml = xmltodict.parse(open("robot.xml", "rb"))
    cells = xml["mxGraphModel"]["root"]["mxCell"]
    non_curved_arrows = [
        cell for cell in cells if is_arrow(cell) and not is_curved(cell)
    ]
    start = next(
        cell["@target"] for cell in non_curved_arrows if "@source" not in cell
    )
    end = next(
        cell["@source"] for cell in non_curved_arrows if "@target" not in cell
    )
    graph = {
        cell["@source"]: [cell["@target"]] for cell in non_curved_arrows
        if "@source" in cell and "@target" in cell
    }
    path = find_path(graph, start, end)
    cells_by_id = {cell["@id"]: cell for cell in cells}
    print("    ")
    print("First test case")
    print("\n".join("    " + cells_by_id[_id]["@value"] for _id in path))
    print("    ")

if __name__ == '__main__':
    main()
