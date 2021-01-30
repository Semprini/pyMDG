from arango_orm import Collection, fields


class Country(Collection):
    __collection__ = 'country'
    
    _key = fields.CharField(required=True)
    
    @property
    def countryName(self):
        return self._key
    
    @countryName.setter
    def countryName(self, value):
        self._key = value
        
    
    def __str__(self):
        return "<Country({})>".format(self._key)    
    

class Department(Collection):
    __collection__ = 'department'
    
    departmentName = fields.CharField()
    _key = fields.IntegerField(required=True)
    
    @property
    def id(self):
        return self._key
    
    @id.setter
    def id(self, value):
        self._key = value
        
    
    def __str__(self):
        return "<Department({})>".format(self._key)    
    

class Employee(Collection):
    __collection__ = 'employee'
    
    firstName = fields.CharField()
    _key = fields.IntegerField(required=True)
    
    @property
    def id(self):
        return self._key
    
    @id.setter
    def id(self, value):
        self._key = value
        
    lastName = fields.CharField()
    
    def __str__(self):
        return "<Employee({})>".format(self._key)    
    

class JobHistory(Collection):
    __collection__ = 'jobhistory'
    
    _key = fields.IntegerField(required=True)
    
    @property
    def id(self):
        return self._key
    
    @id.setter
    def id(self, value):
        self._key = value
        
    language = fields.String()
    startDate = fields.DateField()
    
    def __str__(self):
        return "<JobHistory({})>".format(self._key)    
    

class Location(Collection):
    __collection__ = 'location'
    
    name = fields.CharField()
    
    def __str__(self):
        return "<Location({})>".format(self._key)    
    

class Region(Collection):
    __collection__ = 'region'
    
    _key = fields.CharField(required=True)
    
    @property
    def regionName(self):
        return self._key
    
    @regionName.setter
    def regionName(self, value):
        self._key = value
        
    
    def __str__(self):
        return "<Region({})>".format(self._key)    
    

class TestAbstract(Collection):
    __collection__ = 'testabstract'
    
    _key = fields.IntegerField(required=True)
    
    @property
    def test(self):
        return self._key
    
    @test.setter
    def test(self, value):
        self._key = value
        
    
    def __str__(self):
        return "<TestAbstract({})>".format(self._key)    
    
