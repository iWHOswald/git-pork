from espn_api.football import League
import CommonFunctions
# gui here
import pandas as pd
from tkinter import filedialog
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.pylab as pl
import tkinter as tk
from tkinter import *
from tkinter import ttk
import re
import os
import glob
from ast import literal_eval
pd.options.mode.chained_assignment = None  # default='warn'


font = {'family': 'arial',
        'weight': 'normal',
        'size': 18}
matplotlib.rc('font', **font)


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'',text)


def side_points(box_scores, week, df_og, year):

    team_dic = {}
    #df = pd.DataFrame(data, columns=['Team','Week','Matchup','home/away'])

    for i in range(6):
        # get names and format as oppropriate

        name_trim_home = deEmojify(box_scores[i].home_team.team_name)
        name_trim_away = deEmojify(box_scores[i].away_team.team_name)
        # get weekly point totals for each team
        home_weeklyscore = box_scores[i].home_score
        away_weeklyscore = box_scores[i].away_score
        # get wins and losses as a function of time (i.e. these represent values thru the season)
        if week == 1:
            if box_scores[i].home_score > box_scores[i].away_score:
                home_wins = 1
                home_losses = 0
                home_ties = 0
                away_wins = 0
                away_losses = 1
                away_ties = 0
            elif box_scores[i].home_score < box_scores[i].away_score:
                home_wins = 0
                home_losses = 1
                home_ties = 0
                away_wins = 1
                away_losses = 0
                away_ties = 0
            elif box_scores[i].home_score == box_scores[i].away_score:
                home_wins = 0
                home_losses = 0
                home_ties = 1
                away_wins = 0
                away_losses = 0
                away_ties = 1
        else:
            # df_wlt = df.set_index('Team ID')
            stats_temp_home_wins = df_og.at[box_scores[i].home_team.team_id, 'Wins']
            stats_temp_home_losses = df_og.at[box_scores[i].home_team.team_id, 'Losses']
            stats_temp_home_ties = df_og.at[box_scores[i].home_team.team_id, 'Ties']
            stats_temp_away_wins = df_og.at[box_scores[i].away_team.team_id, 'Wins']
            stats_temp_away_losses = df_og.at[box_scores[i].away_team.team_id, 'Losses']
            stats_temp_away_ties = df_og.at[box_scores[i].away_team.team_id, 'Ties']
            if box_scores[i].home_score > box_scores[i].away_score:
                home_wins = stats_temp_home_wins + 1
                home_losses = stats_temp_home_losses
                home_ties = stats_temp_home_ties
                away_wins = stats_temp_away_wins
                away_losses = stats_temp_away_losses + 1
                away_ties = stats_temp_away_ties
            elif box_scores[i].home_score < box_scores[i].away_score:
                home_wins = stats_temp_home_wins
                home_losses = stats_temp_home_losses + 1
                home_ties = stats_temp_home_ties
                away_wins = stats_temp_away_wins + 1
                away_losses = stats_temp_away_losses
                away_ties = stats_temp_away_ties
            if box_scores[i].home_score == box_scores[i].away_score:
                home_wins = stats_temp_home_wins
                home_losses = stats_temp_home_losses
                home_ties = stats_temp_home_ties + 1
                away_wins = stats_temp_away_wins
                away_losses = stats_temp_away_losses
                away_ties = stats_temp_away_ties + 1
        try:
            print(box_scores[i].home_team.ties)
            home_record = str(box_scores[i].home_team.wins) + "-" + str(box_scores[i].home_team.losses) + "-" + + box_scores[i].home_team.ties
        except:
            home_record = str(box_scores[i].home_team.wins) + "-" + str(box_scores[i].home_team.losses) + "-0"
        try:
            print(box_scores[i].away_team.ties)
            away_record = str(box_scores[i].away_team.wins) + "-" + str(box_scores[i].away_team.losses) + "-" + + box_scores[i].away_team.ties
        except:
            away_record = str(box_scores[i].away_team.wins) + "-" + str(box_scores[i].away_team.losses) + "-0"
        home_plusminus = home_weeklyscore - away_weeklyscore
        away_plusminus = away_weeklyscore - home_weeklyscore
        if week == 1:
            cume_home_points = home_weeklyscore
            cume_away_points = away_weeklyscore
        else:
            cume_home_points = df_og.at[box_scores[i].home_team.team_id, 'Cumulative points'] + home_weeklyscore
            cume_away_points = df_og.at[box_scores[i].away_team.team_id, 'Cumulative points'] + away_weeklyscore

        home_array = [box_scores[i].home_team.team_id, box_scores[i].home_team.owner,name_trim_home,week,i,"Home", box_scores[i].home_team.division_name, home_wins,home_losses,home_ties, "(" + str(home_record) + ")",box_scores[i].home_team.points_for,cume_home_points, home_weeklyscore,home_plusminus]
        away_array = [box_scores[i].away_team.team_id, box_scores[i].away_team.owner,name_trim_away,week,i,"Away", box_scores[i].away_team.division_name, away_wins,away_losses,away_ties, "(" + str(away_record) + ")",box_scores[i].away_team.points_for,cume_away_points, away_weeklyscore,away_plusminus]
        if year < 2019:
            print('ESPN deleted all weekly data prior to 2019. only stats are final roster and weekly team scores.')

            # pl_home_starters_array = positional_stat_puller(box_scores[i].home_team)
            # pl_away_starters_array = positional_stat_puller(box_scores[i].away_team)
        else:
            pl_home_starters_array = positional_stat_puller(box_scores[i].home_lineup)
            pl_away_starters_array = positional_stat_puller(box_scores[i].away_lineup)

        for value in pl_home_starters_array:
            home_array.append(value)
        team_dic[name_trim_home] = home_array
        for value in pl_away_starters_array:
            away_array.append(value)
        team_dic[name_trim_away] = away_array

    df = pd.DataFrame(team_dic)
    df1_transposed = df.T

    df1_transposed = df1_transposed.rename(columns={0: "Team ID", 1:'Owner' ,2:'Team Name', 3: 'Week', 4: "Matchup_ID", 5: "Home/Away", 6: "Division",7:'Wins', 8: 'Losses', 9:'Ties', 10: 'Record (season)', 11: "Total pts (season)",12:'Cumulative points',13:'Points for (week)', 14: 'Plus/Minus'})
    #
    rb_count = 0
    wr_count = 0
    for col in range(9):
        if pl_home_starters_array[col][1] == "RB" and rb_count == 0:
            new_col = "RB1"
            rb_count = 1
        elif pl_home_starters_array[col][1] == "RB" and rb_count == 1:
            new_col = "RB2"
        elif pl_home_starters_array[col][1] == "WR" and wr_count == 0:
            new_col = "WR1"
            wr_count = 1
        elif pl_home_starters_array[col][1] == "WR" and rb_count == 1:
            new_col = "WR2"
        else:
            new_col = pl_home_starters_array[col][1]
        df1_transposed = df1_transposed.rename(columns={col+15: new_col})
    df1_transposed = df1_transposed.rename(columns={24: "BE"})
    df1_transposed = df1_transposed.set_index('Team ID')
    return df1_transposed

    ######################################
    # data for each individual position
    ######################################
    # stats = stats_display(df1_transposed, position)
    """"
    RB_stats = stats_display(df1_transposed, "RB1")
    RB_stats = stats_display(df1_transposed, "RB2")
    WR_stats = stats_display(df1_transposed, "WR1")
    WR_stats = stats_display(df1_transposed, "WR2")
    TE_stats = stats_display(df1_transposed, "TE")
    DHC_stats = stats_display(df1_transposed, "D/ST")
    """
    # return stats


