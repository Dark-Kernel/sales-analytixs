import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import logging
from typing import Dict, Any
import os

class KPIDashboard:
    def __init__(self, sales_file: str):
        """
        Initialize KPI Dashboard with sales data.
        
        Args:
            sales_file (str): Path to the sales file (CSV or Excel)
        """
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        try:
            # It Supports both CSV and Excel files :)
            file_extension = os.path.splitext(sales_file)[1].lower()
            
            if file_extension == '.csv':
                self.sales_data = pd.read_csv(sales_file)
            elif file_extension in ['.xls', '.xlsx']:
                self.sales_data = pd.read_excel(sales_file)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            self.sales_data['Date'] = pd.to_datetime(self.sales_data['Date'])
            
            required_columns = ['Date', 'ProductID', 'ProductName', 'Category', 'QuantitySold', 'PricePerUnit', 'TotalSales']
            missing_columns = [col for col in required_columns if col not in self.sales_data.columns]
            
            if missing_columns:
                raise ValueError(f"Missing columns: {', '.join(missing_columns)}")
            
        except Exception as e:
            self.logger.error(f"Error loading sales data: {e}")
            raise

    def calculate_kpis(self) -> Dict[str, Any]:
        """
        Calculate KPIs by categories.
        
        Returns:
            A Dictionary of calculated KPIs
        """
        category_kpis = self.sales_data.groupby('Category').agg({
            'TotalSales': 'sum',
            'QuantitySold': 'sum',
            'ProductID': 'count'  # Number of unique products
        }).reset_index()
        
        # Renaming columns for my clarity
        category_kpis.columns = ['Category', 'Total_Sales', 'Total_Quantity_Sold', 'Unique_Products']
        
        # Calculate Average Sales Price per Category
        avg_sales_price = self.sales_data.groupby('Category')['PricePerUnit'].mean().reset_index()
        avg_sales_price.columns = ['Category', 'Avg_Price_Per_Unit']
        
        # Merge KPIs
        category_kpis = category_kpis.merge(avg_sales_price, on='Category')
        
        # Calculate Additional Metrics
        category_kpis['Avg_Sales_Per_Product'] = category_kpis['Total_Sales'] / category_kpis['Unique_Products']
        
        return category_kpis.to_dict('records')

    def create_visualizations(self, kpis: Dict[str, Any]):
        """
        Creating an interactive Plotly visualizations.
        
        Args:
            kpis (Dict): Calculated KPI data
        
        Returns:
            List of Plotly figure objects, to display
        """
        df = pd.DataFrame(kpis)
        
        # Total Sales by Category
        sales_fig = go.Figure(data=[
            go.Bar(
                x=df['Category'], 
                y=df['Total_Sales'], 
                text=[f'${x:,.0f}' for x in df['Total_Sales']],
                textposition='auto',
                marker_color='blue'
            )
        ])
        sales_fig.update_layout(
            title='Total Sales by Category',
            xaxis_title='Category',
            yaxis_title='Total Sales ($)',
            template='plotly_white'
        )
        
        # Total Quantity Sold by Category
        quantity_fig = go.Figure(data=[
            go.Bar(
                x=df['Category'], 
                y=df['Total_Quantity_Sold'], 
                text=[f'{x:,.0f}' for x in df['Total_Quantity_Sold']],
                textposition='auto',
                marker_color='green'
            )
        ])
        quantity_fig.update_layout(
            title='Total Quantity Sold by Category',
            xaxis_title='Category',
            yaxis_title='Total Quantity Sold',
            template='plotly_white'
        )
        
        # Average Sales Price by Category
        price_fig = go.Figure(data=[
            go.Bar(
                x=df['Category'], 
                y=df['Avg_Price_Per_Unit'], 
                text=[f'${x:,.2f}' for x in df['Avg_Price_Per_Unit']],
                textposition='auto',
                marker_color='red'
            )
        ])
        price_fig.update_layout(
            title='Average Price per Unit by Category',
            xaxis_title='Category',
            yaxis_title='Average Price per Unit ($)',
            template='plotly_white'
        )
        
        return [sales_fig, quantity_fig, price_fig]

    def generate_dashboard(self, output_file: str = 'sales_kpi_dashboard.html'):
        """
        Generate an interactive HTML dashboard.
        
        Args:
            output_file (str): Output HTML filename
        """
        try:
            kpis = self.calculate_kpis()
            
            visualizations = self.create_visualizations(kpis)
            
            dashboard = []
            for fig in visualizations:
                dashboard.append(pio.to_html(fig, full_html=False))
            
            # Write to HTML file with embedded data table
            with open(output_file, 'w') as f:
                f.write("""
                <html>
                <head>
                    <title>Sales KPI Dashboard</title>
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
                        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                        th { background-color: #f2f2f2; }
                    </style>
                </head>
                <body>
                <h1>Sales Performance Dashboard</h1>
                """)
                
                # Embedding visualizationsss
                f.write(''.join(dashboard))
                
                # Create data table of KPIs
                f.write("<h2>Category KPI Summary</h2>")
                f.write("<table>")
                f.write("<tr>" + "".join(f"<th>{col}</th>" for col in kpis[0].keys()) + "</tr>")
                for row in kpis:
                    f.write("<tr>" + "".join(f"<td>{val}</td>" for val in row.values()) + "</tr>")
                f.write("</table>")
                
                f.write("""
                </body>
                </html>
                """)
            
            self.logger.info(f"Dashboard generated: {output_file}")
            
            # Optional: Print KPI summary to console (Just for development purposes)
            print("\nCategory KPI Summary:")
            for category in kpis:
                print(f"\nCategory: {category['Category']}")
                print(f"Total Sales: ${category['Total_Sales']:,.2f}")
                print(f"Total Quantity Sold: {category['Total_Quantity_Sold']:,}")
                print(f"Unique Products: {category['Unique_Products']}")
                print(f"Average Price per Unit: ${category['Avg_Price_Per_Unit']:,.2f}")
        
        except Exception as e:
            self.logger.error(f"Dashboard generation failed: {e}")

def main():
    dashboard = KPIDashboard('sales_data.csv')  # or 'sales_data.xls'
    # dashboard = KPIDashboard('sales_data.xls')
    dashboard.generate_dashboard()

if __name__ == "__main__":
    main()
