import os
from tqdm.auto import tqdm
import csv

# Set the variables containing the filenames of the preprocessed data
# that needs to be concatenated
filename1 = "" #Older Data Set
filename2 = "" #Newer Data Set

cwd = os.getcwd()

# Set the path to the file directorys
file1 = cwd + "\\DATA_SETS\\CLEAN\\" + filename1
file2 = cwd + "\\DATA_SETS\\CLEAN\\" + filename2
fileO = cwd + "\\DATA_SETS\\CLEAN\\TRAINING_DATA\\" +"ConcatTrainingValues_%s.csv" %(filename1[:-4]+filename2[:-4],)

# Count the number of rows in file1
with open(file1, "r", encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter="\t")
    num_rows1 = sum(1 for row in reader)

# Count the number of rows in file2
with open(file2, "r", encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter="\t")
    num_rows2 = sum(1 for row in reader)

# Print total number of rows for each file
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
    writer.writerow(["GENRE","PUBLISHER","NUM LINKING FIELDS", "PRICE", "VALUE RATING"])

     # Iterate over the lines in the first input file
    #for row1 in tqdm(reader1, desc="Looping through file #1", total=num_rows1, leave=True):
    for row1 in tqdm(reader1, desc="Looping through file #1", total=num_rows1, leave=True):
        # Set the file object index to the beginning of the file
        # Then skip the header row
        file2.seek(0)
        next(reader2)

        # Start a counter at 0 to identify the row index of the csv
        counter = 0

        # Then iterate over the second file
        for row2 in reader2:

            # Add 1 to the counter
            counter += 1

            # Check if the first element in the current row of file1
            # matches the first element in the current row of file2
            if row1[0] == row2[0]:

                # Set the publisher variable
                try:
                    PUBLISHER = row1[5]
                except(IndexError):
                    PUBLISHER = "NULL"

                # Set the price variable
                PRICE = row1[2]

                # Set the total checkouts variable
                TOT_CHKOUT = int(row2[1]) - int(row1[1])

                # Then set the value rating variable based on the total checkouts variable
                if TOT_CHKOUT == 0:
                    VALUE_RATING = 1

                elif TOT_CHKOUT == 1:
                    VALUE_RATING = 2

                elif TOT_CHKOUT > 1:
                    VALUE_RATING = 3

                # Set the linking fields list
                try:
                    Linking_Fields = row1[6].split(".")
                except(IndexError):
                    Linking_Fields = [""]

                # Check is the list is empty
                if Linking_Fields[0] == "":
                    # If it is, then set the  genre and number of linking fields variables
                    GENRE = "NULL"
                    NUM_LINKING_FIELDS = 0
                
                # If it is not, then remove empty list items and set the genre and number of linking fields variables
                elif Linking_Fields[0] != "":
                    clean_linking_fields = []
                    for i in Linking_Fields:
                        if i == "":
                            continue
                        else:
                            clean_linking_fields.append(i)
                    
                    GENRE = clean_linking_fields[0]
                    NUM_LINKING_FIELDS = len(clean_linking_fields)
                
                # Create a list to be written to the new csv and populate it with the variables
                new_row = []
                new_row = [GENRE, PUBLISHER, NUM_LINKING_FIELDS, PRICE, VALUE_RATING]

                # Loop through the list and change any empty variables to NULL
                for i in range(len(new_row)):
                    if new_row[i] == "":
                        new_row[i] = "NULL"

                # Write the line to the new csv
                writer.writerow(new_row)

                # Then break the nested loop to speed up processing time
                break

            # Check if the first element in the current row of file1
            # dose not match the first element in the current row of file2
            if row1[0] != row2[0]:

                # And that the counter is equal to the last row of the second file
                if counter == num_rows2:

                    # Set the publisher variable
                    PUBLISHER = row1[7]

                    # Set the price variable
                    PRICE = row1[2]

                    # Set the total checkouts variable
                    VALUE_RATING = 1

                    # Set the linking fields list
                    Linking_Fields = row1[11].split(".")

                    # Check is the list is empty
                    if Linking_Fields[0] == "":
                        # If it is, then set the  genre and number of linking fields variables
                        GENRE = "NULL"
                        NUM_LINKING_FIELDS = 0
                    
                    # If it is not, then remove empty list items and set the genre and number of linking fields variables
                    elif Linking_Fields[0] != "":
                        clean_linking_fields = []
                        for i in Linking_Fields:
                            if i == "":
                                continue
                            else:
                                clean_linking_fields.append(i)
                        
                        GENRE = clean_linking_fields[0]
                        NUM_LINKING_FIELDS = len(clean_linking_fields)
                    
                    # Create a list to be written to the new csv and populate it with the variables
                    new_row = []
                    new_row = [GENRE, PUBLISHER, NUM_LINKING_FIELDS, PRICE, VALUE_RATING]

                    # Loop through the list and change any empty variables to NULL
                    for i in range(len(new_row)):
                        if new_row[i] == "":
                            new_row[i] = "NULL"

                    # Write the line to the new csv
                    writer.writerow(new_row)

    # After the first iteration of the first file is complete
    # Reset the second file index to the beginning and skip the
    # header row
    file2.seek(0)
    next(reader2)

    # Iterate over the second file
    for row2 in tqdm(reader2, desc="Looping through file #2", total=num_rows2, leave=True):

        # Iterate over the lines in the first input file
        file1.seek(0)
        next(reader1)  # Skip the header row

        # Start a counter at -1 to identify the row index of the csv
        counter = -1    

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

                    # Set the publisher variable
                    PUBLISHER = row2[7]

                    # Set the price variable
                    PRICE = row2[2]

                    # Set the total checkouts variable
                    TOT_CHKOUT = int(row2[1])
                    
                    # Then set the value rating variable based on the total checkouts variable
                    if TOT_CHKOUT == 0:
                        VALUE_RATING = 1

                    elif TOT_CHKOUT == 1:
                        VALUE_RATING = 2

                    elif TOT_CHKOUT > 1:
                        VALUE_RATING = 3

                    # Set the linking fields list
                    Linking_Fields = row2[11].split(".")

                    # Check is the list is empty
                    if Linking_Fields[0] == "":
                        # If it is, then set the  genre and number of linking fields variables
                        GENRE = "NULL"
                        NUM_LINKING_FIELDS = 0
                    
                    # If it is not, then remove empty list items and set the genre and number of linking fields variables
                    elif Linking_Fields[0] != "":
                        clean_linking_fields = []
                        for i in Linking_Fields:
                            if i == "":
                                continue
                            else:
                                clean_linking_fields.append(i)
                        
                        GENRE = clean_linking_fields[0]
                        NUM_LINKING_FIELDS = len(clean_linking_fields)
                    
                    # Create a list to be written to the new csv and populate it with the variables
                    new_row = []
                    new_row = [GENRE, PUBLISHER, NUM_LINKING_FIELDS, PRICE, VALUE_RATING]

                    # Loop through the list and change any empty variables to NULL
                    for i in range(len(new_row)):
                        if new_row[i] == "":
                            new_row[i] = "NULL"

                    # Write the line to the new csv
                    writer.writerow(new_row)