def positional_stat_puller(data):
    ##########################
    # positional data
    ##########################
    rb_cnt = 0
    wr_cnt = 0
    total_bench = []
    qb_home_array = []
    rb1_home_array = []
    rb2_home_array = []
    wr1_home_array = []
    wr2_home_array = []
    te_home_array = []
    flex_home_array = []
    dst_home_array = []
    hc_home_array = []
    for j in range(len(data)):
        print(data[j].slot_position)
        if data[j].slot_position == "IR":
            pass
        elif data[j].slot_position == "BE":
            bench_home_array = [data[j].name, data[j].slot_position, data[j].points]
            total_bench.append([data[j].name, data[j].slot_position, data[j].points])

        elif data[j].slot_position == "QB":
            qb_home_array = [data[j].name, data[j].slot_position, data[j].points]
        elif data[j].slot_position == "RB":
            if rb_cnt == 0:
                rb1_home_array = [data[j].name, data[j].slot_position, data[j].points]
                rb_cnt = 1
            else:
                rb2_home_array = [data[j].name, data[j].slot_position, data[j].points]
        elif data[j].slot_position == "WR":
            if wr_cnt == 0:
                wr1_home_array = [data[j].name, data[j].slot_position, data[j].points]
                wr_cnt = 1
            else:
                wr2_home_array = [data[j].name, data[j].slot_position, data[j].points]
        elif data[j].slot_position == "TE":
            te_home_array = [data[j].name, data[j].slot_position, data[j].points]
        elif data[j].slot_position == "RB/WR/TE":
            flex_home_array = [data[j].name, data[j].slot_position, data[j].points]
        elif data[j].slot_position == "D/ST":
            dst_home_array = [data[j].name, data[j].slot_position, data[j].points]
        elif data[j].slot_position == "HC":
            hc_home_array = [data[j].name, data[j].slot_position, data[j].points]
    pl_array = [qb_home_array, rb1_home_array, rb2_home_array, wr1_home_array, wr2_home_array,
                              te_home_array, flex_home_array, dst_home_array, hc_home_array, total_bench]
    return pl_array


