import os
import json
import toml
from colorama import init, Fore, Back, Style
from zipfile import ZipFile
init(convert=True)
dir = str(input("Mods Directory: "))
if not os.path.isdir(dir):
    exit('Directory not found!')
    
mods = []

obj = os.scandir(dir)
for entry in obj : 
    if entry.is_file():
        if(entry.name[-3:].lower() == ("jar" or "zip")):
            with ZipFile(dir+"/"+entry.name, 'r') as zip:
                modname = entry.name[0:-4]
                modid = ''
                required = []
                dependencies = []
                description = ''
                url = ''
                try:
                    m = zip.read('mcmod.info') # 1.7+
                except:
                    print(Fore.YELLOW + "Scan:", entry.name, "- mcmod not found!" + Style.RESET_ALL)
                    try:
                        m = zip.read('META-INF/mods.toml') # 1.16+
                    except:
                        print(Fore.YELLOW + "Scan:", entry.name, "- mods.toml not found!" + Style.RESET_ALL)
                    else:
                        try:
                            m_toml = toml.loads(m.decode("utf-8"))
                        except Exception as e:
                            print(Fore.YELLOW + f'[{entry.name}] TOML not readable! ({e})' + Style.RESET_ALL)
                        else:
                            #if 'dependencies' in m_toml:
                            #    required = m_toml['dependencies']
                            if 'displayName' in m_toml['mods'][0]:
                                modname = m_toml['mods'][0]['displayName']
                            if 'dependencies' in m_toml:
                                    dependencies = list(m_toml['dependencies'].keys())
                            if 'modId' in m_toml['mods'][0]:
                                modid = m_toml['mods'][0]['modId']
                            if 'description' in m_toml['mods'][0]:
                                    description = m_toml['mods'][0]['description']
                            if 'displayURL' in m_toml['mods'][0]:
                                    url = m_toml['mods'][0]['displayURL']

                else:
                    print(Fore.GREEN + "Scan:", entry.name, "- mcmod found!" + Style.RESET_ALL)
                    try:
                        mcmeta = json.loads(m)
                    except:
                        print("Json not redable!")
                    else:
                        if len(mcmeta) == 1:
                            if 'requiredMods' in mcmeta[0]:
                                required = mcmeta[0]['requiredMods']
                            if 'name' in mcmeta[0]:
                                modname = mcmeta[0]['name']
                            if 'dependencies' in mcmeta[0]:
                                dependencies = mcmeta[0]['dependencies']
                            if 'modid' in mcmeta[0]:
                                modid = mcmeta[0]['modid']
                            if 'description' in mcmeta[0]:
                                description = mcmeta[0]['description']
                            if 'url' in mcmeta[0]:
                                url = mcmeta[0]['url']
                            # v2
                        if len(mcmeta) > 1:
                            if 'modList' in mcmeta:
                                if 'requiredMods' in mcmeta['modList'][0]:
                                    required = mcmeta['modList'][0]['requiredMods']
                                if 'name' in mcmeta['modList'][0]:
                                    modname = mcmeta['modList'][0]['name']
                                if 'dependencies' in mcmeta['modList'][0]:
                                    dependencies = mcmeta['modList'][0]['dependencies']
                                if 'modid' in mcmeta['modList'][0]:
                                    modid = mcmeta['modList'][0]['modid']    
                                if 'description' in mcmeta['modList'][0]:
                                    description = mcmeta['modList'][0]['description']
                                if 'url' in mcmeta['modList'][0]:
                                    url = mcmeta['modList'][0]['url']
                finally:
                    mod = []
                    print("Modname: ", modname)
                    
                    if(len(required) > 0):
                        print(Fore.CYAN + "RequiredMods: ", required, Style.RESET_ALL)
                        
                    if(len(dependencies) > 0):
                        print(Fore.MAGENTA + "Dependencies: ", dependencies, Style.RESET_ALL)
                        
                    if(modid != ''):
                        print(Fore.CYAN + "modid: ", modid, Style.RESET_ALL)
                        
                    if(description != ''):
                        print(Fore.MAGENTA + "Description: ", description, Style.RESET_ALL)
                        
                    if(url != ''):
                        print(Fore.CYAN + "URL: ", url, Style.RESET_ALL)
                    
                    mod.append(modname) #0
                    mod.append(modid) #1
                    mod.append(required) #2                    
                    mod.append(dependencies) #3
                    mod.append(description) #4
                    mod.append(url) #5
                    mods.append(mod) #6
                    zip.close()
#print(mods) #debug

def createLi(mod, level):
    if mod[5] == '':
        mod[5] = "#"
    html = "<li>"
    html += "<a href='{url}' title='{desc}'>{modname}</a>".format(url=mod[5], desc=mod[4], modname=mod[0])
    html += "</li>\r\n"
    for i in range(level):
        html = "  " + html
    return html

while True:
    print("\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n")
    print(Fore.CYAN, "-------------------")
    print("1 - Generate HTML")
    print("2 - Print JSON")
    print("3 - Exit")
    print(Fore.CYAN, "-------------------", Style.RESET_ALL)
    mode = input('Select: ');
    if mode == '2':
        print(Fore.GREEN, json.dumps(mods), Style.RESET_ALL)
    if mode == '3':
        exit('Bye!')
    if mode == '1':
        mods_req = []
        used_for_req = []
        for i in range(len(mods)):
            mods_req.append([mods[i], []])
            used_for_req.append(0)
            
        html = '<ul>\r\n'
        for i in range(len(mods)):
            if mods[i][2] != []:
                for req in mods[i][2]:
                    for j in range(len(mods)):
                        if req == mods[j][1]:
                            mods_req[j][1].append(mods[i])
                            used_for_req[i] = 1
                            break;
        #print(mods_req)    
        for i in range(len(mods)):
            if(used_for_req != 1):
                html += createLi(mods_req[i][0], 1)
            if len(mods_req[i][1]) > 0:
                html += "  <ul>\r\n"
                for mod_r in mods_req[i][1]:
                    html += createLi(mod_r, 2)
                html += "  </ul>\r\n"
        html += '\r\n</ul>'
        print(Fore.GREEN, html, Style.RESET_ALL)
input()
