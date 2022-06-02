import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# Converts the JSON file to a python dictionary
with open('car_sales.json') as json_file:
    car_dict = json.load(json_file)


# Processes sales data into different categories
def get_stats():
    global max_revenue
    global max_sales
    
    max_revenue = {'revenue': 0, 'car_make': '', 'car_model': '', 'car_year': 0000}
    max_sales = {'car_make': '', 'car_model': '', 'car_year': 0000, 'total_sales': 0}
    popular_car_year = {}  
    
    global max_sales_in_year
    global most_popular_year
    
    for vehicle in car_dict:
        #Gets the car that generated the most revenue 
        vehicle_price = vehicle['price'].strip('$')
        vehicle_revenue = vehicle['total_sales'] * float(vehicle_price)
        if vehicle_revenue > max_revenue['revenue']:
            max_revenue['revenue'] = vehicle_revenue
            max_revenue['car_make'] = vehicle['car']['car_make']
            max_revenue['car_model'] = vehicle['car']['car_model']
            max_revenue['car_year'] = vehicle['car']['car_year']
            

        #Gets the car model with the most sales
        if vehicle['total_sales'] > max_sales['total_sales']:
            max_sales['car_make'] = vehicle['car']['car_make']
            max_sales['car_model'] = vehicle['car']['car_model']
            max_sales['car_year'] = vehicle['car']['car_year']
            max_sales['total_sales'] = vehicle['total_sales']
            
        
        #Gets the most popular car year. i.e the year with the most sales
        if vehicle['car']['car_year'] not in popular_car_year.keys():
            popular_car_year[vehicle['car']['car_year']] = vehicle['total_sales']
        else:
            popular_car_year[vehicle['car']['car_year']] += vehicle['total_sales']
            
        max_sales_in_year = 0
        for year, sales_in_year in popular_car_year.items():
            if sales_in_year > max_sales_in_year:
                max_sales_in_year = sales_in_year
                most_popular_year = year


# Generates a summary report    
def generate_summary(delimeter):
    summary = 'The {} {} ({}) generated the most revenue: ${}.'.format(max_revenue['car_make'], max_revenue['car_model'], max_revenue['car_year'], str(max_revenue['revenue']).replace('.', ',')) + 'The {} {} ({}) had the most sales: {}.'.format(max_sales['car_make'], max_sales['car_model'], max_sales['car_year'], max_sales['total_sales']) + 'The most popular year was {} with {} sales.'.format(most_popular_year, max_sales_in_year)
    formatted_summary = delimeter.join(summary.split('.'))
    
    return formatted_summary


# Generates the PDF table and sorts the values based on total_sales
def generate_table():
    table_data = []
    for vehicle in car_dict:
        car_id = vehicle['id']
        car_name = '{} {} ({})'.format(vehicle['car']['car_make'], vehicle['car']['car_model'], vehicle['car']['car_year'])
        car_price = vehicle['price']
        car_sales = vehicle['total_sales']
        table_data.append([car_id, car_name, car_price, car_sales])
    sorted_table_data = sorted(table_data, key=lambda x: x[3], reverse=True)
    sorted_table_data.insert(0, ['ID', 'Car', 'Price', 'Total Sales'])
    
    return sorted_table_data


# Generates PDF
def generate_pdf():
    global title
    global summary
    
    title = 'Sales summary for last month'  
    summary = generate_summary('<br/>')
    sub_title = 'Cars sorted in descending order based on total sales.'  

    report = SimpleDocTemplate('tmp/cars.pdf')
    styles = getSampleStyleSheet()
    table_style = [('GRID', (0,0), (-1,-1), 1, colors.teal), ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')]
    
    report_title = Paragraph(title, styles['h1'])
    report_summary = Paragraph(summary)
    report_subtitle = Paragraph(sub_title, styles['h2'])
    report_table = Table(data=generate_table(), style=table_style, hAlign='LEFT')
    
    report.build([report_title, report_summary, report_subtitle, report_table])
    

get_stats()
generate_table()
generate_pdf()