def stats_display(df, position):
    # stat_df = df[['Team ID','Week','Matchup_ID',position]]
    # stat_df[['Player', 'Position', 'Points']] = pd.DataFrame(stat_df[position].tolist(), index=stat_df.index)
    # stat_df = stat_df[['Player', 'Points']]
    # stat_df = stat_df.sort_values(by='Points', ascending=False)
    #df[['Player', 'Position', 'Points']] = pd.DataFrame(df[position].tolist(), index=df.index)

    return df


def compile_stats(position):
    for pos in position:
        print(pos)
        for i in range(1,14):
            print("##############################")
            print("week " + str(i) + " " + str(pos) +  " points")
            print("##############################")
            if i == 1:

                df = side_points(0,i, pos)
            elif i > 1:
                df2 = side_points(0,i, pos)
                df = df.append(df2)
                print(df)

        print(df)
        # df.to_csv(str(position) + "_out.csv", encoding="utf-8-sig")
        df.to_csv(str('Fulldata') + "_out.csv", encoding="utf-8-sig")


def pull_all_data(league_index, username, password, draft):
    weekly_df_array = []
    for year in range(2020,2021):

        # league = League(league_id=league_index, year=year,username=username, password=password)
        league = League(league_id=league_index, year=year,espn_s2=username, swid=password)

        if draft == 0:
            for i in range(1, 14):
                if year < 2019:
                    box_scores = league.scoreboard(i)
                    print(box_scores)
                else:
                    box_scores = league.box_scores(i)
                if i == 1:
                    stats = side_points(box_scores, i, 'null', year)
                    weekly_df_array.append(stats)
                else:
                    print(i)
                    stats_append = side_points(box_scores, i, weekly_df_array[i-2], year)
                    weekly_df_array.append(stats_append)
            combined_df = pd.concat(weekly_df_array)
            print(combined_df)
            #combined_df.to_csv(str(league_index) + "_" + str(year) + "_team_stats.csv", encoding="utf-8-sig")
        elif draft == 1:
            pick = league.draft
            array = []
            for p in range(len(pick)):
                temp_player = league.player_info(name=None, playerId=pick[p].playerId)
                player_value = round(temp_player.total_points / pick[p].bid_amount,2)
                pick_array = {'team ID': pick[p].team.team_id,'Owner': pick[p].team.owner,'Player ID': pick[p].playerId, 'Player Name': pick[p].playerName,
                              'Pro Team':temp_player.proTeam,'Position':temp_player.position,'Total Points':
                                  temp_player.total_points,'Round Drafted': pick[p].round_num, 'round_pick':
                                  pick[p].round_pick,'Position Drafted':p+1, 'bid_amount': pick[p].bid_amount, "Dollar value":player_value}
                array.append(pick_array)
            df = pd.DataFrame(array)
            print(df)
            df.to_csv(str(league_index) + "_" + str(year) + "draft_stats.csv", encoding='utf-8-sig')


