This script allows you to get data from Google Analytics and export it to Google Sheets.

At first, you should setup connection with Google API Console:
1. Go to https://console.cloud.google.com/apis/dashboard.
2. Create a new project. Doesn't matter what project's name is.
3. Find a topic Marketplace in Google Api Concole or just go link https://console.cloud.google.com/marketplace. Find 'Google Drive api' - Press Enable, firnd 'Google Sheets API' - press Enable, find 'Google Analytics Reporting API' - press Enable
4. Find a topic Credentials in Google Api Concole or just go link https://console.cloud.google.com/apis/credentials. Create Credentials - Service account - type the nane (doesn't matter what project's name is) - Create. Choose role - Editor. Press Continue - Done. 
5. Click your new account name. Press Keys - Add key - Create new key - JSON - Create. Save this file. The path to this file should be describe in ga_export_to_sheets.py. 
6. Click Details, copy email. In your google shhets where you want do export your data go to access settings and give editor acces to this email.
7. Go to Google Analitics and give your GA view acces to this email (only reading).
8. Put path to JSON KEY FROM GOOGLE API CONSOLE and google sheet url to ga_export_to_sheets.py script.
9. Change metrics in the script, choose what necessary for you.
