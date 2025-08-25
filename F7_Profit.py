def main(silent=False):
    from random import random
    import numpy
    import requests

    def rng(run):
        return min(30*run*300/274000,30)  # returns the extra weight from rng meter (up to 30)
    def f7(meter,run,use_kismets,stop_at=999999999):
        inirun = run
        totalweight = 13710
        handleweight = 15
        scrollweight = 20
        recombweight = 400
        handles = 0
        recombs = 0
        scrolls = 0
        kismets = 0
        while True:
            if run >= stop_at:
                break
            run += 1
            if meter:
                if run > 914:
                    handles += 1
                    break
                handleweight = 15 + rng(run)
                totalweight = 13710 + rng(run)

            drop = random()
            handlechance = handleweight/totalweight
            scrollchance = scrollweight*3/totalweight + handlechance
            recombchance = recombweight/totalweight + scrollchance
            if drop < handlechance:
                handles += 1
                break
            elif drop < scrollchance:
                scrolls += 1
            elif drop < recombchance:
                recombs += 1
            elif use_kismets:
                kismets += 1
                drop = random()
                if drop < handlechance:
                    handles += 1
                    break
                elif drop < scrollchance:
                    scrolls += 1
                elif drop < recombchance:
                    recombs += 1

        return (run-inirun,scrolls,recombs,kismets,handles)
    
    api = "https://api.hypixel.net/skyblock/bazaar"
    bz = requests.get(api).json()
    if bz['success'] != True:
        return
    
    CHEST_COSTS = {'scroll': 50000000,
                   'handle': 100000000,
                   'recomb': 6000000}
    SCROLL_PRICES = numpy.mean([bz['products']['IMPLOSION_SCROLL']['quick_status'][SELL_TYPE],
                                bz['products']['SHADOW_WARP_SCROLL']['quick_status'][SELL_TYPE],
                                bz['products']['IMPLOSION_SCROLL']['quick_status'][SELL_TYPE]]) - CHEST_COSTS['scroll']
    HANDLE_PRICES = 550000000  - CHEST_COSTS['handle']
    RECOMB_PRICES = bz['products']['RECOMBOBULATOR_3000']['quick_status'][SELL_TYPE] - CHEST_COSTS['recomb']
    KISMET_PRICES = bz['products']['KISMET_FEATHER']['quick_status'][BUY_TYPE]

    player = 0
    drops = []
    
    if option == '1': # have rng selected til drop handle
        while player < target_players:
            player += 1
            drops.append(f7(True,0,USE_KISMETS))
    elif option == '2': # have rng unselected til drop handle, then select rng and drop handle again
        while player < target_players:
            player += 1
            first_run = f7(False,0,USE_KISMETS)
            second_run = f7(True,first_run[0],USE_KISMETS)
            drops.append([a + b for a, b in zip(first_run, second_run)])
    elif option == '3': # have rng selected for first x runs, then unselect and go til handle drop(if havent dropped one), then select and go til drop handle
        # so basically you either drop 1 handle in first x runs, or 2 handles 
        while player < target_players:
            player += 1
            first_run = f7(True,0,USE_KISMETS,stop_at=stop)
            if first_run[4]:
                second_run = [0,0,0,0,0]
                third_run = [0,0,0,0,0]
            else:
                second_run = f7(False,first_run[0],USE_KISMETS,stop_at=914)
                third_run = f7(True,first_run[0]+second_run[0],USE_KISMETS)
            drops.append([a + b + c for a, b, c in zip(first_run, second_run, third_run)])
    else:
        # have rng unselected for first x runs, then select and go til handle drop
        while player < target_players:
            player += 1
            first_run = f7(False,0,USE_KISMETS,stop_at=stop)
            second_run = f7(True,first_run[0],USE_KISMETS)
            drops.append([a + b for a, b in zip(first_run, second_run)])
    run = numpy.median([drops[i][0] for i in range(len(drops))])
    scroll = numpy.median([drops[i][1] for i in range(len(drops))])
    recomb = numpy.median([drops[i][2] for i in range(len(drops))])
    kismets = numpy.median([drops[i][3] for i in range(len(drops))])
    handles = numpy.median([drops[i][4] for i in range(len(drops))])

    mean_run = numpy.mean([drops[i][0] for i in range(len(drops))])
    mean_scroll = numpy.mean([drops[i][1] for i in range(len(drops))])
    mean_recomb = numpy.mean([drops[i][2] for i in range(len(drops))])
    mean_kismets = numpy.mean([drops[i][3] for i in range(len(drops))])
    mean_handles = numpy.mean([drops[i][4] for i in range(len(drops))])

    median_profit = (HANDLE_PRICES*handles + SCROLL_PRICES*scroll + RECOMB_PRICES*recomb - KISMET_PRICES*kismets)/run
    mean_profit = (HANDLE_PRICES*mean_handles + SCROLL_PRICES*mean_scroll + RECOMB_PRICES*mean_recomb - KISMET_PRICES*mean_kismets)/mean_run
    if not silent:
        print(f"Average handle profit: {HANDLE_PRICES}")
        print(f"Average scroll profit: {SCROLL_PRICES}")
        print(f"Average recomb profit: {RECOMB_PRICES}")
        print(f"Average kismet price: {KISMET_PRICES}")
        print(f'Sample size of {target_players} players')
        print(f"Mean handles per player: {mean_handles}")
        print(f"Median handles per player: {handles}")
        print(f"Mean runs per player: {mean_run}")
        print(f"Median runs per player: {run}")
        print(f"Mean scrolls per player: {mean_scroll}")
        print(f"Median scrolls per player: {scroll}")
        print(f"Mean recombs per player: {mean_recomb}")
        print(f"Median recombs per player: {recomb}")
        print(f"Mean kismets per player: {mean_kismets}")
        print(f"Median kismets per player: {kismets}")
        print(f"profit per run (Median): {median_profit}")
        print(f"profit per run (Mean): {mean_profit}")
    return (median_profit,median_profit)

menu = True
if menu:
    SELL_TYPE = 'sellPrice' if input("Enter sell method for items\n1: Sell instantly\nany other key: Sell offer\n> ") == '1' else 'buyPrice'
    USE_KISMETS = True if input("Do you want to use kismets when possible\n1: Use kismets\nany other key: No kismets\n> ") == '1' else False
    if USE_KISMETS:
        BUY_TYPE = 'buyPrice' if input("Enter buy method for kismets\n1: Buy instantly\nany other key: Buy offer\n> ") == '1' else 'sellPrice'
    target_players = int(input('Enter number of players to simulate (min 1) \n> '))
    print("Enter RNG meter strat\n1: RNG meter from start\n2: No rng meter from start, then RNG meter for second handle")
    option = input('3: rng meter til certain run, then disable til handle(if havent dropped), then rng for handle again\nany other key: no rng til certain run, then rng til handle\n> ')
    if option != '1' or option != '2':
        stop = int(input('Enter the run to switch rng meter\n> '))
else:
    SELL_TYPE = 'buyPrice'
    USE_KISMETS = True
    BUY_TYPE = 'sellPrice'
    target_players = 1000000
    option = '3'
    stop = 270

main()
