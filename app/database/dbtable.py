from database.dbread import read_table

class DBTable:
    def __init__(self):
        self.bridge_pop = None
        self.bridge_pop_old = None
        self.county = None
        self.county_combined = None
        self.data = None
        self.dataset = None
        self.type_pop = None
        self.type_rate = None
        self.type_unit = None
        self.variable = None
    
    def print_note_success(self, name):
        print(f"NOTE: Successfully fetched '{name}' from database.")

    def read_bridge_pop(self):
        try:
            name = 'BridgePop'
            self.bridge_pop = read_table(name)
            self.print_note_success(name)
        except:
            raise

    def read_bridge_pop_old(self):
        try:
            name = 'BridgePopOld'
            self.bridge_pop_old = read_table(name)
            self.print_note_success(name)
        except:
            raise

    def read_county(self):
        try:
            name = 'County'
            self.county = read_table(name)
            self.print_note_success(name)
        except:
            raise

    def read_county_combined(self):
        try:
            name = 'CountyCombined'
            self.county_combined = read_table(name)
            self.print_note_success(name)
        except:
            raise

    def read_data(self):
        try:
            name = 'Data'
            self.data = read_table(name)
            self.print_note_success(name)
        except:
            raise
    
    def read_dataset(self):
        try:
            name = 'Dataset'
            self.dataset = read_table(name)
            self.print_note_success(name)
        except:
            raise

    def read_types(self):
        try:
            self.type_pop = read_table('TypePop')
            print("NOTE: Successfully fetched 'TypePop' from database.")
            self.type_rate = read_table('TypeRate')
            print("NOTE: Successfully fetched 'TypeRate' from database.")
            self.type_unit = read_table('TypeUnit')
            print("NOTE: Successfully fetched 'TypeUnit' from database.")
        except:
            raise

    def read_variable(self):
        try:
            name = 'Variable'
            self.variable = read_table(name)
            self.print_note_success(name)
        except:
            raise

    def read_all(self):
        self.read_bridge_pop()
        self.read_bridge_pop_old()
        self.read_county()
        self.read_county_combined()
        self.read_data()
        self.read_dataset()
        self.read_types()
        self.read_variable()

    def __str__(self):
        text = "***Report start***\n"
        text += "- BridgePop "
        text += "(not loaded)" if self.bridge_pop is None else "(loaded)\n"
        text += "- BridgePopOld "
        text += "(not loaded)" if self.bridge_pop_old is None else "(loaded)\n"
        text += "- County "
        text += "(not loaded)" if self.county is None else "(loaded)\n"
        text += "- CountyCombined "
        text += "(not loaded)" if self.county_combined is None else "(loaded)\n"
        text += "- Data "
        text += "(not loaded)" if self.data is None else "(loaded)\n"
        text += "- Dataset "
        text += "(not loaded)" if self.dataset is None else "(loaded)\n"
        text += "- TypePop "
        text += "(not loaded)" if self.type_pop is None else "(loaded)\n"
        text += "- TypeRate "
        text += "(not loaded)" if self.type_rate is None else "(loaded)\n"
        text += "- TypeUnit "
        text += "(not loaded)" if self.type_unit is None else "(loaded)\n"
        text += "- Variable "
        text += "(not loaded)" if self.variable is None else "(loaded)\n"
        text += "***Report end***\n"

        return text

    def __repr__(self):
        return self.__str__