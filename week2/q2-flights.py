from typing import Dict, List, ForwardRef
from dataclasses import dataclass, field
import sys
import heapq

@dataclass
class Route:
    airports: List[str]
    price: int
    def __lt__(self, other):
        return self.price < other.price

@dataclass
class Flight:
    departs: str
    arrives: str
    price: int
@dataclass
class Node:
    code: str
    connections: Dict[str, ForwardRef("Edge")] = field(default_factory=dict)

@dataclass
class Edge:
    price: int
    node: Node

def build_graph(flights: List[Flight]) -> Dict[str, Node]:
    nodes: Dict[str, Node] = {}
    for flight in flights:
        assert flight.price > 0
        node = nodes.setdefault(flight.departs, Node(flight.departs))
        assert flight.arrives not in node.connections, f"Duplicate!"
        node.connections[flight.arrives] = Edge(flight.price, Node(flight.arrives))
    return nodes 

def find_connections(graph: Dict[str, Node], start: str, end: str, limit=10) -> List[Route]:
    if not graph[start]:
        return []
    result = []
    heapq.heapify(result)
    queue = [(0, Route([start], 0))]
    heapq.heapify(queue)
    cheapest_option_per_city: Dict[str, int] = { start: 0 }
    while queue:
        route: Route = heapq.heappop(queue)[1]
        if route.airports[-1] == end:
            # found a route
            heapq.heappush(result, route)
        else:
            if len(route.airports) < limit:
                current_terminus = route.airports[-1]
                if current_terminus in graph:
                    for next_dest, edge in graph.get(current_terminus).connections.items():
                        airports = [*route.airports, next_dest]
                        price_for_route = route.price + edge.price
                        if next_dest not in cheapest_option_per_city or cheapest_option_per_city.get(next_dest) >= price_for_route: 
                            cheapest_option_per_city[next_dest] = price_for_route
                            new_route = Route(airports, price_for_route)
                            heapq.heappush(queue, (price_for_route, new_route))
    return [route for route in heapq.nsmallest(limit, result)]


def read_flight() -> Flight:
    line = str(sys.stdin.readline())
    split = line.split(' ')
    assert len(split) == 3
    origin = split[0]
    dest = split[1]
    price = int(split[2])
    return Flight(origin, dest, price)


def print_plan(route: Route):
    airports = " ".join(route.airports)
    print(f"{airports} {route.price}")

def main():
  flights = []
  number_of_flights = int(sys.stdin.readline())
  for i in range(number_of_flights):
    flights.append(read_flight())

  graph = build_graph(flights) 
  limit = int(sys.stdin.readline())
  source_airport, destination_airport = sys.stdin.readline().strip().split(' ')
  connections = find_connections(graph, source_airport, destination_airport, limit)

  if len(connections) == 0:
    print("<no solution>")
  
  for connection in connections:
      print_plan(connection)


if __name__ == '__main__':
  main()

