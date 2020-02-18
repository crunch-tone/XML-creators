from lxml import etree
import datetime
import time
import csv

panel_barcodes_list = []
first_panel_barcode = ''
last_panel_barcode = ''
multi = ''
batch_name = ''

with open('barcodes.csv', newline='') as csvfile:
     barcodes_list_csv = csv.reader(csvfile, delimiter=';', quotechar='|')
     for row in barcodes_list_csv:
        panel_barcodes_list.append(row[0].strip())

#print(panel_barcodes_list)

#first_panel_barcode = input("Enter the first in range panel barcode:")
#last_panel_barcode = input("Enter the last in range panel barcode:")
multi = int(input("Enter the quantity of boards on one panel:"))
batch_name = input("Enter the batch name:")

#if len(first_panel_barcode) != len(last_panel_barcode):
#    first_panel_barcode = input("Error! Enter the first in range panel barcode:")
#    last_panel_barcode = input("Error! Enter the last in range panel barcode:")
#elif first_panel_barcode == '':
#    first_panel_barcode = input("Error! Enter the first in range panel barcode:")
#elif last_panel_barcode == '':
#    last_panel_barcode = input("Error! Enter the last in range panel barcode:")
if batch_name == '':
    batch_name = input("Error! Enter the batch name:")
else:
    try:
        int(multi)
        pass
    except:
        multi = int(input("Error! Enter the quantity of boards on one panel:"))


#    print("Input correct data")
#    get_input()
#else:
#    try:
#        int(multi)
#        pass
#    except:
#        get_input()
#init()

#current timestamp



def init():

    #creating XML structure function
    def create_xml(batch_name, panel_barcode, quantity):
        currentDT = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone().replace(microsecond=0).isoformat()
        barcode_list = etree.Element("BarcodeList", operator="nutek")
        job = etree.SubElement(barcode_list, "Job", assembly="", assemblyRev="", batch="", lot="", name=batch_name)
        barcode = etree.SubElement(job, "Barcode", id=panel_barcode, scan="Pass", scanTime=currentDT)
        for i in range(quantity):
            single_barcode = panel_barcode[:-2]+str(i+1).zfill(2)
            image_barcode = etree.SubElement(barcode, "ImageBarcode", id=single_barcode, scan="Pass", scanTime="")

        return barcode_list

    def create_range(first, last):
        reduced_first = ""
        reduced_last = ""
        const_part = ""
        result = []

        for i in first:
            try:
                int(i)
                reduced_first += i
            except:
                reduced_first = ""
                pass

        const_part = first.replace(reduced_first, "")
        reduced_first = reduced_first[:-2]

        for i in last:
            try:
                int(i)
                reduced_last += i
            except:
                reduced_last = ""
                pass

        const_part_2 = last.replace(reduced_last, "")
        reduced_last = reduced_last[:-2]

        if const_part != const_part_2:
            print("Please check the range and start again!")
            exit()

        if int(reduced_first) < int(reduced_last):
            i = int(reduced_first)
            while i <= int(reduced_last):
                result.append(const_part+str(i)+"00")
                i += 1
        elif int(reduced_first) > int(reduced_last):
            i = int(reduced_last)
            while i <= int(reduced_first):
                result.append(const_part+str(i)+"00")
                i += 1
        else:
            print("Please, enter actual range!")
            exit()

        return result

#    panel_barcodes_list = create_range(first_panel_barcode, last_panel_barcode)
    count = 0

    for i in panel_barcodes_list:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        try:
            with open('./'+timestamp+".xml", 'wb') as f:
                f.write(etree.tostring(create_xml(batch_name, i, multi), pretty_print=True, xml_declaration=True, encoding='utf-8'))
            time.sleep(1)
            count += 1
        except:
            print("Failed to write correct file")
            count = 0
    
    print(str(count)+" files were saved")
    #print(panel_barcodes_list)

init()