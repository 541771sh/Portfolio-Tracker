from controllers.portfolio_controller import PortfolioController
from models.portfolio import Portfolio

def main():
    portfolio = Portfolio()  # ✅ Create a Portfolio instance
    controller = PortfolioController(portfolio)  # ✅ Pass it to PortfolioController
    
    while True:
        print("\n1. Add Asset")
        print("2. Edit Asset")
        print("3. Remove Asset")
        print("4. Update Prices")
        print("5. Show Current & Historical Price Graph")
        print("6. Show Portfolio")
        print("7. Show Portfolio Value & Weights")
        print("8. Show Portfolio Performance Over Time")
        print("9. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            controller.add_asset()

        elif choice == "2":
            controller.edit_asset()
        
        elif choice == "3":
            controller.remove_asset()
        
        elif choice == "4":
            controller.update_prices()
            print("Prices updated.")
        
        elif choice == "5":
            tickers = input("Enter ticker(s) (comma separated for multiple): ").upper().split(",")
            controller.display_asset_graph(tickers)
        
        elif choice == "6":
            controller.display_portfolio()
        
        elif choice == "7":
            controller.display_portfolio_summary()
        
        elif choice == "8":
            controller.display_portfolio_performance_graph()
        
        elif choice == "9":
            break
        
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
