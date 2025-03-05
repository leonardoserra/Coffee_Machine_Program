import sys

# import utils
# import menu
from . import utils
from . import menu
from time import sleep


def shut_down():
    print("Machine...")
    sleep(0.50)
    print(".")
    sleep(0.50)
    print("..")
    sleep(0.50)
    print("...")
    sleep(0.50)
    print("...off")


def show_status():
    for k, v in utils.status.items():
        print(f"{k}: {v}")


def prepare_params(choice):
    params = {
        "selected": menu.MENU[choice]["ingredients"],
        "cost": menu.MENU[choice]["cost"],
        "status": utils.status,
    }

    return params


def is_available(selected, status):
    available = True
    for k in selected:
        if selected[k] > status[k]:
            print(f"{k} not enough: {status[k]} left, needed {selected[k]}")
            available = False

    if not available:
        print("Choose another product.")

    return available


def manage_money(cost, selected, status):
    total = 0

    while total < cost:
        coin = input(
            f"\nCost: ${cost}\n- quarter = $0.25\n- dime = $0.10\n- nickle = $0.05\n- penny = $0.01\n- : "
        )
        if coin == "end money":
            print(f"take back your dirty poorman money... ${round(total, 2)}")
            cost = 0
            total = 0
            break

        elif coin in utils.coin_map:
            total += utils.coin_map[coin]

        else:
            print("choose a valid coin format.")

        print(f"inserted: ${total}")

    for k in selected:
        status[k] -= selected[k]

    status.setdefault("Money", 0)
    status["Money"] += cost

    change = total - cost

    return change


def main():

    while True:
        choice = input("What would you like?\n- espresso\n- latte\n- cappuccino\n: ")

        if choice == "off":  # secret word for technicians
            shut_down()
            break

        elif choice == "report":
            show_status()

        elif choice in ("espresso", "latte", "cappuccino"):

            selected = menu.MENU[choice]["ingredients"]
            cost = menu.MENU[choice]["cost"]
            status = utils.status

            # check if resources are enough
            if not is_available(selected, status):
                continue

            else:
                change = manage_money(cost, selected, status)

                if change:
                    print(f"Here's your change: ${round(change,2)}")

                print(f"Enjoy your {choice.title()}")

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
