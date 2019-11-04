class Matrix(object):
    """
    Trida pro praci s maticemi
    """

    def __init__(self, width, height, default_value=0):
        """ 
        Konstruktor pro tridu Matrix 
  
        Parametery: 
           width (int): Sirka matice. 
           height (int): vyska matice.   
           default_value (int): Defaultni prvek kterym se vyplni matice
        """  
        self.width = width # pocet sloupcu
        self.height = height # pocet radku
        self.size = self.width * self.height # velikost matice pro ucel range limitu pri vkladani hodnot uzivatelem
        self.rows = [[default_value] * width for _ in range(height)] # naplni matici defaultnimi prvky 0


    def __repr__(self):
        return f'<Matrix values="{self.rows}">'


    def print_matrix(self):
        """
        Metoda ktera vytiskne matici po radcich,
        Slouzi uzivateli pro kontrolu zda jsou prvky na spravnych pozicich
        """
        print(f"\nMatrix values:")
        for row in self.rows:
            print(row)


    def fill(self, values_list):
        """
        Metoda pro vlozeni prvku do matice ktere nahradi default prvky 0 v self.rows;

        Parametery: 
           values_list (list): seznam s prvky matice, 
                mela by byt pouzita metoda create_value_list, 
                ktera vraci  seznam z dat zadanych na vstup uzivatelem.
        """
        index = 0
        for i in range(self.height):
            for j in range(self.width):
                self.rows[i][j] = values_list[index]
                index += 1
        return self.rows

    
    def create_value_list(self):
        """
        Metoda vola metodu usr_input_values, 
        ktera necha uzivatele vkladat nove prvky.
        Metoda nasladne vraci seznam techto prvku.
        Velikost seznamu je urcena velikosti matice.
        Vystupni seznam je urcen pro metodu fill

        """
        return [self.usr_input_values() for _ in range(0, self.size)]


    
    def __matmul__(self, multiplier):
        """
        Metoda pro nasobeni matic s pouzitim operatoru @ (od Pythonu 3.5)
        Vraci seznam s hodnotami odpovidajicimi vysledku nasobeni matic

        Parametry:
           multiplier (Matrix class object): nasobitel matice
        """
        if self.width != multiplier.height: # vyvola vyjimku pokud matice nejdou nasobit kvuli cols1 vs rows2 
            raise ValueError("There must be the same number of columns in mat1 and rows in mat2.")
        return [[sum(a*b for a,b in zip(srow,mcol)) for mcol in zip(*multiplier.rows)] for srow in self.rows]


    @staticmethod
    def usr_input_values():
        """
        funkce preda hodnotu zadanou uzivatelem, 
        osetri aby bylo na vstupu cislo
        tato funkce slouzi k vytvoreni seznamu prvku pro metodu fill
        """
        while True:
            try:
                value = int(input())
            except ValueError: # input se opakuje do doby nez uzivatel zada cislo
                print("Input must be a integer, repeat your input")
            else:
                return value


def usr_input_width_height():
    """
    funkce preda delku a vysku zadanou uzivatelem, 
    osetri aby bylo na vstupu cislo
    """
    while True:
        try:
            width = abs(int(input("width: ")))   # uzivatel zada delku 
            height = abs(int(input("height: "))) # a vysku prvni matice
        except ValueError: # input se opakuje do doby nez uzivatel zada cislo
            print("Input must be a integer, repeat your input")
        else:
            return width, height




if __name__ == '__main__':

    print("Matrix A")
    matrix_A = Matrix(*usr_input_width_height()) # vytvori instanci tridy Matrix, jako argumenty rozbali tuple vraceny funkci usr_input_width_height

    print("\nMatrix B")
    matrix_B = Matrix(*usr_input_width_height()) # vytvori instanci tridy Matrix, jako argumenty rozbali tuple vraceny funkci usr_input_width_height

    print("\nEnter numerical values for Matrix A separated by Enter") # uzivatel zada prvky matice, odesila Enterem
    matrix_A.fill(matrix_A.create_value_list()) # seznam s prvky predame jako argument metode fill
    matrix_A.print_matrix() # vytiskne prave vytvorenou matici, pro kontrolu

    print("\nEnter numerical values for Matrix B separated by Enter") # uzivatel zada prvky matice, odesila Enterem
    matrix_B.fill(matrix_B.create_value_list()) # seznam s prvky predame jako argument metode fill
    matrix_B.print_matrix() # vytiskne prave vytvorenou matici, pro kontrolu


    print("\nResult of multiplication:")
    mat3 = matrix_A @ matrix_B # vysledek nasobeni matic se ulozi do seznamu mat3
    for row in mat3:
        print(row) # vytiskne matici pro potvrzeni po radcich, aby to vypadalo jako matice
