import os
from tqdm.auto import tqdm
import csv

filename1 = "dataset_lkv_01022023.tsv" #Older Data Set
filename2 = "dataset_lkv_01032023.tsv" #Newer Data Set

cwd = os.getcwd()

file1 = cwd + "\\DATA_SETS\\CLEAN\\" + filename1
file2 = cwd + "\\DATA_SETS\\CLEAN\\" + filename2
fileO = cwd + "\\DATA_SETS\\CLEAN\\COMPARATIVE_DATA\\" +"ConcatTotalPatronSavings_%s.csv" %(filename1[:-4]+filename2[:-4],)

# Count the number of rows in file1
with open(file1, "r", encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter="\t")
    num_rows1 = sum(1 for row in reader) - 1

# Count the number of rows in file2
with open(file2, "r", encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter="\t")
    num_rows2 = sum(1 for row in reader) - 1

print("file1", num_rows1, "file2", num_rows2)

# Open the input and output CSV files
with open(file1, newline='', encoding='UTF-8') as file1, \
     open(file2, newline='', encoding='UTF-8') as file2, \
     open(fileO, 'w', newline='', encoding='UTF-8') as output_file:

    # Create CSV readers and writer objects
    reader1 = csv.reader(file1, delimiter="\t")
    reader2 = csv.reader(file2, delimiter="\t")
    writer = csv.writer(output_file, delimiter= "|")

    # Skip the header rows in both input files
    header1 = next(reader1)
    header2 = next(reader2)

    # Write the header row to the output file
    writer.writerow(["BARCODE","INIT CHKOUT","SECD CHKOUT","TOT CHKOUT","PRICE","SAVED"])

    # Iterate over the lines in the first input file
    for row1 in tqdm(reader1, desc="Looping through file #1", total=num_rows1, leave=True):
    #for row1 in reader1:

        # Iterate over the lines in the second input file
        file2.seek(0)
        next(reader2)  # Skip the header row

        counter = 0    # Start a counter at 0 to identify the row index of the csv
        for row2 in reader2:

            counter += 1    # Add 1 to the counter

            # Check if the first element in the current row of file1
            # matches the first element in the current row of file2
            if row1[0] == row2[0]:
                BARCODE = row1[0] #barcode
                INIT_CHKOUT = float(row1[1]) #Init_checkout
                SECD_CHKOUT = float(row2[1]) #Secd_checkout
                TOT_CHKOUT = SECD_CHKOUT - INIT_CHKOUT #total_chkout
                PRICE = float(row1[2].replace("$", "")) #price
                SAVED = TOT_CHKOUT * PRICE #saved
                # Perform operations on the matched rows
                
                new_row = BARCODE + " | " + str(INIT_CHKOUT) + " | " + str(SECD_CHKOUT) + " | " + str(TOT_CHKOUT) + " | " + str(PRICE) + " | " + str(SAVED)
                # Write the new row to the output file
                writer.writerow(new_row.split(" | "))

                break

            # If the first element in the current row of file1
            # does not match the first element in the current row of file2
            if row1[0] != row2[0]:
                # And if the current row of file2 is the last row of file2
                if counter == num_rows2:
                    BARCODE = row1[0]
                    INIT_CHKOUT = float(row1[1])
                    SECD_CHKOUT = float(0)
                    TOT_CHKOUT = float(0)
                    PRICE = float(row1[2].replace("$", ""))
                    SAVED = TOT_CHKOUT * PRICE
                    # Perform operations on the unmatched row
                    new_row = BARCODE + " | " + str(INIT_CHKOUT) + " | " + str(SECD_CHKOUT) + " | " + str(TOT_CHKOUT) + " | " + str(PRICE) + " | " + str(SAVED)
                    # Write the new row to the output file
                    writer.writerow(new_row.split(" | "))

    print("counter", counter)

    file2.seek(0)
    next(reader2)

    # Iterate over the lines in the second input file
    for row2 in tqdm(reader2, desc="Looping through file #2", total=num_rows2 + 1, leave=True):
    #for row2 in reader2:
        # Iterate over the lines in the first input file
        file1.seek(0)
        next(reader1)  # Skip the header row

        counter = -1    # Start a counter at 0 to identify the row index of the csv

        #for row1 in tqdm(reader1, total=num_rows1, leave=True):
        for row1 in reader1:

            counter += 1    # Add 1 to the counter

            # Check if the first element in the current row of file2
            # does not match the first element in the current row of file1
            # because all matched lines should have been captured in the 
            # first iteration over file1
            if row2[0] != row1[0]:
                # And if the current row of file1 is the last row of file1
                if counter == num_rows1:
                    BARCODE = row2[0]
                    INIT_CHKOUT = float(0)
                    SECD_CHKOUT = float(row2[1])
                    TOT_CHKOUT = SECD_CHKOUT
                    PRICE = float(row2[2].replace("$", ""))
                    SAVED = TOT_CHKOUT * PRICE
                    # Perform operations on the unmatched row
                    new_row = BARCODE + " | " + str(INIT_CHKOUT) + " | " + str(SECD_CHKOUT) + " | " + str(TOT_CHKOUT) + " | " + str(PRICE) + " | " + str(SAVED)

                    # Write the new row to the output file
                    writer.writerow(new_row.split(" | "))


    print("counter", counter)
