import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    # Read and load CSV data for the census on median total household income for 2021
    census_df = pd.read_csv('2021Census_G02_NSW_SAL.csv', usecols=['SAL_CODE_2021', 'Median_tot_hhd_inc_weekly'])

    # Read the Excel file for the ASGS Structure for the 'SAL' code 
    suburb_data = pd.read_excel(
        '2021Census_geog_desc_1st_2nd_3rd_release.xlsx',
        sheet_name='2021_ASGS_Non_ABS_Structures',
        usecols=['ASGS_Structure', 'Census_Code_2021', 'Census_Name_2021']
    )
    suburb_data = suburb_data[suburb_data['ASGS_Structure'] == 'SAL']

   # Read and load the CSV file for all crime and group it for each suburb for August 2021
    crime_df = pd.read_csv('SuburbData25Q1.csv')
    crime_grouped = crime_df.groupby('Suburb', as_index=False)['Aug 2021'].sum()
    crime_grouped.rename(columns={'Aug 2021': 'Aug-21-Crime'}, inplace=True)

    # Combine the census and suburb dataframes together
    merged_df = pd.merge(
        census_df,
        suburb_data,
        left_on='SAL_CODE_2021',
        right_on='Census_Code_2021',
        how='inner'
    )

    # Merge the crime data and suburb names together
    final_df = pd.merge(
        merged_df,
        crime_grouped,
        left_on='Census_Name_2021',
        right_on='Suburb',
        how='inner'
    )

    return final_df

# Scatter plot graph created to show the Median Household income versus crime in August 2021
def show_scatter_plot(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Median_tot_hhd_inc_weekly'], df['Aug-21-Crime'], alpha=0.6)
    plt.title('Median Household Income vs Crime in August 2021')
    plt.xlabel('Median Total Household Income Weekly')
    plt.ylabel('August 2021 Crime Count')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def show_bar_graph(df):
    # Bar graph created to display the Top 20 suburbs by Crime in August 2021
    df_sorted = df.sort_values('Aug-21-Crime', ascending=False).head(20)
    
    plt.figure(figsize=(12, 6))
    plt.bar(df_sorted['Census_Name_2021'], df_sorted['Aug-21-Crime'], color='orange')
    plt.title('Top 20 Suburbs by Crime in August 2021')
    plt.xlabel('Suburb in New South Wales')
    plt.ylabel('Crime Count')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Simple text-based UI created to make the program easily accessible for all users
def main():
    print("Loading the data...")
    df = load_data()
    print("Successfully generated data.\n")

    while True:
        print("Welcome! Choose a visual to display:")
        print("1. Scatter Plot (Income vs Crime)")
        print("2. Bar Graph (Top 20 Suburbs by Crime)")
        print("3. Exit the program")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            show_scatter_plot(df)
        elif choice == "2":
            show_bar_graph(df)
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()
