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

def find_patients(patients: pd.DataFrame) -> pd.DataFrame:
    # use Regex again
    # str.contains() checks if the string contains the value
    # r'\bDIAB1' checks for the regular expression containing DIAB1
    # \b ensures it is the beginning of a word essentially
    return patients[patients['conditions'].str.contains(r'\bDIAB1')]

def nth_highest_salary_slow(employee: pd.DataFrame, N: int) -> pd.DataFrame:
    sals = employee['salary'].unique()
    if len(sals)<N:
        return pd.DataFrame({'Nth Highest Salary': [None]})
    else:
       employee = employee.sort_values(by='salary', ascending=False)
       employee = employee.drop_duplicates(subset=['salary'])
       print(employee)
       return employee.iloc[N-1:N][['salary']]
    
def nth_highest_salary(employee: pd.DataFrame, N: int) -> pd.DataFrame:
    # Extract salary column and remove duplicate values
    employee = employee['salary'].drop_duplicates()
    # Then sort the array by descending 'salary' values
    employee = employee.sort_values(ascending=False)

    # if N > num of unique salarys
    if N > len(employee):
        # return error as required
        return pd.DataFrame({'Nth Highest Salary': [None]})
    #print(employee)
    # Otherwise, return the Nth highest as a dataframe
    return pd.DataFrame({'Nth Highest Salary': [employee.iloc[N-1]]})

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    # Extract salary column and remove duplicate values
    sals = employee.salary.unique()
    if len(sals) < 2:
        # return error as required
        return pd.DataFrame({'SecondHighestSalary': [None]})
    else:
        # Then sort the array by descending 'salary' values
        # and take out second value (at index 1)
        sals = sorted(sals, reverse=True)[1] 
        return pd.DataFrame({'SecondHighestSalary': [sals]})

def department_highest_salary(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    # Merge the DFs employee and department into one dataframe, merging on the departmentId and id keys
    all_df = employee.merge(department, left_on='departmentId', right_on='id', suffixes=('_employee','_department'))
    #print(all_df)
    # Group the merged table into sets of employees with matching departmentId
    # Then apply a 'lambda' function : filter out maximum salary values from each group
    sal_df = all_df.groupby('departmentId').apply(lambda x: x[x.salary == x.salary.max()])
    #print(sal_df)
    # now de-group the dataframe -> Unnecesary for the answer to be extracted
    #sal_df = sal_df.reset_index(drop=True)
    #print(sal_df)
    # Now pick out the columns we want and rename them
    sal_df = sal_df[['name_department', 'name_employee', 'salary']]
    sal_df.columns = ['Department','Employee', 'Salary']
    return sal_df

def order_scores_manual(scores: pd.DataFrame) -> pd.DataFrame:
    # Sort by the 'score' in decreasing order
    # and reset the index, so that accessing the DF at index j corresponds to the jth index in the sorted DF
    scores = scores.sort_values(by='score', ascending=False).reset_index(drop = True)
    #print(scores)
    
    # storing ranks, start with rank 1
    rank = [1]*len(scores)
    # keep track of previous score
    score = scores.score[0]
    # loop over scores starting from second, already know the first is top rank
    for j in range(1,len(scores)):
        # current score
        c_score = scores.score[j]
        #print("Current score ",c_score)
        if c_score != score: # if not equal to the previous score
            # then it is the next rank
            rank[j] = rank[j-1]+1
            # update previous score value
            score = c_score
        else:
            # if same score as previous
            # rank is the same as previous
            rank[j] = rank[j-1]
    # add the ranks to the DF
    scores['rank'] = rank
    # return the relevant columns of the DF
    return scores[['score','rank']]

def order_scores(scores: pd.DataFrame) -> pd.DataFrame:
    if len(scores) == 0:
        return pd.DataFrame({'score': [], 'rank' : []})

    # Assign a new column named rank, using the rank method to assign a rank to the score values
    # method = 'dense' ensures that ties result in equal ranks, and ranks are not skipped
    scores['rank'] = scores['score'].rank(method='dense', ascending=False)

    # Now simply return the table as required
    return scores[['score','rank']].sort_values(by='score',ascending=False)

# Modify Person in place
def delete_duplicate_emails(person: pd.DataFrame) -> None:
    # Question requires everything be done inplace
    # i.e. we update the DF inplace
    # This is done by using inplace=True in most function calls

    # Sort the DF inplace by id in ascending order
    person.sort_values(by='id',ascending=True,inplace=True)
    # Then drop duplicate emails from the table, keep the first one encountered
    # as the elements are sorted by id values
    person.drop_duplicates(subset='email', keep='first', inplace=True)

def rearrange_products_table(products: pd.DataFrame) -> pd.DataFrame:
    # Melt essentially unfolds a multicolumn table
    # id_vars pickst the 'pivot' values to unfold around
    # it essentially makes a new row for the pivot values for each other column in the table
    # var_name assigns the column name that will store the old column names
    # val_name assigns the column name that will store the values from those columns
    # lastly we drop null values
    return pd.melt(products, id_vars='product_id', var_name='store', value_name='price').dropna()   

def rearrange_products_table_stack(products: pd.DataFrame) -> pd.DataFrame:
    # Setting the index and then stacking works similarly to melt
    
    # set product_id as the index, preparing for stacking stores
    products.set_index('product_id', inplace=True)

    # stack stores
    products = products.stack(dropna=True).reset_index()

    # rename columns
    products.columns = ['product_id','store','price']
    return pd.DataFrame(products)