import pandas as pd
import re

df = pd.read_excel('PAN Number Validation Dataset.xlsx')
# print(df.head(10))
print('Total records =', len(df))
total_records = len(df)


##### DATA CLEANING ####
df["Pan_Numbers"] = df['Pan_Numbers'].astype('string').str.strip().str.upper()
# print(df.head(10))

# print("\n")
# print(df[df['Pan_Numbers']=='']) #this just showcases 2 values which is not true
# print(df[df['Pan_Numbers'].isna()]) #finds all the empty values
# Now in pandas we drop all the na values but not values with " " so we have to convert " " these to na values.

df = df.replace({"Pan_Numbers": ''}, pd.NA).dropna(
    subset="Pan_Numbers")  # Converts " " to NA
# print(df[df['Pan_Numbers']==''])
# print(df[df['Pan_Numbers'].isna()]) # 2 records gets added

print("Total records =", len(df))

print("Unique values =", df['Pan_Numbers'].nunique())

df = df.drop_duplicates(subset="Pan_Numbers", keep='first')
print("Total records =", len(df))


##### DATA VALIDATION ####

# check for if the ajacent character are same
def has_adjacent_repitition(pan):
    # for i in range(len(pan)-1):
    #     if pan[i] == pan[i+1]:
    #         return True
    # return False

    # similar function, however minimilistic
    return any(pan[i] == pan[i+1] for i in range(len(pan)-1))

# print(has_adjacent_repitition('ABCCF'))
# print(has_adjacent_repitition('ABDES'))
# print(has_adjacent_repitition('ACCFD'))
# print(has_adjacent_repitition('NFSQW'))


def is_sequential(pan):  # Checks if the character are in a sequence
    # for i in range(len(pan)-1):
    #     if ord(pan[i+1]) - ord(pan[i]) != 1:
    #         return False
    # return True
    return all(ord(pan[i+1]) - ord(pan[i]) == 1 for i in range(len(pan)-1))

# print(is_sequential('ABCDE'))
# print(is_sequential('LMNOI'))
# print(is_sequential('XACDF'))
# print(is_sequential('RASDQ'))


def is_valid_pan(pan):
    if len(pan) != 10:
        return False

    if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan):
        return False

    if has_adjacent_repitition(pan):
        return False

    if is_sequential(pan):
        return False

    return True


df["Status"] = df["Pan_Numbers"].apply(
    lambda x: "Valid" if is_valid_pan(x) else "Invalid")
print(df.head(10))
# Checks for the conditions and print Valid or Invalid in front of each PAN number

valid_cnt = (df["Status"] == 'Valid').sum()
invalid_cnt = (df["Status"] == 'Invalid').sum()
missing_cnt = total_records - (valid_cnt + invalid_cnt)

print("Total Count = ", total_records)
print("Valid Count = ", valid_cnt)
print("Invalid Count = ", invalid_cnt)
print("Missing Count = ", missing_cnt)

df_summary = pd.DataFrame({"Total Processed Records": [total_records], "Total Valid Count": [
                          valid_cnt], "Total Invalid Count": [invalid_cnt], "Total Missing PANs": [missing_cnt]})
print(df_summary.head())


# This is to create a new excel file with 2 sheets one with valid or invalid status and another one to tell me the summary.
with pd.ExcelWriter("PAN Validation Result.xlsx") as writer:
    df.to_excel(writer, sheet_name="PAN Validations", index=False)
    df_summary.to_excel(writer, sheet_name="Summary", index=False)
