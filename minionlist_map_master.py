from map_master import get_target_master


def map_masters_for_minionlist(minion_ids):
    print(minion_ids)
    minionlist_master_map = {}

    for minion_id in minion_ids:
        master_info = get_target_master(minion_id)
        print(minion_id, master_info)
        minionlist_master_map[minion_id] = master_info
    return minionlist_master_map

if __name__ == '__main__':
    minionlist = ['myminion', 'myminion2', 'myminion3']
    master_mapping = map_masters_for_minionlist(minionlist)
    print(master_mapping)