# ================================== The beginning of the class ================================
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"Country: {self.country} \nCode: {self.code} \nProduct: {self.product} \nCost: {self.cost} \n" \
               f"Quantity: {self.quantity}\n"


# ====================================== Shoe list ==========================================
# The shoe_list will be used to store a list of objects of shoes.

shoe_list = []


# ============================== Functions outside the class ====================================
def read_shoes_data():
    """
    Function reads each line in inventory.txt file. Each line contains information from one stock-taking list.
    Function creates a shoe object for each line and appends it to shoe_list.
    Function contains try-excepts for potential errors surrounding the inventory.txt file.
    :return: the list shoe_list.
    """
    try:
        # Checking existence and correct placement of file inventory.txt.
        inventory_f = open("inventory.txt", "r", encoding="utf-8-sig")
        lines_inventory_f = inventory_f.readlines()
        inventory_f.close()
    except FileNotFoundError as e:
        print(f"Error:{e}")
        return "The file inventory.txt does not exist in this folder. " \
               "Try again once inventory.txt file is in the folder which contains the program inventory.py."

    if not lines_inventory_f[0] == "Country,Code,Product,Cost,Quantity\n":
        # Checking first line of inventory.txt contains correct header.
        return "Error: inventory.txt does not contain the correct header first line. Try again after correction."

    if len(lines_inventory_f) < 3:
        # Checking inventory.txt contains stock takes (data/ lines excluding the header).
        return "Error: file inventory.txt contains no data. Try again after checking the contents of the file. "

    # Removing header line in order to read from only stock takes.
    lines_inventory_f.pop(0)

    for line_counter, line in enumerate(lines_inventory_f, start=2):
        # If an error handled for exists, line counter gives the line number in inventory.txt which contains the error.

        # Forms a list for a stock take. List contains items 'country', 'name', 'code', 'product', 'cost', 'quantity'.
        line_details = line.strip("\n").split(",")

        if line_details[0] == "" or line_details[2] == "" or line_details[3] == "":
            # Checking entries for country, name code and product are non-empty.
            return f"Line {line_counter} in file inventory.txt is missing information." \
                   f" Check the details for 'country name,code,product' in the line."

        try:
            # Checking each stock take (which is each line) 'cost' and 'quantity' data are integers.
            line_details[3] = int(line_details[3])
            line_details[4] = int(line_details[4])
        except ValueError as e:
            print(f"Error: {e}.")
            return f"Line {line_counter} in file inventory.txt has incorrect cost or quantity details. " \
                   f"Try again after checking each lines details."

        # Creating shoe objects and appending object to list.
        shoe_object = Shoe(line_details[0], line_details[1], line_details[2], line_details[3], line_details[4])
        shoe_list.append(shoe_object)

    return shoe_list


def capture_shoes():
    """
    Function captures data about a shoe from the user.
    It uses this data to create a shoe object and append this object inside shoe_list.
    """
    # Obtaining user inputs
    capture_country = input("What country is the product (shoe) from? ")
    capture_code = input("What is the code of the shoe? ")
    capture_product = input("What is the product called? ")

    while True:
        capture_cost = input("What is the cost of the shoe? "
                             "Format without decimal point e.g. if the shoe costs £20 input 2000: ")
        try:
            capture_cost = int(capture_cost)
            break
        except ValueError:
            print("The cost of the shoe must be an integer. Please try again.")

    while True:
        capture_quantity = input("What is the quantity held of the product? ")
        try:
            capture_quantity = int(capture_quantity)
            break
        except ValueError:
            print("The quantity of the shoe must be an integer. Please try again.")

    # Creating shoe object and appending it to list.
    shoe_object = Shoe(capture_country, capture_code, capture_product, capture_cost, capture_quantity)
    shoe_list.append(shoe_object)

    return "The shoe has been captured. " \
           "It is available for only for this running program and will not be saved to inventory.txt."
    # Potential Edit: add option to add captured shoe to inventory.txt.


def view_all():
    """
    Function iterates over shoe_list and prints its items into terminal using __str__.
    """
    print(" ")
    for shoe in shoe_list:
        print(shoe)
    # Optional: you can organise your data in a table format by using Python’s tabulate module.


