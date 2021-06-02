class Node:
    def __init__(self, x=0, y=0, color=(0,0,0)):
        self.x = x
        self.y = y
        self.color = color

    def search(self, source, target, graph, costs):
        parents = {}
        nextNode = source
        while nextNode != target:
            for neighbor in graph[nextNode]:
                if graph[nextNode][neighbor] + costs[nextNode] < costs[neighbor]:
                    costs[neighbor] = graph[nextNode][neighbor] + costs[nextNode]
                    parents[neighbor] = nextNode
                del graph[neighbor][nextNode]
            del costs[nextNode]
            nextNode = min(costs, key=costs.get)
        return (parents)

    def backpedal(self, source, target, searchResult):
        node = target
        backpath = [target]
        path = []
        while node != source:
            backpath.append(searchResult[node])
            node = searchResult[node]
        for i in range(len(backpath)):
            path.append(backpath[-i - 1])
        return path