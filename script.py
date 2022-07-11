#Abertura dos arquivos para analise e edição
myfile = open("data.txt", "r")
myexport = open("output.txt", "w")

#Inicio logica
#4000 é a base de identificação da OLT
ponRef = 4000
slotRef = 4000
slot = 0
pon = 0
slotTemp = 0
op = int(input("1-Export 1\n2-Export 2\n3-Debug\nOption: "))
vlan = int(input("VLAN: "))

if op != 2:
    olt = input("OLT: ")

#Inicio export
if op != 2:
    myexport.write(str(olt))
    myexport.write("\n")
    myexport.write("interface gpon 0/")
    myexport.write(str(slot))
    myexport.write("\n\n")

#Inicio analise
while myfile:
    line = myfile.readline()
    lineBase = int(line[43:48])
    dLine = line[43:51]

    #Verifica se chegou no final do arquivo
    if str(line) == "":
        myfile.close()
        myexport.close()
        break

    #Verifica SLOT
    while slotRef < lineBase:
        pon = pon + 1
        if pon > 15:
            slot = slot + 1
            pon = 0
        slotRef = slotRef + 512

    #Verifica se o Slot é diferente do antigo para inclusão do titulo
    if slotTemp != slot:
        if op != 2:
            myexport.write("\n\n")
            myexport.write("interface gpon 0/")
            myexport.write(str(slot))
            myexport.write("\n\n")

    slotTemp = slot
    pon = 0

    #Verifica PON
    while ponRef < lineBase:
        pon = pon + 1
        if pon > 15:
            pon = 0
        ponRef = ponRef + 256

    #Identificação da ONT
    id_ont = int(line[49:51])
    id_ont = str(id_ont)

    if op == 1:
        #Inicio do export
        myexport.write("ont ipconfig ")
        myexport.write(str(pon))
        myexport.write(" ")
        myexport.write(id_ont)
        myexport.write(" ip-index 1 dhcp vlan ")
        myexport.write(str(vlan))
        myexport.write(" priority 5\nont tr069-server-config ")
        myexport.write(str(pon))
        myexport.write(" ")
        myexport.write(id_ont)
        myexport.write(" profile-id 1\n")

    if op == 2:
        #Segundo exporte
        myexport.write("service-port vlan ")
        myexport.write(str(vlan))
        myexport.write(" gpon 0/")
        myexport.write(str(slot))
        myexport.write("/")
        myexport.write(str(pon))
        myexport.write(" ont ")
        myexport.write(id_ont)
        myexport.write(" gemport 2 multi-service user-vlan ")
        myexport.write(str(vlan))
        myexport.write(" tag-transform translate inbound traffic-table name GERENCIA-ONT outbound traffic-table name GERENCIA-ONT\n")
 
    if op == 3:
        #Trecho para debug
        myexport.write(str(dLine))
        myexport.write(" Slot ")
        myexport.write(str(slot))
        myexport.write(" PON ")
        myexport.write(str(pon))
        myexport.write(" ID ")
        myexport.write(id_ont)
        myexport.write(" VLAN ")
        myexport.write(str(vlan))
        myexport.write("\n")


    #Zera contadores
    ponRef = 4000
    slotRef = 4000
    pon = 0
    slot = 0