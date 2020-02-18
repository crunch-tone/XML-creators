from lxml import etree
import datetime
import time
import csv

panel_barcodes_list = []
first_panel_barcode = '' #first panel of the range
last_panel_barcode = '' #last panel of the range
#actyally it doesn't matter what is the first and what is the last, there is check of the range in the code below

multi = '' #how many boards are in the one panel
batch_name = ''

#recieve inputs
first_panel_barcode = input("Enter the first in range panel barcode:")
last_panel_barcode = input("Enter the last in range panel barcode:")
multi = int(input("Enter the quantity of boards on one panel:"))
batch_name = input("Enter the batch name:")

#checking if there is correct data was input
if len(first_panel_barcode) != len(last_panel_barcode):
    first_panel_barcode = input("Error! Enter the first in range panel barcode:")
    last_panel_barcode = input("Error! Enter the last in range panel barcode:")
elif first_panel_barcode == '':
    first_panel_barcode = input("Error! Enter the first in range panel barcode:")
elif last_panel_barcode == '':
    last_panel_barcode = input("Error! Enter the last in range panel barcode:")
elif batch_name == '':
    batch_name = input("Error! Enter the batch name:")
else:
    try:
        int(multi)
        pass
    except:
        multi = int(input("Error! Enter the quantity of boards on one panel:"))



def init():

    #the function that creates structure of the XML
    def create_xml(batch_name, panel_barcode, quantity):
        currentDT = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone().replace(microsecond=0).isoformat()
        barcode_list = etree.Element("BarcodeList", operator="nutek")
        job = etree.SubElement(barcode_list, "Job", assembly="", assemblyRev="", batch="", lot="", name=batch_name)
        barcode = etree.SubElement(job, "Barcode", id=panel_barcode, scan="Pass", scanTime=currentDT)
        for i in range(quantity):
            if int(panel_barcode[-1:]) == 1:
                j = i
            else:
                j = i + 5
            
            single_barcode = panel_barcode[:-3]+str(j+1).zfill(2)
            image_barcode = etree.SubElement(barcode, "ImageBarcode", id=single_barcode, scan="Pass", scanTime="")

        return barcode_list

    #the function that checks the range and creates panel barcodes list
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
                result.append(const_part+str(i)+"001")
                result.append(const_part+str(i)+"002")
                i += 1
        elif int(reduced_first) > int(reduced_last):
            i = int(reduced_last)
            while i <= int(reduced_first):
                result.append(const_part+str(i)+"001")
                result.append(const_part+str(i)+"002")
                i += 1
        elif reduced_first == reduced_last:
            result.append(const_part+str(int(reduced_first))+"00")
        else:
            print("Please, enter actual range!")
            exit()

        return result

    panel_barcodes_list = create_range(first_panel_barcode, last_panel_barcode)

    #simple counter for generated files
    count = 0

    for i in panel_barcodes_list:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        try:
            with open('./'+timestamp+".xml", 'wb') as f:
                f.write(etree.tostring(create_xml(batch_name, i, multi), pretty_print=True, xml_declaration=True, encoding='utf-8'))
            #adding little delay to ensure unique filenames
            time.sleep(1)
            count += 1
        except:
            print("Failed to write correct file")
            count = 0
    
    print(str(count)+" files were saved")

init()