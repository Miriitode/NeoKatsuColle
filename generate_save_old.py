import json
import os

def generate_save():
    export = open(os.path.join(os.getcwd(),f'save.json'), 'w', encoding='utf-8')
    #rudimentary save file, will add more details when I think of them along the way.
    save_main = {
        'Profile': 'Mirimin',
        'CardsCollected': 0,
        'Total': 0,
        'Statistics': {
            'OGKatsu':{
                'Series_Total': [0]*23,
                'Series_Collected': [0]*23,
                'N_Count': [0]*23,
                'N_Total': [0]*23,
                'R_Count': [0]*23,
                'R_Total': [0]*23,
                'PR_Count': [0]*23,
                'PR_Total': [0]*23,
                'CPR_Count': [0]*23,
                'CPR_Total': [0]*23,
            },
            'Stars':{
                'Series_Total': [0]*15,
                'Series_Collected': [0]*15,
                'N_Count': [0]*15,
                'N_Total': [0]*15,
                'R_Count': [0]*15,
                'R_Total': [0]*15,
                'PR_Count': [0]*15,
                'PR_Total': [0]*15,
                'CR_Count': [0]*15,
                'CR_Total': [0]*15,                
                'SPR_Count': [0]*15,
                'SPR_Total': [0]*15,
            },
            'Friends':{
                'Series_Total': [0]*11,
                'Series_Collected': [0]*11,
                'N_Count': [0]*11,
                'N_Total': [0]*11,
                'R_Count': [0]*11,
                'R_Total': [0]*11,
                'PR_Count': [0]*11,
                'PR_Total': [0]*11,
                'FR_Count': [0]*11,
                'FR_Total': [0]*11,
                'CR_Count': [0]*11,
                'CR_Total': [0]*11,
                'JR_Count': [0]*11,
                'JR_Total': [0]*11,
                'BFR_Count': [0]*11,
                'BFR_Total': [0]*11,
            },
            'Parade':{
                'Series_Total': [0]*9,
                'Series_Collected': [0]*9,
                'N_Count': [0]*9,
                'N_Total': [0]*9,
                'R_Count': [0]*9,
                'R_Total': [0]*9,
                'PR_Count': [0]*9,
                'PR_Total': [0]*9,
                'CR_Count': [0]*9,
                'CR_Total': [0]*9,
                'LPR_Count': [0]*9,
                'LPR_Total': [0]*9,
            },
            'Planet':{
                'Series_Total': [0]*10,
                'Series_Collected': [0]*10,
                'N_Count': [0]*10,
                'N_Total': [0]*10,
                'R_Count': [0]*10,
                'R_Total': [0]*10,
                'PR_Count': [0]*10,
                'PR_Total': [0]*10,
                'CP_Count': [0]*10,
                'CP_Total': [0]*10,
                'SEC_Count': [0]*10,
                'SEC_Total': [0]*10,
            },
            },
        'OGKatsu':[],
        'Stars':[],
        'Friends':[],
        'Parade':[],
        'Planet':[],
    }

    def determine_rarity(series, rarity, refnum):
        match series:
            case 'OGKatsu':
                match rarity:
                    case 'ノーマル':
                        save_main['Statistics'][series]['N_Total'][refnum] += 1
                    case 'レア':
                        save_main['Statistics'][series]['R_Total'][refnum] += 1
                    case 'プレミアムレア':
                        save_main['Statistics'][series]['PR_Total'][refnum] += 1
                    case 'キャンペーンレア':
                        save_main['Statistics'][series]['CPR_Total'][refnum] += 1
                    case _:
                        ...
            case 'Stars':
                match rarity:
                    case 'ノーマル':
                        save_main['Statistics'][series]['N_Total'][refnum] += 1
                    case 'レア':
                        save_main['Statistics'][series]['R_Total'][refnum] += 1
                    case 'プレミアムレア':
                        save_main['Statistics'][series]['PR_Total'][refnum] += 1
                    case 'キャンペーンレア':
                        save_main['Statistics'][series]['CR_Total'][refnum] += 1
                    case 'スタープレミアムレア':
                        save_main['Statistics'][series]['SPR_Total'][refnum] += 1
                    case _:
                        ...
            case 'Friends':
                match rarity:
                    case 'ノーマル':
                        save_main['Statistics'][series]['N_Total'][refnum] += 1
                    case 'レア':
                        save_main['Statistics'][series]['R_Total'][refnum] += 1
                    case 'プレミアムレア':
                        save_main['Statistics'][series]['PR_Total'][refnum] += 1
                    case 'フレンズレア':
                        save_main['Statistics'][series]['FR_Total'][refnum] += 1
                    case 'キャンペーンレア':
                        save_main['Statistics'][series]['CR_Total'][refnum] += 1
                    case 'ジュエリングレア':
                        save_main['Statistics'][series]['JR_Total'][refnum] += 1
                    case 'ベストフレンズレア':
                        save_main['Statistics'][series]['BFR_Total'][refnum] += 1
                    case _:
                        ...
            case 'Parade':
                match rarity:
                    case 'ノーマル':
                        save_main['Statistics'][series]['N_Total'][refnum] += 1
                    case 'レア':
                        save_main['Statistics'][series]['R_Total'][refnum] += 1
                    case 'プレミアムレア':
                        save_main['Statistics'][series]['PR_Total'][refnum] += 1
                    case 'キャンペーンレア':
                        save_main['Statistics'][series]['CR_Total'][refnum] += 1
                    case 'レジェンドプレミアムレア':
                        save_main['Statistics'][series]['LPR_Total'][refnum] += 1
                    case _:
                        ...
            case 'Planet':
                match rarity:
                    case 'N':
                        save_main['Statistics'][series]['N_Total'][refnum] += 1
                    case 'R':
                        save_main['Statistics'][series]['R_Total'][refnum] += 1
                    case 'PR':
                        save_main['Statistics'][series]['PR_Total'][refnum] += 1
                    case 'CP':
                        save_main['Statistics'][series]['CP_Total'][refnum] += 1
                    case 'SEC':
                        save_main['Statistics'][series]['SEC_Total'][refnum] += 1
                    case _:
                        ...

    for i in ['OGKatsu', 'Stars', 'Friends', 'Parade', 'Planet']:
        dir = os.path.join(os.getcwd(),f'Database/{i}/CardList/')
        
        for j in range(len(os.listdir(dir))):
            cardcount = 0
            pre = f'{i}_Data-{j}.json'
            pro = os.path.join(dir,pre)

            if pre == 'Friends_Data-11.json':
                continue
            
            print(f"Creating Save Structure: {pre}")
            with open(f'{pro}', encoding='utf-8') as data:
                base = json.load(data)

            save = {}
            for k in base:
                cardcount += 1
            # save = {k["ID"]:False for k in base}
                if i == "Friends" or i == "Parade":
                    rar = k["RarityFull"]
                else:
                    rar = k["Rarity"]

                save[k["ID"]] = False

                determine_rarity(i, rar, j)

            save_main['Statistics'][i]['Series_Total'][j] = cardcount
            save_main['Total'] += cardcount
            save_main[i].append(save)
            data.close()
    
    out = json.dumps(save_main,ensure_ascii=False,indent=3)
    export.write(out)
    export.close()

generate_save()