import pandas as pd

def big_countries(world: pd.DataFrame) -> pd.DataFrame:
    # access the column via DF['key']
    # | is the or operator (like || in julia)
    #res = world[(world['area'] >= 3000000) | (world['population'] >= 25000000)] # filter to entries with specified values
    res = world.loc[(world['area'] >= 3000000) |
                    (world['population'] >= 25000000)]
    # need double brackets for some reason?
    return res[['name', 'population', 'area']]

def find_products(products: pd.DataFrame) -> pd.DataFrame:
    res = products.loc[(products['low_fats'] == 'Y') &
                       (products['recyclable'] == 'Y')]
    return res[['product_id']]

def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # filter customers to those with IDs that are NOT in orders
    # do this with '~' to negate the 'isin()' function
    res = customers.loc[(~customers['id'].isin(orders['customerId']))]

    # then return the result df with only the name column
    # and rename the column to customers as requested
    return res[['name']].rename(columns={'name': 'Customers'})

def article_views(views: pd.DataFrame) -> pd.DataFrame:
    res = views[(views['viewer_id'] == views['author_id'])]
    ids = res['author_id'].unique() # extract unique ids of self viewed authors
    ids = sorted(ids) # sort em
    
    # return a new df with just ids
    return pd.DataFrame({'id':ids})

def invalid_tweets(tweets: pd.DataFrame) -> pd.DataFrame:
    res = tweets[tweets['content'].str.len() > 15]
    return res[['tweet_id']]

def calculate_special_bonus(employees: pd.DataFrame) -> pd.DataFrame:
    # using a separate array
    # get number of employees
    n = len(employees['name'])
    bonus = [0]*n # array of zeros for bonus storage
    
    for j in range(n):
        # if condition met
        if (employees['employee_id'][j] % 2 != 0) & (employees['name'][j][0] != 'M'):
            # update the bonus
            bonus[j] = employees['salary'][j]
    print(bonus)
    employees['bonus'] = bonus # add as a new column

    #employees['bonus'] = 0 # new zero column
    #employees.loc[(employees['employee_id'] % 2 != 0) & (~employees['name'].str.startswith('M')), 'bonus'] = employees['salary']

    return employees[['employee_id','bonus']].sort_values(by='employee_id', ascending=True)

def fix_names(users: pd.DataFrame) -> pd.DataFrame:
    # use .str to access the stored strings, and then .capitalize to alter them
    users['name'] = users['name'].str.capitalize()
    #print(users)
    # return sorted by user_id
    return users.sort_values(by='user_id', ascending=True)

def valid_emails(users: pd.DataFrame) -> pd.DataFrame:
    # TRYING MANUALLY INSTEAD OF REGEX

    #n = len(users['name'])
    #users['valid'] = True
    #for j in range(n):
    #    s = users['mail'][j] # current string
    #    i = s.find('@') # find the @
    #    #print("@ - ", i)
    #    if i == -1: # if not there, invalid email
    #        users['valid'][j] = False
    #        continue
    #    #print(s[i::])
    #    if s[i::] != "@leetcode.com": # if does not end with proper domain
    #        users['valid'][j] = False
    #        continue
    #   # Then check to see if s[::i] only contains valid characters
    #   # This requires making an array of ALL valid characters
    #   # I can see why regex is useful 

    # use Regex (regular expression)
    """
        Must match the pattern
        ^[A-Za-z][A-Za-z0-9_\.\-]*@leetcode(\?com)?\.com$

        ^: Anchor the regex pattern to match from the start of the string.
        [A-Za-z]: Match any single uppercase or lowercase letter. The email prefix name must start with a letter.
        [A-Za-z0-9_.-]*: Match any number of characters following the first letter in the email prefix name. 
            It includes letters    (upper or lower case), digits, underscore '_', period '.', and/or dash '-'.
        @: Match the literal '@' character, which separates the prefix name and the domain.
        leetcode: Match the literal 'leetcode', which is part of the email domain.
        (?com)?: Make the sequence ?com optional in the email domain. 
            Allows the pattern to match both '@leetcode.com' and '@leetcode?com'.
        . : Match the literal '.' character, which separates the 'leetcode' part from the 'com' part of the domain.
        com: Match the literal 'com' at the end of the email domain.
        $: Anchor the regex pattern to match until the end of the string.
    """
    #
    # str.match(r'') checks if the string matches the regex in the quotation marks
    #users = users[users['mail'].str.match(r'^[A-Za-z][A-Za-z0-9_\.\-]*@leetcode.com$')] # << should work but testcase has ?com 
    #users = users[users['mail'].str.match(r'^[A-Za-z][A-Za-z0-9_\.\-]*@leetcode(\?com)?\.com$')]
    #return users[['user_id','name','mail']]

    return users[users['mail'].str.match(r'^[A-Za-z][A-Za-z0-9_\.\-]*@leetcode(\?com)?\.com$')]






