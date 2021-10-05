#!/bin/sh
echo “Resolving dependencies…“
pip install -r requirements.txt
pip install -e ./dependencies/niryo_one_tcp_client_package
echo “Finished.“