def side_points_tabulator(start, end):
    df = pd.read_csv('917761_2020_team_stats.csv', encoding='utf-8-sig')
    # iterate thru all weeks to pull all weekly stats
    for i in range(start,end):
        print('++++++++++++++++++++++++++'
              'week ' + str(i) + "+++++"
                                 "++++++++")
        df_week = df.loc[df['Week'] == i]   # trim df to be only those for the week of interest
        #print(df_week)

        # positions for stats
        pos = ['QB', 'RB1', 'RB2','WR1','WR2','TE','D/ST','HC','Points for (week)','Plus/Minus']
        df_meta = df_week[['Team ID', 'Week', "Owner"]]
        df_array = []
        for count, var in enumerate(pos):
            df_pos_temp = df_week[[var]] # make temporary dataframe with only the column of interest
            if count < 8:
                df_pos_temp[var] = df_pos_temp[var].apply(literal_eval) # make sure it's the correct type (list, int)
                df_pos_temp[['Player','Position','Points']] = pd.DataFrame(df_pos_temp[var].tolist(),index= df_pos_temp.index) # split array into individual columns
                del df_pos_temp[var]

            else:
                df_pos_temp = df_pos_temp.sort_values(by=var, ascending=False)
            df_final = pd.concat([df_meta, df_pos_temp], axis=1)  # array with all data
            df_array.append(df_final)

        side_point_list = []

        #### Most total points ##################################
        df_tot_pts = df_array[8].copy()
        df_tot_pts = df_tot_pts.sort_values(by='Points for (week)', ascending=False).reset_index(drop=True) #Side point RB data
        df_tot_pts['Side points'] = 0.0
        # do logic to figure out if multiple top scorers
        if df_tot_pts.at[0,'Points for (week)'] == df_tot_pts.at[1,'Points for (week)']:
            df_tot_pts.at[0,'Side points'] = 1
            df_tot_pts.at[1,'Side points'] = 1
        else:
            df_tot_pts.at[0, 'Side points'] = 2
        side_point_list.append(df_tot_pts)

        #### QB points ##################################
        df_array[0]['Total QB points'] = df_array[0]['Points']
        del df_array[0]['Points']
        df_array[0] = df_array[0].sort_values(by='Total QB points', ascending=False).reset_index(drop=True) #Side point RB data
        df_array[0]['Side points'] = 0.0
        # do logic to figure out if multiple top scorers
        if df_array[0].at[0,'Total QB points'] == df_array[0].at[1,'Total QB points']:
            df_array[0].at[0,'Side points'] = 0.5
            df_array[0].at[1,'Side points'] = 0.5
        else:
            df_array[0].at[0, 'Side points'] = 1
        side_point_list.append(df_array[0])

        #### RB points ##################################
        df_array[1]['RB1'] = df_array[1]['Player']
        df_array[1]['RB2'] = df_array[2]['Player']
        df_array[1]['Total RB points'] = df_array[1]['Points'] + df_array[2]['Points']
        del df_array[1]['Points']
        df_array[1] = df_array[1].sort_values(by='Total RB points', ascending=False).reset_index(drop=True) #Side point RB data
        df_array[1]['Side points'] = 0.0
        # do logic to figure out if multiple top scorers
        if df_array[1].at[0,'Total RB points'] == df_array[1].at[1,'Total RB points']:
            df_array[1].at[0,'Side points'] = 0.5
            df_array[1].at[1,'Side points'] = 0.5
        else:
            df_array[1].at[0, 'Side points'] = 1
        side_point_list.append(df_array[1])

        #### WR points ##################################
        df_array[3]['WR1'] = df_array[3]['Player']
        df_array[3]['WR2'] = df_array[4]['Player']
        df_array[3]['Total WR points'] = df_array[3]['Points'] + df_array[4]['Points']
        del df_array[3]['Points']
        df_array[3] = df_array[3].sort_values(by='Total WR points', ascending=False).reset_index(drop=True) #Side point RB data
        df_array[3]['Side points'] = 0.0
        # do logic to figure out if multiple top scorers
        if df_array[3].at[0,'Total WR points'] == df_array[3].at[1,'Total WR points']:
            df_array[3].at[0,'Side points'] = 0.5
            df_array[3].at[1,'Side points'] = 0.5
        else:
            df_array[3].at[0, 'Side points'] = 1
        side_point_list.append(df_array[3])

        #### TE points ##################################
        df_array[5]['Total TE points'] = df_array[5]['Points']
        del df_array[5]['Points']
        df_array[5] = df_array[5].sort_values(by='Total TE points', ascending=False).reset_index(drop=True) #Side point RB data
        df_array[5]['Side points'] = 0.0
        # do logic to figure out if multiple top scorers
        if df_array[5].at[0,'Total TE points'] == df_array[5].at[1,'Total TE points']:
            df_array[5].at[0,'Side points'] = 0.25
            df_array[5].at[1,'Side points'] = 0.25
        else:
            df_array[5].at[0, 'Side points'] = 0.5
        side_point_list.append(df_array[5])

        #### DST/HC points ##################################
        df_array[6]['D/ST'] = df_array[6]['Player']
        df_array[6]['HC'] = df_array[7]['Player']
        df_array[6]['Total DST/HC points'] = df_array[6]['Points'] + df_array[7]['Points']
        del df_array[6]['Points']
        df_array[6]['Position'] = 'DST/HC'
        df_array[6] = df_array[6].sort_values(by='Total DST/HC points', ascending=False).reset_index(drop=True) #Side point RB data
        df_array[6]['Side points'] = 0.0
        # do logic to figure out if multiple top scorers
        if df_array[6].at[0,'Total DST/HC points'] == df_array[6].at[1,'Total DST/HC points']:
            df_array[6].at[0,'Side points'] = 0.25
            df_array[6].at[1,'Side points'] = 0.25
        else:
            df_array[6].at[0, 'Side points'] = 0.5
        side_point_list.append(df_array[6])

        #### most point scored by owner who loses (0.5), dfs 8 and 9 ##################################
        df_mpsl = df_array[8].copy()
        df_mpsl['Plus/Minus'] = df_array[9]['Plus/Minus']
        df_mpsl_neg = df_mpsl[df_mpsl['Plus/Minus'] < 0.0]   # trim df to be only those for the week of interest
        df_mpsl_pos = df_mpsl[df_mpsl['Plus/Minus'] >= 0.0]   # trim df to be only those for the week of interest
        df_mpsl_neg = df_mpsl_neg.sort_values(by='Points for (week)', ascending=False).reset_index(drop=True)
        df_mpsl_pos = df_mpsl_pos.sort_values(by='Points for (week)', ascending=True).reset_index(drop=True)
        df_mpsl = df_mpsl_neg.append(df_mpsl_pos).reset_index(drop=True)
        df_mpsl['Side points'] = 0.0
        df_mpsl.at[0,'Side points'] = 0.5
        side_point_list.append(df_mpsl)

        #### Lost with second highest score out of all owners (1 pt) dfs 8 and 9 ##################################
        df_lshs = df_array[8].copy()
        df_lshs['Plus/Minus'] = df_array[9]['Plus/Minus']
        df_lshs = df_lshs.sort_values(by='Points for (week)', ascending=False).reset_index(drop=True)
        df_lshs['Side points'] = 0.0
        if df_lshs.at[1,'Plus/Minus'] < 0:
            df_lshs.at[1,'Side points'] = 1.0
        else:
            pass
        side_point_list.append(df_lshs)

        #### Least amount of points scored by an owner (-.5 points) ##################################
        df_least = df_array[8].copy()
        df_least = df_least.sort_values(by='Points for (week)', ascending=True).reset_index(drop=True)
        df_least['Side points'] = 0.0
        ### if tie code
        if df_least.at[0,'Points for (week)'] == df_least.at[1,'Points for (week)']:
            df_least.at[0,'Side points'] = -0.25
            df_least.at[1,'Side points'] = -0.25
        else:
            df_least.at[0, 'Side points'] = -0.5
        side_point_list.append(df_least)

        #### Largest margin of victory (0.5 points) ##################################
        df_lrgst_margin = df_array[9].copy()
        df_lrgst_margin = df_lrgst_margin.sort_values(by='Plus/Minus', ascending=False).reset_index(drop=True)
        df_lrgst_margin['Side points'] = 0.0
        ### if tie code
        if df_lrgst_margin.at[0,'Plus/Minus'] == df_lrgst_margin.at[1,'Plus/Minus']:
            df_lrgst_margin.at[0,'Side points'] = 0.25
            df_lrgst_margin.at[1,'Side points'] = 0.25
        else:
            df_lrgst_margin.at[0, 'Side points'] = 0.5

        side_point_list.append(df_lrgst_margin)

        ## format the DF to store stuff
        df_names = ['Total points', 'QB points', 'RB points','WR points','TE points','DST/HC points','Most pts scored by losing owner','Lost with second highest pts','Least amount of pts','Largest margin of victory']
        final_total_sidepts = side_point_list[0].copy()
        final_total_sidepts = final_total_sidepts[['Team ID','Owner', 'Side points']]
        final_total_sidepts.at[0,"Side points"] = 0.0
        final_total_sidepts = final_total_sidepts.set_index('Team ID')
        print(len(side_point_list))
        print(side_point_list)
        print("$E^#$&##$&#$&#2222222222222222222222222222222222222222222222")
        for v in range(len(side_point_list)):
            #side_point_list[v] = side_point_list[v].head(2)  # trim df to be only top 1 for the week of interest
            if v == 0:
                final_deep_stats = side_point_list[v].copy()
            else:
                final_deep_stats = pd.concat([final_deep_stats, side_point_list[v]], axis=0, ignore_index=True)

            side_point_list[v] = side_point_list[v].set_index('Team ID') # set index to team id
            for team in range(1,13):
                final_total_sidepts.at[team, 'Side points'] = final_total_sidepts.at[team, 'Side points'] + side_point_list[v].at[team, 'Side points']
        final_total_sidepts = final_total_sidepts[final_total_sidepts['Owner'].notna()]
        final_total_sidepts['Week'] = i
        if i == start:
            export_df = final_total_sidepts
            export_deep_stats = final_deep_stats
        else:
            print('appending')
            export_df = export_df.append(final_total_sidepts)
            export_deep_stats = export_deep_stats.append(final_deep_stats)
    print(export_df)
    print(export_deep_stats)
    #export_df.to_csv("side-points-2020.csv", encoding='utf-8-sig')
    #export_deep_stats.to_csv("side-point-deep-stats-2020.csv", encoding='utf-8-sig')


