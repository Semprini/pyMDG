from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings

class Test_DomainConfig(AppConfig):
    name = 'Test_Domain'

    def ready(self):
        import drf_nest.signals
        from Test_Domain.models import Country, Department, Employee, JobHistory, Location, Region, TestAbstract
        from Test_Domain.serializers import CountrySerializer, DepartmentSerializer, EmployeeSerializer, JobHistorySerializer, LocationSerializer, RegionSerializer, TestAbstractSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name

        
        exchange_header_list = ()
        post_save.connect(  drf_nest.signals.notify_extra_args( serializer=DepartmentSerializer, 
                                                                exchange_prefix=exchange_prefix + ".Department", 
                                                                exchange_header_list=exchange_header_list)(drf_nest.signals.notify_save_instance), 
                                                                sender=Department, weak=False)