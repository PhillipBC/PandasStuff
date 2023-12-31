import pandas as pd

# Data Filtering

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

# String Methods

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

# Data Manipulation

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

# STATISTICS 

def count_rich_customers(store: pd.DataFrame) -> pd.DataFrame:
    # filter the df to only bills greater than 500
    store = store[store.amount > 500]
    #print(store)
    # then use .nunique to count the number of unique elements in the customer_id column
    res = store.customer_id.nunique()

    return pd.DataFrame({'rich_count': [res]})

def food_delivery(delivery: pd.DataFrame) -> pd.DataFrame:
    # total number of orders
    total = len(delivery.order_date)

    immediate = delivery[(delivery.order_date == delivery.customer_pref_delivery_date)]
    #print(immediate)
    res = round(100*len(immediate.order_date)/total,2)

    return pd.DataFrame({'immediate_percentage': [res]})

def count_salary_categories_loop(accounts: pd.DataFrame) -> pd.DataFrame:
    lsal, asal, hsal = 0, 0, 0
    for j in range(len(accounts)):
        if accounts.income[j] > 50000:
            hsal += 1
        elif accounts.income[j] < 20000:
            lsal += 1
        else:
            asal += 1
    return pd.DataFrame({'category': ['High Salary','Low Salary','Average Salary'], 'accounts_count' : [hsal,lsal,asal]})

def count_salary_categories(accounts: pd.DataFrame) -> pd.DataFrame:
    sals = [0]*3 # high, low, avg

    sals[0] = len(accounts[accounts.income > 50000]) # high
    sals[1] = len(accounts[accounts.income < 20000]) # low
    sals[2] = len(accounts[(accounts.income <= 50000) & (accounts.income >= 20000)]) # avg

    return pd.DataFrame({'category': ['High Salary','Low Salary','Average Salary'], 'accounts_count' : sals})

# Data Aggregation

def total_time(employees: pd.DataFrame) -> pd.DataFrame:
    # Add a new column that contains the time spent in the office, as the difference of out and in time
    employees['total_time'] = employees['out_time'] - employees['in_time']

    # Because employees can have multiple entries in the table, we will group the table into 
    # employee IDs and find the sum within each group, and remembering to reset the index
    employees = employees.groupby(['emp_id','event_day'])['total_time'].sum().reset_index()
    print(employees)
    # rename the day column
    employees.rename(columns={'event_day': 'day'}, inplace=True)
    return employees

def game_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    # We will sort the frame by player_id and by the event_date
    activity = activity.sort_values(by=['player_id','event_date'])
    # Now group into player_ids and select the earliest date from each group using min()
    # remembering to reset the index so we get a DF instead of a series
    activity = activity.groupby('player_id')['event_date'].min().reset_index()
    # then just rename the column and return
    activity.rename(columns={'event_date': 'first_login'},inplace=True)
    #print(activity)
    return activity

def count_unique_subjects(teacher: pd.DataFrame) -> pd.DataFrame:
    # group teachers by teacher_id
    # then use nunique to count the number of unique subjects they teach
    # again remembering to reset the index to get a DF
    teacher = teacher.groupby('teacher_id')['subject_id'].nunique().reset_index()
    #print(teacher)
    teacher.rename(columns={'subject_id': 'cnt'}, inplace=True)
    return teacher

def find_classes(courses: pd.DataFrame) -> pd.DataFrame:
    # Group by class, and count the number of students per class
    classes = courses.groupby('class')['student'].count().reset_index()
    #print(classes)
    # Then filter to classes with at least 5 students
    classes = classes[classes.student >= 5]
    return classes[['class']]

def largest_orders(orders: pd.DataFrame) -> pd.DataFrame:
    # Group by customer number
    res = orders.groupby('customer_number')['order_number'].count().reset_index()
    # now pick out the customer with highest number of orders
    res = res[res.order_number == res.order_number.max()]
    #print(res)
    return res[['customer_number']]

