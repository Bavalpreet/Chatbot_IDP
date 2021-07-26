import os
import glob
import hiyapyco

path = '/home/bavalpreet/IDP/domain-grp'
yaml_list = []

for filename in glob.glob(os.path.join(path, '*.yml')):
    with open(filename) as fp:
        yaml_file = fp.read()
        yaml_list.append(yaml_file)

merged_yaml = hiyapyco.load(yaml_list, method=hiyapyco.METHOD_MERGE)
print(hiyapyco.dump(merged_yaml))

domain_yml_file = open("domain.yml","w+")
domain_yml_file.writelines(hiyapyco.dump(merged_yaml))
