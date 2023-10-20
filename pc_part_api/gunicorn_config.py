import os

workers = 2  # You can adjust the number of workers based on your server's resources
bind = "0.0.0.0:80"  # Bind to port 80 and all available network interfaces
chdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pc_part_api')
module = 'pc_part_api.wsgi:application'
pythonpath = '/path/to/your/virtualenv/bin/python'