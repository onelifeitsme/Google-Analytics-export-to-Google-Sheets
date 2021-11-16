import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'C:\Python39\django\google_analytics_export_to_google_sheets\client_secrets.json'
VIEW_ID = '190893994'
SHEET_ID = '10Ej6zDdhs2yKMQgIFgTjUXTb2NB3T08ABoE-4A5zEqo'

# For the full list of dimensions & metrics, check https://developers.google.com/analytics/devguides/reporting/core/dimsmets
DIMENSIONS = ['ga:city']
METRICS = ['ga:sessions']

main_dict_six_day = [
    {'Babruysk': 0},
    {'Baranovichi': 0},
    {'Brest': 0},
    {'Gomel': 0},
    {'Grodno': 0},
    {'Lida': 0},
    {'Mazyr': 0},
    {'Minsk': 0},
    {'Mogilev': 0},
    {'Orsha': 0},
    {'Polatsk': 0},
    {'Recyca': 0},
    {'Salihorsk': 0},
    {'Viciebsk': 0},
    {'Zhlobin': 0}]



def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics, day):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': day, 'endDate': day}],
                    'metrics': [{'expression': i} for i in METRICS],
                    'dimensions': [{'name': j} for j in DIMENSIONS]
                }]
        }
    ).execute()

finalRows = []
def convert_to_dataframe(response):
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = [i.get('name', {}) for i in columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])]


        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [])[0].get('values', {})
            rowObject = {}

            for header, dimension in zip(dimensionHeaders, dimensions):
                rowObject[header] = dimension

            for metricHeader, metric in zip(metricHeaders, metrics):
                rowObject[metricHeader] = metric

            finalRows.append(rowObject)


    dataFrameFormat = pd.DataFrame(finalRows)
    return dataFrameFormat


def main(day):
    analytics = initialize_analyticsreporting()
    response = get_report(analytics, day)
    df = convert_to_dataframe(response)  # df = pandas dataframe
    # export_to_sheets(df)  # outputs to spreadsheet. comment to skip


if __name__ == '__main__':
    sixday = main('6daysAgo')
    for i in finalRows:
        for o in main_dict_six_day:
            if i['ga:city'] in o:
                o[i['ga:city']] += int(i['ga:sessions'])
    for i in main_dict_six_day:
        print(i)
    print('выше результат 1го представления 6 дней назад')


# вывод в таблицы
import gspread

gc = gspread.service_account(filename='C:\Python39\sheets\my_json.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/10Ej6zDdhs2yKMQgIFgTjUXTb2NB3T08ABoE-4A5zEqo/edit#gid=0')


worksheet = sh.get_worksheet(0)
values_list = worksheet.col_values(1)
# # cell_wanted = worksheet.find("546754")
# # #
# worksheet.update('F10', [[list(main_dict_six_day[0])[0], main_dict_six_day[0][list(main_dict_six_day[0])[0]]], [list(main_dict_six_day[1])[0], main_dict_six_day[1][list(main_dict_six_day[1])[0]]], [list(main_dict_six_day[2])[0], main_dict_six_day[2][list(main_dict_six_day[2])[0]]], [list(main_dict_six_day[3])[0], main_dict_six_day[3][list(main_dict_six_day[3])[0]]], [list(main_dict_six_day[4])[0], main_dict_six_day[4][list(main_dict_six_day[4])[0]]] , [list(main_dict_six_day[5])[0], main_dict_six_day[5][list(main_dict_six_day[5])[0]]], [list(main_dict_six_day[6])[0], main_dict_six_day[6][list(main_dict_six_day[6])[0]]] ,[list(main_dict_six_day[7])[0], main_dict_six_day[7][list(main_dict_six_day[7])[0]]], [list(main_dict_six_day[8])[0], main_dict_six_day[8][list(main_dict_six_day[8])[0]]], [list(main_dict_six_day[9])[0], main_dict_six_day[9][list(main_dict_six_day[9])[0]]], [list(main_dict_six_day[10])[0], main_dict_six_day[10][list(main_dict_six_day[10])[0]]], [list(main_dict_six_day[11])[0], main_dict_six_day[11][list(main_dict_six_day[11])[0]]], [list(main_dict_six_day[12])[0], main_dict_six_day[12][list(main_dict_six_day[12])[0]]], [list(main_dict_six_day[13])[0], main_dict_six_day[13][list(main_dict_six_day[13])[0]]], [list(main_dict_six_day[14])[0], main_dict_six_day[14][list(main_dict_six_day[14])[0]]]])
worksheet.update('B2', [[main_dict_six_day[0]['Babruysk']], [main_dict_six_day[1]['Baranovichi']], [main_dict_six_day[2]['Brest']], [main_dict_six_day[3]['Gomel']], [main_dict_six_day[4]['Grodno']], [main_dict_six_day[5]['Lida']], [main_dict_six_day[6]['Mazyr']], [main_dict_six_day[7]['Minsk']], [main_dict_six_day[8]['Mogilev']], [main_dict_six_day[9]['Orsha']], [main_dict_six_day[10]['Polatsk']], [main_dict_six_day[11]['Recyca']], [main_dict_six_day[12]['Salihorsk']], [main_dict_six_day[13]['Viciebsk']], [main_dict_six_day[14]['Zhlobin']]])





