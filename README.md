# git-pork
This is the official data and analytics repo of Pork Rub Fantasy Football. Functions that allow for pulling tons or raw data for any league can be found here. Here is a brief listing of functions and what they can do (located in main.py):  

pull_all_data(league_index, username, password, draft)

This function pulls data using your league ID (league_index arg). username and password can also be used if it's a private league. draft is a boolean where 0 does not pull draft data (strictly seasonal data) and 1 pulls strictly draft data.

The seasonal data pulls many types of data and saves them into a pandas dataframe which is then saved as a csv file that can be further analyzed/plotted with matplotlib or excel.

Example of dataframe saving data from 2020 season:
![alt text](https://i.imgur.com/cfPEVCQ.png)
