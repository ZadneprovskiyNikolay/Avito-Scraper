class Item:

    def __init__(self, title, price, href, date_str):
        self.title = title
        self.price = price
        self.href = href
        self.time = None

        # Set time
        date_words = date_str.split()
        if date_words[1][:3] == 'час':
            self.time = int(date_words[0])
        elif date_words[1][:3] == 'сек':
            self.time = 0                        
        elif date_words[1][:3] == 'мин':
            self.time = int(date_words[0]) / 60
        elif date_words[1][:3] == 'ден' or date_words[1][:2] == 'дн':
            self.time = int(date_words[0]) * 24
        elif date_words[1][:3] == 'нед':
            self.time = int(date_words[0]) * 24 * 7
        else:
            # logging.error(f"Can't parse time str: '{date_str}'")
            self.time = 13371337

    def __eq__(self, other): 
        if not isinstance(other, Item):
            return NotImplemented

        return self.__dict__ == other.__dict__
    
    def __hash__(self):
        return hash(self.href)
    
    def __repr__(self):
        return f'{self.title}: {self.price} ({self.time:.1f})'
