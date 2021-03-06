import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import gspread

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'FULL PATH TO JSON KEY FROM GOOGLE API CONSOLE'
VIEW_ID = 'YOU GOOGLE ANALYTICS VIEW ID'

my_cities = ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Krasnodar', 'Samara', 'Kazan']


def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics


analytics = initialize_analyticsreporting()


class Report():
    my_cities_dict = [{city: visitors} for city, visitors in zip(my_cities, [0] * 6)]

    def __init__(self, days_ago):
        self.days_ago = days_ago

    def get_report(self, analytics):
        days_ago = self.days_ago
        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': days_ago, 'endDate': days_ago}],
                        'metrics': [{'expression': 'ga:sessions'}],
                        'dimensions': [{'name': 'ga:city'}]
                    }]
            }
        ).execute()

    def convert_to_dataframe(self):
        my_cities_dict = self.my_cities_dict
        response = self.get_report(analytics)
        finalRows = []
        finalReport = []
        for report in response.get('reports', []):
            columnHeader = report.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = [i.get('name', {}) for i in
                             columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])]

            for row in report.get('data', {}).get('rows', []):
                dimensions = row.get('dimensions', [])
                metrics = row.get('metrics', [])[0].get('values', {})
                rowObject = {}

                for header, dimension in zip(dimensionHeaders, dimensions):
                    rowObject[header] = dimension

                for metricHeader, metric in zip(metricHeaders, metrics):
                    rowObject[metricHeader] = metric

                finalRows.append(rowObject)

        for fr in finalRows:
            for mcd in my_cities_dict:
                if fr['ga:city'] in mcd:
                    mcd[fr['ga:city']] = fr['ga:sessions']

        dataFrameFormat = pd.DataFrame(finalReport)
        return dataFrameFormat


# ???????????????????? ???????????? ?????? ?????????????? ???? 7 ????????
sixdaysago = Report('6daysAgo')
fivedaysago = Report('5daysAgo')
fourdaysago = Report('4daysAgo')
threedaysago = Report('3daysAgo')
twodaysago = Report('2daysAgo')
onedayago = Report('1daysAgo')
today = Report('today')


# ?????????? ?? ??????????????
gc = gspread.service_account(filename='ONLY NAME OF JSON KEY FROM GOOGLE API CONSOLE')
sh = gc.open_by_url('GOOGLE SHEET URL')
worksheet = sh.get_worksheet(0)

worksheet.update('B3', [[sixdaysago.my_cities_dict[0]['Moscow']],
                        [sixdaysago.my_cities_dict[1]['Saint Petersburg']],
                        [sixdaysago.my_cities_dict[2]['Novosibirsk']],
                        [sixdaysago.my_cities_dict[3]['Krasnodar']],
                        [sixdaysago.my_cities_dict[4]['Samara']],
                        [sixdaysago.my_cities_dict[5]['Kazan']]])
worksheet.update('C3', [[fivedaysago.my_cities_dict[0]['Moscow']],
                        [fivedaysago.my_cities_dict[1]['Saint Petersburg']],
                        [fivedaysago.my_cities_dict[2]['Novosibirsk']],
                        [fivedaysago.my_cities_dict[3]['Krasnodar']],
                        [fivedaysago.my_cities_dict[4]['Samara']],
                        [fivedaysago.my_cities_dict[5]['Kazan']]])
worksheet.update('D3', [[fourdaysago.my_cities_dict[0]['Moscow']],
                        [fourdaysago.my_cities_dict[1]['Saint Petersburg']],
                        [fourdaysago.my_cities_dict[2]['Novosibirsk']],
                        [fourdaysago.my_cities_dict[3]['Krasnodar']],
                        [fourdaysago.my_cities_dict[4]['Samara']],
                        [fourdaysago.my_cities_dict[5]['Kazan']]])
worksheet.update('E3', [[threedaysago.my_cities_dict[0]['Moscow']],
                        [threedaysago.my_cities_dict[1]['Saint Petersburg']],
                        [threedaysago.my_cities_dict[2]['Novosibirsk']],
                        [threedaysago.my_cities_dict[3]['Krasnodar']],
                        [threedaysago.my_cities_dict[4]['Samara']],
                        [threedaysago.my_cities_dict[5]['Kazan']]])
worksheet.update('F3', [[twodaysago.my_cities_dict[0]['Moscow']],
                        [twodaysago.my_cities_dict[1]['Saint Petersburg']],
                        [twodaysago.my_cities_dict[2]['Novosibirsk']],
                        [twodaysago.my_cities_dict[3]['Krasnodar']],
                        [twodaysago.my_cities_dict[4]['Samara']],
                        [twodaysago.my_cities_dict[5]['Kazan']]])
worksheet.update('G3', [[onedayago.my_cities_dict[0]['Moscow']],
                        [onedayago.my_cities_dict[1]['Saint Petersburg']],
                        [onedayago.my_cities_dict[2]['Novosibirsk']],
                        [onedayago.my_cities_dict[3]['Krasnodar']],
                        [onedayago.my_cities_dict[4]['Samara']],
                        [onedayago.my_cities_dict[5]['Kazan']]])
worksheet.update('H3', [[today.my_cities_dict[0]['Moscow']],
                        [today.my_cities_dict[1]['Saint Petersburg']],
                        [today.my_cities_dict[2]['Novosibirsk']],
                        [today.my_cities_dict[3]['Krasnodar']],
                        [today.my_cities_dict[4]['Samara']],
                        [today.my_cities_dict[5]['Kazan']]])
