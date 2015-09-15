from django.db.models import signals
from django.contrib.auth.models import Group, Permission
import models 

college_group_permissions = {
  "Profesores": [
    "add_calificacion",
    "change_calificacion",
    "delete_calificacion",
    "add_asistencia",         
    "change_asistencia",
    "delete_asistencia",
    ],
}

def create_user_groups(app, created_models, verbosity, **kwargs):
  if verbosity>0:
    print "Initialising data post_syncdb"
  for group in college_group_permissions:
    role, created = Group.objects.get_or_create(name=group)
    if verbosity>1 and created:
      print 'Creating group', group
    for perm in college_group_permissions[group]: 
      role.permissions.add(Permission.objects.get(codename=perm))
      if verbosity>1:
        print 'Permitting', group, 'to', perm
    role.save()

signals.post_syncdb.connect(
  create_user_groups, 
  sender=models, # only run once the models are created
  dispatch_uid='college.models.create_user_groups' # This only needs to universally unique; you could also mash the keyboard
  )