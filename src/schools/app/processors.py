from schools import settings
def settings_processor(request):
    return {'MEDIA_URL':settings.MEDIA_URL,
            'ADMIN_MEDIA_PREFIX':settings.ADMIN_MEDIA_PREFIX,
            'ADMIN_URL':settings.ADMIN_URL,
            }