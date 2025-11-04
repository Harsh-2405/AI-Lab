from graph_data import create_social_graph
from suggestion import suggest_friends_by_degree
from visualize import visualize_graph

def main():
    graph = create_social_graph()
    visualize_graph(graph)

    user = input("Enter user name for friend suggestions: ").strip()

    if user not in graph:
        print(f"User '{user}' not found in the network.")
        return

    suggestions = suggest_friends_by_degree(graph, user, max_depth=3)

    print(f"\n Friend suggestions for {user}:")
    print("➡ 1st-degree friends (Direct):")
    print("   ", ', '.join(suggestions[1]) if suggestions[1] else "None")

    print("➡ 2nd-degree friends (Friends of Friends):")
    second = suggestions[2] - suggestions[1] - {user}
    print("   ", ', '.join(second) if second else "None")

    print("➡ 3rd-degree friends (Mutual of Mutual):")
    third = suggestions[3] - suggestions[2] - suggestions[1] - {user}
    print("   ", ', '.join(third) if third else "None")

if __name__ == "__main__":
    main()
