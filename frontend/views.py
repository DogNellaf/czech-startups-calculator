from django.shortcuts import render
from calc.settings import PRODUCT_GROUPS, DEFAULT_PARAMS

GROWTH_RATE = 0.25

def index(request):
    
    args = DEFAULT_PARAMS

    if 'start_users_count' in request.GET:
        group_product = request.GET['group'].split('-')
        args = {
            'product_name': request.GET['product_name'],
            'group': group_product[0],
            'product': group_product[1],
            'start_users_count': request.GET['start_users_count'],
            'churn_rate': request.GET['churn_rate'],
            'ARPU': request.GET['ARPU'],
            'TCPC': request.GET['TCPC'],
            'target_users_count': request.GET['target_users_count'],
            'discount_rate': request.GET['discount_rate'],
            # 'starting_costs': request.GET['starting_costs']
        }
        
    results = __calculate_results(args)

    return render(request, 'index.html', {"users": results['users'], 
                                          "profit": results['profit'],
                                          "args": args,
                                          "text_results": [],
                                          "PRODUCT_GROUPS": PRODUCT_GROUPS})
    
def __calculate_results(args) -> dict:
    result = {
        'users': [],
        'profit': [0]
    }

    ARPU = float(args['ARPU'])
    TCPC = float(args['TCPC'])

    churn_rate = float(args['churn_rate']) / 100

    profit = 0

    if 'market_share' in args:
        market_share = float(args['market_share']) / 100
        customers_share = float(args['customers_share']) / 100
        population = int(args['population'])
        target_customers_number = population * customers_share
    else:
        target_customers_number = int(args['target_users_count'])

    discount_rate = float(args['discount_rate']) / 100

    initial_customers_number = int(args['start_users_count'])

    CAGR = (target_customers_number / initial_customers_number) ** (1/5) - 1

    customers = initial_customers_number * (1 - churn_rate) * (1 + CAGR)
    result['users'].append(customers)

    company_value = 0
    
    if 'market_share' in args:
        market_size = ARPU * population * customers_share * market_share
    else:
        market_size = ARPU * target_customers_number

    for year in range(1, 6):
        customers = round(customers * (1 + CAGR) * (1 - churn_rate))
        result['users'].append(customers)

        revenue_growth_rate = GROWTH_RATE * (1 - churn_rate)
        revenue_per_each_year = initial_customers_number * ARPU * (1 - revenue_growth_rate)
        TCPC_per_year = initial_customers_number * TCPC * CAGR
        net_profit_per_year = revenue_per_each_year - TCPC_per_year
        profit+=net_profit_per_year
        result['profit'].append(profit)

        discount_factor_per_year = 1 / ((1 + discount_rate)**year)
        DCF_per_year = net_profit_per_year * discount_factor_per_year
        company_value += DCF_per_year

    result['company_value'] = company_value

    return result