def categorize_products(activities: pd.DataFrame) -> pd.DataFrame:
    # Group by sell_date
    # now use .agg to call multiple functions at once
    # Count number of unique products (nunique), and append the string name using a lambda function
    # remembering to reset the index
    res = activities.groupby('sell_date')['product'].agg( ['nunique', lambda x: ','.join(sorted(set(x)))] ).reset_index()
    
    # rename columns
    res.columns = ['sell_date','num_sold','products']
    
    return res

def daily_leads_and_partners(daily_sales: pd.DataFrame) -> pd.DataFrame:
    # use group by both date_id and make_name
    # then use .agg to call nunique on both groups
    # remembering to reset the index
    #res = daily_sales.groupby(['date_id','make_name']).agg({'lead_id':'nunique', 'partner_id':'nunique'}).reset_index()
    # or just call nunique on two columns
    res = daily_sales.groupby( ['date_id', 'make_name']).nunique().reset_index()

    # rename the columns
    res.columns = ['date_id', 'make_name', 'unique_leads','unique_partners']
    return res

# Data Integration

def actors_and_directors(actor_director: pd.DataFrame) -> pd.DataFrame:
    res = actor_director.groupby(['actor_id', 'director_id']).count().reset_index()
    res = res[res.timestamp >= 3]#.rename(columns={'timestamp': 'cooperation_count'})
    #res.rename(columns={'timestamp': 'cooperation_count'}, inplace=True)
    # Dont need to rename column, but could
    return res[['actor_id','director_id']]

def replace_employee_id(employees: pd.DataFrame, employee_uni: pd.DataFrame) -> pd.DataFrame:
    # merge tables into one, pivot about the id
    #res = employees.merge(employee_uni, left_on='id', right_on='id') # this does NOT put in nulls
    res = pd.merge(employees, employee_uni, how='left', on='id') # this puts in nulls
    return res[['unique_id', 'name']]

def students_and_examinations(students: pd.DataFrame, subjects: pd.DataFrame, examinations: pd.DataFrame) -> pd.DataFrame:
    # Count number of number of exams for each subject for each student
    # using agg to do the count, and name the count column
    examinations = examinations.groupby(['student_id','subject_name']).agg(attended_exams=('subject_name', 'count')).reset_index()
    
    # now merge the students and subjects table, join via cross
    students = students.merge(subjects, how='cross')

    # now merge this with the examinations table, right keeps keys from the right frame, i.e. students
    examinations = examinations.merge(students, on=['student_id', 'subject_name'], how='right')
    # Replace null values with 0
    examinations = examinations.fillna(0)
    
    # sorting by 'student_id', 'subject_name'
    examinations = examinations.sort_values(['student_id', 'subject_name'])

    return examinations[['student_id', 'student_name', 'subject_name', 'attended_exams']]

def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    # Group employees by managerId, and count the number of things in the group, 
    # and store under new column 'directReports'
    res = employee.groupby('managerId')['id'].count().reset_index(name='counts')
    # now filter to employees with a count of at least 5 
    res = res[res.counts >= 5].reset_index()

    # now merge this table with the employee table to identify the name of the managers with >=5
    #res = res.merge(employee[['id','name']], left_on='managerId', right_on='id')
    # return just the names
    #return res[['name']]

    # instead of merge, can just filter employee table to those that are in res
    employee = employee[(employee.id).isin(res.managerId)]
    return employee[['name']]

def sales_person(sales_person: pd.DataFrame, company: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # find com_id for 'RED' in company table
    company = company[company.name == 'RED']
    # filter orders to those with com_id == comp, i.e. RED
    orders = orders[(orders.com_id).isin(company.com_id)]
    # then filters sales_persons to those who DO NOT appear in this table ( using ~ to negate .isin() )
    sales_person = sales_person[~(sales_person.sales_id).isin(orders.sales_id)]
    # then return just the names
    return sales_person[['name']]