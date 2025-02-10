from tabulate import tabulate
from app import create_app


app = create_app()

if __name__ == '__main__':
    """
    Run the application using the Flask server.
    """

    route_list = []
    for rule in app.url_map.iter_rules():
        route_list.append((rule.rule, rule.methods, rule.endpoint))
    print("Version 1.0")
    print(tabulate(route_list, headers=['Route', 'Methods', 'Endpoint']))
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])