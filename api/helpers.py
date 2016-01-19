import mistune
from urlparse import urlparse
import MySQLdb


def return_md_as_html(filename, title):
    """Return a Markdown file as HTML.

    Args:
        filename (str): The Markdown file to convert to HTML.
        title (str): The title of the new HTML page.

    Returns:
        str: An HTML blob.
    """

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
    """.format(title=title, problem_html=markdown_html.strip())

    return html


def connect_to_mysql(mysql_url):
    """Connect to a MySQL database.

    Args:
        mysql_url (str): The MySQL Connections string.
            This should come in the form of:
                mysql://username:password@hostname.com/database

    Returns:
        MySQLdb.connections.Connection: An open MySQL connection.
    """

    mysql_connection_string = urlparse(mysql_url)

    db = MySQLdb.connect(host=mysql_connection_string.hostname,
                         user=mysql_connection_string.username,
                         passwd=mysql_connection_string.password,
                         db=mysql_connection_string.path.strip('/'))

    return db