def analysis(file):
    df = pd.read_csv(file, encoding='utf-8-sig')
    #df = df.set_index('team ID')
    array = []
    for i in range(1,13):
        df_2 = df[df['team ID']==i]
        df_2['inverse_pos'] = (192 - df_2["Position Drafted"])
        df_2['weighted pos'] =  df_2['inverse_pos'] * df_2["bid_amount"]
        weighted_value = df_2["weighted pos"].mean()
        array.append(weighted_value)
        print(df_2)
        print(weighted_value)
        print(array)

password = '{71735CA3-D03A-47E3-BB18-B4314B399BB1}'
espn = "AEAI2axDp0zJHsR%2BXUt496H0E1r56UjU7QjY6OBYkXXGFkO%2FWgfyUys%2BVo%2B4Rsz4k9MBskSsCb8Si6mY1bZDdFzekj4vZ0g5RSHx0T7lNpQP%2BnmkKR5B21OJ9%2Bfpfwt4IMyajlCjG8G%2FU1Z6PnEQXS1l9daaP2gF4palYuw9zjNy%2ByI7NXDj0VDRDc2cw17KRwwjeU3NP%2FbsCF2t3PDPBgAplsX%2BhpUmYXnDa1jSQ5h2rRdI7Rrea7GzztnLtg94MfBkQk5QkRrsUFoq2U96iQk7ugXqpoo7u3azVG9EzDiSPw%3D%3D"


# analysis('917761_2020draft_stats.csv')
# side_points_tabulator(1,14)
# pull_all_data(917761, espn, password,1)


