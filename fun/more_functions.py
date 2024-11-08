import numpy as np
import pandas as pd
import statistics

def rearmar_csv(path, date):
    df = pd.read_csv(path)
    df = df.rename(columns={'Unnamed: 1':'N° player', 'Nombre':'Player',
                     'Min': 'Minutes', 'PTS': 'Total points', '%': '2P %',
                     '%.1': '3P %', '%.2': 'Frees %', 'Def.': 'Defensive Rebound',
                     'Ofe.':'Ofensive Rebound', 'Tot.':'Total Rebound',
                     'AS': 'Asistences', 'REC':'Recover', 'PÉR': 'Turnover',
                     'Com.':'Block Committed', 'Rec.':'Block Received',
                     'Com..1':'Foul Committed', 'Rec..1':'Foul Received'})
    df['Minutes'] = pd.to_datetime(df['Minutes'], format="%M:%S").dt.time
    df['Date'] = date
    scored = []
    intentados = []
    for j in range(len(df['A/I.2'])):
        libres = df['A/I.2'][j]
        c, i = libres.split('/')
        scored.append(int(c))
        intentados.append(int(i))
    df['Free throws scored'] = scored
    df['Free throws I.P.P.'] = intentados
    scored = []
    intentados = []
    for j in range(len(df['A/I.1'])):
        triples = df['A/I.1'][j]
        c, i = triples.split('/')
        scored.append(int(c))
        intentados.append(int(i))
    df['3P throws scored'] = scored
    df['3P throws I.P.P.'] = intentados
    scored = []
    intentados = []
    for j in range(len(df['A/I'])):
        dobles = df['A/I'][j]
        c, i = dobles.split('/')
        scored.append(int(c))
        intentados.append(int(i))
    df['2P throws scored'] = scored
    df['2P throws I.P.P.'] = intentados
    df.drop(['Unnamed: 0','A/I','A/I.1','A/I.2'], axis=1)
    nuevo_orden = ['Date', 'N° player','Player', 'Minutes','Total points','Free throws scored','Free throws I.P.P.',
        'Frees %','2P throws scored','2P throws I.P.P.','2P %','3P throws scored','3P throws I.P.P.','3P %',
        'Ofensive Rebound','Defensive Rebound','Total Rebound','Asistences','Block Committed','Block Received',
        'Recover','Turnover','Foul Committed','Foul Received']
    df = df[nuevo_orden]
    return df

def shooting(local_path, visit_path):
    df = pd.read_csv(local_path)
    FG = df['2P throws scored'].sum()+df['3P throws scored'].sum()
    P3 = df['3P throws scored'].sum()
    FGA = df['2P throws I.P.P.'].sum()+df['3P throws I.P.P.'].sum()
    offense = (FG+0.5*P3)/FGA
    df = pd.read_csv(visit_path)
    FG = df['2P throws scored'].sum()+df['3P throws scored'].sum()
    P3 = df['3P throws scored'].sum()
    FGA = df['2P throws I.P.P.'].sum()+df['3P throws I.P.P.'].sum()
    defense = (FG+0.5*P3)/FGA
    return offense, defense

def turnover(local_path, visit_path):
    df = pd.read_csv(local_path)
    TOV = df['Turnover'].sum()
    FTA = df['Free throws I.P.P.'].sum()
    FGA = df['2P throws I.P.P.'].sum()+df['3P throws I.P.P.'].sum()
    offense = TOV/(FGA+0.44*FTA+TOV)
    df = pd.read_csv(visit_path)
    TOV = df['Turnover'].sum()
    FTA = df['Free throws I.P.P.'].sum()
    FGA = df['2P throws I.P.P.'].sum()+df['3P throws I.P.P.'].sum()
    defense = TOV/(FGA+0.44*FTA+TOV)
    return offense, defense

def rebounding(local_path, visit_path):
    df = pd.read_csv(local_path)
    df_op = pd.read_csv(visit_path)
    ORB = df['Ofensive Rebound'].sum()
    DRB = df['Defensive Rebound'].sum()
    ORB_op = df_op['Ofensive Rebound'].sum()
    DRB_op = df_op['Defensive Rebound'].sum()
    offense = ORB/(ORB+DRB_op)
    defense = DRB/(ORB_op+DRB)
    return offense, defense

def free_throws(local_path, visit_path):
    df = pd.read_csv(local_path)
    FT = df['Free throws scored'].sum()
    FGA = df['Free throws I.P.P.'].sum()
    offense = FT/FGA
    df = pd.read_csv(visit_path)
    FT = df['Free throws scored'].sum()
    FGA = df['Free throws I.P.P.'].sum()
    defense = FT/FGA
    return offense, defense

