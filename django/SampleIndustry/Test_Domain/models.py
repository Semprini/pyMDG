from django.utils.translation import gettext_lazy as _
from django.db import models
from simple_history.models import HistoricalRecords

from sample_industry.validators import validate_even



class ENUM_Language(models.TextChoices):

    FRENCH = 'French', _('French')
    ENGLISH = 'English', _('English')
    SPANISH = 'Spanish', _('Spanish')







class TestAbstract( models.Model ):

    test = models.AutoField( primary_key=True,  )

    class Meta:
        abstract = True



class Country( models.Model ):

    country_name = models.CharField( primary_key=True, max_length=100 )



    regions = models.ForeignKey( 'Test_Domain.Region', related_name='country', on_delete=models.CASCADE, blank=True, null=True )
    


    






class Department( models.Model ):

    department_name = models.CharField( blank=True, null=True, max_length=100 )

    id = models.AutoField( primary_key=True,  )



    

    employees = models.ForeignKey( 'Test_Domain.Employee', related_name='department', on_delete=models.CASCADE, blank=True, null=True )
    




    history = HistoricalRecords()


class Employee( models.Model ):

    first_name = models.CharField( blank=True, null=True, max_length=100 )

    id = models.AutoField( primary_key=True,  )

    last_name = models.CharField( blank=True, null=True, max_length=100 )




    


    jobhistorys = models.ForeignKey( 'Test_Domain.JobHistory', on_delete=models.CASCADE, related_name='employee', blank=True, null=True )






class JobHistory( models.Model ):

    id = models.AutoField( primary_key=True,  )

    language = models.CharField( max_length=100, choices=ENUM_Language.choices, blank=True, null=True )

    start_date = models.DateField( blank=True, null=True,  )



    






class Location( TestAbstract ):

    name = models.CharField( blank=True, null=True, max_length=100 )



    country = models.OneToOneField( 'Test_Domain.Country', on_delete=models.CASCADE, blank=True, null=True )
    


    departments = models.ForeignKey( 'Test_Domain.Department', on_delete=models.CASCADE, related_name='location', blank=True, null=True )






class Region( models.Model ):

    region_name = models.CharField( primary_key=True, max_length=100 )




    







