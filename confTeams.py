def get_teams(conference):
    if conference == 'ACC':
        return ['boston-college', 'clemson', 'duke', 'florida-state', 'georgia-tech',
                'louisville', 'miami-fl', 'north-carolina', 'north-carolina-state', 'notre-dame',
                'pittsburgh', 'syracuse', 'virginia', 'virginia-tech', 'wake-forest']
    elif conference == 'Big10':
        return ['illinois', 'indiana', 'iowa', 'maryland', 'michigan',
                'michigan-state', 'minnesota', 'nebraska', 'northwestern',
                'ohio-state', 'penn-state', 'purdue', 'rutgers', 'wisconsin']
    elif conference == 'Big12':
        return ['baylor', 'iowa-state', 'kansas', 'kansas-state', 'oklahoma',
                'oklahoma-state', 'texas', 'texas-christian',
                'texas-tech', 'west-virginia']
    elif conference == 'BigEast':
        return ['butler', 'connecticut', 'creighton', 'depaul', 'georgetown',
                'marquette', 'providence', 'seton-hall', 'st-johns-ny',
                'villanova', 'xavier']
    elif conference == 'PAC12':
        return ['arizona', 'arizona-state', 'california', 'colorado', 'oregon',
                'oregon-state', 'southern-california', 'stanford', 'ucla', 'utah',
                'washington', 'washington-state']
    elif conference == 'SEC':
        return ['alabama', 'arkansas', 'auburn', 'florida', 'georgia', 'kentucky',
                'louisiana-state', 'mississippi', 'mississippi-state', 'missouri',
                'south-carolina', 'tennessee', 'texas-am', 'vanderbilt']
    else:
        print("Invalid Conference")
