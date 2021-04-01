def collect_data(text,string,column):
    '''Get the list of strings for the zth columns.
    text - the text we want to process
    string - the string we want to treat as cut-off rule
    column - the column we want to process
    Return the list of strings.'''
    file = open(text,'r')
    content = file.read()
    list_of_lines = content.splitlines()
    row = []
    for strings in list_of_lines:
        list_of_strings = strings.split(string)
        row.append(list_of_strings[column])
    return row
class Data:
    def __init__(self):
        '''Initialize the object 'Data'.
        Return nothing'''
        self.products = 'products.txt'
        self.suppliers = 'suppliers.txt'
        self.availability = 'availability.txt'
        self.onshelves = 'onshelves.txt'
    def find_goods(self):
        '''Find the number of good we should add in
        Return the number of goods we need to store'''
        numbers = collect_data(self.onshelves,'#',1)
        inventories = []
        for number in numbers:
            if int(number) < 20:
                add = 50 - int(number)
                inventories.append(add)               
        return inventories
    def find_code(self):
        '''Find the code of the goods
        Return a list of the codes of products'''
        numbers = collect_data(self.onshelves,'#',1)
        products = collect_data(self.onshelves,'#',0)
        product = []
        num = 0
        for number in numbers:
            if int(number) < 20:
                product.append(products[num])
                num += 1
            else:
                num += 1
        return product
    def find_name(self):
        '''Find the name of the products
        Return the name of the products'''
        products = self.find_code()
        names = collect_data(self.products,';',1)
        codes = collect_data(self.products,';',0)
        name = []
        for product in products:
            for code in codes:
                if product == code:
                    name.append(names[codes.index(code)])
        return name  
    def find_price_number(self):
        '''Find which goods we want to choose in the self.availability
        Return a list of which goods we want to choose in the self.availability'''
        products = self.find_code()
        codes = collect_data(self.availability,',',0)
        prices = collect_data(self.availability,',',2)
        price_number = []
        for product in products:
            number = 0
            compare = []
            for code in codes:
                if product == code:
                    compare.append([prices[number],number])
                    number += 1
                else:
                    number += 1
            compare.sort()
            price_number.append(compare[0][1])
        return price_number
    def find_price(self):
        '''Find the price of the goods
        Return the price of each kind of goods'''
        price = []
        price_numbers = self.find_price_number()
        prices = collect_data(self.availability,',',2)
        for price_number in price_numbers:
            price.append(prices[price_number])
        return price  
    def find_cost(self):
        '''Find how much we will cost when we store a good
        Return the cost of each kinds of goods'''
        number = 0
        inventory = self.find_goods()
        prices = self.find_price()
        cost_list = []
        for price in prices:
                cost = float(price)*int(inventory[number])
                number += 1
                cost_list.append('%.2f'%(cost))
        return cost_list    
    def find_phonenumber(self):
        '''Find the phonenumber of the companys
        Return the phonenumber of the companys'''
        phonenumber = []
        price_numbers = self.find_price_number()
        phonenumbers = collect_data(self.availability,',',1)
        for price_number in price_numbers:
            phonenumber.append(phonenumbers[price_number])
        return phonenumber    
    def total_cost(self):
        '''Find the total cost of the goods.
        Return the total cost of all of the goods.'''
        number = 0
        cost_list = self.find_cost()
        for cost in cost_list:
            number = number + float(cost)
        number = '%.2f'%(number)
        return number    
    def combine(self):
        '''Combine the information of goods
        Return the list of rows we want to print on the file'''
        product_code = self.find_code()
        product_name = self.find_name()
        quantity = self.find_goods()
        supplier = self.find_phonenumber()
        suppliers = [int(number) for number in supplier]
        cost = self.find_cost()
        number = len(product_code)
        num = range(number)
        list_of_rows = []
        for i in num:
            rows = []
            rows.append(product_code[i])
            rows.append(product_name[i])
            rows.append(quantity[i])
            rows.append(suppliers[i])
            rows.append(cost[i])
            list_of_rows.append(rows)
            list_of_rows.sort(key = lambda x:x[3])
        return list_of_rows
    def biggest_cost(self):
        '''Find the biggest cost among the goods we store, and its company name and phonenumber.
        Return a list includes the biggest cost among the goods we store, and its company name and phonenumber'''
        cost_list = self.find_cost()
        price_number = self.find_price_number()
        phone = self.find_phonenumber()
        name = self.find_name()
        new_list = []
        biggest = []
        for n in cost_list:
            new_list.append(float(n))
        cost_list = new_list
        dic1 = dict(map(lambda x,y:[x,y], phone,cost_list))
        dic2 = dict(map(lambda x,y:[x,y], phone,name))
        biggest_cost = max(cost_list)
        for phone,cost in dic1.items():
            if cost == biggest_cost:
                company = []
                company.append(biggest_cost)
                company.append(self.change_format(phone))
                company.append(dic2[phone])
                biggest.append(company)
        return biggest
    def change_format(self, alist):
        '''Change the format of the phonenumber
        Return the list which change the phone number into correct format'''
        alist = '(' + alist[:3] + ') ' + alist[4:7] + ' ' + alist[-4:] 
        return alist    
class Display:
    def __init__(self):
        '''Initialize the Class Display
        Return nothing'''
        self.data = Data()
        self.list_of_rows = self.data.combine()

    def show(self):
        '''Print the table and the highest cost.
        Return nothing'''
        a = '+--------------+------------------+--------+----------------+----------+\n| Product code | Product Name     |Quantity| Supplier       | Cost     |\n+--------------+------------------+--------+----------------+----------+\n'
        for rows in self.list_of_rows:
            output = '|'+rows[0].center(14)+'|'
            if rows[2]>40:
                output = output + '*'
            else:
                output = output + ' '
            name = ''
            num = 0
            for string in rows[1]:
                if num <16:
                    name = name + string
                    num += 1
                rows[1] = name
            rows[3] = self.data.change_format(str(rows[3]))
            a = a + output + '%-17s'%(rows[1]) + '|' + '%7d'%(rows[2]) + ' |' + '{:^16s}'.format(rows[3]) + '| $' + '%7s'%(rows[4]) + ' |\n'
        total_amount = self.data.total_cost()
        a = a + '+--------------+------------------+--------+----------------+----------+\n| Total Cost   |                $' + '%10s'%(total_amount) + '|\n+--------------+---------------------------+\n'
        biggest_cost = self.data.biggest_cost()
        for information in biggest_cost:
            a = a +'Highest cost: ' + information[2] + ' ' + information[1] + ' [$' + str(information[0]) + ']\n'
        print(a)
        file = open('orders.txt','w+')
        file.write(a)
def main():
    '''Run the code
    Return nothing'''
    display = Display()
    display.show()

main()
