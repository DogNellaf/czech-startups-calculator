def __calculate_results(args) -> dict:
    result = {
        'users': [],
        'profit': [0]
    }

    initial_customers_number = int(args['start_users_count'])

    # if 'market_share' in args:
    #     market_share = float(args['market_share']) / 100
    #     customers_share = float(args['customers_share']) / 100
    #     population = int(args['population'])
    #     target_customers_number = population * customers_share
    # else:
    target_customers_number = int(args['target_users_count'])

    CAGR = (target_customers_number / initial_customers_number) ** (1/5) - 1    

    churn_rate = float(args['churn_rate']) / 100

    ARPU = float(args['ARPU'])
    TCPC = float(args['TCPC'])

    discount_rate = float(args['discount_rate']) / 100

    profit = 0
    growth_rate = CAGR * (1 - churn_rate)

    company_value = 0
    
    # year 1
    revenue = ARPU * initial_customers_number * (1 + growth_rate)
    TCPC_per_year = TCPC * (1 + CAGR) * initial_customers_number

    customers = initial_customers_number * (1 + CAGR) * (1 - churn_rate)
    result['users'].append(customers)

    # if 'market_share' in args:
    #     market_size = ARPU * population * customers_share * market_share
    # else:
    #     market_size = ARPU * target_customers_number

    for year in range(2, 6):

        revenue *= (1 + growth_rate)
        
        customers = round(customers * (1 + CAGR) * (1 - churn_rate))
        result['users'].append(customers)

        TCPC_per_year *= (1 + CAGR)
        
        net_profit = revenue - TCPC_per_year

        profit+=net_profit
        result['profit'].append(profit)

        discount_factor_per_year = 1 / ((1 + discount_rate)**year)
        DCF_per_year = net_profit * discount_factor_per_year
        company_value += DCF_per_year

    result['company_value'] = company_value

    return result

args = {
    'product_name': 'SOM Sneakers',
    'group': 'Footwear',
    'product': 'Sneakers',
    'target_users_count': 4000,
    'start_users_count': 1200,
    'population': 1200000,
    'market_share': 10,
    'customers_share': 10,
    'churn_rate': 10,
    'ARPU': 200,
    'TCPC': 90,
    'discount_rate': 20,
    'starting_costs': 15000
}

print(__calculate_results(args))