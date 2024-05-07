from map_master import get_target_master


def map_masters_for_minionlist(minionlist):
    minionlist_master_map = {}

    for minion in minionlist: #minion is what's passed, maybe an ip
        master_info = get_target_master(minion) #gives single item dictionary whose key is minion_id of ip/minion passed and value is a nested dictionary with master details

        for minion_id, master_dict in master_info.items():

            minionlist_master_map[minion] = master_info[minion_id] 
            #making a multi-item dictionary whose key is what's passed (ip/id) and value is master detail dict
        
        
    return minionlist_master_map

if __name__ == '__main__':
    minionlist = ['myminion1','myminion2']
    master_mapping = map_masters_for_minionlist(minionlist)
    print(master_mapping)