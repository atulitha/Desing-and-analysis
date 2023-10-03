import os
import ast
import json

def extract_routes_from_file(file_path):
    routes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.read()

    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    if isinstance(decorator.func, ast.Attribute):
                        if decorator.func.attr == 'route':
                            route = decorator.args[0].s if decorator.args else ''
                            view_func = node.name
                            routes.append({'route': route, 'view_function': view_func})
    return routes

def find_python_files(root_directory):
    python_files = []
    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def build_route_tree(all_routes):
    route_tree = {}
    for route_info in all_routes:
        route_parts = route_info['route'].split('/')
        current_node = route_tree
        for part in route_parts:
            current_node = current_node.setdefault(part, {})
        current_node['__view_function__'] = route_info['view_function']
    return route_tree

def jsonify_route_tree(route_tree):
    children = []
    for key, value in route_tree.items():
        if key == '__view_function__':
            children.append({'name': value})
        else:
            child_node = {'name': key, 'children': jsonify_route_tree(value)}
            if '__view_function__' in value:
                child_node['children'].append({'name': value['__view_function__']})
            children.append(child_node)
    return children

if __name__ == '__main__':
    # Replace 'your_project_directory' with the path to your Python project's root directory
    your_project_directory = os.getcwd()  # Use the current working directory

    python_files = find_python_files(your_project_directory)

    all_routes = []
    for python_file in python_files:
        routes_in_file = extract_routes_from_file(python_file)
        if routes_in_file:
            all_routes.extend(routes_in_file)

    # Build the route tree with routes and respective functions
    route_tree = build_route_tree(all_routes)

    # Convert the route tree to a JSON-compatible format
    mind_map_data = {'name': 'Routes', 'children': jsonify_route_tree(route_tree)}

    # Convert the mind map data to JSON
    mind_map_json = json.dumps(mind_map_data, indent=4)

    # Generate HTML code for the mind map
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>App Routes Mind Map</title>
        <script src="https://d3js.org/d3.v5.min.js"></script>
        <style>
            .node circle {{
                fill: #fff;
                stroke: steelblue;
                stroke-width: 2px;
            }}
            .node text {{
                font: 12px sans-serif;
            }}
            .link {{
                fill: none;
                stroke: #ccc;
                stroke-width: 1.5px;
            }}
        </style>
    </head>
    <body>
        <script>
            var data = {mind_map_json};
            var width = 800;
            var height = 600;

            var svg = d3.select("body").append("svg")
                .attr("width", width)
                .attr("height", height);

            var g = svg.append("g").attr("transform", "translate(50,0)");

            var tree = d3.tree()
                .size([height, width - 100]);

            var root = d3.hierarchy(data);

            tree(root);

            var link = g.selectAll(".link")
                .data(root.descendants().slice(1))
                .enter().append("path")
                .attr("class", "link")
                .attr("d", function(d) {{
                    return "M" + d.y + "," + d.x
                        + "C" + (d.y + d.parent.y) / 2 + "," + d.x
                        + " " + (d.y + d.parent.y) / 2 + "," + d.parent.x
                        + " " + d.parent.y + "," + d.parent.x;
                }});

            var node = g.selectAll(".node")
                .data(root.descendants())
                .enter().append("g")
                .attr("class", "node")
                .attr("transform", function(d) {{
                    return "translate(" + d.y + "," + d.x + ")";
                }});

            node.append("circle")
                .attr("r", 5);

            node.append("text")
                .attr("dy", ".31em")
                .attr("x", function(d) {{
                    return d.children ? -8 : 8;
                }})
                .style("text-anchor", function(d) {{
                    return d.children ? "end" : "start";
                }})
                .text(function(d) {{
                    return d.data.name;
                }});
        </script>
    </body>
    </html>
    """

    # Save the HTML code to a file
    with open("app_routes_mind_map.html", "w") as html_file:
        html_file.write(html_code)

    print("Mind map HTML file generated: app_routes_mind_map.html")
