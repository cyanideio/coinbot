if [ $1 = 'sync' ]; then 
    if [ $2 = 'start' ]; then
        echo "SYNC START" 
        python coin_manage.py sync yunbi &
        python coin_manage.py sync poloniex &
        # python coin_manage.py sync coincap &
    fi
    if [ $2 = 'stop' ]; then
        echo "SYNC STOP"
        pkill -f coin_manage.py       
    fi
fi
exit 1
