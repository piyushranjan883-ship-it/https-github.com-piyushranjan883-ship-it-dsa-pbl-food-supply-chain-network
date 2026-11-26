"""Console program for the Smart Food Supply Chain Collaboration Network."""
import sys

from food_network.network import FoodNetwork
from sample_data import load_sample


def demo(net):
    print("--- Most urgent 3 batches ---")
    for r in net.most_urgent(3):
        print(f"#{r['id']} {r['product']} [{r['location']}] "
              f"{r['kg']} kg, {r['days_left']} day(s) left, priority {r['priority']}")
    print("--- Load plan for Farm Hub A, 1000 kg truck (knapsack) ---")
    print(net.load_plan("Farm Hub A", 1000))
    print("--- Exact 700 kg loads at Farm Hub A (backtracking) ---")
    print(net.exact_load_plans("Farm Hub A", 700))
    print("--- Best route Farm Hub A -> City Food Bank ---")
    print(net.best_route("Farm Hub A", "City Food Bank"))
    print("--- Places within 2 roads of Warehouse W1 ---")
    print(net.nearby_places("Warehouse W1", 2))


def menu(net):
    while True:
        print("\n1 Add batch  2 Find by ID  3 Find by name  4 Urgent batches")
        print("5 Load plan  6 Exact load  7 Nearby places  8 Best route  0 Exit")
        c = input("Choice: ").strip()
        try:
            if c == "1":
                ok, msg = net.add_batch(input("Product: "), input("Location: "),
                                        int(input("Kg: ")), int(input("Days left: ")),
                                        int(input("Priority 1-10: ")))
                print(msg)
            elif c == "2":
                print(net.find_by_id(int(input("ID: "))) or "Not found")
            elif c == "3":
                print(net.find_by_name(input("Name: ")) or "Not found")
            elif c == "4":
                for r in net.most_urgent(3):
                    print(r)
            elif c == "5":
                print(net.load_plan(input("Location: "), int(input("Truck kg: "))))
            elif c == "6":
                print(net.exact_load_plans(input("Location: "), int(input("Truck kg: "))))
            elif c == "7":
                print(net.nearby_places(input("Place: ")) or "Unknown place")
            elif c == "8":
                print(net.best_route(input("From: "), input("To: ")))
            elif c == "0":
                break
        except ValueError:
            print("Please enter numbers where numbers are needed.")


if __name__ == "__main__":
    net = FoodNetwork()
    load_sample(net)
    demo(net) if len(sys.argv) > 1 and sys.argv[1] == "demo" else menu(net)
