from map_master import get_target_master


def map_masters_for_minionlist(minionlist):
    minionlist_master_map = {}

    for minion in minionlist:
        master_info = get_target_master(minion)

        for minion_id, master_dict in master_info.items():

                minionlist_master_map[minion] = master_info[minion_id]
            #minionlist_master_map[minion] = {master_id: details[0]}
        
    return minionlist_master_map

if __name__ == '__main__':
    minionlist = ['192.168.64.32', '192.168.64.35', 'boo']
    master_mapping = map_masters_for_minionlist(minionlist)
    print(master_mapping)