def lowest_stock():
    """
    The first for loop simultaneous creates two lists. One list is the quantities of each shoe.
    The other is a 2D list where each item is [shoe object, shoe_quantity].
    The second loop takes the minimum quantity and identifies which shoe object it belong too.
    This loop allows for if there are multiple shoes with the lowest quantity.
    The shoe objects with the lowest quantities are printed to the terminal.
    :return: a list containing shoe objects which have the lowest quantity stocked.
    """
    stock_list = []
    quantities = []
    lowest_shoes_objects = []

    for shoe in shoe_list:
        # Need to read_shoe_data() first to create shoe_list
        quantities.append(shoe.get_quantity())
        stock_list.append([shoe, shoe.get_quantity()])
    # QUESTION: is there a way to get the shoe object from the attribute quantity?
    # i.e. for shoe in shoe_list:
    #           shoe_list = shoe.get_quantity
    #      min(shoe_list) <---- a way to get which shoe object this integer value came from?

    print("The shoes(s) below have the lowest quantity of all the stock takes: \n")

    for item in stock_list:
        if item[1] == min(quantities):
            lowest_shoes_objects.append(item[0])
            print(item[0])

    return lowest_shoes_objects


def re_stock():
    """
    Function asks user if they want to add stock to the shoes of the lowest quantities.
    If yes, it updates the quantity on inventory.txt and the objects attribute quantity,
    :return: completion message to user.
    """
    # This means all the info from lowest_stock() is printed first.
    low_objs_list = lowest_stock()

    restock = input("Would you like to restock the shoes? (y/n): ")

    if restock == "y":
        num_restock = int(input("How many pairs of shoes would you like to restock with? "))

        # Can take any object from lowest_stock list as they all have the same (lowest) stock.
        current_stock = low_objs_list[0].quantity
        new_stock = current_stock + num_restock

        for shoe_o in low_objs_list:
            # Loop for each shoe object which needs to be restocked.
            with open("inventory.txt", "r", encoding="utf-8-sig") as f:
                # Reads the inventory file each time so each stock update is saved.
                lines = f.readlines()

            file = open("inventory.txt", "w", encoding="utf-8-sig")
            for line in lines:
                # Re-writes the line for one shoe object with updated quantity (stock). All other line are copied.
                if line == f"{shoe_o.country},{shoe_o.code},{shoe_o.product},{shoe_o.cost},{shoe_o.quantity}\n":
                    file.write(f"{shoe_o.country},{shoe_o.code},{shoe_o.product},{shoe_o.cost},{new_stock}\n")

                else:
                    file.write(line)

            file.close()
            shoe_o.quantity = new_stock

    return "The shoe(s) quantity/ quantities has been updated."
    # Future edit: multiple shoes with same lowest quantity they can be restocked different amounts.
    # At the moment all lowest quantities shoes are restocked by the same amount.


def search_shoe():
    """
    Function searches for shoe from shoe_list using the shoe code,
    :return: if the shoe code is valid, the object is returned, else an error message is returned.
    """
    search_code = input("What is the shoe code you wish to search for? ")

    for shoe in shoe_list:
        if shoe.code == search_code:
            return f"The shoe: \n{shoe}"

    return "You have entered an invalid shoe code. "


def value_per_item():
    """
    Function calculates the total value for each shoe and prints the information in the console for all shoes.
    """
    for shoe in shoe_list:
        value = (shoe.get_cost() / 100) * shoe.get_quantity()
        # Divide by 100 to account for how money is formatted in inventory.txt
        print(f"£{value:.2f} is the value for the shoe given in the stock take: \n{shoe}\n")


def highest_qty():
    """
    Function determines which shoe stock-take has the highest quantity.
    :return: the shoe object with the highest quantity and states that it is for sale.
    """
    quantity = 0
    shoe_largest_quantity = None

    for shoe in shoe_list:
        if shoe.get_quantity() > quantity:
            quantity = shoe.get_quantity()
            shoe_largest_quantity = shoe

    return f"FOR SALE! \n{shoe_largest_quantity}"


# ==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''

read_shoes_data()

while True:
    menu_choice = input("""
    Welcome to the Nike Warehouse menu. Select the option you would like from below:
    1. View all shoes
    2. Capture shoes (this does not add the captured shoes to inventory.txt)
    3. Determine the product with the lowest quantity and restock it
    4. Search products by code
    5. Calculate the total value of each stock item  
    6. Determine the product with the highest quantity
    7. Exit
    """)

    if int(menu_choice.strip(".")) == 1:
        view_all()

    elif int(menu_choice.strip(".")) == 2:
        print(capture_shoes())

    elif int(menu_choice.strip(".")) == 3:
        print(re_stock())

    elif int(menu_choice.strip(".")) == 4:
        print(search_shoe())

    elif int(menu_choice.strip(".")) == 5:
        value_per_item()

    elif int(menu_choice.strip(".")) == 6:
        print(highest_qty())

    elif int(menu_choice.strip(".")) == 7:
        break

    else:
        print("Please select a valid number from the menu option.")
