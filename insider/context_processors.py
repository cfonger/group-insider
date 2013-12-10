from insider.webapp import models


def exported_settings(request):
    context = {
        'request': request,
        'user': request.user,
    }

    if request.user.is_authenticated():
        if not hasattr(request.user, 'linkedin_data'):
            userdataobjs = models.LinkedInUserData.objects.filter(
                user=request.user)
            if userdataobjs:
                request.user.linkedin_data = userdataobjs[0]
                context['linkedin_data'] = request.user.linkedin_data

    return context
