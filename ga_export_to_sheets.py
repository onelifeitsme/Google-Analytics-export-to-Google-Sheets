import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'C:\Python39\django\google_analytics_export_to_google_sheets\onelifeitsme-project-d2788e2cba49.json'
VIEW_ID = '234753675'

my_cities = ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Krasnodar', 'Samara', 'Kazan']

my_cities_dict_6_days_ago = [{city: visitors} for city, visitors in zip(my_cities, [0]*6)]
my_cities_dict_5_days_ago = [{city: visitors} for city, visitors in zip(my_cities, [0]*6)]
my_cities_dict_4_days_ago = [{city: visitors} for city, visitors in zip(my_cities, [0]*6)]
my_cities_dict_3_days_ago = [{city: visitors} for city, visitors in zip(my_cities, [0]*6)]
my_cities_dict_2_days_ago = [{city: visitors} for city, visitors in zip(my_cities, [0]*6)]
my_cities_dict_1_days_ago = [{city: visitors} for city, visitors in zip(my_cities, [0]*6)]
my_cities_dict_today = [{city: visitors} for city, visitors in zip(my_cities, [0]*6)]

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics

def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{'name': 'ga:city'}]
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



def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  df = convert_to_dataframe(response)
  for fr in finalRows:
    if fr['ga:city'] in my_cities:
      print(fr)


if __name__ == '__main__':
  main()



# вывод в таблицы
# import gspread
#
# gc = gspread.service_account(filename='onelifeitsme-project-2051d536d681.json')
# sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1f2WOUaNlrGvFaQlgUOnc_9uO11S1wNbafturfWuIrjk/edit#gid=0')
# a = sh.sheet1.get('A1')
# print(type(a))
# print(a)


# worksheet = sh.get_worksheet(0)
# values_list = worksheet.col_values(1)
# # # cell_wanted = worksheet.find("546754")
# # # #
# # worksheet.update('F10', [[list(main_dict_six_day[0])[0], main_dict_six_day[0][list(main_dict_six_day[0])[0]]], [list(main_dict_six_day[1])[0], main_dict_six_day[1][list(main_dict_six_day[1])[0]]], [list(main_dict_six_day[2])[0], main_dict_six_day[2][list(main_dict_six_day[2])[0]]], [list(main_dict_six_day[3])[0], main_dict_six_day[3][list(main_dict_six_day[3])[0]]], [list(main_dict_six_day[4])[0], main_dict_six_day[4][list(main_dict_six_day[4])[0]]] , [list(main_dict_six_day[5])[0], main_dict_six_day[5][list(main_dict_six_day[5])[0]]], [list(main_dict_six_day[6])[0], main_dict_six_day[6][list(main_dict_six_day[6])[0]]] ,[list(main_dict_six_day[7])[0], main_dict_six_day[7][list(main_dict_six_day[7])[0]]], [list(main_dict_six_day[8])[0], main_dict_six_day[8][list(main_dict_six_day[8])[0]]], [list(main_dict_six_day[9])[0], main_dict_six_day[9][list(main_dict_six_day[9])[0]]], [list(main_dict_six_day[10])[0], main_dict_six_day[10][list(main_dict_six_day[10])[0]]], [list(main_dict_six_day[11])[0], main_dict_six_day[11][list(main_dict_six_day[11])[0]]], [list(main_dict_six_day[12])[0], main_dict_six_day[12][list(main_dict_six_day[12])[0]]], [list(main_dict_six_day[13])[0], main_dict_six_day[13][list(main_dict_six_day[13])[0]]], [list(main_dict_six_day[14])[0], main_dict_six_day[14][list(main_dict_six_day[14])[0]]]])
# worksheet.update('B2', 'sex')