def four_factors(local_path, visit_path):
    df = pd.read_csv(local_path)
    df_op = pd.read_csv(visit_path)
    FG = df['2P throws scored'].sum()+df['3P throws scored'].sum()
    P3 = df['3P throws scored'].sum()
    FGA = df['2P throws I.P.P.'].sum()+df['3P throws I.P.P.'].sum()
    TOV = df['Turnover'].sum()
    FTA = df['Free throws I.P.P.'].sum()
    ORB = df['Ofensive Rebound'].sum()
    DRB = df['Defensive Rebound'].sum()
    FT = df['Free throws scored'].sum()

    FG_op = df_op['2P throws scored'].sum()+df_op['3P throws scored'].sum()
    P3_op = df_op['3P throws scored'].sum()
    FGA_op = df_op['2P throws I.P.P.'].sum()+df_op['3P throws I.P.P.'].sum()
    TOV_op = df_op['Turnover'].sum()
    FTA_op = df_op['Free throws I.P.P.'].sum()
    ORB_op = df_op['Ofensive Rebound'].sum()
    DRB_op = df_op['Defensive Rebound'].sum()
    FT_op = df_op['Free throws scored'].sum()

    shoot_offense = (FG + 0.5*P3)/FGA
    shoot_defense = (FG_op + 0.5*P3_op)/FGA_op
    turn_offense = TOV/(FGA+0.44*FTA+TOV)
    turn_defense = TOV_op/(FGA_op+0.44*FTA_op+TOV_op)
    rb_offense = ORB/(ORB+DRB_op)
    rb_defense = DRB/(ORB_op+DRB)
    free_offense = FT/FGA
    free_defense = FT_op/FGA_op

    return shoot_offense, shoot_defense, turn_offense, turn_defense, rb_offense, rb_defense, free_offense, free_defense

def show_four_factors(local_path, visit_path):
    [shoot_offense, shoot_defense, turn_offense, turn_defense, rb_offense, rb_defense, free_offense, free_defense] = four_factors(local_path, visit_path)

    print('shooting offensive: ', shoot_offense)
    print('shooting defensive: ', shoot_defense)
    print('turnover offensive: ', turn_offense)
    print('turnover defensive: ', turn_defense)
    print('rebounding offensive: ', rb_offense)
    print('rebounding defensive: ', rb_defense)
    print('Free throws offensive: ', free_offense)
    print('Free throws defense: ', free_defense)

def four_factors_season(list_path_local, list_path_visit):
    shoot_offense = []
    shoot_defense = []
    turn_offense = []
    turn_defense = []
    rb_offense = []
    rb_defense = []
    free_offense = []
    free_defense = []
    for i in range(len(list_path_local)):
        local_path =list_path_local[i]
        visit_path =list_path_visit[i]
        [shoot_o, shoot_d, turn_o, turn_d, rb_o, rb_d, free_o, free_d] = four_factors(local_path, visit_path)
        shoot_offense.append(shoot_o)
        shoot_defense.append(shoot_d)
        turn_offense.append(turn_o)
        turn_defense.append(turn_d)
        rb_offense.append(rb_o)
        rb_defense.append(rb_d)
        free_offense.append(free_o)
        free_defense.append(free_d)
    shoot_offense = statistics.mean(shoot_offense)
    shoot_defense = statistics.mean(shoot_defense)
    turn_offense = statistics.mean(turn_offense)
    turn_defense = statistics.mean(turn_defense)
    rb_offense = statistics.mean(rb_offense)
    rb_defense = statistics.mean(rb_defense)
    free_offense = statistics.mean(free_offense)
    free_defense = statistics.mean(free_defense)
    return shoot_offense, shoot_defense, turn_offense, turn_defense, rb_offense, rb_defense, free_offense, free_defense

def show_four_factors_season(list_path_local, list_path_visit):
    [shoot_offense, shoot_defense, turn_offense, turn_defense, rb_offense, rb_defense, free_offense, free_defense] = four_factors_season(list_path_local, list_path_visit)

    print('shooting offensive: ', shoot_offense)
    print('shooting defensive: ', shoot_defense)
    print('turnover offensive: ', turn_offense)
    print('turnover defensive: ', turn_defense)
    print('rebounding offensive: ', rb_offense)
    print('rebounding defensive: ', rb_defense)
    print('Free throws offensive: ', free_offense)
    print('Free throws defense: ', free_defense)