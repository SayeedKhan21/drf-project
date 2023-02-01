from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
        User ,
        Recipe ,
        Tag ,
        Ingredient
    )
from django.contrib import admin
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin) : 
    ordering = ['id']
    list_display = ['id' , 'email' , 'name']
    fieldsets = (
        (None , {'fields' : ('email' ,'password')}),
        ('Permissions' ,
            {'fields' : 
                (
                    'is_active' ,
                    'is_staff' ,
                    'is_superuser' ,
                )
            }
        ),
        ('Important Dates' ,
            {'fields' :
                (
                    'last_login' ,
                )
            }
        )
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None ,
            {'fields' :
                (
                    'email' ,
                    'password1' ,
                    'password2' ,
                    'name' ,
                    'is_active' ,
                    'is_staff' ,
                    'is_superuser'
                )
            }
        ),
    )

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)