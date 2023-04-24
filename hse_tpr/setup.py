import repository.models as models
import json


with open('../setup/jsons/case_types.json', 'r') as case_types:
    case_types_data = json.load(case_types)
    for type in case_types_data['types']:
        models.CaseType.objects.create(title=type)

with open('../setup/jsons/ed_lvls.json', 'r') as ed_lvls:
    ed_lvls_data = json.load(ed_lvls)
    for lvl in ed_lvls_data:
        for sublvl in ed_lvls_data[lvl]:
            models.EducationalLevel.objects.create(title=sublvl)

with open('../setup/jsons/facs_and_deps.json', 'r') as facs_and_deps:
    facs_and_deps_data = json.load(facs_and_deps)
    for fac in facs_and_deps_data:
        instance = models.Faculty.objects.create(title=fac)
        for dep in facs_and_deps_data[fac]:
            models.Department.objects.create(title=dep, faculty=instance)


    