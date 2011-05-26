from itrack.equipments.models import CustomField, Equipment, CustomFieldData, AvailableFields, EquipmentType
from django.contrib import admin


class AvailableAdmin(admin.ModelAdmin):
    filter_horizontal = ["custom_fields"]
    
class EquipTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ["custom_field"]
    
    
admin.site.register(CustomField)
admin.site.register(CustomFieldData)
admin.site.register(Equipment)
admin.site.register(EquipmentType, EquipTypeAdmin)
admin.site.register(AvailableFields,AvailableAdmin)
