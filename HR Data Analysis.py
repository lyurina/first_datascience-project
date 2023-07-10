import pandas as pd
import os

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    a_office_df = pd.read_xml('https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1')
    a_office_df['employee_office_id'] = 'A' + a_office_df['employee_office_id'].astype(str)
    a_office_df.set_index('employee_office_id', inplace=True)

    b_office_df = pd.read_xml('https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1')
    b_office_df['employee_office_id'] = 'B' + b_office_df['employee_office_id'].astype(str)
    b_office_df.set_index('employee_office_id', inplace=True)

    hr_df = pd.read_xml('https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1')
    hr_df.set_index('employee_id', inplace=True)

    a_office_index_list = a_office_df.index.tolist()
    b_office_index_list = b_office_df.index.tolist()
    hr_index_list = hr_df.index.tolist()

    office_df = pd.concat([a_office_df, b_office_df])
    office_df = office_df.merge(hr_df, how='inner', left_index=True, right_index=True, indicator=True)
    office_df.sort_index(inplace=True)
    office_df.drop(['_merge'], axis=1, inplace=True)
    office_df_index_list = office_df.index.tolist()
    office_df_column_list = office_df.columns.tolist()

    ##print(office_df_index_list)
    ##print(office_df_column_list)

    top_ten_df = office_df[['Department', 'average_monthly_hours']].sort_values('average_monthly_hours',  ascending=False).nlargest(10,'average_monthly_hours')
    top_departments = top_ten_df['Department'].tolist()

    only_for_low_it = office_df[(office_df.Department == 'IT') & (office_df.salary == 'low')]
    total_it_low_projects = only_for_low_it.number_project.sum()

    desired_employees = ['A4', 'B7064', 'A3033']
    special_employees = office_df.loc[['A4', 'B7064', 'A3033'], ['last_evaluation', 'satisfaction_level']].values.tolist()
    ##print(str(top_departments) + '\n' + str(total_it_low_projects) + '\n' + str(special_employees) + '\n')

    office_df['count_bigger_5'] = office_df.apply(lambda x: 1 if x['number_project'] > 5 else 0, axis=1)
    number_project = office_df.groupby(['left']).agg({'number_project': 'median', 'count_bigger_5': 'sum'}).round(2)
    number_project.columns = pd.MultiIndex.from_tuples([('number_project', 'median'), ('number_project', 'count_bigger_5')])

    time_spend_company = office_df.groupby(['left'])['time_spend_company'].agg(['median', 'mean']).round(2)
    time_spend_company.columns = pd.MultiIndex.from_tuples([('time_spend_company', 'median'), ('time_spend_company', 'mean')])

    Work_accident = round(
        office_df.groupby('left')['Work_accident'].apply(lambda x: len(x[x == 1]) / len(x)).reset_index(name='mean').set_index('left'), 2)
    Work_accident.columns = pd.MultiIndex.from_tuples([('Work_accident', 'mean')])

    last_evaluation = office_df.groupby(['left'])['last_evaluation'].agg(['mean', 'std']).round(2)
    last_evaluation.columns = pd.MultiIndex.from_tuples([('last_evaluation', 'mean'), ('last_evaluation', 'std')])

    result = pd.concat([number_project, time_spend_company, Work_accident, last_evaluation], axis=1)
    print(result.to_dict())
    ##print(office_df)
