class Department:
    """ 
    Department class represents data about a department
    """

    def __init__(self, ID, name, specialty, icu = None, first = None, last = None):
        """ Create a new Department """
        self.ID = ID
        self.name = name
        self.specialty = specialty
        self.icu = icu #Yes/No/Inactive
        self.first = first #Date first appeared as ICU
        self.last = last #Date last appeared as ICU
    
    def __repr__(self):
        return "<Department ID:%s, Name:%s, Specialty:%s, ICU:%s, First Appeared as ICU:%s, Last Appeared as ICU:%s>" %(self.ID,
            self.name, self.specialty, self.icu, self.first, self.last)
       
