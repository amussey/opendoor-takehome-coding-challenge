import mistune


def return_md_as_html(filename, title):
    markdown = open(filename, 'r')
    markdown_html = mistune.markdown(markdown.read())
    markdown.close()

    html = """
<html>
    <head>
        <title>{title}</title>
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />
        <style>
        table, th, td {{
            border: 1px solid black;
            padding: 5px;
        }}
        body {{
            padding: 0 20px;
        }}
        </style>
    </head>
    <body>
        <div id="content">
    {problem_html}
        </div>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    </body>
</html>
""".format(title=title, problem_html=markdown_html)

    return html
